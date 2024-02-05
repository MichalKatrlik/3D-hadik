import pygame as py
import math
import numpy as np
import random
from collections import deque

global eventy,selected,rotation           # eventy slúžia momentálne len na zapamätanie ľavého kliku myšky pre funkcie. Selected zase slúži na zapamätanie si selekcie z funkcie pre hlavnú časť programu.
eventy=[False]*10
rotation=True           # Určuje či sa kocka bude otáčať alebo nie



def nic(prazdne):      # Keďže používam class Button na vytváranie akéhokoľvek textu, tak potrebujem funkciu ktorá nič nerobí. Určená pre buttony na ktoré sa nedá kliknúť.
    return 0


 
def vyber(co):          # Zmena globalnej premennej pre z kliknutia buttonu
    global selected
    selected=co[0]


    
class Button:   # Classa určená na vykreslovanie tlačítka ktoré má text a volá funkciu po tom čo je kliknuté.
    def __init__(self,text_passed,plocha_passed,funkcia_passed,x_passed,y_passed,x_size_passed,y_size_passed,farba_passed,parametry_passed):
        self.x=x_passed
        self.y=y_passed
        self.x_size=x_size_passed
        self.y_size=y_size_passed
        self.plocha=plocha_passed
        self.farba=farba_passed
        self.funkcia=funkcia_passed
        self.text=text_passed
        self.parametry=parametry_passed
        if(self.x_size<len(self.text)*8.8):
            self.x_size=len(self.text)*8.8
        if(self.y_size<20):
            self.y_size=20
            
    def vykresli(self):        # Vykreslenie tlačitka do plochy
        py.draw.rect(self.plocha,self.farba,py.Rect(self.x,self.y,self.x_size,self.y_size))
        font = py.font.Font(None, 24)
        textik=font.render(self.text, False, 'yellow')
        self.plocha.blit(textik,(self.x+(self.x_size/2)-self.x_size/2,self.y+(self.y_size/2)-8))
        
    def detekuj_klik(self):     # Detekcia kliku
        if(eventy[0]==True):
            if(py.mouse.get_pos()[0]>=self.x and py.mouse.get_pos()[0]<=self.x+self.x_size and py.mouse.get_pos()[1]>=self.y and py.mouse.get_pos()[1]<=self.y+self.y_size):
                self.funkcia(self.parametry)


