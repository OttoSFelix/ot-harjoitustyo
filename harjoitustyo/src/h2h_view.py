import tkinter as tk
from tkinter import ttk, constants
from search import get_h2h_record

class H2HView:
    def __init__(self, root, change_to_home):
        self._root = root
        self._change_to_home = change_to_home
        self._frame = None
        self._player1_entry = None
        self._player2_entry = None
        self._result_label = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)

    def destroy(self):
        self._frame.destroy()

    def _handle_search(self):
        p1_name = self._player1_entry.get().strip()
        p2_name = self._player2_entry.get().strip()

        if not p1_name or not p2_name:
            self._result_label.config(text="Please enter both player names", foreground="red")
            return

        result_text = get_h2h_record(p1_name, p2_name)
        self._result_label.config(text=result_text, foreground="")

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        header_frame = ttk.Frame(self._frame)
        header_frame.pack(fill=constants.X, padx=10, pady=10)

        title = ttk.Label(header_frame, text="Head-to-Head Comparison", font=("Arial", 14, "bold"))
        title.pack(side=constants.LEFT)

        home_btn = ttk.Button(header_frame, text="Home", command=self._change_to_home)
        home_btn.pack(side=constants.RIGHT)

        input = ttk.Frame(self._frame)
        input.pack(pady=20)

        ttk.Label(input, text="Player 1 Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self._player1_entry = ttk.Entry(input, width=25)
        self._player1_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input, text="Player 2 Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self._player2_entry = ttk.Entry(input, width=25)
        self._player2_entry.grid(row=1, column=1, padx=5, pady=5)

        search_btn = ttk.Button(input, text="Compare Players", command=self._handle_search)
        search_btn.grid(row=2, column=0, columnspan=2, pady=15)

        self._result_label = ttk.Label(
            self._frame, 
            text="", 
            font=("Arial", 12),
            anchor="center",
            justify="center",
            wraplength=500 
        )
        self._result_label.pack(pady=10, padx=20)