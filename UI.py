import time
import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
from tkinter.filedialog import askopenfilename

from _VideoCapture import _VideoCapture


class App:
    def __init__(self, window, window_title, video_source=0):

        self.window = window
        self.window.title(window_title)

        self.path = 0
        self.video = _VideoCapture(video_source)

        self.canvas = tkinter.Canvas(window, width=700, height=400)
        self.canvas.pack()

        self.button_play = tkinter.Button(window, text='Play', width=20, command=self.play)
        self.button_play.pack(side=tkinter.LEFT) # , expand=True)

        self.button_pause = tkinter.Button(window, text='Pause', width=20, command=self.pause)
        self.button_pause.pack(side=tkinter.LEFT) # , expand=True)

        self.button_choose_file = tkinter.Button(window, text='Choose video-file', width=20, command=self.choose_file)
        self.button_choose_file.pack(side=tkinter.LEFT)

        self.button_snapshot = tkinter.Button(window, text='Snapshot!', width=20, command=self.take_snapshot)
        self.button_snapshot.pack(side=tkinter.LEFT)  # , expand=True)

        self.is_pause_video = True
        self.is_new_video_choosen = False

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        print(22)
        if self.is_new_video_choosen:
            self.video = _VideoCapture(self.path)
            self.is_new_video_choosen = False



        ret, frame = self.video.get_frame()

        while True:
            if self.is_pause_video == False:
                break
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
        self.is_pause_video = True

    def choose_file(self):
        self.path = askopenfilename(defaultextension='.mp4', filetypes=[('Video files', '*.mp4'), ('All files', '*.*')])
        self.is_new_video_choosen = True
        print(self.path)

        # return text



App(tkinter.Tk(), 'VideoAnalysis')




# , 'my_video.mp4')



