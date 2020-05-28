import time
import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
from tkinter.filedialog import askopenfilename
from MyVideoRecongnition import MyVideoRecognition

from _VideoCapture import _VideoCapture
import threading


class FileType:
    def __init__(self, extension=".mp4", file_types=[('Video files', '*.mp4'), ('All files', '*.*')]):
        self.default_extension = extension
        self.file_types = file_types


class HUD:
    def __init__(self, window, window_title, b_start_loop=True):
        self.window = window
        self.window.title(window_title)

        self.init(window)

        self.delay = 1

        self.is_video_paused = False

        self.video = None

        if b_start_loop:
            self.start_loop()

    def start_loop(self):
        self.update()
        self.window.mainloop()

    def init(self, window):
        self.canvas = tkinter.Canvas(window, width=700, height=400)
        self.canvas.pack()

        self.create_text(window)
        self.create_buttons(window)

    def create_text(self, window):
        self.text = tkinter.Label(window, text='')
        self.text.pack()

    def create_buttons(self, window):
        button_size = 15

        self.button_play = tkinter.Button(window, text='Play', width=button_size)#, command=self.play_video_clicked)
        self.button_play.pack(side=tkinter.LEFT)  # , expand=True)

        self.button_pause = tkinter.Button(window, text='Pause', width=button_size)#, command=self.pause_video_clicked)
        self.button_pause.pack(side=tkinter.LEFT)  # , expand=True)

        self.button_choose_file = tkinter.Button(window, text='Choose video-file', width=button_size)
        self.button_choose_file.pack(side=tkinter.LEFT)

        self.button_choose_builtin_camera = tkinter.Button(window, text='Choose my webcam', width=button_size)
        self.button_choose_builtin_camera.pack(side=tkinter.LEFT)

        self.button_analysis = tkinter.Button(window, text='Analysis', width=button_size)
        self.button_analysis.pack(side=tkinter.LEFT)

        self.button_play_analyzed = tkinter.Button(window, text='Play Analyzed', width=button_size)
        self.button_play_analyzed.pack(side=tkinter.LEFT)

        self.button_snapshot = tkinter.Button(window, text='Snapshot!', width=button_size, command=self.take_snapshot)
        self.button_snapshot.pack(side=tkinter.LEFT)

    def update(self):
        if not self.is_video_paused:
            self.capture_video()

        self.window.after(self.delay, self.update)

    def capture_video(self):
        if self.video is not None:
            ret, frame = self.video.get_frame()
            if ret:
                image = PIL.Image.fromarray(frame)
                image.thumbnail((750, 750), PIL.Image.ANTIALIAS)
                self.photo = PIL.ImageTk.PhotoImage(image=image)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def stop_recognition(self):
        self.video = None
        print("stop_recognition")

    def play_video(self, path=0):
        self.video = _VideoCapture(path)
        print("play_video")

    def set_is_video_paused(self, is_paused):
        self.is_video_paused = is_paused

    def take_snapshot(self):
        if self.video is not None:
            ret, frame = self.video.get_frame()
            if ret:
                cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))


class MyApp:
    def __init__(self, b_should_start_looping=False):

        self.analysed_video_name = ""
        self.count_analyzed_video = 0
        self.default_dialog = FileType()

        self.path_to_opened_video = ""
        self.thread1 = None

        self.my_hud = HUD(tkinter.Tk(), 'VideoAnalysis', False)
        self.init_buttons_behavior()
        if b_should_start_looping:
            self.my_hud.start_loop()

    def choose_file_clicked(self):
        self.open_dialog(self.default_dialog)

# OMP_NUM_THREADS
    def analyse_clicked(self):
        self.increment_analysed_video_counter()
        self.stop_thread()
        if self.path_to_opened_video:
            self.thread1 = threading.Thread(target=MyVideoRecognition,
                                            args=(self.analysed_video_name, self.path_to_opened_video, 'fromVideo', self.stop_thread))
            self.thread1.start()
        else:
            self.thread1 = threading.Thread(target=MyVideoRecognition, args=(self.analysed_video_name, 0, 'fromCamera',  self.stop_thread))
            self.thread1.start()
        print("analyse_clicked")

    def increment_analysed_video_counter(self):
        self.count_analyzed_video += 1
        self.analysed_video_name = 'AnalyzedVideo' + str(self.count_analyzed_video)

    def play_analysed_video(self):
        if len(self.analysed_video_name) != 0:
            self.my_hud.play_video(self.analysed_video_name + ".avi")
            print("play_analysed_video")

    def init_buttons_behavior(self):
        self.my_hud.button_choose_file['command'] = self.choose_file_clicked
        self.my_hud.button_analysis['command'] = self.analyse_clicked
        self.my_hud.button_play_analyzed['command'] = self.play_analysed_video
        self.my_hud.button_choose_builtin_camera['command'] = self.turn_camera_on_clicked
        self.my_hud.button_play['command'] = self.play_video_clicked
        self.my_hud.button_pause['command'] = self.pause_video_clicked


    def turn_camera_on_clicked(self):
        self.path_to_opened_video = ""
        self.my_hud.play_video()
        if self.my_hud.is_video_paused:
            self.my_hud.capture_video()

    def open_dialog(self, file_type):
        self.path_to_opened_video = askopenfilename(defaultextension=file_type.default_extension,
                                               filetypes=file_type.file_types)
        if self.path_to_opened_video is None:
            self.path_to_opened_video = ""
        if len(self.path_to_opened_video) > 0:
            self.my_hud.play_video(self.path_to_opened_video)
        if self.my_hud.is_video_paused:
            self.my_hud.capture_video()

    def pause_video_clicked(self):
        self.my_hud.set_is_video_paused(True)
        self.stop_thread()

    def play_video_clicked(self):
        self.my_hud.set_is_video_paused(False)
        if len(self.path_to_opened_video) <= 0:
            self.turn_camera_on_clicked()

    def stop_thread(self):
        if self.thread1 is not None and self.thread1.is_alive():
            self.thread1.join
            self.thread1 = None


#my_app = MyApp(True)
