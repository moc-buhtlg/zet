from PIL import Image, ImageDraw, ImageFont
from webcolors import rgb_to_hex, hex_to_rgb

font = ImageFont.truetype(r"C:\Users\kukur\AppData\Local\Microsoft\Windows\Fonts\KappasPororoca.ttf", 35)


l=3

cords2=[(62,114),(101,90),(440+55,103+2)] #156 38 маленькое
#1123 пикселя вправо мапу сдвинуть корды
img=Image.open("fullmap.png")
img = img.convert("RGBA")

def textbox(size, bgColor, message, font, fontColor):
    W, H = size
    image = Image.new('RGB', size, bgColor)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)/2, (H-h)/2), message, font=font, fill=fontColor)
    return image

def draw_name(name: str, color: str, nomer: int):
    global img
    d = ImageDraw.Draw(img)
    
    dy=nomer*174
    color=hex_to_rgb(color)
    
    x, y = (62,114) #заливка кружка
    y+=dy
    d.ellipse([(x-24,y-24),(x+23,y+23)], color)
    
    x, y = (102,90)
    y+=dy
    #    размер поля имя 
    namebox=textbox((315,48), "yellow", name, font, color)
    img.paste(namebox, (x,y))

def draw_res():
    global img
    d = ImageDraw.Draw(img)
    
    
    
    

draw_name("asd","#aaaaaa",0)
img.show()
        

quit()
with Image.open("Классика.png") as img:
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    
    
    
    for x, y in cords:
        d.rectangle((x-l, y-l, x+l, y+l), (225, 0, 0))
        d.text((x,y),"123",(0,0,0),font=font)
    
    
    
img.show()

# в квадратиках - 1877 1427
# карта в классике - -35 1877 1427
# классика вся - 3000 1800
# вставлять на 1158 / 1159 x
#87 + 27 = 114 1ое текст поле
#122 + 27 = 149 расстояние между игроками