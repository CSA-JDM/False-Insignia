# Jacob Meadows
# 6th Period, Computer Programming
# 26 October 2018
"""
A simplistic version of
"""
import tkinter as tk


class App(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)

    def __str__(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()