class Cube:     # Classa reprezentujúca kocky z ktorých sa skladá hra
    def __init__(self,x_passed,y_passed,z_passed,size_passed,fill_passed,color_passed,outline_passed,transparent_passed,plocha_passed,alpha_passed):
        self.alpha=alpha_passed
        self.x=x_passed
        self.y=y_passed
        self.z=z_passed
        self.size=size_passed
        self.fill=fill_passed
        self.color=color_passed     
        self.transparent=transparent_passed
        self.plocha=plocha_passed
        self.outline=outline_passed
        self.points=[
             [self.x,self.y,self.z]
             
            ,[self.x+self.size,self.y,self.z]
             
            ,[self.x+self.size,self.y-self.size,self.z]
             
            ,[self.x,self.y-self.size,self.z]
             
            ,[self.x,self.y-self.size,self.z-self.size]
             
            ,[self.x,self.y,self.z-self.size]
             
            ,[self.x+self.size,self.y,self.z-self.size]
             
            ,[self.x+self.size,self.y-self.size,self.z-self.size]]
        
    def get_new_points(self,degree):         # V závisloti od uhla vráti pozíciu vrcholov 2D polygonu reprezentujúceho kocku. Na tento prevod je použité zobrazenie vytorené štýlom pokus-omyl.
        new_points=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        degree=degree*(6.28/360)
        a=0
        for i in self.points:
            new_points[a][0]=i[0]-i[1]*math.cos(degree)*0.5
            new_points[a][1]=i[2]+i[1]*math.sin(degree)*0.5-math.sin(degree)*100
            a+=1
        return new_points
    
    def fill_change(self):       # Zmení či je kocka vyplnená alebo nie
        if self.fill==True:
            self.fill=False
        else:
            self.fill=True
            
    def color_change(self,color):   # Zmení farbu kocky
        self.color=color
        
    def get_image(self,degree):         # Pridá 2D reprezentáciu našej kocky do plochy v závisloti od uhla "pohľadu".
        new_points=self.get_new_points(degree)
        rl=self.get_new_points(degree)
        degree=degree*(6.28/360)
        kont=[new_points[0][0],new_points[1][0],new_points[2][0],new_points[3][0],new_points[4][0],new_points[5][0],new_points[6][0],new_points[7][0]]
        kont2=[new_points[0][1],new_points[1][1],new_points[2][1],new_points[3][1],new_points[4][1],new_points[5][1],new_points[6][1],new_points[7][1]]
        nov=py.Surface((max(kont)-min(kont),max(kont2)-min(kont2)),py.SRCALPHA)
        for ii in rl:
            ii[0]-=min(kont)
            ii[1]-=min(kont2)
        if(degree<=3.14/2):
            if(self.fill==True):
                py.draw.polygon(nov,self.color,[rl[0],rl[1],rl[2],rl[7],rl[4],rl[5]])
            
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[1])
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[5]) 
            py.draw.line(self.plocha,self.outline,new_points[1],new_points[2])
            py.draw.line(self.plocha,self.outline,new_points[1],new_points[6])
            py.draw.line(self.plocha,self.outline,new_points[2],new_points[7])
            py.draw.line(self.plocha,self.outline,new_points[4],new_points[5])
            py.draw.line(self.plocha,self.outline,new_points[4],new_points[7])
            py.draw.line(self.plocha,self.outline,new_points[5],new_points[6])
            py.draw.line(self.plocha,self.outline,new_points[6],new_points[7])
        elif(degree>3.14/2 and degree<=3.14):
            if(self.fill==True):
                py.draw.polygon(nov,self.color,[rl[0],rl[1],rl[6],rl[7],rl[4],rl[3]])
            
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[1])
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[3])
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[5]) 
            py.draw.line(self.plocha,self.outline,new_points[1],new_points[6])
            py.draw.line(self.plocha,self.outline,new_points[3],new_points[4])
            py.draw.line(self.plocha,self.outline,new_points[4],new_points[5])
            py.draw.line(self.plocha,self.outline,new_points[4],new_points[7])
            py.draw.line(self.plocha,self.outline,new_points[5],new_points[6])
            py.draw.line(self.plocha,self.outline,new_points[6],new_points[7])
        elif(degree>3.14 and degree<=3.14*3/2):
            if(self.fill==True):
                py.draw.polygon(nov,self.color,[rl[2],rl[1],rl[6],rl[5],rl[4],rl[3]])
            
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[1])
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[3])
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[5]) 
            py.draw.line(self.plocha,self.outline,new_points[1],new_points[2])
            py.draw.line(self.plocha,self.outline,new_points[1],new_points[6])
            py.draw.line(self.plocha,self.outline,new_points[2],new_points[3])
            py.draw.line(self.plocha,self.outline,new_points[3],new_points[4])
            py.draw.line(self.plocha,self.outline,new_points[4],new_points[5])
            py.draw.line(self.plocha,self.outline,new_points[5],new_points[6])
        else:
            if(self.fill==True):
                py.draw.polygon(nov,self.color,[rl[0],rl[3],rl[2],rl[7],rl[6],rl[5]])
            
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[1])
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[3])
            py.draw.line(self.plocha,self.outline,new_points[0],new_points[5]) 
            py.draw.line(self.plocha,self.outline,new_points[1],new_points[2])
            py.draw.line(self.plocha,self.outline,new_points[1],new_points[6])
            py.draw.line(self.plocha,self.outline,new_points[2],new_points[3])
            py.draw.line(self.plocha,self.outline,new_points[2],new_points[7])
            py.draw.line(self.plocha,self.outline,new_points[5],new_points[6])
            py.draw.line(self.plocha,self.outline,new_points[6],new_points[7])
        if(self.fill==True):
            self.plocha.blit(nov,(min(kont),min(kont2)))


            
    def get_rank(self,degree):    # Vráti číslo určené na zoradenie kociek tak aby boli vykreslené v správnom poradí. Teda či by sme ich mali vidieť bližšie alebo ďalej.
        degree=degree*(6.28/360)
        if(degree<=3.14/2):
            a=-(self.x**2)-self.y**2+self.z**2
        elif(degree>3.14/2 and degree<=3.14):
            a=(self.x**2)-self.y**2+self.z**2
        elif(degree>3.14 and degree<=3.14*3/2):
            a=(self.x**2)-self.y**2-self.z**2

        else:
            a=-(self.x**2)-self.y**2-self.z**2

        return a
                

