from tkinter import Tk
from home_view import HomeView
from rating_view import RatingView
from h2h_view import H2HView
from database_connection import get_database_connection

class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None
        self.connection = get_database_connection()
        self.cursor = self.connection.cursor()

    def start(self):
        self._show_home_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _change_to_rating(self):
        self._show_rating_view()

    def _change_to_home(self):
        self._show_home_view()

    def _show_home_view(self):
        self._hide_current_view()

        self._current_view = HomeView(
            self._root,
            self._change_to_rating,
            self._change_to_h2h
        )

        self._current_view.pack()

    def _show_rating_view(self):
        self._hide_current_view()

        self._current_view = RatingView(
            self._root,
            self._change_to_home,
            self.cursor,
            self.connection
        )

        self._current_view.pack()

    def _change_to_h2h(self):
        self._show_h2h_view()

    def _show_h2h_view(self):
        self._hide_current_view()

        self._current_view = H2HView(
            self._root,
            self._change_to_home,
            self.cursor
        )

        self._current_view.pack()

window = Tk()
window.title("Player Statistics")

ui = UI(window)
ui.start()

window.mainloop()