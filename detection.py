import dlib
import glob
import os
from skimage import io

info_det = dlib.simple_object_detector("info.svm")
giveway_det = dlib.simple_object_detector("giveway.svm")
mandatory_det = dlib.simple_object_detector("mandatory.svm")
priority_det = dlib.simple_object_detector("priority.svm")
prohibitory_det = dlib.simple_object_detector("prohibitory.svm")
stop_det = dlib.simple_object_detector("stop.svm")
warning_det = dlib.simple_object_detector("warning.svm")

win = dlib.image_window()

pictures_folder = ('pics')

for f in glob.glob(os.path.join(pictures_folder, "*.png")):
    print ("Processing file: {}". format(f))
    img = io.imread(f)
    dets_info = info_det(img)
    dets_giveway = giveway_det(img)
    dets_manda = mandatory_det(img)
    dets_priority = priority_det(img)
    dets_proh = prohibitory_det(img)
    dets_stop = stop_det(img)
    dets_warn = warning_det(img)
    print (len(dets_info), len(dets_giveway), len(dets_manda), len(dets_priority), len(dets_proh), len(dets_stop), len(dets_warn))
    for k, d in enumerate(dets_info):
        print (("Detection {}: Left: {} Top: {} Right: {} Bottom: {}").format(
            k, d.left(), d.top(), d.right(), d.bottom()))

    win.clear_overlay()
    win.set_image(img)
    win.add_overlay(dets_info)
    dlib.hit_enter_to_continue()