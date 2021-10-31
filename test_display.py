import cv2
from matplotlib import pyplot as plt
from PIL import Image
import time
import psutil

url = "download.jpeg"
image = cv2.imread(url)

# cannot display in terminal
#cv2.imshow("display", image)

# can display
#plt.figure()
#plt.imshow(image)
#plt.show()


#display(Image(url))

for i in range(10):
    if i % 2 == 0:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    img = Image.fromarray(image)
    img.show()

    #time.sleep(1)
    for proc in psutil.process_iter():
        if proc.name() == "display":
            proc.kill()
