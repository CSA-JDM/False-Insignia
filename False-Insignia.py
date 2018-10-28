# Jacob Meadows
# 6th Period, Computer Programming
# 26 October 2018
"""
A simplistic version of Final Fantasy
Copyright (C) 2018  Jacob Meadows

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import tkinter as tk
import ctypes


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class App(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title("False Insignia")
        self.master.geometry(f"{screensize[0]}x{screensize[1]}+0+0")
        self.master.overrideredirect(1)
        super().__init__(self.master, width=screensize[0], height=screensize[1])
        self.active = [0]
        self.place(relx=0, rely=0)

        self.widgets = dict()
        self.main_menu()

    def main_menu(self):
        self.reset_window()
        self.widgets["title_label"] = tk.Label(self, text="False Insignia", font=("Times New Roman", 40, "bold"))
        self.widgets["title_label"].place(relx=5 / screensize[0], rely=5 / screensize[1])
        self.widgets["new_game_button"] = tk.Button(self, text="New Game", command=self.introduction, width=20,
                                                    height=2, font=("Times New Roman", 16))
        self.widgets["new_game_button"].place(relx=5 / screensize[0], rely=195 / screensize[1])
        self.widgets["load_game_button"] = tk.Button(self, text="Load Game", command=self.load_menu, width=20,
                                                     height=2, font=("Times New Roman", 16))
        self.widgets["load_game_button"].place(relx=5 / screensize[0], rely=265 / screensize[1])
        self.widgets["options_button"] = tk.Button(self, text="Options", command=self.options_menu, width=20, height=2,
                                                   font=("Times New Roman", 16))
        self.widgets["options_button"].place(relx=5 / screensize[0], rely=335 / screensize[1])
        self.widgets["exit_button"] = tk.Button(self, text="Exit", command=self.exit_choice, width=20, height=2,
                                                font=("Times New Roman", 16))
        self.widgets["exit_button"].place(relx=5 / screensize[0], rely=415 / screensize[1])
        self.master.bind("<Motion>", self.button_highlight)
        for widget in self.widgets.values():
            if isinstance(widget, tk.Button):
                widget.bind("<Motion>", self.button_highlight)

    def username_input(self):
        pass

    def load_menu(self):
        pass

    def options_menu(self):
        pass

    def exit_choice(self):
        self.master.unbind("<Motion>")
        for widget in self.widgets.values():
            widget.config(state="disabled")
            widget.unbind("<Motion>")
        self.widgets["exit_frame"] = tk.Frame(self, width=200, height=60)
        self.widgets["exit_label"] = tk.Label(self.widgets["exit_frame"], text="Are you sure you want to quit?")
        self.widgets["exit_label"].place(x=0, y=0)
        self.widgets["exit_yes_button"] = tk.Button(self.widgets["exit_frame"], text="Yes", command=self.quit)
        self.widgets["exit_yes_button"].place(x=0, y=30)
        self.widgets["exit_yes_button"] = tk.Button(self.widgets["exit_frame"], text="No", command=self.main_menu)
        self.widgets["exit_yes_button"].place(x=100, y=30)
        self.widgets["exit_frame"].place(x=0, y=0)
        self.widgets["exit_frame"].update()
        self.widgets["exit_frame"].place(
            relx=(screensize[0] / 2) / screensize[0], rely=(screensize[1] / 2) / screensize[1], anchor="center"
        )

    def introduction(self):
        pass

    def button_highlight(self, event):
        for widget in self.widgets.values():
            if isinstance(widget, tk.Button):
                widget.update()
                widget_x, widget_y = widget.winfo_geometry().split("+")[1:]
                widget_x, widget_y = int(widget_x), int(widget_y)
                widget_width, widget_height = int(widget.winfo_width()), int(widget.winfo_height())
                if event.x_root in range(widget_x, widget_x + widget_width) and \
                        event.y_root in range(widget_y, widget_y + widget_height) and self.active[-1] == 0:
                    self.active[-1] = 1
                    self.button_animation(widget)
                else:
                    for _widget in self.widgets.values():
                        if isinstance(_widget, tk.Button):
                            _widget.update()
                            _widget_x, _widget_y = _widget.winfo_geometry().split("+")[1:]
                            _widget_x, _widget_y = int(_widget_x), int(_widget_y)
                            _widget_width, _widget_height = int(_widget.winfo_width()), int(_widget.winfo_height())
                            if _widget["width"] != 20 and \
                                    (event.x_root not in range(_widget_x, _widget_x + _widget_width) or
                                     event.y_root not in range(_widget_y, _widget_y + _widget_height)):
                                self.active[-1] = 0
                                _widget.config(width=20)
                                if event.x_root in range(widget_x, widget_x + widget_width) and \
                                        event.y_root in range(widget_y, widget_y + widget_height) and self.active[-1] == 0:
                                    self.active[-1] = 1
                                    self.button_animation(widget)

    def button_animation(self, widget):
        if self.active[-1] != 0 and len([_widget for _widget in self.widgets.values()
                                         if isinstance(_widget, tk.Button) and _widget["width"] != 20]) < 2:
            widget.update()
            if widget["width"] < 25:
                widget.config(width=widget["width"] + 1)
                self.after(20, lambda: self.button_animation(widget))
        else:
            widget.config(width=20)

    def reset_window(self):
        for widget in self.widgets.values():
            widget.destroy()
        self.widgets = dict()
        self.active[-1] = 0

    def __str__(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()
