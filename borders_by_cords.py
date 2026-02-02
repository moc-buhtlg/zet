import numpy as np
from skimage.segmentation import flood, flood_fill, expand_labels, find_boundaries
from skimage.io import imread, imsave 
from itertools import combinations
from json import dump, load, JSONEncoder
from os import path, mkdir
from pathlib import Path

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

img = imread("c_cubes.png")
if len(img.shape)!=2:
    img=img[:,:,0]

with open("REGS.json", "r") as f:
    REGS=load(f)

with open("only_cords.json", "r") as f:
    CORDS=load(f)



for reg in CORDS.keys():
    print(reg)
    mask=flood(img, tuple(CORDS[reg][::-1]), connectivity=1).astype(np.uint8)
    
    cords=REGS[reg]["cords"] #[lu,rd]
    lu=cords[0]
    rd=cords[1]
    maxy=lu[0]
    miny=rd[0]
    maxx=lu[1]
    minx=rd[1]
    
    mask=mask[maxy : miny, maxx : minx]
            #[maxy, maxx], lu
            #[miny, minx]] rd
    REGS[reg]["tiles_mask"]=mask

with open("REGS_cubes.json", "w") as f:
    dump(REGS, f, cls=NumpyArrayEncoder, indent=2)









