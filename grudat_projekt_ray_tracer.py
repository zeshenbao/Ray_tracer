"""
Grudat projekt v1.0.0
Zeshen Bao


En simpel statisk raytracer

En statisk raytracer renderar en 2d bild som ögat ser genom att man simulerar
en öga som står vid en punkt och kollar på ett 3d rum med en ljuskälla som lyser på olika objekt.
Tar in en 3d scene och returnerar en bild på scenen sett från en bestämd punkt.

Den fungerar på det sättet att istället för att simulera alla ljusstrålar från en ljuskälla så
backtrackar man endast ljusstrålar som når ögat tillbaka till ljuskällan. Dvs. vi skickar ut ljusstrålar
från ögat mot ett 2d plan som kommer bli vår bild och kollar vilka objekt de träffar på och hur de reflekteras.
I 3d rummet kan vi placera ut kameran, sfärer och ljuskällor och med hjälp av raytracern rendera hur rummet ser
ut från en viss punkt där kameran står.
"""

from math import *
import time


class Vector():
    """Implementerar en 3d vektor med tre element som motsvarar koordinaterna x, y, z i rummet."""

    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Skapar en Vektor med instansvariablerna x, y, z och deras värde från input.
            positiv x är riktad åt höger, positiv y nedåt och positiv z inåt eller in mot xy planet."""
        
        self.x, self.y, self.z = x, y, z


    def __repr__(self):
        """Representerar Vektor som en sträng (klass Str) av en lista med vektorkomponenterna x, y och z som element.
           Returnerar t.ex. '[1, 2, 3]' om man skriver v = Vector(1, 2, 3), print(v)."""
        
        return str([self.x, self.y, self.z])
    

    def __add__(self, v):
        """Tar in en vektor v och returnerar vektorsumman (klass Vector) av self och v."""
        
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
    

    def __sub__(self, v):
        """Tar in en vektor v och returnerar vektordifferansen (klass Vector) mellan self och v, dvs. man tar self - v."""
        
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
    

    def __mul__(self, num):
        """Tar en ett tal num och returnerar skalär multiplikationen mellan self och num (klass Vector), observera att num ej är en vektor."""
        
        return Vector(self.x * num, self.y * num, self.z * num)

    def __rmul__(self, num):
        """Exakt som __mul__ men behövs för att definiera höger multiplikation."""
        return self*num


    def dot(self, v):
        """Tar in en vetkor v och returnerar skalärprodukten mellan self och v (klass Int)."""
        
        return self.x * v.x + self.y * v.y + self.z * v.z
    

    def length(self):
        """Returnerar längden av vektor self (klass Int)."""

        return sqrt(self.dot(self))
    

    def norm(self):
        """Returnerar den normaliserade vektor self (klass Vector)."""
        len = self.length()
        
        return Vector(self.x / len, self.y / len, self.z / len)


RGB = Vector
"""RGB klass som använder sig av vektorklassen, dvs. samma instansvariabler och metoder men med namnet RGB eller anropet RGB()."""

Point = Vector
"""Point klass som använder sig av vektorklassen med namnet Point."""




class Sphere():
    """Implementerar ett sfär objekt som motsvarar ett matematisk beskrivning av en sfär."""

    def __init__(self, radie, punkt, material):
        """Skapar en sfär med input radie (av klass Int) som radie på sfär instansen, instansens centrum i input punkten (klass Vector)
           och sfärens ljusegenskaper efter input material (klass Material).
           (self.shadow_dots och self.light_dots är privata diktionaries som lagrar punkter och implementerar soft shadows, borde ha lagt till _ framför)
        """
        
        self.radius = radie
        self.center = punkt
        self.material = material
        self.shadow_dots = {}
        self.light_dots = {}

    def intersect(self, ray):
        """Tar in en ljusstråle ray (klass Ray) som input och returnerar tiden (klass Int) det tar för strålen att träffa sfären eller self.
           Om den inte träffar sfären så returnerar intersect metoden None (typen NoneType)."""
        
        a = 1 #ray.direction.dot(ray.direction)

        sphere_ray = ray.point - self.center 

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
        """Tar in en punkt hit (klass Vektor) på sfären och returnerar normalen ut ur sfären i punkten."""
        
        return (hit - self.center).norm()
        
                 
class Ray():
    """Implementerar en ljusstråle objekt."""

    def __init__(self, rikt, punkt):
        """Skapar en stråle med sin origo self.point i input punkt (klass Vector) och riktningen self.directions från input rikt (klass Vector).
           OBS self.direction normaliseras."""
        
        self.direction = rikt.norm() #normalisera riktningen
        self.point = punkt


    def hit(self, sphere): #(self, objekt) 
        """Tar in en sfär eller Sphere objekt (klass Sphere) som input och returnerar (klass Vector) var ljusstrålen self träffar sfären.
           Returnerar None om den inte träffar något."""
        if sphere.intersect(self) == None:
            return None
        hit_pos = self.point + self.direction*sphere.intersect(self)
        
        return hit_pos

    
class Material():
    """Implementerar en material objekt som lagrar alla egenskaper på ett viss material."""
    
    def __init__(self, color = RGB(255, 0, 0), ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5): 
        """Skapar en instans till material objektet. Tar in color (klass Vector samma som RBG) i RBG format,
           styrkan på ambientljus ambient (klass Int), en diffuse parameter på material ytan diffuse (klass Int),
           en specular parameter specular (klass Int) på materialet och en parameter på reflexivitet reflection (klass Int).
           Standardvärdena på inputvärdena står inom metodparantesen. Dividerar RGB färgerna med 255 så man får ett värde mellan 0 och 1."""
        
        self.color = color * (1/255)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def get_color(self, hit_pos):
        """Tar in en position (behövs egentligen inte, tar in för att ha samma anrop som Chessboard). Retrunerar self.color, dvs färgen på material instansen."""
        
        return self.color


class Chessboard():
    """Implementerar ett liknande klass som Material, bara att den tar in två färger och annan get_color metod att se ut som en schakbräda."""
    
    def __init__(self, color1 = RGB(255, 255, 255), color2 = RGB(0, 0, 0), ambient=0.0, diffuse=1.0, specular=1.0, reflection=0.5):
        """Skapar ett Chessboard instans med indata som instansvariablerna. Precis som klassen Material men tar in två färger i RGB format (klass Vector).
           Se metoden __init__ för Material. Standardvärdena på inputvärdena står inom metodparantesen. Dividerar RGB färgerna med 255 så man får ett värde mellan 0 och 1."""

        self.color = color1
        self.color1 = color1 * (1/255)
        self.color2 = color2 * (1/255)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection


    def get_color(self, hit_pos):
        """Tar in en position (klass Vector) av t.ex. en Sphere objekt och returnerar material Chessboards färg (klass Vector) i punkten."""
        
        if int(hit_pos.x*2.5) % 2  == int(hit_pos.z*2.5) % 2: #när både rad och colonn är jämna
            return self.color1
        else:
            return self.color2

    
class Light():
    """Implementerar ljusobjektet som är ljuskällan i rummet."""
    
    def __init__(self, point=Point(), color= RGB(255, 255, 255) * (1/255)):
        """Tar in en punkt (klass Vector eller Point) och sparar den i self.point och en färg i RGB format (klass Vector eller RBG) och sparar den i self.color.
           Standardvärdena på inputvärdena står inom metodparantesen."""
        
        self.point = point
        self.color = color

    

def ppm(bild_fil, bild):
    """Tar in en bild som består av en lista av formatet [[], [], [], ...] som en ixj matris där varje element i listan är rader och
       varje element i rader är colonn elementet. Varje colonn element består av en RGB färg som klass RGB eller Vector.
       Tar också en bild_fil som är i en tom ppm format och konverterar bild listans RGB färger till ppm format. Bilden får inte vara tom."""
    
    bild_fil.write("P3 {} {}\n255\n".format(len(bild[0]), len(bild)))
   
    
    for j in range(len(bild)):
        for i in range(len(bild[j])):
            #print(len(bild), len(bild[j]))
            bild_fil.write("{} {} {} ".format(round(max(0, min(bild[j][i].x*255, 255))), round(max(0, min(bild[j][i].y*255, 255))), round(max(0, min(bild[j][i].z*255, 255))))) #begränsar intervallet mellan 0 och 255
            
        bild_fil.write("\n")


def render(width, height, rum, kamera, lights): 
    """Tar in width (klass Int) och height (klass Int) som är bredden och höjden på den färdiga bilden,  rum (klass List) med alla objekt dvs. en lista med Sphere instanser,
       kamerapunkten (klass Vector) där man vill kolla på 3d rummet igenom det förutbestämda planet med koordinaterna x0, x1, y0, y1. Tar också in lights (klass List)
       som är en lista med ljuskällor (klass Light) dvs. [Light(), Light(), ...]. Funktionen returnerar en bild lista i ixj matris formatet beskrivet i ppm() med width x height pixel
       där vi renderar 3d rummet sett från kamerapunkten. Inget av inputs får vara None och listorna måste ha någon objekt."""
    
    #Justerar bilden efter height och width.
    ratio = height/width

    #Var 2d bilden finns i 3d rummet.
    x0, x1 = -1.0, 1.0
    y0, y1 = -1.0*ratio, 1.0*ratio #Justerar efter ratio, detta eftersom x och y ska ha lika långa steg.

    x_step =(x1 - x0)/(width)
    y_step =((y1 - y0))/(height)
    bild = [[0 for j in range(width)] for i in range(height)]

    for light in lights:
        x = x0
        for el in rum:
            el.shadow_dots = {}
            el.light_dots = {}
        
        for j in range(width):
            x += x_step
            y = y0
            for i in range(height):
                y += y_step
                ray = Ray(Point(x,y)-kamera, kamera)
                if bild[i][j] == 0:
                    bild[i][j] = ray_trace(ray, rum, light, kamera, i, j, 0)
                else:
                    bild[i][j] += ray_trace(ray, rum, light, kamera, i, j, 0)
        
        #soft shadows
        for el in range(len(rum)):
            lista = list(rum[el].shadow_dots)
            
            for k in lista:
                i = int(k[0])
                j = int(k[1])
                count = 0 #Visible shadow_dots
                full = 0 #Totala shadow_dots
                area = 5 #Område av sampling 
                start_styrka = bild[i][j].length() 
                
                for n in range(i-area,i+area):
                    for m in range(j-area, j+area):
                        if rum[el].light_dots.get((str(n),str(m))) == 0:
                            count += 1
                            full +=1
                        elif rum[el].shadow_dots.get((str(n),str(m))) == 1:
                            full +=1

                bright = count/full
                bild[i][j] = bild[i][j]*bright**(1)*3 #Justerar efter sampling och justering
                        
    return bild
            
    

def ray_trace(ray, rum, light, kamera, i, j, depth):
    """En privat funktion som används i render och som tar en ray (klass Ray) och följer hur den rör sig i
       rummet med olika objekt och en ljuskälla (klass Light) och räknar ut hur den den studsar på och reflekteras.
       Tar också in olika paramerar i, j och depth från render."""
    
    color = RGB(0,0,0) #Start färgen
    k = 50 #Konstant för specular
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


    #Shadows
    shadow_ray = Ray((light.point - hit_pos).norm(), hit_pos)

    for antal in range(len(rum)): #Kollar alla objekt
            if rum[antal] != obj_hit:
                                
                block_t = rum[antal].intersect(shadow_ray)
        
                if block_t != None:
                    block_dist = shadow_ray.point + ray.direction * block_t
                    if block_dist.length() < (light.point - shadow_ray.point).length():
                        if depth == 0:
                            obj_hit.shadow_dots[str(i),str(j)] = 1
                        return color
                    
    if depth == 0:
        obj_hit.light_dots[str(i),str(j)] = 0
        
    
    normal = obj_hit.normal(hit_pos)  
    hit_cam = (kamera - hit_pos).norm()
    
    material = obj_hit.material
    
    ambient_val = material.ambient * RGB(20, 24, 82) * 0.01
    
    color += ambient_val #lägger till ambient color

    hit_light = Ray((light.point - hit_pos), hit_pos)

    #Lägger till diffustljus på ytan med lambert modellen
    color += max(0, normal.dot(hit_light.direction))*material.diffuse*material.get_color(hit_pos) * (1/(light.point - hit_pos).length()) *4 #ej för negativa värden, vinklar större än 90 grader
    
    half_vec = (hit_cam + hit_light.direction).norm() #Räknar ut half vector
    
    #Lägger till specularljus, med Blinn-phong modellen
    color +=  (max(0, normal.dot(half_vec))**k)*material.specular*light.color * (1/(light.point - hit_pos).length()) *4

    delta = 0.0001 # Konstant för reflektion

    #Rekursionen
    if depth < max_depth:
        
        reflected_ray = hit_pos + normal * delta
        reflected_dir = ray.direction - normal * (2*ray.direction.dot(normal))
        new_ray = Ray(reflected_dir, reflected_ray )
              
        color += ray_trace(new_ray, rum, light, kamera, i, j, depth+1) * material.reflection
        
    return color


def main():
    """Integrerar alla klasser, konstanter, variabler och funktioner och skapar en färdigbild med namnet bild122.ppm i directory.
       Skriver även ut hur många till det tar att köra progrmmet. Här är ett exempel på hur biblioteket används."""
    
    width = 320 #Bild bredd
    height = 200 #Bild höjd

    start_t = time.time()  

    kamera = Vector(0, -0.35, -1.0) #Kamera positionen

    #Rum med olika objekt i
    rum = [Sphere(0.6, Vector(1.25, -0.1, 1), Material(RGB(0,100,0))),
           Sphere(0.4, Vector(-0.25, -0.1, 1.5), Material()),
           Sphere(0.2, Vector(0.6, 0.1, 1.5), Material(RGB(0,0,100))),
           Sphere(0.8, Vector(-1.25, -0.6, 2), Material(RGB(0,50, 50),0, 0.5, 0.3, 0.01)),
           Sphere(10000, Vector(0, 10000.5, 1), Chessboard(RGB(255, 255, 255), RGB(0, 0, 0), 0, 1.0, 1.0, 0.2))]

    lights = [Light(Point(-2, -0.5, -2)), Light(Point(1, -1.5, -2))] #Ljuskällor
  
    bild = render(width, height, rum, kamera, lights) #Bild matrisen som skapas av render funktionen för scenen


    with open("bild122.ppm", "w") as bild_fil: #Sparar filen som bild122.ppm
        ppm(bild_fil, bild) #Konverterar bild matris till ppm format

    print(time.time()-start_t) 



#if __name__ == "__main__": main() 



#Unit test


#Testar Vector klassen
v = Vector(1, 2, 3)
u = Vector(1, -1, 0)
n = Vector(0, 0, 0)
w = Vector(3, 0, 0)

assert str(v) == "[1, 2, 3]" #Testar __repr__() och __init__()
assert str(v + v) ==  "[2, 4, 6]" #Testar __add__ (med operation overload)
assert str(v + n) == str(v)
assert str(v - u) == "[0, 3, 3]" #Testar __sub__()
assert str(2*v) == "[2, 4, 6]" #Testar __mul__()
assert str(v*2) == "[2, 4, 6]" #Testar __rmul__()
assert str(v*0) == "[0, 0, 0]"
assert v.dot(v) == 9+4+1 #Testar dot()
assert v.dot(u) == 1-2
assert n.dot(n) == 0
assert v.length() == sqrt(1**2+2**2+3**2) #Testar length()
assert n.length() == 0
assert str(w.norm()) == "[1.0, 0.0, 0.0]" #Testar norm()




#Testar RBG och Point klasserna som är samma som Vector klassen

r = RGB(1, 2, 3)
v = Vector(1, 2, 3)
p = Point(1, 2, 3)


assert str(r) == str(v)
assert str(v) == str(p)
assert str(r) == str(p)





#Testar klasserna Sphere och Ray
#Dvs intersect(), __init__() av Sphere och Ray samt normal() och hit()

#Observera att programmet har koordinatsystemet pos x är höger, pos y är ner, pos z är inåt.
boll = Sphere(1, Vector(1, -2, 0), Material())

###Kolla på test_intersect.png för en bild

#Ingen skärning
ray0 = Ray(Vector(-1, 0, 0), Vector(4, 0, 0))

assert boll.intersect(ray0) == None #Ingen skärning
assert ray0.hit(boll) == None


#En skärning
ray1 = Ray(Vector(0.000001, -1, 1), Vector(0, 0, -2)) #om x = 0 så skär den precis inte 
assert str(str(boll.intersect(ray1)))[:3] == str(sqrt(8))[:3]

#Numeriska värden är ej exakta så avrundar
assert round(ray1.hit(boll).x) == 0
assert floor(ray1.hit(boll).y) == -2
assert round(ray1.hit(boll).z) == 0


#Två skärningar
ray2 = Ray(Vector(0, -1, 0), Vector(1, 0, 0))

assert boll.intersect(ray2) == 1
assert str(ray2.hit(boll)) == "[1.0, -1.0, 0.0]"

#Kollar normalen i skärning mellan ray2 och boll
assert str(boll.normal(ray2.hit(boll))) == "[0.0, 1.0, 0.0]"





#Testar Material klassen, __init__ och get_color
m = Material(RGB(0, 123, 432))

assert str(m.get_color(Vector(1,2,3))) == "[0.0, " +str(123/255) +", " +str(432/255) +"]"





#Testar Chessboard klassen, __init__ och get_color
chess = Chessboard(RGB(0, 100, 0),RGB(0, 0, 100))

assert str(chess.get_color(Vector(1,1,0))) == "[0.0, " +str(100/255) +", " +str(0.0) +"]" #Udda rutor

assert str(chess.get_color(Vector(2,2,0))) == "[0.0, " +str(0.0) +", " +str(100/255) +"]" #Jämna rutor





#Testar Light klassen
light = Light(Point(1, 0, 1), RGB(255, 0, 0))

assert str(light.point) == "[1, 0, 1]"
assert str(light.color) == "[255, 0, 0]"





#Testar ppm funktionen

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
    assert bild_fil.read() == "P3 3 2\n255\n255 0 0 0 255 0 0 0 255 \n255 255 0 255 255 255 0 0 0 \n" #Vi ser också att pixlarna har rätt färg på screenshot bilden av ppm
    




#Alla bilder i ppm format skapade i mappen test_bilder är visuella tester av koden
#Se test.ppm och test.png för test av render()
""" Har t.ex. kollat på bilderna och kollat om skuggorna stämmer eller om objekten är på rätt plats med realistiska spcular, diffuse light. Buggar som har fixats
på detta sätt är när jag flyttade på ljusen men ljuset på den renderade bilden är på samma ställa, hade då råkat ta för många steg i ppm() funktionen i y led.

