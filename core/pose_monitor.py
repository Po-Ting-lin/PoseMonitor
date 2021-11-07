import cv2
import time
import PIL.Image
from matplotlib import pyplot as plt
import ipywidgets
import json
import torch
import torchvision.transforms as transforms

from torch2trt import TRTModule, torch2trt
import trt_pose.models
import trt_pose.coco
from trt_pose.draw_objects import DrawObjects
from trt_pose.parse_objects import ParseObjects

from jetcam.usb_camera import USBCamera


class PoseMonitor(object):
    def __init__(self, display):
        self.parse_objects = None
        self.draw_objects = None
        self.model = None
        self.camera = None
        self.width = 224
        self.height = 224
        self.frame_rate = 30
        self.display = display
        self.display.info.RealWidth = self.width
        self.display.info.RealHeight = self.height
        self.optimized_model_path = r'resources/resnet18_baseline_att_224x224_A_epoch_249_trt.pth'
        self.human_config_path = r'resources/human_pose.json'
        self.frame_count = 0.0
        self.start_time = None
        self.end_time = None
        
        self.__init_model()
        self.__init_camera()

    def start(self):
        self.camera.running = True
        self.camera.observe(self.__execute, names='value')
        self.start_time = time.time()

    def stop(self):
        self.camera.unobserve_all()
        self.camera.running = False

    def __init_model(self):
        print("loading parse object...")
        with open(self.human_config_path, 'r') as f:
            human_pose = json.load(f)
        topology = trt_pose.coco.coco_category_to_topology(human_pose)
        self.parse_objects = ParseObjects(topology)
        self.draw_objects = DrawObjects(topology)
        
        print("loading optimized model...")
        self.model = TRTModule()
        self.model.load_state_dict(torch.load(self.optimized_model_path))

    def __init_camera(self):
        print("init camera...")
        self.camera = USBCamera(width=self.width, height=self.height, capture_fps=self.frame_rate)

    def __execute(self, change):
        image = change['new']
        data = self.__preprocess(image)
        cmap, paf = self.model(data)
        cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
        counts, objects, peaks = self.parse_objects(cmap, paf)
        self.draw_objects(image, counts, objects, peaks)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.frame_count += 1
        if self.frame_count == 50:
            self.end_time = time.time()
            print("frame rate: " + str(self.frame_count / (self.end_time - self.start_time)) + " fps")
            self.frame_count = 0
            self.start_time = time.time()
        self.display.display(image)

    def __preprocess(self, image):
        mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
        std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
        device = torch.device('cuda')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        image = transforms.functional.to_tensor(image).to(device)
        image.sub_(mean[:, None, None]).div_(std[:, None, None])
        return image[None, ...]



