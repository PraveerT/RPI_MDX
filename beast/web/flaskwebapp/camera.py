from time import time

class Camera(object):
    def __init__(self):
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['/home/pi/Desktop/sync/web/flaskwebapp/static/image', '/home/pi/Desktop/sync/web/flaskwebapp/static/image2', '/home/pi/Desktop/sync/web/flaskwebapp/static/image3']]

    def get_frame(self):
        return self.frames[int(time()) % 3]
