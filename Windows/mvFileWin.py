import os
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Extension presets for dropdown
EXTENSION_PRESETS = {
    "All Files": "",
    "Image Files": "png, jpg, jpeg, gif, bmp, tiff, webp, svg",
    "Installer Files": "exe, msi, msix, dmg, deb, pkg, rpm",
    "Audio Files": "mp3, wav, ogg, flac, aac",
    "Video Files": "mp4, avi, mkv, mov, mpg, webm",
    "Document Files": "pdf, doc, docx, txt, xls, xlsx, ppt, pptx"
}

class FileMoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk File Mover/Copy Utility")

        # Source Directory
        self.src_label = ttk.Label(root, text="Source Directory:")
        self.src_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.src_path = tk.StringVar()
        self.src_entry = ttk.Entry(root, textvariable=self.src_path, width=40)
        self.src_entry.grid(row=0, column=1, padx=5, pady=5)
        self.src_button = ttk.Button(root, text="Browse", command=self.browse_src)
        self.src_button.grid(row=0, column=2, padx=5)

        # Target Directory
        self.dst_label = ttk.Label(root, text="Target Directory:")
        self.dst_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.dst_path = tk.StringVar()
        self.dst_entry = ttk.Entry(root, textvariable=self.dst_path, width=40)
        self.dst_entry.grid(row=1, column=1, padx=5, pady=5)
        self.dst_button = ttk.Button(root, text="Browse", command=self.browse_dst)
        self.dst_button.grid(row=1, column=2, padx=5)

        # Extension preset dropdown
        self.ext_group_label = ttk.Label(root, text="File Type Preset:")
        self.ext_group_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ext_group_var = tk.StringVar(value="All Files")
        self.ext_group_menu = ttk.Combobox(
            root, textvariable=self.ext_group_var,
            values=list(EXTENSION_PRESETS.keys()), state="readonly"
        )
        self.ext_group_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.ext_group_menu.bind("<<ComboboxSelected>>", self.set_extensions_from_dropdown)

        # Extension entry
        self.ext_label = ttk.Label(root, text="File Extension(s):")
        self.ext_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.ext_var = tk.StringVar()
        self.ext_entry = ttk.Entry(root, textvariable=self.ext_var, width=40)
        self.ext_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Search Button
        self.search_button = ttk.Button(root, text="Find Files", command=self.find_files)
        self.search_button.grid(row=4, column=1, padx=5, pady=20, sticky="w")

        # Listbox for found files
        self.files_listbox = tk.Listbox(root, width=70, height=15)
        self.files_listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        # Operation Buttons
        self.copy_button = ttk.Button(root, text="Copy Files", command=self.copy_files)
        self.copy_button.grid(row=6, column=0, padx=5, pady=10)
        self.move_button = ttk.Button(root, text="Move Files", command=self.move_files)
        self.move_button.grid(row=6, column=1, padx=5, pady=10)
        self.clear_button = ttk.Button(root, text="Clear List", command=self.clear_list)
        self.clear_button.grid(row=6, column=2, padx=5, pady=10)

        # Internal
        self.found_files = []

    def set_extensions_from_dropdown(self, event=None):
        preset = EXTENSION_PRESETS.get(self.ext_group_var.get(), "")
        self.ext_var.set(preset)

    def browse_src(self):
        path = filedialog.askdirectory()
        if path:
            self.src_path.set(path)

    def browse_dst(self):
        path = filedialog.askdirectory()
        if path:
            self.dst_path.set(path)

    def find_files(self):
        self.files_listbox.delete(0, tk.END)
        self.found_files = []
        src = os.path.normpath(self.src_path.get())
        ext_text = self.ext_var.get()
        if not src or not os.path.isdir(src):
            messagebox.showerror("Error", "Please select a valid source directory.")
            return
        # Split input on commas or spaces, and clean up
        extensions = [x.strip().lstrip('.') for x in ext_text.replace(',', ' ').split() if x.strip()]
        count = 0
        for ext in extensions:
            if ext:
                pattern = f"**/*.{ext}"
                for fp in Path(src).glob(pattern):
                    if fp.is_file():
                        self.found_files.append(fp)
                        self.files_listbox.insert(tk.END, str(fp))
                        count += 1
        if not extensions or all([not e for e in extensions]):
            # No extension entered -- find all files
            for fp in Path(src).glob("**/*"):
                if fp.is_file():
                    self.found_files.append(fp)
                    self.files_listbox.insert(tk.END, str(fp))
                    count += 1
        messagebox.showinfo("File Search", f"Found {count} file(s){' with specified extensions' if extensions else ''}.")

    def copy_files(self):
        self._execute_file_op(shutil.copy2, "copied")

    def move_files(self):
        self._execute_file_op(shutil.move, "moved")

    def _execute_file_op(self, op, op_name):
        dst = os.path.normpath(self.dst_path.get())
        if not dst:
            messagebox.showerror("Error", "Please select a valid target directory.")
            return
        if not os.path.exists(dst):
            if messagebox.askyesno("Create Directory", f"{dst} does not exist. Create it?"):
                os.makedirs(dst)
            else:
                return
        count = 0
        for fp in self.found_files:
            fname = os.path.basename(fp)
            new_path = os.path.join(dst, fname)
            try:
                op(fp, new_path)
                count += 1
            except Exception as e:
                messagebox.showerror("Operation Error", f"Failed on {fp}:\n{e}")
        messagebox.showinfo("Operation Complete", f"{count} file(s) {op_name}.")

    def clear_list(self):
        self.files_listbox.delete(0, tk.END)
        self.found_files = []

if __name__ == "__main__":
    root = tk.Tk()
    FileMoverGUI(root)
    root.mainloop()
