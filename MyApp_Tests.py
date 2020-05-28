import unittest

from HUD import MyApp
import threading
import time


class MyApp_Tests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MyApp_Tests, self).__init__(*args, **kwargs)
        self.my_app = MyApp(False)

    def test_post_init_test(self):
        self.assertEqual(self.my_app.count_analyzed_video, 0)

    def test_increment_test(self):
        self.my_app.increment_analysed_video_counter()
        self.assertEqual(self.my_app.count_analyzed_video, 1)
        self.assertEqual(self.my_app.analysed_video_name + ".avi", "AnalyzedVideo1.avi")

    def test_stop_thread_test(self):
        self.my_app.thread1 = threading.Thread()
        time.sleep(3)
        self.my_app.stop_thread()
        self.assertEqual(self.my_app.thread1 is None or not self.my_app.thread1.is_alive(), True)

    def test_paused_clicked(self):
        self.my_app.pause_video_clicked()
        self.assertEqual(self.my_app.my_hud.is_video_paused, True)

    def test_play_clicked(self):
        self.my_app.play_video_clicked()
        self.assertEqual(self.my_app.my_hud.is_video_paused, False)




if __name__ == '__main__':
    unittest.main()
