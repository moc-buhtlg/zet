##################################
# передача территорий и ресурсов работает сразу а не на след ход так что делайте ее в конце хода
# отображение колва построек в начале след хода
##################################
vse={}
strana=[{},[0,0,0],[0,0,0]]
def normtile(tiles):
    new=[]
    for tile in tiles:
        for x, y in [("а","a"),("б","b"),("с","c"),("ф","f"),("д","d"),("е","e")]:
            tile=tile.replace(x,y)
        new.append(tile)
    return new

def buy(country, N, cost, balance):
    global vse, fcontinue
    ost=[b-N*a for a, b in zip(cost, balance)]
    if ost[0]<0 or ost[1]<0 or ost[2]<0:
        print("не хватает ресов")
        fcontinue=True
    else:
        vse[country][2]=ost

def chyakletka(tile):
    for country in vse.keys():
        if tile in vse[country][0].keys():
            return country


fcontinue=False
ats=set() #active tiles
maxb=1 #сколько максимум на тайле построек
renta=[0,0,0] #сколько и чего одна клетка зарабатывает
daily=[1,1,1]

buildkeys="FKO"

Gcost = {'Z': [1,1,1],
         'F': [5,0,10],
         'K': [10,1,5],
         'O': [15,0,0],
         'I': [0,0,100]}

fabs=["fab","fac","f","фаб","фактори","ф","п"]
kazs=["kaz","k","каз","к","в"]
offs=["off","of","o","оф","о","оф","офис","э","и","ислед"]

backups=[{}]
redos=[]
maxbackups=5
maxredos=5
#
# сделать инвистирование
#
#
def visualizase(world):
    print("траны Т  прокач       ресы     постройки")
    for country in vse.keys():
        print(country,len(vse[country][0]),*vse[country][1:])
    
