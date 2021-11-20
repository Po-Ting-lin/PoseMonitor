from jetcam_custom.camera import Camera
import atexit
import cv2
import traitlets


class USBCamera(Camera):
    capture_fps = traitlets.Integer(default_value=30)
    capture_width = traitlets.Integer(default_value=320)
    capture_height = traitlets.Integer(default_value=240)
    capture_device = traitlets.Integer(default_value=0)

    def __init__(self, *args, **kwargs):
        super(USBCamera, self).__init__(*args, **kwargs)
        try:
            self.cap = cv2.VideoCapture(self.capture_device)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_height)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_width)
            self.cap.set(cv2.CAP_PROP_FPS, self.capture_fps)
            re, image = self.cap.read()
            if not re:
                raise RuntimeError('Could not read image from camera.')
        except Exception:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.cap.release)
                
    def _gst_str(self):
        return 'v4l2src device=/dev/video{} ! video/x-raw, width=(int){}, height=(int){}, framerate=(fraction){}/1 ! videoconvert !  video/x-raw, format=(string)BGR ! appsink'.format(self.capture_device, self.capture_width, self.capture_height, self.capture_fps)
    
    def _read(self):
        re, image = self.cap.read()
        # print(image.shape)
        if re:
            return cv2.resize(image, (int(self.width), int(self.height)))
        else:
            raise RuntimeError('Could not read image from camera')
