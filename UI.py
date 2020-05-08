import time
import tkinter as tk
import imageio
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

global pause_video


video_name = "my_video.mp4"
video = imageio.get_reader(video_name)


def video_frame_generator():
    def current_time():
        return time.time()

    start_time = current_time()
    _time = 0

    for frame, image in enumerate(video.iter_data()):

        image = Image.fromarray(image)
        image.thumbnail((750, 750), Image.ANTIALIAS)

        image = ImageTk.PhotoImage(image)

        _time += 1 / 24
        run_time = current_time() - start_time
        while run_time < _time:
            run_time = current_time() - start_time
        else:
            if run_time - _time > 0.1:
                start_time = current_time()
                _time = 0

        yield frame, image


def _stop():
    global pause_video
    pause_video = True


def _start():
    global pause_video
    pause_video = False


def _choose_file():
    text = askopenfilename(defaultextension='.mp4', filetypes=[('Video files','*.mp4'), ('All files','*.*')])
    print(text)
    return text


def create_image_for_buttons(path, length, height):
    icon = Image.open(path)
    icon = icon.resize((length, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(icon)


if __name__ == "__main__":

    root = tk.Tk()
    root.title('Videoan analisys')

    my_label = tk.Label(root)
    my_label.pack()

    #create icons
    play_icon = create_image_for_buttons('icon_play.png', 40, 30)
    pause_icon = create_image_for_buttons('icon_pause.png', 40, 30)


    #create buttons
    tk.Button(root, image=play_icon, command=_start).pack(side=tk.LEFT)
    tk.Button(root, image=pause_icon, command=_stop).pack(side=tk.LEFT)
    a = tk.Button(root, text='Choose the video file', command=_choose_file).pack(side=tk.LEFT)

    pause_video = False

    movie_frame = video_frame_generator()

    while True:

        if not pause_video:
            frame_number, frame = next(movie_frame)

            my_label.config(image=frame)

        root.update()

    root.mainloop()
