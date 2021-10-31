import json
import torch
import queue
import trt_pose.coco
from torch2trt import TRTModule
import cv2
import torchvision.transforms as transforms
import PIL.Image
from trt_pose.draw_objects import DrawObjects
from trt_pose.parse_objects import ParseObjects
from jetcam.usb_camera import USBCamera
from jetcam.utils import bgr8_to_jpeg
import ipywidgets
from IPython.display import display
from matplotlib import pyplot as plt

WIDTH = 224
HEIGHT = 224
OPTIMIZED_MODEL = 'resnet18_baseline_att_224x224_A_epoch_249_trt.pth'
callback_queue = queue.Queue()

def from_dummy_thread(func_to_call_from_main_thread):
    global callback_queue
    callback_queue.put(func_to_call_from_main_thread)

def from_main_thread_blocking():
    global callback_queue
    callback = callback_queue.get() #blocks until an item is available
    callback()

def preprocess(image):
    global device
    device = torch.device('cuda')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device)
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]

# topology
with open('human_pose.json', 'r') as f:
    human_pose = json.load(f)
topology = trt_pose.coco.coco_category_to_topology(human_pose)


# load model
model_trt = TRTModule()
model_trt.load_state_dict(torch.load(OPTIMIZED_MODEL))

mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
device = torch.device('cuda')

parse_objects = ParseObjects(topology)
draw_objects = DrawObjects(topology)

camera = USBCamera(width=WIDTH, height=HEIGHT, capture_fps=30)

save_mode = False
length = 20.0
frame_number = 0
if save_mode:
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output_movie = cv2.VideoWriter('output1.mp4', fourcc, length, (WIDTH, HEIGHT))


def display_image(image):
    cv2.imshow('Capture', frame)
    print("display function")
    #plt.figure()
    #plt.imshow(image)
    #plt.show()

def execute(change):
    global frame_number
    global save_mode
    image = change['new']
    data = preprocess(image)
    cmap, paf = model_trt(data)
    cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
    counts, objects, peaks = parse_objects(cmap, paf)#, cmap_threshold=0.15, link_threshold=0.15)
    draw_objects(image, counts, objects, peaks)
    if save_mode:
    	output_movie.write(image)
    frame_number += 1
    print("frame number: ", frame_number)
    
    if save_mode and frame_number == 700:
        output_movie.release()
    from_dummy_thread(lambda: display_image(image))
    

camera.running = True
camera.observe(execute, names='value')





