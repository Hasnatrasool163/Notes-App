#########Code written by Muhammad Hasnat Rasool#####################

# A basic implementation of a notes app with features like
#           save , search and load notes


##########################start#############################

# imports

from tkinter import simpledialog, messagebox, filedialog, Menu
from cryptography.fernet import Fernet
import os
from customtkinter import (
    CTk,
    CTkTextbox,
    CTkToplevel,
    set_appearance_mode,
    set_default_color_theme,
    CTkOptionMenu,
)

# color theme and mode

set_default_color_theme("Hades")
set_appearance_mode("system")


class NotesApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple Secured Notes App")
        master.geometry("800x500")
        master.resizable(False, True)

        self.notes_dir = "notes"
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)

        # Generate or load a key for encryption
        self.key_file = "secret.key"
        self.key = self.load_or_generate_key()

        self.text = CTkTextbox(
            master,
            fg_color="#40E0D0",
            wrap=None,
            text_color="purple",
            scrollbar_button_color="yellow",
            scrollbar_button_hover_color="orange",
            border_color="orange",
            spacing1=5,
            spacing2=5,
            spacing3=10,
            undo=True,
            font=("consolas", 22),
            corner_radius=10,
            tabs=4,
            activate_scrollbars=True,
        )
        self.text.pack(expand=True, fill="both", padx=10, pady=5)

        self.menu = Menu(
            master,
            fg="yellow",
            bg="green",
            cursor="hand2",
            takefocus=0,
            activebackground="green",
            activeforeground="yellow",
            border=2,
        )
        root.configure(menu=self.menu, bg_color="green")
        self.menu.configure(bg="green", fg="yellow")

        self.file_menu = Menu(
            self.menu,
            tearoff=0,
            fg="yellow",
            relief="solid",
            font=("helvetica", 10),
            bg="green",
        )
        self.menu.add_cascade(
            label="File",
            menu=self.file_menu,
            foreground="green",
            background="yellow",
            font=("helvetica", 12),
            activebackground="yellow",
            activeforeground="green",
        )
        self.file_menu.add_command(
            label="New Note",
            command=self.new_note,
            font=("helvetica", 10),
            foreground="yellow",
            background="green",
        )
        self.file_menu.add_command(
            label="Save Note", command=self.save_note, font=("helvetica", 10)
        )
        self.file_menu.add_command(
            label="Load Note", command=self.load_note, font=("helvetica", 10)
        )
        self.file_menu.add_command(
            label="Search Note", command=self.search_note, font=("helvetica", 10)
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)
        # self.file_menu.add_command(label="Instructions", command=self.instruct)

        self.menu.add_cascade(
            label="New note",
            command=self.new_note,
            font=("helvetica", 12),
            activebackground="green",
            activeforeground="yellow",
        )
        self.menu.add_cascade(
            label="Save note",
            command=self.save_note,
            background="green",
            foreground="yellow",
        )
        self.menu.add_cascade(
            label="Search", command=self.search_note, font=("helvetica", 12)
        )
        self.menu.add_cascade(
            label="Load", command=self.load_note, font=("helvetica", 12)
        )
        self.menu.add_cascade(
            label="Instructions", command=self.instruct, font=("helvetica", 12)
        )

    def instruct(self):
        window = CTkToplevel(root, height=400, width=500, fg_color="grey")
        window.title("Instruction-Window!")
        window.resizable(False, False)
        textbox = CTkTextbox(
            window,
            text_color="green",
            font=("consolas", 20),
            width=480,
            height=220,
            border_color="orange",
            undo=False,
        )
        textbox.pack()
        textbox.insert(
            "0.0",
            text="Free Notes App use load and search feature\nEasy to use all options available in menu!\nIf you have encrypted any notes \n->Then use load to decrypt the notes.\n\n\tThankyou for using the notes App",
        )

    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as keyfile:
                key = keyfile.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as keyfile:
                keyfile.write(key)
        return key

    def encrypt_text(self, text):
        f = Fernet(self.key)
        return f.encrypt(text.encode())

    def decrypt_text(self, encrypted_text):
        f = Fernet(self.key)
        try:
            return f.decrypt(encrypted_text).decode()
        except:
            messagebox.showerror(
                "Error", "Failed to decrypt the note. Incorrect key or corrupted file."
            )
            return None

    def new_note(self):
        self.text.delete("0.0", "end")

    def save_note(self):
        note_text = self.text.get("0.0", "end")
        self.text.delete("0.0", "end")
        heading = simpledialog.askstring("Save Note", "Enter heading:")
        is_secure = messagebox.askyesno("Save Note", "Do you want to secure this note?")
        if heading:
            file_path = os.path.join(self.notes_dir, f"{heading}.txt")
            if is_secure:
                encrypted_text = self.encrypt_text(note_text)
                with open(file_path, "wb") as file:
                    file.write(encrypted_text)
            else:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(note_text)
            messagebox.showinfo("Save Note", "Note saved successfully!")

    def load_note(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.notes_dir,
            title="Select Note",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    note_data = file.read()
                # Attempt to decrypt, might be encrypted
                decrypted_text = self.decrypt_text(note_data)
                if decrypted_text is not None:
                    note_text = decrypted_text
                else:
                    # Assuming it's not encrypted if decryption failed
                    note_text = note_data.decode("utf-8")
            except Exception as e:
                messagebox.showerror("Error", "Failed to load the note.")
                return

            self.text.delete("0.0", "end")
            self.text.insert("0.0", note_text)

    def search_note(self):
        search_query = simpledialog.askstring(
            "Search Note", "Enter note heading to search:"
        )
        if search_query:
            for filename in os.listdir(self.notes_dir):
                if search_query.lower() in filename.lower():
                    full_path = os.path.join(self.notes_dir, filename)
                    with open(full_path, "r") as file:
                        note_text = file.read()
                    self.text.delete("0.0", "end")
                    self.text.insert("0.0", note_text)
                    return
            messagebox.showerror("Search Note", "No note found with that heading.")


if __name__ == "__main__":
    root = CTk()
    app = NotesApp(root)
    # main loop
    root.mainloop()

##################END#################################
# this is a basic implementation
# feel free to expand it make it better!
# thankyou for reading

