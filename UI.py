import time
import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
from tkinter.filedialog import askopenfilename

from _VideoCapture import _VideoCapture
from video_recognition import VideoRecognition
import threading


class App:
    def __init__(self, window, window_title, video_source=0):

        self.window = window
        self.window.title(window_title)

        self.path = 0
        self.video = _VideoCapture(video_source)

        self.canvas = tkinter.Canvas(window, width=700, height=400)
        self.canvas.pack()

        self.init_buttons(window)

        self.is_pause_video = True
        self.is_new_video_choosen = False
        self.count_analyzed_video = 0

        self.delay = 1
        self.update()

        self.window.mainloop()

    def init_buttons(self, window):
        button_size = 15
        self.text = tkinter.Label(window, text='')
        self.text.pack()
        self.button_play = tkinter.Button(window, text='Play', width=button_size, command=self.play)
        self.button_play.pack(side=tkinter.LEFT)  # , expand=True)

        self.button_pause = tkinter.Button(window, text='Pause', width=button_size, command=self.pause)
        self.button_pause.pack(side=tkinter.LEFT)  # , expand=True)

        self.button_choose_file = tkinter.Button(window, text='Choose video-file', width=button_size,
                                                 command=self.choose_file)
        self.button_choose_file.pack(side=tkinter.LEFT)

        self.button_choose_builtin_camera = tkinter.Button(window, text='Choose my webcam', width=button_size,
                                                           command=self.choose_builtin_camera)
        self.button_choose_builtin_camera.pack(side=tkinter.LEFT)

        self.button_analysis = tkinter.Button(window, text='Analysis', width=button_size, command=self.analysis)
        self.button_analysis.pack(side=tkinter.LEFT)


        self.button_play_analyzed = tkinter.Button(window, text='Play Analyzed', width=button_size,
                                                   command=self.play_analyzed)
        self.button_play_analyzed.pack(side=tkinter.LEFT)

        self.button_snapshot = tkinter.Button(window, text='Snapshot!', width=button_size, command=self.take_snapshot)
        self.button_snapshot.pack(side=tkinter.LEFT)

    def update(self):
        if self.is_new_video_choosen:
            self.video = _VideoCapture(self.path)
            self.is_new_video_choosen = False

        ret, frame = self.video.get_frame()

        if self.is_pause_video:
            self.window.after(self.delay, self.update)
            return
        self.window.update()

        if ret:
            image = PIL.Image.fromarray(frame)
            image.thumbnail((750, 750), PIL.Image.ANTIALIAS)
            self.photo = PIL.ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    def take_snapshot(self):
        ret, frame = self.video.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def play(self):
        self.is_pause_video = False

    def pause(self):
        print("def pause(self)")
        self.is_pause_video = True

    def change_input(self, input_file=0):
        self.path = input_file
        self.is_new_video_choosen = True
        print(self.path)

    def choose_file(self):
        self.change_input(askopenfilename(defaultextension='.mp4', filetypes=[('Video files', '*.mp4'),
                                                                              ('All files', '*.*')]))

    def choose_builtin_camera(self):
        self.change_input()
        # return text

    def analysis(self):
        self.count_analyzed_video += 1
        self.new_video_name = 'AnalyzedVideo' + str(self.count_analyzed_video)
        if self.path:
            self.thread1 = threading.Thread(target=VideoRecognition,
                                       args=(self.new_video_name, self.path))
            self.thread1.start()
        else:
            self.thread2 = threading.Thread(target=VideoRecognition, args=(self.new_video_name, 0, 'fromCamera'))
            self.thread2.start()
            # self.button_play_analyzed[state=]

    def play_analyzed(self):
        self.change_input(self.new_video_name + '.avi')




App(tkinter.Tk(), 'VideoAnalysis')





