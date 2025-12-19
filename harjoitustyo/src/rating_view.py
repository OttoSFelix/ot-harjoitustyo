import tkinter as tk
from tkinter import ttk, constants
from db_search import get_nth_players, get_player_base_stats, get_seasonal_stats, get_name
from web_search import get_rating

class RatingView:
    def __init__(self, root, change_to_home, cursor, connection):
        self._cursor = cursor
        self._connection = connection
        self._root = root
        self._change_to_home = change_to_home
        self._frame = None
        self._scrollable_frame = None
        self._search_entry = None
        self._style = ttk.Style()
        self._style.configure("Green.TCheckbutton", foreground="green")

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)

    def destroy(self):
        self._frame.destroy()

    def _handle_search(self):
        name = self._search_entry.get().strip()
        name = get_name(name, self._cursor)
        if not name:
            self._handle_show_all()
            return
        seasonal_matches = get_seasonal_stats(name, self._cursor)
        stats_text = get_player_base_stats(name, self._cursor)
        text = [stats_text]
        for season, stats in seasonal_matches.items():
            text.append(f"""{season}
            Matches played: {stats[0]}
            Wins: {stats[1]}
            Losses: {stats[2]}
            Winrate: {stats[3]}
""")
        self._update_scroll_view(text)

    def _handle_show_all(self):
        players = get_nth_players(100, self._cursor)
        stats_list = [get_player_base_stats(p.name, self._cursor) for p in players]
        self._update_scroll_view(stats_list)

    def _update_scroll_view(self, data_list):
        for widget in self._scrollable_frame.winfo_children():
            widget.destroy()

        for text_content in data_list:
            card = ttk.Frame(self._scrollable_frame, relief="groove", borderwidth=1)
            card.pack(fill=constants.X, padx=5, pady=2)
            lbl = ttk.Label(master=card, text=text_content)
            lbl.pack(padx=5, pady=5, anchor="w")

    def _update_rating(self):
        get_rating(connection=self._connection)
        self._connection.commit()
        players = get_nth_players(100, self._cursor)
        stats_list = [get_player_base_stats(p.name, self._cursor) for p in players]
        self._update_scroll_view(stats_list)
        style = 'Green.TCheckbutton'
        self._update_status.config(text='Updated to newest rating', font=('Arial', 14), style=style)


    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        header_frame = ttk.Frame(self._frame)
        header_frame.pack(fill=constants.X, padx=10, pady=10)

        title_lbl = ttk.Label(header_frame, text="Ratinglist", font=("Arial", 14, "bold"))
        title_lbl.pack(side=constants.LEFT)

        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side=constants.RIGHT)
        self._search_entry = ttk.Entry(controls_frame, width=20)
        self._search_entry.pack(side=constants.LEFT, padx=5)

        search_btn = ttk.Button(controls_frame, text="Search", command=self._handle_search)
        search_btn.pack(side=constants.LEFT, padx=5)

        reset_btn = ttk.Button(controls_frame, text="Show All", command=self._handle_show_all)
        reset_btn.pack(side=constants.LEFT, padx=5)

        home_btn = ttk.Button(controls_frame, text="Home", command=self._change_to_home)
        home_btn.pack(side=constants.LEFT, padx=5)

        upd_text = 'Update to newest rating'
        update_btn = ttk.Button(controls_frame, text=upd_text, command=self._update_rating)
        update_btn.pack(side=constants.LEFT, padx=5)
        self._update_status = ttk.Label(header_frame)
        self._update_status.pack(side=constants.LEFT, padx=5)

        canvas = tk.Canvas(self._frame)
        scrollbar = ttk.Scrollbar(self._frame, orient="vertical", command=canvas.yview)
        self._scrollable_frame = ttk.Frame(canvas)

        self._scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self._scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=constants.LEFT, fill=constants.BOTH, expand=True)
        scrollbar.pack(side=constants.RIGHT, fill=constants.Y)
        self._handle_show_all()
