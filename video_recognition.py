from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()


def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
    print("SECOND : ", second_number)
    print("Array for the outputs of each frame ", output_arrays)
    print("Array for output count for unique objects in each frame : ", count_arrays)
    print("Output average count for unique objects in the last second: ", average_output_count)
    if 'person' in average_output_count:
        print('PERRSSSSSOOOOOOOONNN')
    print("------------END OF A SECOND --------------")


detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()


video_path = detector.detectObjectsFromVideo(
    input_file_path=os.path.join(execution_path, "my_video.mp4"),
    output_file_path=os.path.join(execution_path, "video_detected"),
    frames_per_second=10,
    per_second_function=forSeconds,
    log_progress=True,
    minimum_percentage_probability=50
)
print(video_path)