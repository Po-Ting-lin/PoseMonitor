import cv2
import numpy as np
import queue
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
from core.rate_counter import RateCounter


def get_blank_tkImage(width, height):
    img = np.zeros((height, width))
    return ImageTk.PhotoImage(Image.fromarray(img))


class DisplayWindowInfo(object):
    Width = None
    Height = None
    X = None
    Y = None
    XOffset = None
    YOffset = None
    RealWidth = None
    RealHeight = None
    ImageXOffset = None
    ImageYOffset = None
    ImageWidth = None
    ImageHeight = None


class DisplayWindow(object):
    def __init__(self, frame, info, refresh_callback):
        self.info = info
        self.zone = tk.Canvas(frame, width=info.Width, height=info.Height)
        self.zone.grid(row=info.YOffset, column=info.XOffset, rowspan=info.Y, columnspan=info.X)
        self.image = np.zeros((info.Height, info.Width))
        self.tkImage = ImageTk.PhotoImage(Image.fromarray(self.image))
        self.blank_tkImage = ImageTk.PhotoImage(Image.fromarray(self.image))
        self.image_object = self.zone.create_image(0, 0, anchor=tk.NW, image=self.tkImage)
        self.is_displaying = False
        self.display_thread = None
        self.__refresh = refresh_callback
        self.queue = queue.Queue()
        self.display_counter = RateCounter("display rate", 50)

    @staticmethod
    def __tk_image_convert(image):
        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image=image)

    def add_queue(self, image):
        if image is None:
            return
        self.queue.put(image)

    def start_display(self):
        if not self.is_displaying:
            print("start display")
            self.is_displaying = True
            self.display_thread = threading.Thread(target=self.display_loop, name="display thread")
            self.display_thread.daemon = True  # kill the thread when sys.exit
            self.display_thread.start()
            self.display_counter.start()

    def stop_display(self):
        if self.is_displaying:
            print("stop display")
            self.is_displaying = False
            #self.display_thread.join()

    def display_loop(self):
        while self.is_displaying:
            if self.queue is not None:
                if self.queue.not_empty:
                    self.image = self.__resize(self.queue.get())
                    self.update_by_updating_image(self.image)
                elif self.queue.empty:
                    self.image = np.zeros((self.info.Height, self.info.Width))
                    self.update_by_updating_image(self.image)
                self.display_counter.add_to_count()
        print("End of display loop")

    def update_by_updating_image(self, image):
        self.tkImage = self.__tk_image_convert(image)
        self.zone.itemconfig(self.image_object, image=self.tkImage)

    def __resize(self, image):
        self.info.RealWidth = image.shape[1]
        self.info.RealHeight = image.shape[0]
        new_width = self.info.Width
        new_height = self.info.Height
        x_offset = 0
        y_offset = 0
        if self.info.RealWidth > self.info.RealHeight:
            new_width = self.info.Width
            new_height = self.info.Width * self.info.RealHeight / self.info.RealWidth
            y_offset = (self.info.Height - new_height) / 2
        else:
            new_width = self.info.Height * self.info.RealWidth / self.info.RealHeight
            new_height = self.info.Height
            x_offset = (self.info.Width - new_width) / 2
        self.info.ImageYOffset = int(round(y_offset))
        self.info.ImageXOffset = int(round(x_offset))
        self.info.ImageWidth = int(round(new_width))
        self.info.ImageHeight = int(round(new_height))
        resized_image = cv2.resize(image, (self.info.ImageWidth, self.info.ImageHeight), interpolation=cv2.INTER_LINEAR)
        img = np.zeros((self.info.Height, self.info.Width, 3), dtype="uint8")
        img[self.info.ImageYOffset:self.info.ImageYOffset + self.info.ImageHeight,
            self.info.ImageXOffset:self.info.ImageXOffset + self.info.ImageWidth, :] = resized_image
        return img

