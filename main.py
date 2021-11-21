import sys
import tkinter as tk
from tkinter import font as tkfont
from UI.main_page import MainPage
from UI.base_page import GuiInfo


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.initialize()
        self.protocol('WM_DELETE_WINDOW', self.close)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in [MainPage]:
            page_name = F.__name__
            frame = F(parent=container, controller=self, refresh_callback=self.__refresh)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainPage")

    def initialize(self):
        return None

    def close(self):
        print("start close process...")
        self.frames["MainPage"].stop()
        self.destroy()
        print("finish destroy")
        sys.exit()

    def show_frame(self, page_name):
        """ Show a frame for the given page name """
        frame = self.frames[page_name]
        frame.tkraise()

    def __refresh(self):
        self.update()
        self.update_idletasks()


if __name__ == "__main__":
    info = GuiInfo()
    app = MainApp()
    app.title('TRT Pose Monitor')
    app.iconphoto(False, tk.PhotoImage(file=info.icon_path))
    app.wm_geometry(info.window_geometry)
    app.mainloop()
