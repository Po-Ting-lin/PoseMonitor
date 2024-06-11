import tkinter as tk
from UI.base_page import BasePage
from UI.image_display import DisplayWindowInfo, DisplayWindow


class MainPageDesign(BasePage):
    def __init__(self, parent, controller, refresh_callback):
        super(MainPageDesign, self).__init__(parent, controller)

        # left display
        self.left_display_info = None
        self.left_display = None

        # root path
        self.file_path_var = None

        # # parameters
        # self.eraser_flag = None
        # self.b_size = None
        # self.a_size = None
        # self.n_size = None
        # self.step = None

        # message box zone
        self.message = None

        # mouse capture
        self.xy_on_image = None
        self.ix = 0
        self.iy = 0
        self.xy_on_ui = None
        self.ux = 0
        self.uy = 0

        # key capture
        self.key_var = None

        # refresh
        self.__refresh = refresh_callback

        # layout
        self.control_x_start = 180
        self.setup()

    def setup(self):
        self.left_display_layout()
        self.page_switch_layout(self.control_x_start, 0, 8)
        self.motion_layout()
        self.select_root_path_layout()
        self.grab_button_layout()
        # self.select_parameter_layout()

    def left_display_layout(self):
        self.left_display_info = DisplayWindowInfo()
        self.left_display_info.Width = self.info.canvas_width
        self.left_display_info.Height = self.info.canvas_height
        self.left_display_info.RealWidth = self.info.canvas_width
        self.left_display_info.RealHeight = self.info.canvas_height
        self.left_display_info.X = 60
        self.left_display_info.Y = 60
        self.left_display_info.XOffset = 0
        self.left_display_info.YOffset = 0
        self.left_display_info.ImageXOffset = 0
        self.left_display_info.ImageYOffset = 0
        self.left_display_info.ImageWidth = 0
        self.left_display_info.ImageHeight = 0
        self.left_display = DisplayWindow(self, self.left_display_info, self.__refresh)
        self.left_display.start_display()

    def select_root_path_layout(self):
        y = 10
        x = self.control_x_start
        self.file_path_var = tk.StringVar()
        tk.Label(self, text='Root Path:').grid(row=y, column=x, pady=10, columnspan=8)
        tk.Entry(self, textvariable=self.file_path_var, width=18).grid(row=y, column=x+8, columnspan=15)
        tk.Button(self, text='Select Path', command=self.select_path, width=10).grid(row=y, column=x+23, columnspan=10)

    def grab_button_layout(self):
        y = 12
        x = self.control_x_start
        tk.Button(self, text='Grab', command=self.start_grab_image, width=10).grid(row=y, column=x, columnspan=10)
        tk.Button(self, text='Stop', command=self.stop_grab_image, width=10).grid(row=y + 2, column=x, columnspan=10)
        tk.Button(self, text='Simulate', command=self.simulate, width=10).grid(row=y+4, column=x, columnspan=10)

    # def select_parameter_layout(self):
    #     y = 16
    #     x = self.control_x_start
    #     self.b_size = tk.StringVar()
    #     self.a_size = tk.StringVar()
    #     self.n_size = tk.StringVar()
    #     self.step = tk.StringVar()
    #     self.b_size.set("1.0")
    #     self.n_size.set("1.0")
    #     self.a_size.set("1.0")
    #     self.step.set("0:5")
    #     self.eraser_flag = tk.BooleanVar()
    #     self.eraser_flag.set(False)
    #     tk.Checkbutton(self, text='Eraser', var=self.eraser_flag).grid(row=y, column=x, columnspan=5)
    #     tk.Label(self, text='B size:').grid(row=y+4, column=x, pady=10, columnspan=8)
    #     tk.Entry(self, textvariable=self.b_size, width=18).grid(row=y+4, column=x+8, columnspan=15)
    #     tk.Label(self, text='A size:').grid(row=y+9, column=x, pady=10, columnspan=8)
    #     tk.Entry(self, textvariable=self.a_size, width=18).grid(row=y+9, column=x+8, columnspan=15)
    #     tk.Label(self, text='N size:').grid(row=y+14, column=x, pady=10, columnspan=8)
    #     tk.Entry(self, textvariable=self.n_size, width=18).grid(row=y+14, column=x+8, columnspan=15)
    #     tk.Label(self, text='Step:').grid(row=y+19, column=x, pady=10, columnspan=8)
    #     tk.Entry(self, textvariable=self.step, width=18).grid(row=y+19, column=x+8, columnspan=15)

    def motion_layout(self):
        y = 59
        x = self.control_x_start
        self.xy_on_image = tk.StringVar(value="{}, {}".format(0, 0))
        self.xy_on_ui = tk.StringVar(value="{}, {}".format(0, 0))
        tk.Label(self, text="(ix, iy):").grid(row=y, column=x, columnspan=2)
        tk.Label(self, textvariable=self.xy_on_image).grid(row=y, column=x+2, columnspan=15)
        tk.Label(self, text="(ux, uy):").grid(row=y, column=x+20, columnspan=3)
        tk.Label(self, textvariable=self.xy_on_ui).grid(row=y, column=x+23, columnspan=15)

    def select_path(self):
        pass

    def start_grab_image(self):
        pass

    def stop_grab_image(self):
        pass

    def simulate(self):
        pass
