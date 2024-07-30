import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FileDifferenceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Difference Finder")
        
        self.file_a_path = tk.StringVar()
        self.file_b_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
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
        
        # Output File
        tk.Label(self.root, text="Output Result File:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=2, column=2, padx=10, pady=5)
        
        # Process Button
        tk.Button(self.root, text="Find Differences", command=self.find_differences).grid(row=3, column=0, columnspan=3, pady=20)
    
    def browse_file_a(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_a_path.set(file_path)
    
    def browse_file_b(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_b_path.set(file_path)
    
    def browse_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        self.output_path.set(file_path)
    
    def find_differences(self):
        file_a = self.file_a_path.get()
        file_b = self.file_b_path.get()
        output_file = self.output_path.get()
        
        if not os.path.isfile(file_a) or not os.path.isfile(file_b):
            messagebox.showerror("Error", "Both input files must be valid text files.")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please specify a valid output file.")
            return
        
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
        
        for line in smaller_list:
            if line in temp_list:
                temp_list.remove(line)
        
        with open(output_file, 'w') as f_out:
            f_out.writelines(temp_list)
        
        messagebox.showinfo("Success", "The differences have been written to the output file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileDifferenceApp(root)
    root.mainloop()
