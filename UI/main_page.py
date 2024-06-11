from os.path import isfile
import cv2
from tkinter.filedialog import askopenfile
from UI.main_page_design import MainPageDesign
from core.pose_monitor import PoseMonitor


class Tile(object):
    sx = None
    sy = None
    ex = None
    ey = None
    width = None
    height = None
    start = False


class MainPage(MainPageDesign):
    def __init__(self, parent, controller, refresh_callback):
        super(MainPage, self).__init__(parent, controller, refresh_callback)
        self.image_size = 512

        # root path
        self.root_path = None

        self.pm = None

        # box
        self.plot_tile = Tile()

        # pt
        self.prev_pt = None

        # mask
        self.crop_raw_image = None

        # left display bind
        self.left_display.zone.bind("<Motion>", self.__left_display_motion)
        self.left_display.zone.bind("<Button-1>", self.__left_display_mouse_down)
        self.left_display.zone.bind("<B1-Motion>", self.__left_display_mouse_move)
        self.left_display.zone.bind("<ButtonRelease-1>", self.__left_display_mouse_up)

        self.pm = PoseMonitor(self.left_display)

    def stop(self):
        self.left_display.stop_display()

    def select_path(self):
        file_path = askopenfile().name
        self.file_path_var.set(file_path)
        self.root_path = file_path.replace("/", "\\")
        img = self.open_image(self.root_path)
        self.left_display.info.RealWidth = img.shape[1]
        self.left_display.info.RealHeight = img.shape[0]
        self.left_display.add_queue(img)

    def start_grab_image(self):
        self.pm.start_camera()

    def stop_grab_image(self):
        self.pm.stop_camera()

    def simulate(self):
        self.pm.simulate()

    @staticmethod
    def open_image(path):
        if isfile(path):
            return cv2.cvtColor(cv2.imread(path, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        else:
            return None

    def __coordinate_transform(self, x, y):
        tx = -1
        ty = -1
        if self.left_display.info.ImageXOffset <= x < self.left_display.info.ImageXOffset + self.left_display.info.ImageWidth:
            tx = x - self.left_display.info.ImageXOffset
        if self.left_display.info.ImageYOffset <= y < self.left_display.info.ImageYOffset + self.left_display.info.ImageHeight:
            ty = y - self.left_display.info.ImageYOffset
        if self.left_display.info.RealWidth > self.left_display.info.RealHeight:
            tx = int(tx * self.left_display.info.RealWidth / self.info.canvas_width) if tx >= 0 else -1
            ty = int(ty * self.left_display.info.RealWidth / self.info.canvas_width) if ty >= 0 else -1
        else:
            tx = int(tx * self.left_display.info.RealHeight / self.info.canvas_height) if tx >= 0 else -1
            ty = int(ty * self.left_display.info.RealHeight / self.info.canvas_height) if ty >= 0 else -1
        return tx, ty

    def __left_display_motion(self, event):
        self.ix, self.iy = self.__coordinate_transform(event.x, event.y)
        self.ux, self.uy = event.x, event.y
        self.xy_on_ui.set("{}, {}".format(self.ux, self.uy))
        self.xy_on_image.set("{}, {}".format(self.ix, self.iy))

    def __left_display_mouse_down(self, event):
        pass

    def __left_display_mouse_move(self, event):
        pass

    def __left_display_mouse_up(self, event):
        pass

    def __resizeTo512AndColorConvertImage(self, image):
        if image is None:
            return None
        if image.shape[0] != self.image_size or image.shape[1] != self.image_size:
            image = cv2.resize(image, (self.image_size, self.image_size), interpolation=cv2.INTER_LINEAR)
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
