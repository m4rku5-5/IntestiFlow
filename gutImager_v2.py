import skimage as ski
from matplotlib import pyplot as plt
import numpy as np
import av
from alive_progress import alive_bar
import scipy as sp
import pickle as pkl
import sys

def get_widths(im, ul, lr):
    imslic = ski.segmentation.slic(im[ul[1]:lr[1],ul[0]:lr[0]], n_segments=2, min_size_factor=0.1)
    return np.count_nonzero(imslic == 2, axis=0)

v = av.open(sys.argv[1])
v.streams.video[0].thread_type = "AUTO"
total_frames = v.streams.video[0].frames

rot = float(sys.argv[10])

ul1 = [int(i) for i in sys.argv[2].split(",")] 
lr1 = [int(i) for i in sys.argv[3].split(",")]
ul2 = [int(i) for i in sys.argv[4].split(",")] 
lr2 = [int(i) for i in sys.argv[5].split(",")]
ul3 = [int(i) for i in sys.argv[6].split(",")] 
lr3 = [int(i) for i in sys.argv[7].split(",")]
ul4 = [int(i) for i in sys.argv[8].split(",")] 
lr4 = [int(i) for i in sys.argv[9].split(",")]

ROIs = [[ul1, lr1],
        [ul2, lr2],
        [ul3, lr3],
        [ul4, lr4]]

widths = [np.zeros((lr1[0]-ul1[0], total_frames)),
          np.zeros((lr2[0]-ul2[0], total_frames)),
          np.zeros((lr3[0]-ul3[0], total_frames)),
          np.zeros((lr4[0]-ul4[0], total_frames))]

fi = 0
with alive_bar(total_frames) as bar:
    for packet in v.demux():
        for frame in packet.decode():
            im = frame.to_image()
            arr = np.asarray(im.rotate(rot, expand=True))
            for roi in enumerate(ROIs):
                widths[roi[0]][:,fi] = get_widths(arr, roi[1][0], roi[1][1])
            bar()
            fi = fi + 1   

with open(sys.argv[1] + 'widths.pkl', 'wb') as f:
    pkl.dump(widths, f)
