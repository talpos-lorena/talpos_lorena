import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DATA_FILE = "data.json"

# Manager pentru date JSON
class BookManager:
    def __init__(self):
        self.books = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.books = json.load(f)
        else:
            self.books = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, indent=4, ensure_ascii=False)

    def add_book(self, book):
        self.books.append(book)
        self.save_data()

    def update_book(self, index, new_data):
        self.books[index] = new_data
        self.save_data()

    def delete_book(self, index):
        del self.books[index]
        self.save_data()


# Formular pentru Adăugare/Editare
class FormWindow(tk.Toplevel):
    def __init__(self, parent, manager, refresh_callback, book_index=None):
        super().__init__(parent)
        self.manager = manager
        self.refresh_callback = refresh_callback
        self.book_index = book_index

        self.title("Carte nouă" if book_index is None else "Editează cartea")
        self.geometry("300x200")

        self.create_form()
        if book_index is not None:
            self.load_data()

    def create_form(self):
        tk.Label(self, text="Titlu:").pack()
        self.titlu_entry = tk.Entry(self)
        self.titlu_entry.pack()

        tk.Label(self, text="Autor:").pack()
        self.autor_entry = tk.Entry(self)
        self.autor_entry.pack()

        tk.Label(self, text="An publicare:").pack()
        self.an_entry = tk.Entry(self)
        self.an_entry.pack()

        tk.Button(self, text="Salvează", command=self.save).pack(pady=10)

    def load_data(self):
        book = self.manager.books[self.book_index]
        self.titlu_entry.insert(0, book["titlu"])
        self.autor_entry.insert(0, book["autor"])
        self.an_entry.insert(0, str(book["an"]))

    def save(self):
        titlu = self.titlu_entry.get().strip()
        autor = self.autor_entry.get().strip()
        try:
            an = int(self.an_entry.get().strip())
        except ValueError:
            messagebox.showerror("Eroare", "Anul trebuie să fie un număr.")
            return

        if not titlu or not autor:
            messagebox.showerror("Eroare", "Toate câmpurile sunt obligatorii.")
            return

        book = {"titlu": titlu, "autor": autor, "an": an}

        if self.book_index is None:
            self.manager.add_book(book)
        else:
            self.manager.update_book(self.book_index, book)

        self.refresh_callback()
        self.destroy()


# Fereastra Principală
class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.manager = BookManager()
        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Adaugă", width=10, command=self.add_book).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Editează", width=10, command=self.edit_book).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Șterge", width=10, command=self.delete_book).pack(side="left", padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for idx, book in enumerate(self.manager.books):
            self.listbox.insert(tk.END, f"{idx + 1}. {book['titlu']} - {book['autor']} ({book['an']})")

    def add_book(self):
        FormWindow(self, self.manager, self.refresh_list)

    def edit_book(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Atenție", "Selectați o carte pentru editare.")
            return
        index = selected[0]
        FormWindow(self, self.manager, self.refresh_list, index)

    def delete_book(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Atenție", "Selectați o carte pentru ștergere.")
            return
        index = selected[0]
        if messagebox.askyesno("Confirmare", "Sigur doriți să ștergeți această carte?"):
            self.manager.delete_book(index)
            self.refresh_list()


# Punct de pornire aplicație
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Catalog de Cărți")
    root.geometry("500x400")
    app = MainWindow(root)
    root.mainloop()