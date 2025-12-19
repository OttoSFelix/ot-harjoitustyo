import tkinter as tk
import os
from draw_generator import generate
from web_search import validate_date

class DrawView:
    def __init__(self, root, change_to_home, connection):
        self._root = root
        self._change_to_home = change_to_home
        self._connection = connection
        self._cursor = self._connection.cursor()

    def pack(self):
        self._frame = tk.Frame(master=self._root)
        self._file_label = tk.Label(master=self._frame, text="No file selected")
        self._file_button = tk.Button(
            master=self._frame, text="Select file", command=self._select_file
        )
        self._date_label = tk.Label(master=self._frame, text="Date (DD.MM.YYYY)")
        self._date_entry = tk.Entry(master=self._frame)
        self._date_validation = tk.Label(master=self._frame)
        self._generate_button = tk.Button(
            master=self._frame, text="Generate", command=self._generate
        )
        self._home_button = tk.Button(
            master=self._frame, text="Home", command=self._change_to_home
        )

        self._file_label.pack()
        self._file_button.pack()
        self._date_label.pack()
        self._date_entry.pack()
        self._date_validation.pack()
        self._generate_button.pack()
        self._home_button.pack()
        self._frame.pack()

    def _select_file(self):
        self._file = tk.filedialog.askopenfilename()
        self._file_label.config(text=self._file)

    def _generate(self):
        date = self._date_entry.get()
        validate_text = validate_date(date)
        if validate_text:
            self._date_validation.config(text = validate_text)
        generate(self._file, date)
        os.system("open Competition_Draw.xlsx")

    def destroy(self):
        self._frame.destroy()