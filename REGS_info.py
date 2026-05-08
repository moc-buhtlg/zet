from json import dump, load

with open("REGS.json", "r") as f:
    REGS=load(f)

REGS_INFO={
    reg: {"routes": REGS[reg]["routes"],
          "centers": REGS[reg]["centers"]
          }
    for reg in REGS.keys()
    }

with open("REGS_info_raw.json", "w") as f:
    dump(REGS_INFO, f, indent=2)