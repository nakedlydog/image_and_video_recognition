import cv2


class _VideoCapture:
    def __init__(self, video_source=0):
        self.video = cv2.VideoCapture(video_source)
        if not self.video.isOpened():
            raise ValueError('Unable video source', video_source)
        print(video_source)
#        self.width = 700 # self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
#        self.height = 600 # self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        if self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)