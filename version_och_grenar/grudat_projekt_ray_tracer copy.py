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
#from PIL import Image


class Vector():
    """Implementerar en 3d vektor med tre element motsvarar positionen x, y, z i rummet."""
    

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Skapar en Vektor med instansvariablerna x, y, z och deras värde från input."""
        
        self.x, self.y, self.z = x, y, z


    def __repr__(self):
        """Representerar Vektor som en sträng av en lista med vektorkomponenterna."""
        
        return str([self.x, self.y, self.z])
    

    def __add__(self, v):
        """Tar in en vektor v och adderar self med v (elementvis)."""
        
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
    

    def __sub__(self, v):
        """Tar in en vektor v och subtraherar self med v (elementvis)."""
        
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
    

    def __mul__(self, num):
        """Tar en ett tal num och multiplicerar self med ett talet, observera att num ej är en vektor."""
        
        return Vector(self.x * num, self.y * num, self.z * num)

    def __rmul__(self, num):
        """Multiplicerar ett tal med self, vänster multiplikation."""
        return self*num


    def dot(self, v):
        """Tar in en vetkor v och returnerar skalärprodukten mellan self och v."""
        
        return self.x * v.x + self.y * v.y + self.z * v.z
    

    def length(self):
        """Returnerar längden av vektor v."""

        return sqrt(self.dot(self))
    

    def norm(self):
        """Returnerar den normaliserade vektor v."""
        len = self.length()
        
        return Vector(self.x / len, self.y / len, self.z / len)


RGB = Vector #RGB klass som använder sig av vektorklassen
Point = Vector



class Sphere():
    """Implementerar en sfär objekt"""

    def __init__(self, radie, punkt, material):
        """Skapar en sfär med input radie som radie och sin centrum i input punkten och ljusegenskaper efter input material."""
        
        self.radius = radie
        self.center = punkt
        self.material = material
        self.dikt = {}
        self.c = 0

    def intersect(self, ray):
        """Tar in en ljusstråle som input och returnerar tiden det tar för strålen att träffa sfären"""
        a = 1 #ray.direction.dot(ray.direction)
        #print(ray.point, self.center)
        sphere_ray = ray.point - self.center
        #print(sphere_ray)

        """
        self.c += 1
        if self.c == 1000:
            print(ray.direction)
            self.c = 0
        """

        
        b = 2*ray.direction.dot(sphere_ray)
        
        #print(ray.direction.dot(sphere_ray))
        c = (sphere_ray).dot(sphere_ray) - self.radius**2
        #c = ray.point.length()**2 + self.center.length()**2 - 2 * ray.point.dot(self.center) 
        #print((sphere_ray).dot(sphere_ray), self.radius**2)
        #print(c)
        #print(b)
        dis = ((b)**2)-(4*a*c) #räknar ut diskriminanten för att kolla antal skärningar


        #print(ray.direction)
        #print(ray.point)
        #print(dis)
        
        #felsökning:
        """
        if self.dikt.get(dis) == None:
            self.dikt[dis] = 0
            
        else:
            self.dikt[dis] += 1
        """
        """
        if dis >= 0:
            print(dis)
        """

        if dis > 0:
            if (-b + sqrt(dis))/2*a < 0 and (-b - sqrt(dis))/2*a < 0: #punkterna är bakom
                return None

            elif (-b + sqrt(dis))/2*a > 0 and (-b - sqrt(dis))/2*a > 0: #punkterna är framför, ta kortaste
                return min((-b + sqrt(dis))/2*a, (-b - sqrt(dis))/2*a)

            else:
                return max((-b + sqrt(dis))/2*a, (-b - sqrt(dis))/2*a) #en är negativ, ta den positiva

        elif dis == 0: #en skärning
            if -b/(2*a) > 0:
                return -b/(2*a)
            else:
                return None

        else: #dis < 0 #ingen skärning strålen från oänligt bort
            return None


    def normal(self, hit):
        """Tar in en punkt på sfären och returnerar normalen i punkten."""
        return (hit - self.center).norm()
        
                 
class Ray():
    """Implementerar en stråle objekt."""

    def __init__(self, rikt, punkt):
        """Skapar en stråle i input punkten och med input riktningen."""
        self.direction = rikt.norm() #normalisera riktningen
        self.point = punkt


    def hit(self, sphere): #(self, objekt)
        """Tar in en sfär som input och returnerar var ljusstrålen träffar sfären."""

        hit_pos = self.point + self.direction*sphere.intersect(self)
        
        return hit_pos



class Material():
    """Implementerar en material objekt som lagrar alla egenskaper på ett viss material"""

    
    def __init__(self, color = RGB(126, 157, 155), ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5):
        """Skapar ett material med indata som instansvariablerna."""
        self.color = color * (1/255)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection



class Light():
    def __init__(self, point=Point(), color= RGB(255, 229, 124) * (1/255)):
        """Tar in en lista med ljuspunkter och sparar dessa som instansvariabler."""
        self.point = point
        self.color = color
    

def ppm(bild_fil, bild):
    """Tar in en bild som består av en ixj matris och skapar bild_fil som en ppm-fil."""
    bild_fil.write("P3 {} {}\n255\n".format(width, height))
    
    for j in range(len(bild)):
        for i in range(len(bild[j])):
            bild_fil.write("{} {} {} ".format(round(max(0, min(bild[j][i].x*255, 255))), round(max(0, min(bild[j][i].y*255, 255))), round(max(0, min(bild[j][i].z*255, 255))))) #begränsar intervallet mellan 0 och 255
            
        bild_fil.write("\n")


def render(width, height, rum, kamera, lights):
    """Tar in, width, height, rum, kamera och lights och returnerar en bild med höjden height och bredden width och rendering av rummet sett från kamera input och med ljusen lights."""

    ratio = height/width
    x0, x1 = -1.0, 1.0
    y0, y1 = -1.0 * ratio, 1.0 * ratio
    x_step =(x1 - x0)/(width -1)
    y_step =(y1 - y0)/(height -1)
    bild = [[0 for j in range(width)] for i in range(height)]

    x, y = x0, y0

    for j in range(width):
        x = x0 + j * x_step
        for i in range(height):
            y = y0 + i * y_step
            ray = Ray(Point(x,y)-kamera, kamera)
            bild[i][j] = ray_trace(ray, rum, lights)
    print(x, y)
            
    return bild
            
    

def ray_trace(ray, rum, lights):
    """Tar in en pixel i punkten x, y och returnerar pixelns RGB värde."""
    color = RGB(0,0,0) #start färgen, svart bakgrund, kan implemntera så man ser bakgrunden istället

    #Hitta närmaste träff

    obj_hit = None
    t = None

    for i in range(len(rum)):
        t = rum[i].intersect(ray)
        #print(t)

        if t != None:
            if obj_hit == None: #Om man inte 
                obj_hit = rum[i]
                min_t = t

            if t < min_t:
                obj_hit = rum[i]
                min_t = t

    if obj_hit == None:
        return color

    #return color

    hit_pos = ray.point + ray.direction * t
    
    color += obj_hit.material.color #lägger på färgen

    return color
    
    

    

def shadow():
    """Tar in en pixel och ett område runt den och returnerar hur ljust pixeln ska vara."""
    #skapa en shadow ray från träffpunkt till ljuspunkt, varje gång man raytracer träffar något, följ shadow ray och se om startpunkten är närmast till ljuskällan(om den träffar något för första gången), annars skugga
    #kolla på pixlarna runt den om de kommer åt ljuset.


    #traca shadow ray som en vanlig ray och kolla om den hittar någt positivt värde, om inte, ljust
    


def main():
    """Integrerar alla klasser, konstanter, variabler och funktioner och returnerar en färdigbild"""
    width = 320
    height = 200
    

    kamera = Vector(0, 0, -1)
    rum = [Sphere(0.5, Vector(0,0,0), Material())]
    lights = [Light(Point(1.5, -0.5, -10.0))]
    

    bild = render(width, height, rum, kamera, lights)
 

    with open("bild2.ppm", "w") as bild_fil:
        ppm(bild_fil, bild)
    
    
    
        




width = 320
height = 200


kamera = Vector(0, 0, -1)
rum = [Sphere(0.5, Vector(0,0,0), Material())]
lights = [Light(Point(1.5, -0.5, -10.0))]


bild = render(width, height, rum, kamera, lights)


with open("bild5.ppm", "w") as bild_fil:
    ppm(bild_fil, bild)




#print(rum[0].dikt)



#Bilden
#width = 2560
#height = 1600



"""
#Unit test
v = Vector(1, 2, 3)

