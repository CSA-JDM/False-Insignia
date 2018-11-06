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
from tkinter import ttk as ttk
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
        self.place(relx=0, rely=0)

        self.active = [0]
        self.widgets = dict()
        self.vars = dict()
        self.main_menu()

    def main_menu(self):
        self.reset_window()
        self.widgets["title_label"] = tk.Label(self, text="False Insignia", font=("Times New Roman", 60, "bold"))
        self.widgets["title_label"].place(relx=5 / screensize[0], rely=5 / screensize[1])
        self.widgets["new_game_button"] = tk.Button(self, text="New Game", command=self.character_sheet, width=20,
                                                    height=2, font=("Times New Roman", 20))
        self.widgets["new_game_button"].place(relx=5 / screensize[0], rely=245 / screensize[1])
        self.widgets["load_game_button"] = tk.Button(self, text="Load Game", command=self.load_menu, width=20,
                                                     height=2, font=("Times New Roman", 20))
        self.widgets["load_game_button"].place(relx=5 / screensize[0], rely=365 / screensize[1])
        self.widgets["options_button"] = tk.Button(self, text="Options", command=self.options_menu, width=20, height=2,
                                                   font=("Times New Roman", 20))
        self.widgets["options_button"].place(relx=5 / screensize[0], rely=485 / screensize[1])
        self.widgets["exit_button"] = tk.Button(self, text="Exit", command=self.exit_choice, width=20, height=2,
                                                font=("Times New Roman", 20))
        self.widgets["exit_button"].place(relx=5 / screensize[0], rely=605 / screensize[1])
        self.master.bind("<Motion>", self.mouse_button_highlight)
        self.master.bind("<KeyRelease>", self.button_button_highlight)
        for widget in self.widgets.values():
            if isinstance(widget, tk.Button):
                widget.bind("<Motion>", self.mouse_button_highlight)

    def character_sheet(self):
        self.reset_window()
        self.widgets["character_sheet_label"] = tk.Label(self, text="Character Sheet",
                                                         font=("Times New Roman", 40, "bold"))
        self.widgets["character_sheet_label"].place(relx=5 / screensize[0], rely=5 / screensize[1])
        self.widgets["username_label"] = tk.Label(self, text="Name:", font=("Times New Roman", 20))
        self.widgets["username_label"].place(relx=5 / screensize[0], rely=100 / screensize[1])
        self.widgets["username_entry"] = tk.Entry(self, font=("Times New Roman", 20))
        self.widgets["username_entry"].place(relx=100 / screensize[0], rely=100 / screensize[1])
        self.widgets["stats_label"] = tk.Label(self, text="Stats:", font=("Times New Roman", 20))
        self.widgets["stats_label"].place(relx=5 / screensize[0], rely=195 / screensize[1])
        self.vars["available_points"] = tk.StringVar(value="Available Points: 20")
        self.widgets["available_points_label"] = tk.Label(self, textvariable=self.vars["available_points"],
                                                          font=("Times New Roman", 16))
        self.widgets["available_points_label"].place(relx=400 / screensize[0], rely=100 / screensize[1])
        try:
            character_info_txt = open("character_info.txt", "r")
            character_info = character_info_txt.readline()
            y_values = [195, 220]
            while character_info:
                if character_info == "<Stats>\n":
                    character_info = character_info_txt.readline().strip()
                    while character_info != "</Stats>":
                        stat_name, stat_description = character_info.split(" - ")
                        stat_description = stat_description.replace("; ", "\n")
                        self.widgets[f"{stat_name.lower()}_label"] = tk.Label(self, text=f"{stat_name}",
                                                                              font=("Times New Roman", 16))
                        self.widgets[f"{stat_name.lower()}_label"].place(relx=100 / screensize[0],
                                                                         rely=y_values[0] / screensize[1])
                        self.widgets[f"{stat_name.lower()}_value_button"] = tk.Button(self, text="5",
                                                                                      font=("Times New Roman", 16))
                        self.widgets[f"{stat_name.lower()}_value_button"].place(relx=550 / screensize[0],
                                                                                rely=(y_values[0] - 14) / screensize[1])
                        self.widgets[f"{stat_name.lower()}_value_button"].bind("<Button>", self.stat_change)
                        self.widgets[f"{stat_name.lower()}_value_button"].bind("<Key>", self.stat_change)
                        self.widgets[f"{stat_name.lower()}_description_label"] = tk.Label(
                            self, text=f"{stat_description}", font=("Times New Roman", 12), justify="left"
                        )
                        self.widgets[f"{stat_name.lower()}_label"].update()
                        self.widgets[f"{stat_name.lower()}_description_label"].place(relx=100 / screensize[0],
                                                                                     rely=y_values[1] / screensize[1])
                        self.widgets[f"{stat_name.lower()}_separator"] = ttk.Separator(self, orient="horizontal")
                        self.widgets[f"{stat_name.lower()}_label"].update()
                        self.widgets[f"{stat_name.lower()}_separator"].place(relx=100 / screensize[0],
                                                                             rely=y_values[1] / screensize[1],
                                                                             relwidth=450 / screensize[0])
                        y_translation = self.widgets[f"{stat_name.lower()}_label"].winfo_height() + \
                            self.widgets[f"{stat_name.lower()}_description_label"].winfo_height()
                        y_values = [y_values[0] + y_translation, y_values[1] + y_translation]
                        character_info = character_info_txt.readline().strip()
                character_info = character_info_txt.readline()
                y_values = [195, 220]
                if character_info == "<Stats-Info>\n":
                    character_info = character_info_txt.readline().strip()
                    while character_info != "</Stats-Info>":
                        stat_name, stat_description = character_info.split(" - ")
                        stat_description = stat_description.replace("; ", "\n")
                        self.widgets[f"{stat_name.lower()}_label"] = tk.Label(self, text=f"{stat_name}",
                                                                              font=("Times New Roman", 16))
                        self.widgets[f"{stat_name.lower()}_label"].place(relx=600 / screensize[0],
                                                                         rely=y_values[0] / screensize[1])
                        self.widgets[f"{stat_name.lower()}_value_label"] = tk.Label(self, text="005",
                                                                                    font=("Times New Roman", 16))
                        self.widgets[f"{stat_name.lower()}_value_label"].place(relx=950 / screensize[0],
                                                                               rely=y_values[0] / screensize[1])
                        self.widgets[f"{stat_name.lower()}_description_label"] = tk.Label(
                            self, text=f"{stat_description}", font=("Times New Roman", 12), justify="left"
                        )
                        self.widgets[f"{stat_name.lower()}_description_label"].place(relx=600 / screensize[0],
                                                                                     rely=y_values[1] / screensize[1])
                        self.widgets[f"{stat_name.lower()}_label"].update()
                        self.widgets[f"{stat_name.lower()}_separator"] = ttk.Separator(self, orient="horizontal")
                        self.widgets[f"{stat_name.lower()}_separator"].place(relx=600 / screensize[0],
                                                                             rely=y_values[1] / screensize[1],
                                                                             relwidth=400 / screensize[0])
                        y_translation = self.widgets[f"{stat_name.lower()}_label"].winfo_height() + \
                            self.widgets[f"{stat_name.lower()}_description_label"].winfo_height()
                        y_values = [y_values[0] + y_translation, y_values[1] + y_translation]
                        character_info = character_info_txt.readline().strip()
        except FileNotFoundError:
            self.widgets["error_label"] = tk.Label(self, text="MISSING VITAL FILES", font=("Times New Roman", 20))
            self.widgets["error_label"].place(relx=100 / screensize[0], rely=195 / screensize[1])
        self.widgets["back_button"] = tk.Button(self, text="Back", font=("Times New Roman", 16), command=self.main_menu)
        self.widgets["back_button"].place(relx=5 / screensize[0], rely=(screensize[1] - 5) / screensize[1], anchor="sw")
        self.widgets["reset_button"] = tk.Button(self, text="Reset", font=("Times New Roman", 16),
                                                 command=self.character_sheet)
        self.widgets["reset_button"].place(relx=(screensize[0] - 95) / screensize[0],
                                           rely=(screensize[1] - 5) / screensize[1], anchor="se")
        self.widgets["submit_button"] = tk.Button(self, text="Submit", font=("Times New Roman", 16))
        self.widgets["submit_button"].place(relx=(screensize[0] - 5) / screensize[0],
                                            rely=(screensize[1] - 5) / screensize[1], anchor="se")

    def load_menu(self):
        pass

    def options_menu(self):
        pass

    def exit_choice(self):
        self.master.unbind("<Motion>")
        for widget in self.widgets.values():
            widget.config(state="disabled")
            widget.unbind("<Motion>")
        self.widgets["exit_frame"] = tk.Frame(self, width=200, height=90)
        self.widgets["exit_label"] = tk.Label(self.widgets["exit_frame"], text="Are you sure you want to quit?")
        self.widgets["exit_label"].place(x=90, y=30, anchor="center")
        self.widgets["exit_yes_button"] = tk.Button(self.widgets["exit_frame"], text="Yes", command=self.quit, width=10)
        self.widgets["exit_yes_button"].place(x=0, y=60)
        self.widgets["exit_yes_button"] = tk.Button(self.widgets["exit_frame"], text="No", command=self.main_menu,
                                                    width=10)
        self.widgets["exit_yes_button"].place(x=100, y=60)
        self.widgets["exit_frame"].place(x=0, y=0)
        self.widgets["exit_frame"].update()
        self.widgets["exit_frame"].place(
            relx=(screensize[0] / 2) / screensize[0], rely=(screensize[1] / 2) / screensize[1], anchor="center"
        )

    def introduction(self):
        pass

    def stat_change(self, event):
        if event.keysym == "space" or event.keysym == "Return":
            if event.state % 2 == 1:
                if isinstance(self.master.focus_get(), tk.Button) and \
                        int(self.master.focus_get().config("text")[-1]) > 0:
                    self.vars["available_points"].set(self.vars["available_points"].get().split(": ")[0] + ": " +
                                                      str(int(self.vars["available_points"].get().split(": ")[1]) + 1))
                    self.master.focus_get().config(text=int(self.master.focus_get().config("text")[-1]) - 1)
            else:
                if isinstance(self.master.focus_get(), tk.Button) and \
                        int(self.vars["available_points"].get().split(": ")[1]) > 0:
                    self.vars["available_points"].set(self.vars["available_points"].get().split(": ")[0] + ": " +
                                                      str(int(self.vars["available_points"].get().split(": ")[1]) - 1))
                    self.master.focus_get().config(text=int(self.master.focus_get().config("text")[-1]) + 1)
        elif event.num:
            for widget in self.widgets.values():
                if isinstance(widget, tk.Button):
                    widget.update()
                    widget_x, widget_y = widget.winfo_geometry().split("+")[1:]
                    widget_x, widget_y = int(widget_x), int(widget_y)
                    widget_width, widget_height = int(widget.winfo_width()),\
                        int(widget.winfo_height())
                    if event.x_root in range(widget_x, widget_x + widget_width) and \
                            event.y_root in range(widget_y, widget_y + widget_height):
                        if event.num == 1 and event.state % 2 == 0 and \
                                int(self.vars["available_points"].get().split(": ")[1]) > 0:
                            self.vars["available_points"].set(
                                self.vars["available_points"].get().split(": ")[0] + ": " +
                                str(int(self.vars["available_points"].get().split(": ")[1]) - 1)
                            )
                            widget.config(text=int(widget.config("text")[-1]) + 1)
                        elif (event.num == 3 or (event.num == 1 and event.state % 2 == 1)) and \
                                int(widget.config("text")[-1]) > 0:
                            self.vars["available_points"].set(
                                self.vars["available_points"].get().split(": ")[0] + ": " +
                                str(int(self.vars["available_points"].get().split(": ")[1]) + 1)
                            )
                            widget.config(text=int(widget.config("text")[-1]) - 1)

    def mouse_button_highlight(self, event):
        for widget in self.widgets.values():
            if isinstance(widget, tk.Button):
                widget.update()
                widget_x, widget_y = widget.winfo_geometry().split("+")[1:]
                widget_x, widget_y = int(widget_x), int(widget_y)
                widget_width, widget_height = int(widget.winfo_width()), int(widget.winfo_height())
                if event.x_root in range(widget_x, widget_x + widget_width) and \
                        event.y_root in range(widget_y, widget_y + widget_height) and self.active[-1] == 0:
                    self.active[-1] = 1
                    self.button_animation(widget, "activation")
                else:
                    for _widget in self.widgets.values():
                        if isinstance(_widget, tk.Button):
                            _widget.update()
                            _widget_x, _widget_y = _widget.winfo_geometry().split("+")[1:]
                            _widget_x, _widget_y = int(_widget_x), int(_widget_y)
                            _widget_width, _widget_height = int(_widget.winfo_width()), int(_widget.winfo_height())
                            if _widget["width"] != 20 and \
                                    (event.x_root not in range(_widget_x, _widget_x + _widget_width) or
                                     event.y_root not in range(_widget_y, _widget_y + _widget_height)) and \
                                    self.active[-1] == 1:
                                self.active[-1] = 0
                                self.button_animation(_widget, "deactivation")
                                if event.x_root in range(widget_x, widget_x + widget_width) and \
                                        event.y_root in range(widget_y, widget_y + widget_height) \
                                        and self.active[-1] == 0:
                                    self.active[-1] = 1
                                    self.button_animation(widget, "activation")

    def button_button_highlight(self, event):
        if event.keysym == "Tab":
            break_check = False
            for widget in self.widgets.values():
                if isinstance(widget, tk.Button):
                    if widget.focus_get() == widget and self.active[-1] == 0:
                        self.active[-1] = 1
                        self.button_animation(widget, "activation")
                        break
                    else:
                        for _widget in self.widgets.values():
                            if isinstance(_widget, tk.Button):
                                if _widget.focus_get() != _widget and _widget["width"] != 20 and self.active[-1] == 1:
                                    self.button_animation(_widget, "deactivation")
                                    self.button_animation(widget.focus_get(), "activation")
                                    break_check = True
                                    break
                        if break_check:
                            break

    def button_animation(self, widget, version):
        if version == "activation":
            if self.active[-1] != 0:
                widget.update()
                if widget["width"] < 25:
                    widget.config(width=widget["width"] + 1)
                    self.after(20, lambda: self.button_animation(widget, version))
        elif version == "deactivation":
            widget.update()
            if widget["width"] > 20:
                widget.config(width=widget["width"] - 1)
                self.after(20, lambda: self.button_animation(widget, version))

    def reset_window(self):
        self.master.unbind("<Motion>")
        self.master.unbind("<KeyRelease>")
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