Har fixat buggar som att skuggor inte syns och implementeras på rätt sätt, att soft shadows tar med färger från närliggande objekt som den inte ska. Så omimplementerade
soft shadows genom att endast jämföra skuggade pixlar som syns och inte syns istället för att ta averge färg eller lägga på färg för varje pixel som inte är skuggad.

Vi ser också på bilden att reflektioner fungerar när vi ökar på djupet och kör ray tracing rekursivt jämfört med djup på 0 som inte har någon reflektion. Har testat även
testat diffuse, refkltion och ambient parametrar på objekten och sett hur färgerna ändras. Och mycket annat också som jag inte kommer på direkt nu.

Hoppas det räckte för manuellt visuellt test av render() och ray_trace() funktionerna.
"""






####Lista på saker som kan läggas till:

#Testa raytracern med julgranskulor och schackbräda på svart underlag
#Montecarlo för vilka pixlar som ska ray tracas, resten kollar på närliggande värden
#--Soft shadow, kolla på när liggange shadow rays om, de når ljuset-- Implementerad! 
#Skapa en ljuskällan som sfär eller plan istället för punktkälla
#Skicka ut flera rays per pixel och använd medelvärde av dessa för att minska på brus
#--Desto längre ifrån ljuset, desto svagare ljus-- Implementerad! 
#Varför behöver man shadow rays när man kan ray traca och se om ray kommer till ljuskällan inom ett viss studs till ljuspunkt+en radie, annars lägg inte till färgerna?
#Lägg till så soft shadow area justeras efter storleken på bilden, 5 för 320x200 och 30 för 2560 x 1600
#Lägg till stjärnhimel
#lägg på maxgräns på soft shadow så den inte kan bli för ljust
#Kör på pypy istället för cpython
#Lägga till transparata objekt
#Lägga till flera geometriska objekt
#Lägga till så diffuse light skickar ut flera ljusstrålar
#Gör programmet snabbare, optimering
#Testa göra en real time ray tracer


