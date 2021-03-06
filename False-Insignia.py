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
import random


try:
    import ctypes
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
except ModuleNotFoundError:
    screensize = (1280, 720)
    print("Unable to determine screensize; defaulted to 1280x720.")


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
                                                     height=2, font=("Times New Roman", 20), state="disabled")
        self.widgets["load_game_button"].place(relx=5 / screensize[0], rely=365 / screensize[1])
        self.widgets["options_button"] = tk.Button(self, text="Options", command=self.options_menu, width=20, height=2,
                                                   font=("Times New Roman", 20), state="disabled")
        self.widgets["options_button"].place(relx=5 / screensize[0], rely=485 / screensize[1])
        self.widgets["about_button"] = tk.Button(self, text="About", command=self.about_page, width=20, height=2,
                                                 font=("Times New Roman", 20))
        self.widgets["about_button"].place(relx=5 / screensize[0], rely=605 / screensize[1])
        self.widgets["quit_button"] = tk.Button(self, text="Quit", command=self.quit_choice, width=20, height=2,
                                                font=("Times New Roman", 20))
        self.widgets["quit_button"].place(relx=5 / screensize[0], rely=725 / screensize[1])
        self.master.bind("<Motion>", self.mouse_button_highlight)
        self.master.bind("<KeyRelease>", self.button_button_highlight)
        for widget in self.widgets.values():
            if isinstance(widget, tk.Button):
                widget.bind("<Motion>", self.mouse_button_highlight)

    def character_sheet(self):
        self.reset_window()
        self.vars.clear()
        self.widgets["character_sheet_label"] = tk.Label(self, text="Character Sheet",
                                                         font=("Times New Roman", 40, "bold"))
        self.widgets["character_sheet_label"].place(relx=5 / screensize[0], rely=5 / screensize[1])
        self.widgets["username_label"] = tk.Label(self, text="Name:", font=("Times New Roman", 20))
        self.widgets["username_label"].place(relx=5 / screensize[0], rely=100 / screensize[1])
        self.vars["username_str"] = tk.StringVar(
            value=self.vars["username_str"].get() if "username_str" in self.vars else ""
        )
        self.widgets["username_entry"] = tk.Entry(self, font=("Times New Roman", 20), textvar=self.vars["username_str"])
        self.widgets["username_entry"].place(relx=100 / screensize[0], rely=100 / screensize[1])
        self.widgets["username_entry"].bind("<KeyRelease>", self.stat_change)
        self.widgets["stats_label"] = tk.Label(self, text="Stats:", font=("Times New Roman", 20))
        self.widgets["stats_label"].place(relx=5 / screensize[0], rely=195 / screensize[1])
        self.vars["available_points"] = tk.StringVar(
            value=self.vars["available_points"].get() if "available_points" in self.vars else "Available Points: 20"
        )
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
                        self.widgets[f"{stat_name.lower()}_value_button"] = tk.Button(
                            self, text=self.vars[f"{stat_name.lower()}"] if f"{stat_name.lower()}" in self.vars else 5,
                            font=("Times New Roman", 16)
                        )
                        self.widgets[f"{stat_name.lower()}_value_button"].place(relx=550 / screensize[0],
                                                                                rely=(y_values[0] - 14) / screensize[1])
                        self.widgets[f"{stat_name.lower()}_value_button"].bind("<Button>", self.stat_change)
                        self.widgets[f"{stat_name.lower()}_value_button"].bind("<KeyPress>", self.stat_change)
                        self.widgets[f"{stat_name.lower()}_value_button"].bind("<KeyRelease>", self.stat_change)
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
                        self.widgets[f"{stat_name.lower()}_value_label"] = tk.Label(
                            self,
                            text=self.vars[f"{stat_name.lower()}"] if f"{stat_name.lower()}" in self.vars else "0050",
                            font=("Times New Roman", 16)
                        )
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
                                                 command=lambda: [self.vars.clear(), self.character_sheet()])
        self.widgets["reset_button"].place(relx=(screensize[0] - 95) / screensize[0],
                                           rely=(screensize[1] - 5) / screensize[1], anchor="se")
        self.widgets["submit_button"] = tk.Button(self, text="Submit", font=("Times New Roman", 16), state="disabled",
                                                  command=self.character_selection_choice)
        self.widgets["submit_button"].place(relx=(screensize[0] - 5) / screensize[0],
                                            rely=(screensize[1] - 5) / screensize[1], anchor="se")

    def load_menu(self):
        pass

    def options_menu(self):
        pass

    def about_page(self):
        self.master.unbind("<Motion>")
        self.master.unbind("<KeyRelease>")
        for widget in self.widgets.values():
            try:
                widget.config(state="disabled")
            except tk.TclError:
                pass
            widget.unbind("<Motion>")
        self.widgets["about_frame"] = tk.Frame(self, width=480, height=300, bd=10, relief="groove")
        self.widgets["about_message"] = tk.Message(
            self.widgets["quit_frame"],
            text="A simplistic version of Final Fantasy\n\n"
                 "Copyright (C) 2018  Jacob Meadows\n\n\t"
                 "This program is free software: you can redistribute it and/or modify\n\t"
                 "it under the terms of the GNU General Public License as published by\n\t"
                 "the Free Software Foundation, either version 3 of the License, or\n\t"
                 "(at your option) any later version.\n\n\t"
                 "This program is distributed in the hope that it will be useful,\n\t"
                 "but WITHOUT ANY WARRANTY; without even the implied warranty of\n\t"
                 "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n\t"
                 "GNU General Public License for more details.\n\n\t"
                 "You should have received a copy of the GNU General Public License\n\t"
                 "along with this program.  If not, see <http://www.gnu.org/licenses/>.",
            width=1000
        )
        self.widgets["about_message"].place(relx=.5, rely=.5, anchor="center")
        self.widgets["back_button"] = tk.Button(self, text="Back", font=("Times New Roman", 16), command=self.main_menu)
        self.widgets["back_button"].place(relx=5 / screensize[0], rely=(screensize[1] - 5) / screensize[1], anchor="sw")
        self.widgets["about_frame"].place(x=0, y=0)
        self.widgets["about_frame"].update()
        self.widgets["about_frame"].place(relx=.5, rely=.5, anchor="center")

    def quit_choice(self):
        self.master.unbind("<Motion>")
        self.master.unbind("<KeyRelease>")
        for widget in self.widgets.values():
            try:
                widget.config(state="disabled")
            except tk.TclError:
                pass
            widget.unbind("<Motion>")
        self.widgets["quit_frame"] = tk.Frame(self, width=200, height=90)
        self.widgets["quit_label"] = tk.Label(self.widgets["quit_frame"], text="Are you sure you want to quit?")
        self.widgets["quit_label"].place(x=90, y=30, anchor="center")
        self.widgets["quit_yes_button"] = tk.Button(self.widgets["quit_frame"], text="Yes", command=self.quit, width=10)
        self.widgets["quit_yes_button"].place(x=0, y=60)
        self.widgets["quit_no_button"] = tk.Button(self.widgets["quit_frame"], text="No", command=self.main_menu,
                                                   width=10)
        self.widgets["quit_no_button"].place(x=100, y=60)
        self.widgets["quit_frame"].place(x=0, y=0)
        self.widgets["quit_frame"].update()
        self.widgets["quit_frame"].place(
            relx=(screensize[0] / 2) / screensize[0], rely=(screensize[1] / 2) / screensize[1], anchor="center"
        )

    def character_selection_choice(self):
        self.master.unbind("<Motion>")
        self.master.unbind("<KeyRelease>")
        for widget in self.widgets.values():
            try:
                widget.config(state="disabled")
            except tk.TclError:
                pass
            widget.unbind("<Motion>")
        self.widgets["character_selection_frame"] = tk.Frame(self, width=200, height=90)
        self.widgets["character_selection_label"] = tk.Message(self.widgets["character_selection_frame"], width=150,
                                                               text="Are you sure you are okay with these choices?",
                                                               justify="center")
        self.widgets["character_selection_label"].place(x=90, y=30, anchor="center")
        self.widgets["character_selection_yes_button"] = tk.Button(self.widgets["character_selection_frame"],
                                                                   text="Yes", command=self.main_game, width=10)
        self.widgets["character_selection_yes_button"].place(x=0, y=60)
        self.widgets["character_selection_yes_button"] = tk.Button(self.widgets["character_selection_frame"],
                                                                   text="No", command=self.character_sheet, width=10)
        self.widgets["character_selection_yes_button"].place(x=100, y=60)
        self.widgets["character_selection_frame"].place(x=0, y=0)
        self.widgets["character_selection_frame"].update()
        self.widgets["character_selection_frame"].place(
            relx=(screensize[0] / 2) / screensize[0], rely=(screensize[1] / 2) / screensize[1], anchor="center"
        )

    def main_game(self):
        self.reset_window()
        self.vars.pop("available_points")
        self.widgets["name_separator"] = tk.ttk.Separator(self)
        self.widgets["name_separator"].place(relx=5 / screensize[0], rely=(screensize[1] - 125) / screensize[1],
                                             relwidth=.99, anchor="w")
        self.widgets["name_label"] = tk.Label(self, textvariable=self.vars["username_str"],
                                              font=("Times New Roman", 15))
        self.widgets["name_label"].place(relx=5 / screensize[0], rely=(screensize[1] - 95) / screensize[1], anchor="sw")
        self.widgets["progress_separator"] = tk.ttk.Separator(self)
        self.widgets["progress_separator"].place(relx=5 / screensize[0], rely=(screensize[1] - 95) / screensize[1],
                                                 relwidth=.99, anchor="w")
        progress_bars_style = ttk.Style()
        progress_bars_style.theme_use("clam")
        progress_bars_style.configure("red.Horizontal.TProgressbar", foreground="red", background="red")
        progress_bars_style.configure("green.Horizontal.TProgressbar", foreground="green", background="green")
        progress_bars_style.configure("yellow.Horizontal.TProgressbar", foreground="yellow", background="yellow")
        self.widgets["hp_label"] = tk.Label(self, text="HP:", font=("Times New Roman", 15))
        self.widgets["hp_label"].place(relx=5 / screensize[0], rely=(screensize[1] - 65) / screensize[1], anchor="sw")
        self.widgets["hp_progress_bar"] = tk.ttk.Progressbar(self, maximum=int(self.vars["hp"]),
                                                             value=int(self.vars["hp"]),
                                                             style="red.Horizontal.TProgressbar")
        self.widgets["hp_progress_bar"].place(relx=83 / screensize[0], rely=(screensize[1] - 70) / screensize[1],
                                              relwidth=.8, anchor="sw")
        self.widgets["stamina_progress_bar"] = tk.ttk.Progressbar(self, maximum=int(self.vars["stamina"]),
                                                                  value=int(self.vars["stamina"]),
                                                                  style="green.Horizontal.TProgressbar")
        self.widgets["stamina_progress_bar"].place(relx=83 / screensize[0], rely=(screensize[1] - 40) / screensize[1],
                                                   relwidth=.8, anchor="sw")
        self.widgets["stamina_label"] = tk.Label(self, text="Stamina:", font=("Times New Roman", 15))
        self.widgets["stamina_label"].place(relx=5 / screensize[0], rely=(screensize[1] - 35) / screensize[1],
                                            anchor="sw")
        self.vars["level_int"] = 1
        self.widgets["level_separator"] = tk.ttk.Separator(self)
        self.widgets["level_separator"].place(relx=5 / screensize[0], rely=(screensize[1] - 35) / screensize[1],
                                              relwidth=.845, anchor="w")
        self.widgets["level_label"] = tk.Label(self, text=f"Level: {self.vars['level_int']}",
                                               font=("Times New Roman", 15))
        self.widgets["level_label"].place(relx=5 / screensize[0], rely=(screensize[1] - 5) / screensize[1], anchor="sw")
        self.widgets["level_progress_bar"] = tk.ttk.Progressbar(self, maximum=self.vars["level_int"] * 10, value=0,
                                                                style="yellow.Horizontal.TProgressbar")
        self.widgets["level_progress_bar"].place(relx=83 / screensize[0], rely=(screensize[1] - 10) / screensize[1],
                                                 relwidth=.8, anchor="sw")
        self.widgets["load_game_button"] = tk.Button(self, text="Load Game",
                                                     font=("Times New Roman", 15), state="disabled")
        self.widgets["load_game_button"].place(relx=(screensize[0] - 120) / screensize[0],
                                               rely=(screensize[1] - 50) / screensize[1], anchor="se")
        self.widgets["save_game_button"] = tk.Button(self, text="Save Game",
                                                     font=("Times New Roman", 15), state="disabled")
        self.widgets["save_game_button"].place(relx=(screensize[0] - 5) / screensize[0],
                                               rely=(screensize[1] - 50) / screensize[1], anchor="se")
        self.widgets["options_button"] = tk.Button(self, text="Options",
                                                   font=("Times New Roman", 15), state="disabled")
        self.widgets["options_button"].place(relx=(screensize[0] - 120) / screensize[0],
                                             rely=(screensize[1] - 5) / screensize[1], anchor="se")
        self.widgets["quit_button"] = tk.Button(self, text="Quit", command=self.quit_choice,
                                                font=("Times New Roman", 15))
        self.widgets["quit_button"].place(relx=(screensize[0] - 5) / screensize[0],
                                          rely=(screensize[1] - 5) / screensize[1], anchor="se")
        self.widgets["load_game_button"].update()
        self.widgets["options_button"].place_configure(
            relwidth=self.widgets["load_game_button"].winfo_width() / screensize[0]
        )
        self.widgets["save_game_button"].update()
        self.widgets["quit_button"].place_configure(
            relwidth=self.widgets["save_game_button"].winfo_width() / screensize[0]
        )
        self.widgets["inventory_box"] = tk.Label(self, borderwidth=2, relief="groove")
        self.widgets["inventory_box"].place(relx=self.widgets["load_game_button"].winfo_x() / screensize[0],
                                            rely=5 / screensize[1], anchor="nw", relwidth=.1375, relheight=.845)
        self.widgets["inventory_label"] = tk.Label(self, text="Inventory", font=("Times New Roman", 15))
        self.widgets["inventory_label"].place(relx=(self.widgets["load_game_button"].winfo_x() + 65) / screensize[0],
                                              rely=10 / screensize[1], anchor="nw")
        self.vars["inventory_dict"] = {"HP Potion": 15, "Stamina Potion": 15}
        self.inventory_update()
        self.action_sequence()

    def stat_change(self, event):
        if event.keysym == "space" or event.keysym == "Return":
            if event.type == tk.EventType.KeyPress:
                self.after(1, lambda: event.widget.config(state="disabled", disabledforeground="black"))
                if event.state % 2 == 1:
                    if isinstance(event.widget, tk.Button) and \
                            int(event.widget.config("text")[-1]) > 0:
                        self.vars["available_points"].set(
                            self.vars["available_points"].get().split(": ")[0] + ": " +
                            str(int(self.vars["available_points"].get().split(": ")[1]) + 1)
                        )
                        event.widget.config(text=int(self.master.focus_get().config("text")[-1]) - 1)
                elif event.state % 2 == 0:
                    if isinstance(self.master.focus_get(), tk.Button) and \
                            int(self.vars["available_points"].get().split(": ")[1]) > 0:
                        self.vars["available_points"].set(
                            self.vars["available_points"].get().split(": ")[0] + ": " +
                            str(int(self.vars["available_points"].get().split(": ")[1]) - 1)
                        )
                        self.master.focus_get().config(text=int(self.master.focus_get().config("text")[-1]) + 1)
            elif event.type == tk.EventType.KeyRelease:
                event.widget.config(state="normal")
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
        stat_dict = {"HP": "Vitality", "Stamina": "Endurance", "Physical Defense": "Strength", "Magic Defense": "Faith"}
        for stat_name in stat_dict:
            self.widgets[f"{stat_name.lower()}_value_label"].config(
                text=("0" *
                      (4 - len(str(self.widgets[f"{stat_dict[stat_name].lower()}_value_button"].cget("text") * 10)))) +
                str(self.widgets[f"{stat_dict[stat_name].lower()}_value_button"].cget("text") * 10)
            )
            if self.widgets[f"{stat_name.lower()}_value_label"].cget("text") == "0000":
                self.widgets[f"{stat_name.lower()}_value_label"].config(text="0001")
            self.vars[f"{stat_name.lower()}"] = self.widgets[f"{stat_name.lower()}_value_label"].cget("text")
            self.vars[f"{stat_dict[stat_name].lower()}"] = \
                self.widgets[f"{stat_dict[stat_name].lower()}_value_button"].cget("text")
        if self.vars["available_points"].get()[-2:] == " 0" and self.vars["username_str"].get().strip() != "":
            self.widgets["submit_button"].config(state="normal")
        else:
            self.widgets["submit_button"].config(state="disabled")

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
            if self.active[-1] == 0:
                self.active[-1] = 1
                self.button_animation(event.widget, "activation")
            else:
                for _widget in self.widgets.values():
                    if isinstance(_widget, tk.Button):
                        if _widget.focus_get() != _widget and _widget["width"] != 20 and self.active[-1] == 1:
                            self.button_animation(_widget, "deactivation")
                            self.button_animation(event.widget.focus_get(), "activation")
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

    def inventory_update(self):
        y = 60
        for inventory_item in self.vars["inventory_dict"]:
            self.widgets[f"{inventory_item.lower()}_label"] = tk.Label(
                self, text=f"{inventory_item} - {self.vars['inventory_dict'][inventory_item]}",
                font=("Times New Roman", 12)
            )
            self.widgets[f"{inventory_item.lower()}_label"].place(in_=self.widgets["inventory_box"], x=5, y=y)
            self.widgets[f"{inventory_item.lower()}_use_button"] = tk.Button(self, text="Use",
                                                                             font=("Times New Roman", 12))
            self.widgets[f"{inventory_item.lower()}_use_button"].place(in_=self.widgets["inventory_box"], x=25,
                                                                       y=y + 25)
            self.widgets[f"{inventory_item.lower()}_use_button"].bind("<Key>", self.inventory_commands)
            self.widgets[f"{inventory_item.lower()}_use_button"].bind("<Button-1>", self.inventory_commands)
            y += 60

    def inventory_commands(self, event):
        if event.keysym == "space" or event.keysym == "Return" or event.num == 1:
            name, _int = self.widgets[f'{[x for x in self.widgets.items() if event.widget in x][0][0].split("_")[0]}'
                                      f'_label'].cget('text').split(' - ')
            if int(_int) > 0:
                self.widgets[f"{[x for x in self.widgets.items() if event.widget in x][0][0].split('_')[0]}_label"] \
                    .config(text=f"{name} - {int(_int) - 1}")
                self.widgets[f"{name.split(' ')[0].lower()}_progress_bar"].config(
                    value=self.widgets[f"{name.split(' ')[0].lower()}_progress_bar"].cget("value") + 50
                )

    def action_sequence(self):
        names = ["Wolf", "Zombie", "Slime", "Lizardman"]
        random_name = random.choice(names)
        self.widgets["enemy_name_label"] = tk.Label(self, text=random_name,
                                                    font=("Times New Roman", 15))
        self.widgets["enemy_name_label"].place(relx=5 / screensize[0], rely=35 / screensize[1],
                                               anchor="sw")
        self.widgets["enemy_name_separator"] = tk.ttk.Separator(self)
        self.widgets["enemy_name_separator"].place(relx=5 / screensize[0], rely=35 / screensize[1], relwidth=.845,
                                                   anchor="w")
        progress_bars_style = ttk.Style()
        progress_bars_style.theme_use("clam")
        progress_bars_style.configure("red.Horizontal.TProgressbar", foreground="red", background="red")
        progress_bars_style.configure("green.Horizontal.TProgressbar", foreground="green", background="green")
        progress_bars_style.configure("yellow.Horizontal.TProgressbar", foreground="yellow", background="yellow")
        self.widgets["enemy_hp_label"] = tk.Label(self, text="HP:", font=("Times New Roman", 15))
        self.widgets["enemy_hp_label"].place(relx=5 / screensize[0], rely=65 / screensize[1],
                                             anchor="sw")
        self.widgets["enemy_hp_progress_bar"] = tk.ttk.Progressbar(self, maximum=int(self.vars["hp"]),
                                                                   value=int(self.vars["hp"]),
                                                                   style="red.Horizontal.TProgressbar")
        self.widgets["enemy_hp_progress_bar"].place(relx=83 / screensize[0], rely=60 / screensize[1],
                                                    relwidth=.8, anchor="sw")
        self.widgets["enemy_stamina_progress_bar"] = tk.ttk.Progressbar(self, maximum=int(self.vars["stamina"]),
                                                                        value=int(self.vars["stamina"]),
                                                                        style="green.Horizontal.TProgressbar")
        self.widgets["enemy_stamina_progress_bar"].place(relx=83 / screensize[0],
                                                         rely=90 / screensize[1], relwidth=.8,
                                                         anchor="sw")
        self.widgets["enemy_stamina_label"] = tk.Label(self, text="Stamina:", font=("Times New Roman", 15))
        self.widgets["enemy_stamina_label"].place(relx=5 / screensize[0], rely=95 / screensize[1],
                                                  anchor="sw")
        self.widgets["enemy_progress_separator"] = tk.ttk.Separator(self)
        self.widgets["enemy_progress_separator"].place(relx=5 / screensize[0], rely=100 / screensize[1],
                                                       relwidth=.845, anchor="w")
        self.widgets["combat_message"] = tk.Message(self, text=f"You encountered a {random_name}!",
                                                    width=2000, justify="left", font=("Times New Roman", 12),
                                                    borderwidth=2, relief="groove")
        self.widgets["combat_message"].place(relx=5 / screensize[0], rely=(screensize[1] - 150) / screensize[1],
                                             anchor="w")
        self.widgets["attack_button"] = tk.Button(self, text="Attack", font=("Times New Roman", 15),
                                                  command=self.attack_command)
        self.widgets["attack_button"].place(relx=5 / screensize[0], rely=125 / screensize[1], anchor="w")

    def attack_command(self):
        for widget in self.widgets.values():
            try:
                widget.config(state="disabled")
            except tk.TclError:
                pass
        self.widgets["attack_progress_bar"] = tk.ttk.Progressbar(self)
        self.widgets["attack_progress_bar"].place(relx=.4, rely=.5)
        self.widgets["attack_progress_bar"].start()
        self.widgets["attack_progress_bar"].focus_set()
        self.widgets["attack_progress_bar"].bind("<space>", lambda event: self.successful_hit()
                                                 if self.widgets["attack_progress_bar"].cget("value") > 90 else None)
        self.widgets["attack_instructions_label"] = tk.Label(self, text="Press SPACE when the progressbar is nearly "
                                                                        "full!")
        self.widgets["attack_instructions_label"].place(relx=.375, rely=.55)

    def successful_hit(self):
        for widget in self.widgets.values():
            try:
                widget.config(state="normal")
            except tk.TclError:
                pass
        self.widgets["save_game_button"].config(state="disabled")
        self.widgets["load_game_button"].config(state="disabled")
        self.widgets["options_button"].config(state="disabled")
        self.widgets["combat_message"].config(
            text=self.widgets["combat_message"].cget("text").split("\n")[-1] +
            f"\nSuccess! The {self.widgets['enemy_name_label'].cget('text')} took 5 damage."
        )
        self.widgets["attack_progress_bar"].destroy()
        self.widgets.pop("attack_progress_bar")
        self.widgets["attack_instructions_label"].destroy()
        self.widgets.pop("attack_instructions_label")
        self.widgets["enemy_hp_progress_bar"].config(value=self.widgets["enemy_hp_progress_bar"].cget("value") - 5)

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