def difficulty_2(screen,diff):      # Funkcia je ťažšia verzia hry kde sa hadík hýbe sám aj keď nedostane input. Diff určuje ako rýchlo/ćasto sa hýbe hadík
    global selected,eventy,rotation
    smer=101       # smer 101 reprezentuje pohyb smerom hore
    hrac=0         # hrac je pozícia hráča vyjadrená ako x+y*velkost+z*velkost*velkost
    hracpoz=[3,3,3]     # Začiatočná pozícia hráča v kocke. Vyjadrená ako [x,y,z]
    velkost=6           # Veľkosť veľkej kocky.
    zradlo=1            
    zradlopoz=[1,0,0]   # Pozícia jedla v kocke.
    clock = py.time.Clock()
    objekty=[]         # V tejto implementácii len zoznam tlačítok
    objekty3d=[]       # V tejto implementácii len zoznam kociek
    body=1
    zabrate= np.zeros((velkost*velkost*velkost), dtype=int)       # Pole indetifikujúce či je pozícia v kocke už obsadená
    tail=deque([])
    objekty.append(Button("Pohybujes sa W,A,S,D pre kazdu uroven kocky a medzi urovnami chodis cez Q,E. Q je dole E je hore.",screen,nic,0,0,0,0,'red',["cau"]))
    objekty.append(Button("X zastaví rotovanie. P zastaví hru ak niesi v lahkej obitažnosti",screen,nic,0,20,0,0,'red',["cau"]))
    z=50
    for j in range(velkost):    # Vytvorenie velkej kocky.
        for y in range(velkost):
            for i in range(velkost):
                objekty3d.append(Cube(500+i*60,200+j*60,300+y*60,60,False,(255,0,0),'orange',False,screen,180))
                
    hrackepole=objekty3d[:]                 # V zozname hrackepole sa pozicia kociek nemení
    hrac=hracpoz[0]+hracpoz[1]*velkost+hracpoz[2]*velkost*velkost
    hrackepole[hrac].fill_change()           # Hráč má červenú farbu

    
    py.display.flip()
    hrackepole[zradlo].color_change('green')       # Jedlo má zalenu farbu
    hrackepole[zradlo].fill_change()
    pam=True
    fram=0
    pause=False
    while pam:                  # Loopa jednej hry
        if(pause==False):       
            fram=(fram+1)%diff
        if(rotation==True):
            z=(z+1)%360
        screen.fill('black')
        
        for i in objekty:
            if isinstance(i,Button):
                i.detekuj_klik()
                i.vykresli()
                
        objekty3d=sorted(objekty3d,key=lambda o:o.get_rank(z),reverse=True) # Kocky su sortnuté podľa toho ako majú byť vykreslené
        for i in objekty3d:
            if isinstance(i,Cube):
                i.get_image(z)
        
        pomocna=[False]*10
        for ev in py.event.get():
            if ev.type == py.KEYDOWN:
                if(ev.key==112):
                    pause=not pause        
                if((ev.key==101 and smer!=113) or (ev.key==113 and smer!=101) or (ev.key==97 and smer!=100) or (ev.key==115 and smer!=119) or (ev.key==100 and smer!=97) or (ev.key==119 and smer!=115)):
                # Nepovolujem ísť na polícko kde sme práve boli aby sa user tak ľachko nemohol zabiť
                    smer=ev.key
                if(ev.key==120):
                    rotation=not rotation
            if ev.type == py.MOUSEBUTTONDOWN:  
                pomocna[0]=True   # Potrebné pre kontrolu tlačítok
                
            if ev.type == py.QUIT:
                py.quit()
                raise SystemExit


            
        if(fram==0):      # Hýbeme sa len občas, nie v každej iterácii
            if(smer==101):
                if(hracpoz[1]!=0):
                    hracpoz[1]-=1

            elif(smer==113):
                if(hracpoz[1]!=velkost-1):
                    hracpoz[1]+=1


            elif(smer==97):
                if(hracpoz[0]!=0):
                    hracpoz[0]-=1

            elif(smer==115):
                if(hracpoz[2]!=velkost-1):
                    hracpoz[2]+=1

            elif(smer==100):
                if(hracpoz[0]!=velkost-1):
                    hracpoz[0]+=1

            elif(smer==119):
                if(hracpoz[2]!=0):
                    hracpoz[2]-=1

            if(len(tail)==body):    # Vymazanie posledného prvku ak ak niesme dosť veľký aby sme ho v sebe mali
                sur=tail.pop()
                zabrate[sur]=0
                hrackepole[sur].fill_change()

                
            tail.appendleft(hrac)    # Priadnie nového prvku do chôsta. Toho kde sme práve boli
            zabrate[hrac]=1
            hrackepole[hrac].color_change((255,100,50,140))
            hrac=hracpoz[0]+hracpoz[1]*velkost+hracpoz[2]*velkost*velkost

            
            if(zabrate[hrac]==1):        # Ak sa hadík nepohol tak hra skončila
                text='Prehral si z '+str(body-1)+' bodmi, klikni pre reset'
                if(body>=velkost**3-2):     # Ak user získal dosť bodov tak vyhral
                    text='Vyhral si, klikni pre reset'
                objekty=[Button(text,screen,vyber,500,30,50,50,'orange',[-1])]  # Tlacitko nam dovoli zresetovať hru
                objekty[0].vykresli()
                pam=False  # pom určuje či hra ešte pokračuje
            hrackepole[hrac].color_change('red')
            hrackepole[hrac].fill_change()
            

        if(pam==False):
            py.display.flip()
            break
        
        if(hrac==zradlo): # Ak je hrac na pozícii jedla tak sa zväčšime body a presunieme jedlo na novú pozíciu
            body+=1 
            hrackepole[zradlo].fill_change()
            zradlopoz[0]=random.randint(0,velkost-1)
            zradlopoz[1]=random.randint(0,velkost-1)
            zradlopoz[2]=random.randint(0,velkost-1)
            zradlo=zradlopoz[0]+zradlopoz[1]*velkost+zradlopoz[2]*velkost*velkost
            while(zabrate[zradlo]==1):
                zradlopoz[0]=random.randint(0,velkost-1)
                zradlopoz[1]=random.randint(0,velkost-1)
                zradlopoz[2]=random.randint(0,velkost-1)
                zradlo=zradlopoz[0]+zradlopoz[1]*velkost+zradlopoz[2]*velkost*velkost
            hrackepole[zradlo].color_change('green')
            hrackepole[zradlo].fill_change()
        eventy=pomocna[:]
        py.display.flip()
        clock.tick(60)

        
    while selected!=-1:    # Loopa detekujúca kliknutie na tlačitko resetu
        for i in objekty:
            if isinstance(i,Button):
                i.detekuj_klik()
        pomocna=[False]*10
        for ev in py.event.get():
            if ev.type == py.QUIT:
                py.quit()
            if isinstance(i,Button):
                i.detekuj_klik()
            if ev.type == py.MOUSEBUTTONDOWN:
                pomocna[0]=True
                print("st")
        clock.tick(60)
        eventy=pomocna[:]
    loopa(screen)   # Resetnutie hry
     
