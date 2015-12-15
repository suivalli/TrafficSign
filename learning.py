import cv2
import dlib
import os
from skimage import filter, data, io
from skimage.viewer import ImageViewer


learning_folder = 'learning'

options = dlib.simple_object_detector_training_options()
options.add_left_right_image_flips = True
options.C = 5
options.num_threads = 1
options.be_verbose = True

training_xml_path = os.path.join(learning_folder,'info.xml')

dlib.train_simple_object_detector(training_xml_path, 'info.svm', options)

print ("")
print ("Training accuracy: {}".format(
    dlib.test_simple_object_detector(training_xml_path, "info.svm")
))

detector = dlib.simple_object_detector("info.svm")

win_det = dlib.image_window()
win_det.set_image(detector)

dlib.hit_enter_to_continue()