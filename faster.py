import cv2
import dlib
import sys
import getopt


info_det = dlib.simple_object_detector("detectors/info.svm")
giveway_det = dlib.simple_object_detector("detectors/giveway.svm")
mandatory_det = dlib.simple_object_detector("detectors/mandatory.svm")
priority_det = dlib.simple_object_detector("detectors/priority.svm")
prohibitory_det = dlib.simple_object_detector("detectors/prohibitory.svm")
stop_det = dlib.simple_object_detector("detectors/stop.svm")
warning_det = dlib.simple_object_detector("detectors/warning.svm")



VERBOSE = False

def cli_progress(current_val, end_val, bar_length=20):
    percent = float(current_val) / end_val
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()

def getDetectedFrame(img):
    dets_info = info_det(img)
    dets_giveway = giveway_det(img)
    dets_manda = mandatory_det(img)
    dets_priority = priority_det(img)
    dets_proh = prohibitory_det(img)
    dets_stop = stop_det(img)
    dets_warn = warning_det(img)
    if len(dets_info) > 0:
        for k,d in enumerate(dets_info):
            cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (255,191,0))
    if len(dets_giveway) > 0:
        for k,d in enumerate(dets_giveway):
            cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0,191,255))
    if len(dets_manda) > 0:
        for k,d in enumerate(dets_manda):
            cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (255,0,0), 2)
    if len(dets_priority) > 0:
        for k,d in enumerate(dets_priority):
            cv2.rectangle([(d.left(), d.top()), (d.right(), d.bottom()), (0,255,255)])
    if len(dets_proh) > 0:
        for k,d in enumerate(dets_proh):
            cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0,0,255), 2)
    if len(dets_stop) > 0:
        for k,d in enumerate(dets_stop):
            cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (255,0,255), 2)
    if len(dets_warn) > 0:
        for k,d in enumerate(dets_warn):
            cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0,255,0), 2)
    return img


def process(inputfile, outputfile, skip = 1):
    c = cv2.VideoCapture(inputfile)
    print c.isOpened()

    framecount = c.get(cv2.CAP_PROP_FRAME_COUNT)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = c.get(cv2.CAP_PROP_FPS)

    if VERBOSE:
        print "Frame count: " + str(framecount)
        print "Fps: " + str(fps)

    frames = 0
    while frames < framecount:
        if VERBOSE:
            cli_progress(frames,framecount)
        ret, img = c.read()
        if frames == 0:
            height, width, layers = img.shape
            video = cv2.VideoWriter(outputfile,fourcc,fps,(width,height))
        frames += 1

        if VERBOSE:
            print ("\t" + str(frames) + "/" + str(int(framecount)) + " completed")

        if frames % skip == 0:
            processed = getDetectedFrame(img)
        elif frames == 1:
            processed = getDetectedFrame(img)
        else:
            processed = img



        video.write(processed)

def usage():
    print ("-i or --input: Input file name")
    print ("-o or --output: Output file name")
    print ("-v or --verbose: Verbose/debug mode")
    print ("-h or --help: Shows usage of arguments")

def main(argv):
    global VERBOSE
    input = ""
    output = ""
    skip = 1
    try:
        opts, args = getopt.getopt(argv, "hi:o:vs:", ["skip=","help","input=", "output=", "verbose"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            VERBOSE = True
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-s", "--skip"):
            skip = int(arg)
    if len(output) == 0 or len(input) == 0:
        print ("Invalid arguments!")
        print opts
        usage()
        sys.exit()
    else:
        process(input,output, skip)
        cv2.destroyAllWindows()



main(sys.argv[1:])