
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import time
import json

class GoogleSearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Google Search")
        
        # File selection
        self.file_label = tk.Label(master, text="Select text file:")
        self.file_label.grid(row=0, column=0, sticky='w')
        self.file_entry = tk.Entry(master, width=40)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Prefix input
        self.prefix_label = tk.Label(master, text="Prefix:")
        self.prefix_label.grid(row=1, column=0, sticky='w')
        self.prefix_entry = tk.Entry(master, width=40)
        self.prefix_entry.grid(row=1, column=1, padx=5, pady=5)

        # Suffix input
        self.suffix_label = tk.Label(master, text="Suffix:")
        self.suffix_label.grid(row=2, column=0, sticky='w')
        self.suffix_entry = tk.Entry(master, width=40)
        self.suffix_entry.grid(row=2, column=1, padx=5, pady=5)

        # Search button
        self.search_button = tk.Button(master, text="Search", command=self.search_google)
        self.search_button.grid(row=3, column=1, padx=5, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def search_google(self):
        file_path = self.file_entry.get()
        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                prefix_corrected = prefix
                suffix_corrected = suffix
                if prefix_corrected and not prefix_corrected.endswith(' '):
                    prefix_corrected += ' '
                if suffix_corrected and not suffix_corrected.startswith(' '):
                    suffix_corrected = ' ' + suffix_corrected
                for line in lines:
                    term = prefix_corrected + line.strip() + suffix_corrected
                    search_url = f"https://www.google.com/search?q={term}"
                    webbrowser.open_new_tab(search_url)
                    time.sleep(0.25)  # Pause for 0.25 seconds
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")

def main():
    root = tk.Tk()
    app = GoogleSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

