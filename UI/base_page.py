import tkinter as tk


class GuiInfo:
    icon_path = r"rt.png"
    window_geometry = "930x602+20+20"
    canvas_width = 600
    canvas_height = 600


class PageSwitcherInfo(object):
    Controller = None
    PageNameList = None
    ButtonNameList = None
    ButtonWidth = None
    X = None
    Y = None


class PageButton(object):
    def __init__(self, frame, controller, name, button_name, x, y, button_width):
        self.name = name
        self.button_width = button_width
        button = tk.Button(frame, text=button_name, command=lambda: controller.show_frame(name))
        button.grid(row=y, column=x, columnspan=button_width)


class PageSwitcher(object):
    def __init__(self, frame, info):
        self.controller = info.Controller
        for name, button_name in zip(info.PageNameList, info.ButtonNameList):
            PageButton(frame, info.Controller, name, button_name, info.X, info.Y, info.ButtonWidth)
            info.X += info.ButtonWidth


class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.info = GuiInfo()

    def page_switch_layout(self, x, y, button_width):
        info = PageSwitcherInfo()
        info.X = x
        info.Y = y
        info.ButtonWidth = button_width
        info.Controller = self.controller
        info.PageNameList = ["MainPage"]
        info.ButtonNameList = ["main"]
        PageSwitcher(self, info)