import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import json

SETTINGS_FILE = "settings.json"

class FileDifferenceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Difference Finder")
        
        self.file_a_path = tk.StringVar()
        self.file_b_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.output_file_name = tk.StringVar()
        
        self.load_settings()
        self.create_widgets()
    
    def create_widgets(self):
        # File A
        tk.Label(self.root, text="Input Text File A:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.file_a_path, width=50).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_file_a).grid(row=0, column=2, padx=10, pady=5)
        
        # File B
        tk.Label(self.root, text="Input Text File B:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.file_b_path, width=50).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_file_b).grid(row=1, column=2, padx=10, pady=5)
        
        # Output Directory
        tk.Label(self.root, text="Output Directory:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.output_dir_path, width=50).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_output_dir).grid(row=2, column=2, padx=10, pady=5)
        
        # Output File Name
        tk.Label(self.root, text="Output File Name (without extension):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.output_file_name, width=50).grid(row=3, column=1, padx=10, pady=5)
        
        # Process Button
        tk.Button(self.root, text="Find Differences", command=self.find_differences).grid(row=4, column=0, columnspan=3, pady=20)
    
    def browse_file_a(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_a_path.set(file_path)
    
    def browse_file_b(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_b_path.set(file_path)
    
    def browse_output_dir(self):
        dir_path = filedialog.askdirectory()
        self.output_dir_path.set(dir_path)
    
    def load_settings(self):
        if os.path.isfile(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                self.file_a_path.set(settings.get("file_a_path", ""))
                self.file_b_path.set(settings.get("file_b_path", ""))
                self.output_dir_path.set(settings.get("output_dir_path", ""))
                self.output_file_name.set(settings.get("output_file_name", ""))
    
    def save_settings(self):
        settings = {
            "file_a_path": self.file_a_path.get(),
            "file_b_path": self.file_b_path.get(),
            "output_dir_path": self.output_dir_path.get(),
            "output_file_name": self.output_file_name.get()
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    
    def get_unique_output_file(self, base_name, extension=".txt"):
        counter = 1
        output_file = os.path.join(self.output_dir_path.get(), f"{base_name}{extension}")
        while os.path.exists(output_file):
            output_file = os.path.join(self.output_dir_path.get(), f"{base_name}_{counter}{extension}")
            counter += 1
        return output_file
    
    def show_completion_message(self, matches, output_file):
        message = f"Operation Complete!\n\nNumber of matches found: {matches}\nOutput file written: {output_file}"
        messagebox.showinfo("Operation Complete", message)
    
    def find_differences(self):
        file_a = self.file_a_path.get()
        file_b = self.file_b_path.get()
        output_dir = self.output_dir_path.get()
        output_file_name = self.output_file_name.get()
        
        if not os.path.isfile(file_a) or not os.path.isfile(file_b):
            messagebox.showerror("Error", "Both input files must be valid text files.")
            return
        
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Please specify a valid output directory.")
            return
        
        if not output_file_name:
            messagebox.showerror("Error", "Please specify a valid output file name.")
            return
        
        output_file = self.get_unique_output_file(output_file_name)
        
        with open(file_a, 'r') as fa, open(file_b, 'r') as fb:
            lines_a = fa.readlines()
            lines_b = fb.readlines()
        
        if len(lines_a) >= len(lines_b):
            larger_list = lines_a
            smaller_list = lines_b
        else:
            larger_list = lines_b
            smaller_list = lines_a
        
        temp_list = larger_list.copy()
        matches = 0
        
        for line in smaller_list:
            if line in temp_list:
                temp_list.remove(line)
                matches += 1
        
        with open(output_file, 'w') as f_out:
            f_out.writelines(temp_list)
        
        self.save_settings()
        self.show_completion_message(matches, output_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileDifferenceApp(root)
    root.mainloop()
