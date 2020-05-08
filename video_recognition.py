from imageai.Detection import VideoObjectDetection
import os


class VideoRecognition:

    def __init__(self, input_video, output_video):
        execution_path = os.getcwd()
        detector = VideoObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()
        video_path = detector.detectObjectsFromVideo(
            input_file_path=os.path.join(execution_path, input_video),
            output_file_path=os.path.join(execution_path, output_video),
            frames_per_second=10,
            per_second_function=self.forSeconds,
            log_progress=True,
            minimum_percentage_probability=50
        )
        print(video_path)

    def forSeconds(self, second_number, output_arrays, count_arrays, average_output_count):
        print("SECOND : ", second_number)
        print("Array for the outputs of each frame ", output_arrays)
        print("Array for output count for unique objects in each frame : ", count_arrays)
        print("Output average count for unique objects in the last second: ", average_output_count)
        if 'person' in average_output_count:
            print('PERRSSSSSOOOOOOOONNN')
        print("------------END OF A SECOND --------------")


VideoRecognition(input_video='my_video.mp4', output_video='new_video')