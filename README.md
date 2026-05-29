# IntestiFlow

### Image analysis

The image analysis script takes in an mp4 video and outputs pickle files containing gut width information, which can be analysed using R or python.

Dependencies are managed via conda, by creating an environment with the respective environment file via `conda env create -f gutImagerEnv.yml`
After that the repository can be cloned locally by `git clone github.com/m4rku5-5/IntestiFlow`

Execution is done via the provided script `run_gutImager.sh`, which opens a seperate window to select gut segemnts, first select the upper left corner, then the lower right corner. A red rectangle will appear indicating the analysis area. Up to four segements can be selected. A rotation of the image may be applied in degrees, in case the alignment was not perfect.

```
conda activate gutImager
./run_gutImager.sh file.mp4 rotationInDegrees
```