def difficulty_1(screen):      # Ľachšie verzia hry. Hadík sa pohne len keď dostnae input na pohyb
    global selected,eventy,rotation
    hrac=0          # hrac je pozícia hráča vyjadrená ako x+y*velkost+z*velkost*velkost
    hracpoz=[3,3,3] # Začiatočná pozícia hráča v kocke. Vyjadrená ako [x,y,z]
    velkost=6  # Veľkosť veľkej kocky.
    zradlo=1
    zradlopoz=[1,0,0]     # Pozícia jedla v kocke.
    clock = py.time.Clock()
    objekty=[]            # V tejto implementácii len zoznam tlačítok
    objekty3d=[]          # V tejto implementácii len zoznam kociek
    body=1
    zabrate= np.zeros((velkost*velkost*velkost), dtype=int) # Pole indetifikujúce či je pozícia v kocke už obsadená
    tail=deque([])
    objekty.append(Button("Pohybujes sa W,A,S,D pre kazdu uroven kocky a medzi urovnami chodis cez Q,E. Q je dole E je hore.",screen,nic,0,0,0,0,'red',["cau"]))
    objekty.append(Button("X zastaví rotovanie. P zastaví hru ak niesi v lahkej obitažnosti",screen,nic,0,20,0,0,'red',["cau"]))
    z=50
    for j in range(velkost): # Vytvorenie velkej kocky.
        for y in range(velkost):
            for i in range(velkost):
                objekty3d.append(Cube(500+i*60,200+j*60,300+y*60,60,False,(255,0,0),'orange',False,screen,180))
                
    hrackepole=objekty3d[:] # V zozname hrackepole sa pozicia kociek nemení
    hrac=hracpoz[0]+hracpoz[1]*velkost+hracpoz[2]*velkost*velkost
    hrackepole[hrac].fill_change()   # Hráč má červenú farbu
    
    py.display.flip()
    hrackepole[zradlo].color_change('green') # Jedlo má zalenu farbu
    hrackepole[zradlo].fill_change()
    pam=True
    while pam:        # Loopa jednej hry
        if(rotation==True): 
            z=(z+1)%360 
        screen.fill('black')
        for i in objekty:
            if isinstance(i,Button):
                i.detekuj_klik()
                i.vykresli()
                
        objekty3d=sorted(objekty3d,key=lambda o:o.get_rank(z),reverse=True)  # Kocky su sortnuté podľa toho ako majú byť vykreslené
        for i in objekty3d:
            if isinstance(i,Cube):
                i.get_image(z)
        pomocna=[False]*10
        for ev in py.event.get():
            if ev.type == py.KEYDOWN:
                if(ev.key==120):
                    rotation=not rotation
                # Nepovolujem ísť na polícko kde sme práve boli aby sa user tak ľachko nemohol zabiť
                if(ev.key==101):
                    if(len(tail)==0 or (hracpoz[1]!=0 and tail[0]!=hrac-velkost)):
                        hracpoz[1]-=1
                    else:
                        continue
                elif(ev.key==113):
                    if(len(tail)==0 or (hracpoz[1]!=velkost-1 and tail[0]!=hrac+velkost)):
                        hracpoz[1]+=1
                    else:
                        continue
                elif(ev.key==97):
                    if(len(tail)==0 or (hracpoz[0]!=0 and tail[0]!=hrac-1)):
                        hracpoz[0]-=1
                    else:
                        continue
                elif(ev.key==115):
                    if(len(tail)==0 or (hracpoz[2]!=velkost-1 and tail[0]!=hrac+velkost**2)):
                        hracpoz[2]+=1
                    else:
                        continue
                elif(ev.key==100):
                    if(len(tail)==0 or (hracpoz[0]!=velkost-1 and tail[0]!=hrac+1)):
                        hracpoz[0]+=1
                    else:
                        continue
                elif(ev.key==119):
                    if(len(tail)==0 or (hracpoz[2]!=0 and tail[0]!=hrac-velkost**2)):
                        hracpoz[2]-=1
                    else:
                        continue
                else:
                    continue
                if(len(tail)==body): # Vymazanie posledného prvku ak ak niesme dosť veľký aby sme ho v sebe mali
                    sur=tail.pop()
                    zabrate[sur]=0
                    hrackepole[sur].fill_change()
                tail.appendleft(hrac) # Priadnie nového prvku do chôsta. Toho kde sme práve boli
                zabrate[hrac]=1
                hrackepole[hrac].color_change((255,100,50,140))
                hrac=hracpoz[0]+hracpoz[1]*velkost+hracpoz[2]*velkost*velkost
                if(zabrate[hrac]==1): # Ak hadíkk do seba narazil tak hra skončila. Narazenie do stien tolerujem 
                    text='Prehral si z '+str(body-1)+' bodmi, klikni pre reset'
                    if(body>=velkost**3-2):   # Ak user získal dosť bodov tak vyhral
                        text='Vyhral si, klikni pre reset'
                    objekty=[Button(text,screen,vyber,500,30,50,50,'orange',[-1])]
                    objekty[0].vykresli()
                    pam=False      # pom určuje či hra ešte pokračuje
                    break
                hrackepole[hrac].color_change('red')
                hrackepole[hrac].fill_change()
            if ev.type == py.MOUSEBUTTONDOWN:
                pomocna[0]=True    # Potrebné pre kontrolu tlačítok
            if ev.type == py.QUIT:
                py.quit()
                raise SystemExit
        if(pam==False):
            py.display.flip()
            break
        if(hrac==zradlo): # Ak je hrac na pozícii jedla tak sa zväčšime body a presunieme jedlo na novú pozíciu
            body+=1
            hrackepole[zradlo].fill_change()
            zradlopoz[0]=random.randint(0,velkost-1)
            zradlopoz[1]=random.randint(0,velkost-1)
            zradlopoz[2]=random.randint(0,velkost-1)
            zradlo=zradlopoz[0]+zradlopoz[1]*velkost+zradlopoz[2]*velkost*velkost
            while(zabrate[zradlo]==1):
                zradlopoz[0]=random.randint(0,velkost-1)
                zradlopoz[1]=random.randint(0,velkost-1)
                zradlopoz[2]=random.randint(0,velkost-1)
                zradlo=zradlopoz[0]+zradlopoz[1]*velkost+zradlopoz[2]*velkost*velkost
            hrackepole[zradlo].color_change('green')
            hrackepole[zradlo].fill_change()
        eventy=pomocna[:]
        py.display.flip()
        clock.tick(60)
    while selected!=-1: # Loopa detekujúca kliknutie na tlačitko resetu
        for i in objekty:
            if isinstance(i,Button):
                i.detekuj_klik()
        pomocna=[False]*10
        for ev in py.event.get():
            if ev.type == py.QUIT:
                py.quit()
            if ev.type == py.MOUSEBUTTONDOWN:
                pomocna[0]=True
        eventy=pomocna[:]
        clock.tick(60)
    loopa(screen)


    
