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
"""Koordinaterna x, y, z är riktade åt höger, ner och fram"""



class Sphere():
    """Implementerar en sfär objekt"""

    def __init__(self, radie, punkt, material):
        """Skapar en sfär med input radie som radie och sin centrum i input punkten och ljusegenskaper efter input material."""
        
        self.radius = radie
        self.center = punkt
        self.material = material
        self.shadow_dots = {}
        self.light_dots = {}


    def intersect(self, ray):
        """Tar in en ljusstråle som input och returnerar tiden det tar för strålen att träffa sfären"""
        a = 1 #ray.direction.dot(ray.direction)
        
        sphere_ray = ray.point - self.center # varför sphere to ray om inte omvänt?

        b = 2*ray.direction.dot(sphere_ray)
        
        c = (sphere_ray).dot(sphere_ray) - self.radius**2
       
        dis = (b)**2-(4*a*c) #räknar ut diskriminanten för att kolla antal skärningar


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

    
    def __init__(self, color = RGB(255, 0, 0), ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5): #126, 157, 155
        """Skapar ett material med indata som instansvariablerna."""
        self.color = color * (1/255)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection


    def get_color(self, hit_pos):
        return self.color



class Chessboard():
    def __init__(self, color1 = RGB(255, 255, 255), color2 = RGB(0, 0, 0), ambient=0.0, diffuse=1.0, specular=1.0, reflection=0.5): #126, 157, 155
        """Skapar ett material med indata som instansvariablerna."""
        self.color = color1
        self.color1 = color1 * (1/255)
        self.color2 = color2 * (1/255)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection


    def get_color(self, hit_pos):
        if int(hit_pos.x*2.5) % 2  == int(hit_pos.z*2.5) % 2: #när både rad och colonn är jämna
            #print(hit_pos.x,hit_pos.z)
            return self.color1

        else:
            return self.color2

        


class Light(): 
    def __init__(self, point=Point(), color= RGB(255, 255, 255) * (1/255)): #255, 229, 124
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


