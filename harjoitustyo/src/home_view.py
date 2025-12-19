from tkinter import ttk, constants

class HomeView:
    def __init__(self, root, change_to_rating, change_to_h2h, change_to_draw):
        self._root = root
        self._change_to_rating = change_to_rating
        self._change_to_h2h = change_to_h2h
        self._change_to_draw = change_to_draw
        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        label = ttk.Label(master=self._frame, text="Home View")
        button = ttk.Button(
            master=self._frame,
            text="Ratinglist",
            command=self._change_to_rating
        )

        h2h_button = ttk.Button(
            master=self._frame,
            text="Head to head record calculator",
            command=self._change_to_h2h
        )

        draw_button = ttk.Button(
            master=self._frame,
            text='Draw generator',
            command=self._change_to_draw
        )


        label.grid(row=0, column=0)
        button.grid(row=1, column=0)
        h2h_button.grid()
        draw_button.grid()
