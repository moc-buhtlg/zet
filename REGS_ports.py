from json import dump, load, JSONEncoder

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)


with open("REGS_info_raw.json", "r") as f:
    REGS_INFO=load(f)

a="1c 2b 2c 3f 3d 3a 3b 8c 6a 5a 74b 76b 68c 65b 64b 25 26 13 14 15 16 13c 55b 54b 54c 26b 31 50a 54a 34a 35a 34b 36c 38a 38b 40b 33a"
PORTS_1=set(a.split())
a="56c 47c 48c"
PORTS_2=set(a.split())


for reg in REGS_INFO.keys():
    
    REGS_INFO[reg]["routes"]=set(REGS_INFO[reg]["routes"])
    routes=REGS_INFO[reg]["routes"]
    
    if reg in PORTS_1:
        routes|=PORTS_1
    elif reg in PORTS_2:
        routes|=PORTS_2

with open("REGS_info.json", "w") as f:
    dump(REGS_INFO, f, cls=NumpyArrayEncoder, indent=2)