def render(width, height, rum, kamera, lights): #skicka ut fler strålar per pixel och kör average
    """Tar in, width, height, rum, kamera och lights och returnerar en bild med höjden height och bredden width och rendering av rummet sett från kamera input och med ljusen lights."""



    #justerar bilden efter height och width
    ratio = height/width

    #Var 2d bilden finns i 3d rummet
    x0, x1 = -1.0, 1.0
    y0, y1 = -1.0*ratio, 1.0*ratio #justerar efter ratio, detta eftersom x och y ska ha lika långa steg


    x_step =(x1 - x0)/(width)
    y_step =((y1 - y0))/(height)
    #print(x_step, y_step)
    bild = [[0 for j in range(width)] for i in range(height)]


    for light in lights:
        x = x0
        for el in rum:
            el.shadow_dots = {}
            el.light_dots = {}
        
        for j in range(width):
            x += x_step
            y = y0
            #print(j/width)
            for i in range(height):
                y += y_step
                ray = Ray(Point(x,y)-kamera, kamera)
                if bild[i][j] == 0:
                    bild[i][j] = ray_trace(ray, rum, light, kamera, i, j, 0)
                else:
                    bild[i][j] += ray_trace(ray, rum, light, kamera, i, j, 0)
        
        #soft shadows
        """
        for el in range(len(rum)):
            lista = list(rum[el].shadow_dots)

            for k in lista:
                i = int(k[0])
                j = int(k[1])
                count = 0
                area = 4
                start_styrka = bild[i][j].length()

                for n in range(i-area,i+area):
                    for m in range(j-area, j+area):
                        if rum[el].light_dots.get((str(n),str(m))) == 0:
                            count += 1

                for n in range(i-area,i+area):
                    for m in range(j-area, j+area):
                        if rum[el].light_dots.get((str(n),str(m))) == 0:
                            if bild[n][m].length() != 0:
                                if start_styrka != 0:
                
                                    if bild[i][j].length()/start_styrka < 1.1:
                                        bild[i][j] += bild[n][m] * (1/(bild[n][m].length())**(0.75)) * 0.5 *(1/(count)**(0.4)) # count justerar förhållande mellan shadow_dots/totala_dots, length justerar efter max styrkan
                                else:
                                    bild[i][j] += bild[n][m] * (1/(bild[n][m].length())**(0.75)) * 0.5 *(1/(count)**(0.4))
                #print(x,y) 
        """

        """
        #problemet med att man adderar en konstant värde för varje punkt som inte är skuggad är att det kan bli ljusare än ej skuggade punkter samt att skuggade punkter kan också vara ljusa
        #lägg på en maxvärde på skuggan som får max av ursprungliga värdet
        for el in range(len(rum)):
            lista = list(rum[el].shadow_dots)

            for k in lista:
                i = int(k[0])
                j = int(k[1])
                count = 0
                area = 5
                start_styrka = bild[i][j].length()

                for n in range(i-area,i+area):
                    for m in range(j-area, j+area):
                        if rum[el].light_dots.get((str(n),str(m))) == 0:
                            count += 1

                for n in range(i-area,i+area):
                    for m in range(j-area, j+area):
                        if rum[el].light_dots.get((str(n),str(m))) == 0:
                            if bild[n][m].length() != 0:
                                if start_styrka != 0:
                
                                    if bild[i][j].length()/start_styrka < 1.4:
                                        #print("1")
                                        bild[i][j] += bild[n][m] * (1/(bild[n][m].length())**(0.75)) * 0.08 *(1/(count)**(0.4)) # count justerar förhållande mellan shadow_dots/totala_dots, length justerar efter max styrkan
                                else:
                                    #print("2")
                                    bild[i][j] += bild[n][m] * (1/(bild[n][m].length())**(0.75)) * 0.008 *(1/(count)**(0.4))
                                    #bild[i][j] = RGB(0,0,0)
                #print(x,y)
        
        """

        
        
        #problemet med average är om man har ljusa pixlar nära och skuggan blir för ljust
        for el in range(len(rum)):
            lista = list(rum[el].shadow_dots)
            to = 0
            for k in lista:
                to+=1
                if to % 1:
                    print(to/len(lista))
                #print(k)
                i = int(k[0])
                j = int(k[1])
                count = 0
                full = 0
                area = 10
                start_styrka = bild[i][j].length()
                


                for n in range(i-area,i+area):
                    for m in range(j-area, j+area):
                        if rum[el].light_dots.get((str(n),str(m))) == 0:
                            count += 1
                            full +=1
                        elif rum[el].shadow_dots.get((str(n),str(m))) == 1:
                            full +=1


                bright = count/full

                bild[i][j] = bild[i][j]*bright**(1.2)*2
                      
                            
                #print(x,y) 
        
        
    return bild
            
    

