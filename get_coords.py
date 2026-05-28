import skimage as ski
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import numpy as np
import av
import sys


v = av.open(sys.argv[1])
v.streams.video[0].thread_type = "AUTO"

rot = float(sys.argv[2])

global arr

for packet in v.demux():
    for frame in packet.decode():
        im = frame.to_image()
        arr = np.asarray(im.rotate(rot, expand=True))
        if arr.any():
            break
    else:
        continue
    break


class Selector:
    def __init__(self, fig, ax):
        self.xs = []
        self.ys = []
        self.cid = fig.canvas.mpl_connect('button_press_event', self)
        self.ax = ax
        self.fig = fig
    
    def __call__(self, event):
        print(event.xdata, event.ydata, file=sys.stderr)
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        if len(self.xs) % 2 == 0:
            xy = (self.xs[-2], self.ys[-2])
            w = self.xs[-1] - self.xs[-2]
            h =  self.ys[-1] - self.ys[-2]
            rect = patches.Rectangle(xy, w, h, linewidth=1, edgecolor='r', facecolor='none')
            self.ax.add_patch(rect)
            self.fig.canvas.draw()
        if len(self.xs) == 8:
            self.xs = [str(round(i)) for i in self.xs]
            self.ys = [str(round(i)) for i in self.ys]
            print(self.xs[0] + "," + self.ys[0] + " " +
                  self.xs[1] + "," + self.ys[1] +
                  " " +
                  self.xs[2] + "," + self.ys[2] + " " +
                  self.xs[3] + "," + self.ys[3] +
                  " " +
                  self.xs[4] + "," + self.ys[4] + " " +
                  self.xs[5] + "," + self.ys[5] +
                  " " +
                  self.xs[6] + "," + self.ys[6] + " " +
                  self.xs[7] + "," + self.ys[7]
                  )

fig, ax = plt.subplots()
ax.imshow(arr)
s = Selector(fig, ax)

plt.show()

