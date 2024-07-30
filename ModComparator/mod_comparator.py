import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import re

class FileDifferenceFinder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Difference Finder")
        self.geometry("450x550")
        self.resizable(False, False)
        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        # Input File A
        self.label_file_a = tk.Label(self, text="Input Text File A:")
        self.label_file_a.pack(pady=5)
        self.entry_file_a = tk.Entry(self, width=50)
        self.entry_file_a.pack(pady=5)
        self.button_browse_a = tk.Button(self, text="Browse", command=self.browse_file_a)
        self.button_browse_a.pack(pady=5)

        # Input File B
        self.label_file_b = tk.Label(self, text="Input Text File B:")
        self.label_file_b.pack(pady=5)
        self.entry_file_b = tk.Entry(self, width=50)
        self.entry_file_b.pack(pady=5)
        self.button_browse_b = tk.Button(self, text="Browse", command=self.browse_file_b)
        self.button_browse_b.pack(pady=5)

        # Output Directory
        self.label_output_dir = tk.Label(self, text="Output Directory:")
        self.label_output_dir.pack(pady=5)
        self.entry_output_dir = tk.Entry(self, width=50)
        self.entry_output_dir.pack(pady=5)
        self.button_browse_output_dir = tk.Button(self, text="Browse", command=self.browse_output_dir)
        self.button_browse_output_dir.pack(pady=5)

        # Output File Name
        self.label_output_name = tk.Label(self, text="Output File Name:")
        self.label_output_name.pack(pady=5)
        self.entry_output_name = tk.Entry(self, width=50)
        self.entry_output_name.pack(pady=5)

        # Comparison Option
        self.comparison_var = tk.StringVar(value="differences")
        self.radio_differences = tk.Radiobutton(self, text="Find Differences", variable=self.comparison_var, value="differences")
        self.radio_differences.pack(pady=5)
        self.radio_matches = tk.Radiobutton(self, text="Find Matches", variable=self.comparison_var, value="matches")
        self.radio_matches.pack(pady=5)

        # Exclusion List
        self.label_exclusions = tk.Label(self, text="Exclusions (comma-separated):")
        self.label_exclusions.pack(pady=5)
        self.entry_exclusions = tk.Entry(self, width=50)
        self.entry_exclusions.pack(pady=5)

        # Process Button
        self.button_process = tk.Button(self, text="Process", command=self.process_files)
        self.button_process.pack(pady=20)

    def browse_file_a(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.entry_file_a.delete(0, tk.END)
            self.entry_file_a.insert(0, filename)

    def browse_file_b(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.entry_file_b.delete(0, tk.END)
            self.entry_file_b.insert(0, filename)

    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_output_dir.delete(0, tk.END)
            self.entry_output_dir.insert(0, directory)

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.entry_file_a.insert(0, settings.get("file_a", ""))
                self.entry_file_b.insert(0, settings.get("file_b", ""))
                self.entry_output_dir.insert(0, settings.get("output_dir", ""))
                self.entry_output_name.insert(0, settings.get("output_name", ""))
        except FileNotFoundError:
            pass

    def save_settings(self):
        settings = {
            "file_a": self.entry_file_a.get(),
            "file_b": self.entry_file_b.get(),
            "output_dir": self.entry_output_dir.get(),
            "output_name": self.entry_output_name.get()
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def process_files(self):
        file_a_path = self.entry_file_a.get()
        file_b_path = self.entry_file_b.get()
        output_dir = self.entry_output_dir.get()
        output_name = self.entry_output_name.get() or "output"
        comparison_option = self.comparison_var.get()
        exclusions = self.entry_exclusions.get().split(',')

        if not (file_a_path and file_b_path and output_dir):
            messagebox.showerror("Error", "Please select both input files and the output directory.")
            return

        try:
            with open(file_a_path, 'r') as file_a, open(file_b_path, 'r') as file_b:
                lines_a = file_a.readlines()
                lines_b = file_b.readlines()

            if len(lines_a) > len(lines_b):
                larger_file, smaller_file = lines_a, lines_b
            else:
                larger_file, smaller_file = lines_b, lines_a

            temp_list = larger_file.copy()
            matches_found = 0

            for line in smaller_file:
                line = self.clean_line(line, exclusions)
                for temp_line in temp_list:
                    if self.compare_lines(line, temp_line, comparison_option, exclusions):
                        temp_list.remove(temp_line)
                        matches_found += 1
                        break

            output_file_path = self.get_unique_output_path(output_dir, output_name)

            with open(output_file_path, 'w') as output_file:
                output_file.writelines(temp_list)

            self.save_settings()
            messagebox.showinfo("Process Complete", f"The file comparison is complete!\nMatches Found: {matches_found}\nOutput File: {output_file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clean_line(self, line, exclusions):
        line = line.lower()
        line = re.sub(r'\d', '', line)
        line = re.sub(r'\W', '', line)
        for exclusion in exclusions:
            line = line.replace(exclusion.strip(), '')
        return line

    def compare_lines(self, line1, line2, comparison_option, exclusions):
        line2 = self.clean_line(line2, exclusions)
        if comparison_option == "matches":
            return line1 == line2
        else:
            return line1 != line2

    def get_unique_output_path(self, output_dir, output_name):
        base_name = os.path.join(output_dir, output_name)
        counter = 0
        output_file_path = f"{base_name}.txt"
        while os.path.exists(output_file_path):
            counter += 1
            output_file_path = f"{base_name}_{counter}.txt"
        return output_file_path

if __name__ == "__main__":
    app = FileDifferenceFinder()
    app.mainloop()
