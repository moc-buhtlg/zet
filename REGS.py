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
        elif isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)

MAP_NAME="map.png"

BASE_DIR = Path(__file__).parent.resolve() # 610556
OUTPUT_DIR = BASE_DIR / "result" # python -m cProfile 1stage.py

if not path.exists(OUTPUT_DIR):
        mkdir(OUTPUT_DIR)

def clean_img():
    img = imread(MAP_NAME)

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in [0,1,2]:
                if img[y,x,c]!=255:
                    img[y,x,0]=0
                    break
    img=img[:,:,0]
    imsave(f"c_{MAP_NAME}",img)
    print("очистка завершена")

img = imread(f"c_{MAP_NAME}")
if len(img.shape)!=2:
    img=img[:,:,0]
#proper_names = load(open("only_cords.json"))
REGS={}
i=0

def find_center(a, previous, mass=1): #a - Array
    a=a.copy()
    
    a[:,0]=0 #убрали рамчку
    a[:,-1]=0
    a[0]=0
    a[-1]=0
    
    for prev in previous:
        del_arr=np.zeros(a.shape).astype(bool)
        del_arr[prev]=1
        del_arr=expand_labels(del_arr, mass) #15
        del_arr=~del_arr        
        if (a*del_arr).any():
            a=a*del_arr
    
    while True:
        b=~find_boundaries(a,mode='inner')
        b=a*b
        if b.any():
            a=b
        else:
            break
    
    for y in range(a.shape[0]): #первую единичку возвращает
        for x in range(a.shape[1]):
            if a[y,x]==1:
                return (y,x)

def crop_zeros(arr):
    ys, xs = arr.shape
    
    for y in range(ys):
        if arr[y].any():
            maxy=y
            break
    for y in range(ys-1,-1,-1):
        if arr[y].any():
            miny=y+1
            break
    for x in range(xs):
        if arr[:,x].any():
            maxx=x
            break
    for x in range(xs-1,-1,-1):
        if arr[:,x].any():
            minx=x+1
            break
    
    return [arr[maxy : miny, maxx : minx],
            [maxy, maxx],
            [miny, minx]]
#print(np.pad(crop_zeros(a)[0],[2,2],mode='constant'))

for x in range(img.shape[1]):
    for y in range(img.shape[0]):
        if img[y,x]==255:
            
            mask = flood(img, (y, x), connectivity=1).astype(np.uint8)
            
            img[mask.astype(bool)] = 0
            
            mask, lu, rd = crop_zeros(mask)
            
            borders=np.pad(mask,[2,2],mode='constant')
            borders=expand_labels(borders,2)-borders
            
            blu=lu.copy()
            brd=rd.copy()
            blu[0]-=2
            blu[1]-=2
            brd[0]+=2
            brd[1]+=2
            
            c0=find_center(mask,[])
            c1=find_center(mask,[c0],15)
            
            c0=list(c0)
            c1=list(c1)
            c0[0]+=lu[0]
            c0[1]+=lu[1]
            c1[0]+=lu[0]
            c1[1]+=lu[1]
            c0=tuple(c0)
            c1=tuple(c1)
            
            i+=1
            #name=f"id{i:0>3}"
            name=f"{i}{'cab'[i%3]}"
            print(name,[x,y])
            
            #for key in proper_names.keys():
                #if proper_names[key]==[x,y]:
                    #name=key
                    #print(key,[x,y])
                    #break
            
            REGS[name]={
                "id": name,
                "routes": [],
                "centers": [c0,c1],
                "cords": [lu,rd],
                "bcords": [blu,brd],
                "tiles_mask": mask, #int,
                "borders": borders #1 0
                }


print("тайлы собрали, пошли сравнивать")
for reg1, reg2 in combinations(REGS.keys(),2):
    
    lu1, rd1 = REGS[reg1]["bcords"]
    lu2, rd2 = REGS[reg2]["bcords"]
    
    cs=np.array([lu1, rd1, lu2, rd2])
    cs.sort(axis=0)
    cs=cs[1:3]
    
    a=REGS[reg1]["borders"]
    b=REGS[reg2]["borders"]
    
    a=a[cs[0,0]-lu1[0] : cs[1,0]-lu1[0] , cs[0,1]-lu1[1] : cs[1,1]-lu1[1]]
    b=b[cs[0,0]-lu2[0] : cs[1,0]-lu2[0] , cs[0,1]-lu2[1] : cs[1,1]-lu2[1]]
    
    if (a * b).sum() > 6:
        REGS[reg1]["routes"].append(reg2)
        REGS[reg2]["routes"].append(reg1)

for reg in REGS.keys():
    del REGS[reg]["borders"]
    del REGS[reg]["bcords"]

with open("REGS.json", "w") as f:
    dump(REGS, f, cls=NumpyArrayEncoder, indent=2)









