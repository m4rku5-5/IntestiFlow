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

No special hardware is needed to run this script, howver on a standard desktop PC analysis takes about 45min for a 30min video, as workloads are only single threaded.

### Plotting

STMaps can be created via the following R code:

```
library(tidyverse)
library(reticulate)
library(raster)
library(ggpubr)
library(scales)

bl <- py_load_object("1_BL.mp4widths.pkl")

bl[[2]] %>% .[,seq(1,ncol(bl[[2]])-2000, 30)] %>%
    as_tibble() %>% 
    mutate(y = row_number()) %>% 
    pivot_longer(starts_with("V"), names_to = "x", values_to = "width") %>% 
    mutate(x = as.numeric(str_remove(x, "V"))/60) %>% 
    filter(x < 30) %>% 
    ggplot(aes(x=x, y=y, fill = width)) +
    geom_raster(interpolate = T) +
    scale_fill_gradientn(colours=c("#e34a33", "#ffeda0",  "#2b8cbe")) +
    scale_x_continuous(n.breaks = 10) +
    theme_pubr() +
    rremove("y.axis") +
    rremove("y.text") +
    rremove("y.ticks") +
    ylab("Baseline") +
    xlab("Time (min)") +
    guides(x = guide_axis(cap = "lower")) + 
    scale_x_continuous(breaks = breaks_pretty())
```