while True:
    
    redos.append(str(vse))
    if len(redos)>maxredos+1:
        redos.pop(0)
    if len(backups)>maxbackups+1:
        backups.pop(0)
    
    visualizase(vse)
    #print(vse)
    
    c=input().lower().split() #command
    # ['/new', 'pepe', '43b', '2', '4', '5']
    if c==[]:
        redos.pop(-1)
        continue
    if c[0] in ["/new","/n","/нью","/н",".нью",".н"]:
        if len(c)!=6:
            print("не хватает аргументов ресурсов")
            continue
        c[2]=normtile([c[2]])[0]
        #                  П К О   Инвистиции    П    В    Э        
        vse[c[1]]=[{c[2]: [0,0,0] },[0,0,0],[int(c[3]),int(c[4]),int(c[5])],[0,0,0]]
        ats.add(c[2])
        continue
    
    elif c[0] in ["/redo","/r","/re","/ре","/z",".ре",".р","/-",".-"]:
        if len(redos)==1:
            print("в этом ходу не было действий еще")
            redos.pop(-1)
        else:
            redos.pop(-1)
            exec(f"vse={redos[-1]}")
            redos.pop(-1)      
        continue
    
    elif c[0] in ["/back","/b","/бек","/б",".бек",".б","/--",".--"]:
        if len(redos)==1 and len(backups)!=1:
            backups.pop(-1)
        exec(f"vse={backups[-1]}")
        redos=[]
        continue
    
    elif c[0] in ["/turn","/t","/ход","/х","/s",".ход",".х",".","/"]: #{pepe: [{tile: [0,0,0] },[0,0,0],[13,13,13]]}
        for country in vse.keys():
            vse[country][3]=[0,0,0]
            for buildings in vse[country][0].values():
                for i in range(3):
                    vse[country][3][i]+=buildings[i]
                    vse[country][2][i]+=buildings[i]*(1+vse[country][1][i])   #очки за постройки * на инвестиции
            
            vse[country][2]=[b+a for a, b in zip(daily, vse[country][2])] #очки бесплатные
            
            vse[country][2]=[b+a*len(vse[country][2]) for a, b in zip(renta, vse[country][2])] #очки за территории
            
            
        
        backups.append(str(vse))
        redos=[]
        continue
    
    elif c[0] in vse.keys():
        # ['pepe', 'add', '44b', '35c']
        if c[1] in ["add","a","адд","а"]: 
            c[2:]=normtile(c[2:])
            
            for tile in c[2:]:
                if tile in ats:
                    print(f"клета {tile} уже занята")
                    break
            else:
                
                buy(c[0],len(c[2:]),Gcost["Z"],vse[c[0]][2])                
                if fcontinue:
                    fcontinue=False
                    continue
                
                for tile in c[2:]:
                    vse[c[0]][0][tile]=[0,0,0]
                    ats.add(tile)
            continue
        
         # c=['пепе', 'up', 'o']
        elif c[1] in ["in","i","up","ин","и"]:
            
            if c[2]
            
            
            continue
        
        
        # c=['пепе', 'ту', 'мима', '35c', '33c']
        elif c[1] in ["res","r",">","рес","для","р","+","g","give","дает","to","ту"]:
            if c[2] in vse.keys():
                c.append("0")
                c.append("0")
                c.append("0")
                c[6:]=[]
                if not "".join(c[3:]).isdigit():
                    print("ресурсы должны быть числами")
                    continue
                c[6:]=[]
                c[3]=int(c[3])
                c[4]=int(c[4])
                c[5]=int(c[5])
                buy(c[0],1,c[3:],vse[c[0]][2])                
                if fcontinue:
                    fcontinue=False
                    continue
                
                vse[c[2]][2]=[b+a for a, b in zip(c[3:], vse[c[2]][2])]
                
                continue
            print(f"{c[2]} не существует")
            continue
        elif c[1] in ["war","w","!","вар","в"]: # pepe war f2 5 j3 13 2b 20 ###########################################
            c[2::2]=normtile(c[2::2])
            if len(c[2:])%2!=0:
                print("не зватает размера одной дивизии")
                continue
            if not "".join(c[3::2]).isdigit():
                print("ресурсы должны быть числами")
                continue
            
            c[3::2]=list(map(int, c[3::2]))
            
            for tile in c[2::2]:
                if tile in vse[c[0]][0].keys():
                    print(f"клета {tile} уже ваша")
                    break
                if tile not in ats:
                    print(f"клета {tile} свободна")
                    break
            else:
                buy(c[0],1,[0,sum(c[3::2]),0],vse[c[0]][2])                
                if fcontinue:
                    fcontinue=False
                    continue
                
                
                for tile, division in zip(c[2::2],c[3::2]):
                    attacked=chyakletka(tile)
                    
                    print(f"{attacked} {tile} защищает (любой символ) или терпит(enter)?")
                    if input()!="":
                        print(f"{attacked} дефает")
                        buy(attacked,1,[0,division,0],vse[attacked][2])
                        if not fcontinue:
                            continue
                    fcontinue=False
                    print(f"{attacked} терпит. {tile} отходит {c[0]}")
                    vse[c[0]][0][tile]=vse[attacked][0].pop(tile)
            continue
        
        elif c[1] in ["ter","t",">>","тер","terr","т","++"]:
            if c[2] in vse.keys():
                c[3:]=normtile(c[3:])
                
                for tile in c[3:]:
                    if tile not in vse[c[0]][0].keys():
                        print(f"клета {tile} не ваша")
                        break
                else:
                    for tile in c[3:]:
                        vse[c[2]][0][tile]=vse[c[0]][0].pop(tile)                        
                continue
            print(f"{c[2]} не существует")
            continue
        
        # c=['pepe', '-fab', '44b', '35c']                
                
                
        # c=['pepe', 'fab', '44b', '35c']
        elif c[1] in fabs+kazs+offs or c[1][1:] in fabs+kazs+offs:
            anti=False
            if c[1][0] in ["-","d","д"]:
                anti=True
                c[1]=c[1][1:]
            
            if c[1] in fabs:
                letter=0
            elif c[1] in kazs:
                letter=1
            elif c[1] in offs:
                letter=2
            
            
            c[2:]=normtile(c[2:])
            #  vse[c[0]][0]  ['ads', 'drd'] # словарь клеток {'ad': [0, 0, 0], 'ds': [0, 0, 0], 'af3': [0, 0, 0]}
            
            for tile in c[2:]:
                if tile not in vse[c[0]][0].keys():
                    print(f"клетка {tile} не ваша")
                    break
                if not anti:
                    if sum(vse[c[0]][0][tile])+c[2:].count(tile)>maxb:
                        print(f"максимум построек на {tile}")
                        break
                else:
                    if vse[c[0]][0][tile][letter]-c[2:].count(tile)<0:
                        print(f"нечего разрушать на {tile}")
                        break
            else:
                if not anti:
                    buy(c[0],len(c[2:]),Gcost[buildkeys[letter]],vse[c[0]][2])                
                    if fcontinue:
                        fcontinue=False
                        continue
                    
                    for tile in c[2:]:
                        vse[c[0]][0][tile][letter]+=1
                else:                        
                    for tile in c[2:]:
                        vse[c[0]][0][tile][letter]-=1
                        
                        
            continue
    else:
        redos.pop(-1)
        continue
            
            
            
            
            
            
            
        
