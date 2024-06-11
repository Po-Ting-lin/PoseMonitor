import cv2
import PIL.Image
import json
import torch
import torchvision.transforms as transforms
from torch2trt import TRTModule
import trt_pose.models
import trt_pose.coco
from trt_pose.draw_objects import DrawObjects
from trt_pose.parse_objects import ParseObjects
from jetcam_custom.my_camera import MyCamera
from time import sleep


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

        self.is_init_model = False
        self.is_init_camera = False

    def start_camera(self):
        if not self.is_init_model:
            self.__init_model()
        if not self.is_init_camera:
            self.__init_camera()
        self.camera.start_capture(self.__process_loop)

    def stop_camera(self):
        self.camera.stop_capture()

    def simulate(self):
        if not self.is_init_model:
            self.__init_model()
        image = cv2.imread("", cv2.IMREAD_COLOR)
        if image is None:
            print("Cannot read image, skip")
            return
        image = cv2.resize(image, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        while True:
            self.__process_loop(image)
            sleep(0.05)

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
        self.is_init_model = True

    def __init_camera(self):
        print("init camera...")
        self.camera = MyCamera(device=0, width=self.width, height=self.height, fps=self.frame_rate)
        self.is_init_camera = True

    def __process_loop(self, image):
        data = self.__preprocess(image)
        cmap, paf = self.model(data)
        cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
        counts, objects, peaks = self.parse_objects(cmap, paf)
        self.draw_objects(image, counts, objects, peaks)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.display.add_queue(image)

    def __preprocess(self, image):
        mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
        std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
        device = torch.device('cuda')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        image = transforms.functional.to_tensor(image).to(device)
        image.sub_(mean[:, None, None]).div_(std[:, None, None])
        return image[None, ...]



