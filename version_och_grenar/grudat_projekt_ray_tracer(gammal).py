"""
Grudat projekt
Zeshen Bao


En simpel statisk raytracer

En statisk raytracer renderar en 2d bild som ögat ser genom att man simulerar
en öga som står vid en punkt och kollar på ett 3d rum med en ljuskälla som lyser på olika objekt.

Den fungerar på det sättet att istället för att simulera alla ljusstrålar från en ljuskälla så
backtrackar man endast ljusstrålar som når ögat tillbaka till ljuskällan. I 3d rummet kan vi placera
ut sfärer och en ljuskälla och med hjälp av raytracern rendera hur rummet ser ut från en viss punkt.
"""

from math import *
from PIL import Image


class Vektor():
    """implementerar en 3d vektor med tre element motsvarar positionen x, y, z i rummet"""
    

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """skapar en Vektor med elementen, x, y, z som position"""
        
        self.x, self.y, self.z = x, y, z


    def __repr__(self):
        """representerar Vektor som en sträng av en lista med vektorkomponenterna"""
        
        return str([self.x, self.y, self.z])
    

    def __add__(self, v):
        """addera self med vektor v (elementvis)"""
        
        return Vektor(self.x + v.x, self.y + v.y, self.z + v.z)
    

    def __sub__(self, v):
        """subtraherar self med vektor v (elementvis) """
        
        return Vektor(self.x - v.x, self.y - v.y, self.z - v.z)
    

    def __mul__(self, num):
        """multiplicerar self med ett tal EJ vektor"""
        
        return Vektor(self.x * num, self.y * num, self.z * num)

    def __rmul__(self, num):
        """multiplicerar ett tal med self, vänster multiplikation"""
        return self*num


    def dot(self, v):
        """returnerar skalärprodukten mellan self och v"""
        
        return self.x * v.x + self.y * v.y + self.z * v.z
    

    def length(self):
        """returnerar längden av vektorn"""

        return sqrt(self.dot(self))
    

    def norm(self):
        """returnerar den normaliserade vektor v"""
        len = self.length()
        
        return Vektor(self.x / len, self.y / len, self.z / len)


RGB = Vektor #RGB klass som använder sig av vektorklassen


class  Bild():
    """implementetra en bildklass som lagrar höjden, bredden och pixlarna på en bild"""

    def __init__(self, height, width):
        """skapar en bildklass och tar in höjden och bredden och lagrar dessa i variablerna height och width.
        Skapar en matris ixj genom en lista med element i som raden och elementen av elementen j som colonnen, i = height, j = width"""
    
        self.pixels = [[0 for j in range(width)] for i in range(height)]

    def pixel(self, i, j, color):
        """tilldelar pixeln (i,j) med en färg color"""



def ppm(bild_fil, bild):
    """tar in en bild som består av en ixj matris och skapar en ppm på filen bild_fil"""
    bild_fil.write("P3 {} {}\n255\n".format(width, height))
    
    for j in bild:
        for i in j:
            bild_fil.write("{} {} {} ".format(round(max(0, min(i.x*255, 255))), round(max(0, min(i.y*255, 255))), round(max(0, min(i.z*255, 255))))) #begränsar intervallet mellan 0 och 255

        bild_fil.write("\n")


def Color():
    """implementerar en färgklass som lagrar en färg som RGB-triplett""" #lagra som vektor
    pass


class Sphere():
    """implementerar en sfär objekt"""
    pass

def Ray():
    """implementerar ljustrålen som raytracing sker på"""
    pass

def Ljus():
    """implementerar en ljuskällan i 3d rummet som strålar ut ljusstrålarna"""
    pass

def Rum():
    """implementerar rummet där ljuset, och objekt som sfärer befinner sig i"""
    pass

class Engine():
    


        def render():
            """implementerar en metod som renderar en bild av rummet"""
            pass

        def ray_trace():
            """implementerar ray tracing """
            pass
            





#Bilden
#width = 2560
#height = 1600



#bild_file.close()








#Unit test
v = Vektor(1, 2, 3)

assert str(v) == "[1, 2, 3]" #testar __repr__()
assert str(v + v) ==  "[2, 4, 6]" #testar add()
assert str(v.length()) == str(sqrt(1**2+2**2+3**2)) #testar length()





#ppm

width = 3
height = 2

bild = [[0 for j in range(width)] for i in range(height)]

bild[0][0] = RGB(1, 0, 0) #bild[i][j]
bild[0][1] = RGB(0, 1, 0)
bild[0][2] = RGB(0, 0, 1)

bild[1][0] = RGB(1, 1, 0)
bild[1][1] = RGB(1, 1, 1)
bild[1][2] = RGB(0, 0, 0)

with open("bild.ppm", "w") as bild_fil:
    ppm(bild_fil, bild)

with open("bild.ppm", "r") as bild_fil:
    assert bild_fil.read() == "P3 3 2\n255\n255 0 0 0 255 0 0 0 255 \n255 255 0 255 255 255 0 0 0 \n"
    





    
