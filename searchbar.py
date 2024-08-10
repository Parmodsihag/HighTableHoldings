import tkinter as tk
import tkinter.font as tkfont
from mytheme import Colors

class SearchBar(tk.Frame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, **kwargs)

        self.data = data

        # Search Bar
        self.text_variable = tk.StringVar()  # Text variable
        self.search_bar = tk.Entry(self, textvariable=self.text_variable, 
                                    font="Consolas 14",
                                    borderwidth=0,
                                    # relief="groove",
                                    background=Colors.BACKGROUND,
                                    fg=Colors.FG_SHADE_1,
                                    highlightthickness=2,
                                    highlightbackground=Colors.BG_SHADE_2,
                                    highlightcolor=Colors.ACTIVE_FOREGROUND
                                    )
        self.search_bar.pack(fill='both', expand=True)
        self.search_bar.bind("<KeyRelease>", self.search)
        self.search_bar.bind("<Down>", self.focus_listbox)
        self.search_bar.bind("<FocusOut>", self.hide_listbox)
        self.highlight_border_color = self.search_bar.cget("highlightbackground")
        self.default_border_color = self.search_bar.cget("highlightcolor")

        # Suggestion Listbox (in a Toplevel)
        self.suggestion_toplevel = None
        self.suggestion_listbox = None

        self.current_suggestion_index = -1

    def search(self, event):
        if event.keysym == "Return":  # Ignore Enter key
            return

        search_term = self.search_bar.get().lower()
        suggestions = self.get_suggestions(search_term)

        if suggestions:
            if self.suggestion_toplevel is None:
                self.suggestion_toplevel = tk.Toplevel(self)
                self.suggestion_toplevel.wm_overrideredirect(True)
                self.suggestion_toplevel.wm_geometry("+%d+%d" % (
                    self.search_bar.winfo_rootx(),
                    self.search_bar.winfo_rooty() + self.search_bar.winfo_height()
                ))
                entry_font = tkfont.Font(font=self.search_bar.cget("font"))
                char_width = entry_font.measure("0")
                listbox_width_chars = int(self.search_bar.winfo_width() / (char_width+1 ))

                self.suggestion_listbox = tk.Listbox(
                    self.suggestion_toplevel,
                    width=listbox_width_chars,
                    font=entry_font.actual(),
                    bg=Colors.BACKGROUND,
                    fg=Colors.FG_SHADE_1,
                    bd=1,
                    highlightthickness=0,
                    selectbackground=Colors.ACTIVE_BACKGROUND,
                    selectforeground=Colors.FOREGROUND,
                    activestyle="none",
                    relief='flat'
                )
                self.suggestion_listbox.pack(fill='both', expand=True)
                self.suggestion_listbox.bind("<FocusOut>", self.hide_listbox)
                self.suggestion_listbox.bind("<Return>", self.select_suggestion)
                self.suggestion_listbox.bind("<Up>", self.navigate_listbox)
                self.suggestion_listbox.bind("<Down>", self.navigate_listbox)

                max_height = 6
                listbox_height = min(len(suggestions), max_height)
                self.suggestion_listbox.config(height=listbox_height)

            self.suggestion_listbox.delete(0, tk.END)
            max_height = 6
            listbox_height = min(len(suggestions), max_height)
            self.suggestion_listbox.config(height=listbox_height)
            for suggestion in suggestions:
                self.suggestion_listbox.insert(tk.END, suggestion)
            self.current_suggestion_index = -1
            self.search_bar.config(highlightbackground=self.highlight_border_color)
            self.search_bar.config(highlightcolor=self.default_border_color)
        else:
            self.hide_listbox(None)  # Hide if no suggestions
            self.search_bar.config(highlightbackground="red")
            self.search_bar.config(highlightcolor="red")

    def get_suggestions(self, search_term):
        suggestions = [item for item in self.data if search_term in item.lower()]
        return suggestions

    def focus_listbox(self, event):
        if self.suggestion_listbox and self.suggestion_listbox.winfo_ismapped():
            self.suggestion_listbox.focus()
            self.suggestion_listbox.selection_set(0)
            self.current_suggestion_index = 0

    def hide_listbox(self, event):
        if self.suggestion_toplevel:
            focused_widget = self.focus_get()
            if focused_widget != self.suggestion_listbox and focused_widget != self.search_bar:
                self.suggestion_toplevel.destroy()
                self.suggestion_toplevel = None
                self.suggestion_listbox = None

    def select_suggestion(self, event):
        selection = self.suggestion_listbox.curselection()
        if selection:
            choice = self.suggestion_listbox.get(selection[0])
            self.search_bar.delete(0, tk.END)
            self.search_bar.insert(0, choice)
            self.hide_listbox(None)

            self.search_bar.focus_set()

    def navigate_listbox(self, event):
        if self.suggestion_listbox:
            size = self.suggestion_listbox.size()
            if event.keysym == "Up":
                self.current_suggestion_index = max(0, self.current_suggestion_index - 1)
            elif event.keysym == "Down":
                self.current_suggestion_index = min(size - 1, self.current_suggestion_index + 1)
            self.suggestion_listbox.selection_clear(0, tk.END)
            self.suggestion_listbox.selection_set(self.current_suggestion_index)
            self.suggestion_listbox.see(self.current_suggestion_index)

    def get_text(self):
        return self.search_bar.get()

    def set_text(self, text):
        self.text_variable.set(text)

    def set_data(self, data):
        self.data = data


if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("400x300")
    app.config(background='#dddddd')

    data = ["apple", "banana", "cherry", "grape", "orange", "watermelon", "sdiuo ho "]

    entry1 = SearchBar(app, data)
    entry1.pack(pady=20, padx=20, fill='x')

    entry2 = SearchBar(app, data)
    entry2.pack(pady=20, padx=20, fill='x')

    app.mainloop()