def loopa(screen):         # Funkcia ktorá určuje aká obtiažnosť hry sa má zavolať
    global selected,eventy
    objekty=[]
    screen.fill('black')
    objekty.append(Button("Pohybujes sa W,A,S,D pre kazdu uroven kocky a medzi urovnami chodis cez Q,E. Q je dole E je hore.",screen,nic,0,0,0,0,'red',["cau"]))
    objekty.append(Button("X zastaví rotovanie. P zastaví hru ak niesi v lahkej obitažnosti",screen,nic,0,20,0,0,'red',["cau"]))
    objekty.append(Button("Vyber si obtiaznost",screen,nic,500,100,50,50,'black',[]))
    objekty.append(Button("Lahka, ak nedas input tak sa hadik nepohne",screen,vyber,400,170,50,50,'green',[1]))     # Kliknutie na rôzne obtiažnosti rôzne meni globálnu premennú selected
    objekty.append(Button("Stredna, klasicky hadik ale v 3D. Hybe sa pomali",screen,vyber,400,230,50,50,'orange',[2]))
    objekty.append(Button("Tazka, klasicky hadik ale v 3D. Hybe sa rychlo",screen,vyber,400,290,50,50,'red',[3]))
    pam=True
    clock = py.time.Clock()
    selected=0
    
    for i in objekty:
        if isinstance(i,Button):
            i.vykresli()
            
    while selected==0:      # Kým nebolo nič nevybrané tak kontrolujeme stlačenie tlačítok
        for i in objekty:
            if isinstance(i,Button):
                i.detekuj_klik()
        pomocna=[False]*10
        for ev in py.event.get():
            if ev.type == py.QUIT:
                py.quit()
                raise SystemExit
            if ev.type == py.MOUSEBUTTONDOWN:
                pomocna[0]=True
        eventy=pomocna[:]
        py.display.flip()
        clock.tick(60)
        
    if(selected==1):       # Voláme obtiažnosť podľa toho čo si vybral použivatel
        difficulty_1(screen)
    if(selected==2):
        difficulty_2(screen,40)
    if(selected==3):
        difficulty_2(screen,20)

py.init()
screen = py.display.set_mode((1280, 800))  # Vytvorenie plochy
py.display.set_caption("3D Hadik")
loopa(screen)        # Začiatok hry
