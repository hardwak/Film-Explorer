from data_scraper import get_film_data

import tkinter as tk
from tkinter import ttk
from film_list import FilmList
from user_handler import UserHandler


class FilmExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Film Explorer")
        self.root.geometry("1500x500")

        self.film_list = FilmList()
        self.user_handler = UserHandler()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)

        frame_all = ttk.Frame(notebook)
        frame_to_watch = ttk.Frame(notebook)
        frame_watched = ttk.Frame(notebook)

        notebook.add(frame_all, text="Films")
        notebook.add(frame_to_watch, text="To Watch")
        notebook.add(frame_watched, text="Watched")

        notebook.pack(expand=True, fill=tk.BOTH)

        head_columns = ('Original Index', 'Release date', 'Title', 'Genre', 'Runtime', 'Language', 'Type', 'Rating')

        self.tree_all = ttk.Treeview(frame_all, columns=head_columns, show='headings')
        self.tree_all.heading('Original Index', text='No.', command=lambda: self.sort_by_heading('Original Index'))
        self.tree_all.column('Original Index', width=25, anchor=tk.CENTER)

        self.tree_all.heading('Release date', text='Release date', command=lambda: self.sort_by_heading('Release date'))
        self.tree_all.column('Release date', width=60, anchor=tk.CENTER)

        self.tree_all.heading('Title', text='Title', command=lambda: self.sort_by_heading('Title'))
        self.tree_all.column('Title', width=300)

        self.tree_all.heading('Genre', text='Genre', command=lambda: self.sort_by_heading('Genre'))
        self.tree_all.column('Genre', width=120)

        self.tree_all.heading('Runtime', text='Runtime', command=lambda: self.sort_by_heading('Runtime'))
        self.tree_all.column('Runtime', width=40)

        self.tree_all.heading('Language', text='Language', command=lambda: self.sort_by_heading('Language'))
        self.tree_all.column('Language', width=80)

        self.tree_all.heading('Type', text='Type', command=lambda: self.sort_by_heading('Type'))
        self.tree_all.column('Type', width=80)

        self.tree_all.heading('Rating', text='Rating', command=lambda: self.sort_by_heading('Rating'))
        self.tree_all.column('Rating', width=25, anchor=tk.CENTER)

        self.scrollbar = ttk.Scrollbar(frame_all, orient=tk.VERTICAL, command=self.tree_all.yview)
        self.tree_all.configure(yscroll=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_all.pack(expand=True, fill=tk.BOTH)

        # Add a scrollbar

    def sort_by_heading(self, column):
        for item in self.tree_all.get_children():
            self.tree_all.delete(item)

        self.tree_all.heading(column)
        self.load_data(self.film_list.sort_by(column))

    def load_data(self, films=None):
        if films is None:
            films = self.film_list.get_formatted_film_data()
        for _, row in films.iterrows():
            self.tree_all.insert('', 'end', values=(row['Original Index'], row['Release date'],
                                                    row['Title'], row['Genre'], row['Runtime'], row['Language'],
                                                    row['Type'], row['Rating']))


if __name__ == "__main__":
    root = tk.Tk()
    app = FilmExplorerApp(root)
    root.mainloop()
