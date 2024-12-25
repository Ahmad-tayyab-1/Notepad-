import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser, ttk


class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Untitled - Notepad")
        self.root.geometry("800x600")

        self.file = None
        self.text_changed = False

        # Font settings
        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.text_color = "black"

        self.root.bind("<Control-s>", lambda event: self.save_file())

        # Text widget
        self.text_area = tk.Text(
            root, wrap='word', undo=True, font=(self.current_font_family, self.current_font_size), fg=self.text_color
        )
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.text_area.bind("<<Modified>>", self.on_text_change)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_notepad)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_command(label="Delete", command=self.delete_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Format menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.format_menu.add_command(label="Font Family", command=self.change_font_family)
        self.format_menu.add_command(label="Font Size", command=self.change_font_size)
        self.format_menu.add_command(label="Font Color", command=self.change_font_color)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Handle closing
        self.root.protocol("WM_DELETE_WINDOW", self.exit_notepad)

    def on_text_change(self, event=None):
        if self.text_area.edit_modified():
            self.text_changed = True
            title = f"*{self.file} - Notepad" if self.file else "*Untitled - Notepad"
            self.root.title(title)
            self.text_area.edit_modified(False)

    def new_file(self):
        if self.text_changed:
            self.prompt_save_changes()
        self.text_area.delete(1.0, tk.END)
        self.file = None
        self.text_changed = False
        self.root.title("Untitled - Notepad")

    def open_file(self):
        if self.text_changed:
            self.prompt_save_changes()
        self.file = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if self.file:
            with open(self.file, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
            self.text_changed = False
            self.root.title(f"{self.file} - Notepad")

    def save_file(self):
        if self.file:  # Save to the existing file
            try:
                with open(self.file, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END).rstrip())  # Remove trailing newline
                self.text_changed = False
                self.root.title(f"{self.file} - Notepad")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {e}")
        else:  # If no file exists, fall back to Save As
            self.save_as_file()

    def save_as_file(self):
        self.file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if self.file:
            with open(self.file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.text_changed = False
            self.root.title(f"{self.file} - Notepad")

    def exit_notepad(self):
        if self.text_changed:
            self.prompt_save_changes()
        self.root.destroy()

    def prompt_save_changes(self):
        response = messagebox.askyesnocancel("Notepad", "Do you want to save changes?")
        if response:  # Save and exit
            self.save_file()
        elif response is None:  # Cancel exit
            return

    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def delete_text(self):
        try:
            self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass

    def change_font_family(self):
        font_window = tk.Toplevel(self.root)
        font_window.title("Choose Font Family")
        font_window.geometry("300x200")

        tk.Label(font_window, text="Select Font Family:").pack(pady=10)

        font_list = ttk.Combobox(font_window, values=list(font.families()), state="readonly")
        font_list.set(self.current_font_family)
        font_list.pack(pady=10)

        def set_font_family():
            selected_font = font_list.get()
            if selected_font:
                self.current_font_family = selected_font
                self.text_area.config(font=(self.current_font_family, self.current_font_size))
            font_window.destroy()

        tk.Button(font_window, text="Apply", command=set_font_family).pack(pady=10)

    def change_font_size(self):
        new_size = tk.simpledialog.askinteger("Font Size", "Enter font size (e.g., 8, 12, 16):", minvalue=1, maxvalue=100)
        if new_size:
            self.current_font_size = new_size
            self.text_area.config(font=(self.current_font_family, self.current_font_size))

    def change_font_color(self):
        new_color = colorchooser.askcolor(title="Choose font color")[1]
        if new_color:
            self.text_color = new_color
            self.text_area.config(fg=self.text_color)

    def show_about(self):
        messagebox.showinfo("About", "Notepad application created with tkinter in Python .")


if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
