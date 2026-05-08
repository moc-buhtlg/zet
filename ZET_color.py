import numpy as np
from skimage.io import imread, imsave
from json import dump, load
from os import path, mkdir
from pathlib import Path

from random import randint


BASE_DIR = Path(__file__).parent.resolve() # 610556
OUTPUT_DIR = BASE_DIR / "result" # python -m cProfile 1stage.py

if not path.exists(OUTPUT_DIR):
        mkdir(OUTPUT_DIR)

with open("REGS_cubes.json", "r") as f:
    REGS=load(f)

img = imread("cubes.png")

for reg in REGS.keys():
    
    cords=REGS[reg]["cords"] #[lu,rd]
    lu=cords[0]
    rd=cords[1]
    
    tmask=np.asarray(REGS[reg]["tiles_mask"]).astype(bool)
    mask=np.zeros(img.shape[:2]).astype(bool)
    mask[lu[0] : rd[0], lu[1] : rd[1]]=tmask
    
    img[:,:,0:3][mask]=[randint(0,225),randint(0,225),randint(0,225)]
    
imsave(OUTPUT_DIR / "colored.png",img)    
