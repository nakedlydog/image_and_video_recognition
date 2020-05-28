import tkinter
import unittest

from HUD import HUD

from _VideoCapture import _VideoCapture


class MyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.my_hud = HUD(tkinter.Tk(), 'VideoAnalysis', False)
        # self.thread1 = threading.Thread(target=self.my_hud.start_loop())

    def test_set_is_video_paused(self):
        self.my_hud.set_is_video_paused(True)
        self.assertEqual(self.my_hud.is_video_paused, True)
        self.my_hud.set_is_video_paused(False)
        self.assertEqual(self.my_hud.is_video_paused, False)

    def test_video_capture(self):
        video = _VideoCapture()
        self.assertEqual(video.video.isOpened(), True)
        video = None
        try:
            video = _VideoCapture("test")
            self.assertEqual(video.video.isOpened(), False)
        except:
            self.assertEqual(video is None or not video.video.isOpened(), True)
        video = _VideoCapture("AnalyzedVideo1.avi")
        self.assertEqual(video.video.isOpened(), True)

    def test_capture_video_1(self):
        self.my_hud.play_video()
        try:
            self.my_hud.capture_video()
        except:
            self.assertEqual(True, False)

    def test_capture_video_2(self):
        self.my_hud.video = None
        try:
            self.my_hud.play_video("kek")
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.my_hud.capture_video()
        except:
            self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
