

class PoseMonitor(object):
    def __init__(self):
        self.human_pose = None
        self.topology = None
        self.parse_objects = None
        self.draw_objects = None
        self.width = 224
        self.height = 224
        self.optimized_model_path = r'resnet18_baseline_att_224x224_A_epoch_249_trt.pth'
        self.human_config_path = r'human_pose.json'

        self.__init_model()
        self.__init_camera()

    def start(self):
        pass

    def stop(self):
        pass

    def __init_model(self):
        pass

    def __init_camera(self):
        pass

    def __execute(self, change):
        pass