assert str(v) == "[1, 2, 3]" #Testar __repr__() och __init__()
assert str(v + v) ==  "[2, 4, 6]" #Testar add()
assert str(v.length()) == str(sqrt(1**2+2**2+3**2)) #Testar length()





#Testar ppm

width = 3
height = 2

bild = [[0 for j in range(width)] for i in range(height)]

bild[0][0] = RGB(1, 0, 0) #bild[i][j]
bild[0][1] = RGB(0, 1, 0)
bild[0][2] = RGB(0, 0, 1)

bild[1][0] = RGB(1, 1, 0)
bild[1][1] = RGB(1, 1, 1)
bild[1][2] = RGB(0, 0, 0)

with open("test.ppm", "w") as bild_fil:
    ppm(bild_fil, bild)

with open("test.ppm", "r") as bild_fil:
    assert bild_fil.read() == "P3 3 2\n255\n255 0 0 0 255 0 0 0 255 \n255 255 0 255 255 255 0 0 0 \n"
    



#Testar intersect och bild
width = 320
height = 200

    


#Testar hit och intersect

light = Ray(Point(1,1,0),Point(1,2,3))
boll = Sphere(1, Point(10,2,3), None)

boll.intersect(light)
light.hit(boll)



#Testa raytracern med julgranskulor och schackbräda på svart underlag



#montecarlo för vilka pixlar som ska ray tracas, resten kollar på närliggande värden
#soft shadow, kolla på när liggange shadow rays om, de når ljuset
"""