def ray_trace(ray, rum, light, kamera, i, j, depth):
    """Tar in en pixel i punkten x, y och returnerar pixelns RGB värde."""
    color = RGB(0,0,0) #start färgen, svart bakgrund, kan implemntera så man ser bakgrunden istället
    k = 50 #För specular
    max_depth = 5

    #Hitta närmaste träff

    obj_hit = None
    t = None

    for antal in range(len(rum)): #hittar närmaste objektet
        t = rum[antal].intersect(ray)
        #print(t)

        if t != None:
            if obj_hit == None: #Om man inte har träffat något med strålen än
                obj_hit = rum[antal]
                min_t = t

            if t < min_t:
                obj_hit = rum[antal]
                min_t = t

    if obj_hit == None:
        return color

    hit_pos = ray.point + ray.direction * min_t


    #checka om hit_pos är skuggad
    #skapa en shadow ray från träffpunkt till ljuspunkt, varje gång man raytracer träffar något, följ shadow ray och se om startpunkten är närmast till ljuskällan(om den träffar något för första gången), annars skugga
    #kolla på pixlarna runt den om de kommer åt ljuset.


    #traca shadow ray som en vanlig ray och kolla om den hittar något positivt värde, om inte, ljust

    #print((light.point - hit_pos).norm())

    
    shadow_ray = Ray((light.point - hit_pos).norm(), hit_pos) # multiplicerar med 1.0001 för att skilja från sig själv

    for antal in range(len(rum)):
            if rum[antal] != obj_hit:
                                
                block_t = rum[antal].intersect(shadow_ray)
        
                if block_t != None:
                    block_dist = shadow_ray.point + ray.direction * block_t
                    if block_dist.length() < (light.point - shadow_ray.point).length():
                        if depth == 0:
                            obj_hit.shadow_dots[str(i),str(j)] = 1
                        return color#RGB(0.1,0.1,0.1)
        
    ###
    if depth == 0:
        obj_hit.light_dots[str(i),str(j)] = 0
    
    normal = obj_hit.normal(hit_pos)
    hit_cam = (kamera - hit_pos).norm()
    
    material = obj_hit.material
    
    #ambient_val = material.ambient * RGB(20, 24, 82) * 0.01
    ambient_val = material.ambient * material.color
    
    color += ambient_val #lägger till ambient color


   

    #print(light)
    hit_light = Ray((light.point - hit_pos), hit_pos)

    #Lägger till diffustljus på ytan med lambert modellen
    color += max(0, normal.dot(hit_light.direction))*material.diffuse*material.get_color(hit_pos) * (1/(light.point - hit_pos).length()) *4 #ej för negativa värden, vinklar större än 90 grader
    
    half_vec = (hit_cam + hit_light.direction).norm()
    #Lägger till specularljus, med Blinn-phong modellen
    color +=  (max(0, normal.dot(half_vec))**k)*material.specular*light.color * (1/(light.point - hit_pos).length()) *4

    delta = 0.0001 # konstant för reflektion


    #Rekursionen
    
    if depth < max_depth:
        
        reflected_ray = hit_pos + normal * delta
        reflected_dir = ray.direction - normal * (2*ray.direction.dot(normal))
        new_ray = Ray(reflected_dir, reflected_ray )

              
        color += ray_trace(new_ray, rum, light, kamera, i, j, depth+1) * material.reflection
    
    
    
    return color


    
    
def main():
    """Integrerar alla klasser, konstanter, variabler och funktioner och returnerar en färdigbild"""
    width = 320
    height = 200
    

    kamera = Vector(0, 0, -1)
    rum = [Sphere(0.6, Vector(0,0,0), Material()), Sphere(0.4, Vector(0,1,0), Material(RGB(0,100,0)))]
    #lights = [Light(Point(0, 100, 0)), Light(Point(2, 10, 0)), Light(Point(-2, 10, 0))]
    

    bild = render(width, height, rum, kamera, lights)
 

    with open("bild19.ppm", "w") as bild_fil:
        ppm(bild_fil, bild)
    
    
    


width = 2560
height = 1600


kamera = Vector(0, -0.35, -1.0)
#rum = [Sphere(0.5, Vector(0.2,0,0), Material())]
rum = [Sphere(0.6, Vector(1.25, -0.1, 1), Material(RGB(0,100,0))),
       Sphere(0.4, Vector(-0.25, -0.1, 1.5), Material()),
       Sphere(0.2, Vector(0.6, 0.1, 1.5), Material(RGB(0,0,100))),
       Sphere(0.8, Vector(-1.25, -0.6, 2), Material(RGB(0,50, 50),0, 0.5, 0.3, 0.01)),
       Sphere(10000, Vector(0, 10000.5, 1), Chessboard(RGB(255, 255, 255), RGB(0, 0, 0), 0, 1.0, 1.0, 0.2))]

lights = [Light(Point(-2, -0.5, -2)), Light(Point(1, -1.5, -2))]
#lights = [Light(Point(0, 10, 0)), Light(Point(2, 10, 0)), Light(Point(-2, 10, 0))]
#lights = [Light(Point(-2, -0.5, -2))]

bild = render(width, height, rum, kamera, lights)


with open("bild111.ppm", "w") as bild_fil:
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
#skapa en ljuskällan som sfär eller plan istället för punktkälla
#skicka ut flera rays per pixel och använd medelvärde av dessa för att minska på brus
#desto längre ifrån ljuset, desto svagare ljus
#minska på avståndet mellan hit och light
#varför behöver man shadow rays när man kan ray traca och se om ray kommer till ljuskällan inom ett viss studs till ljuspunkt+en radie, annars lägg inte till färgerna


"""
