## Klasser

### klass Vektor
```python
class Vector():
```   
Implementerar en 3d vektor med tre element som motsvarar koordinaterna x, y, z i rummet.


#### metod __init__
```python
def __init__(self, x=0.0, y=0.0, z=0.0):
```    
Skapar en Vektor med instansvariablerna x, y, z och deras värde från input. Positiv x är riktad åt höger, positiv y nedåt och positiv z inåt eller in mot xy planet.




#### metod __repr__
```python
def __repr__(self):
```    
Representerar Vektor som en sträng (klass Str) av en lista med vektorkomponenterna x, y och z som element. Returnerar t.ex.   
'[1, 2, 3]' om man skriver v = Vector(1, 2, 3) och sedan print(v).



#### metod __add__
```python
def __add__(self, v):
```    
Tar in en vektor v och returnerar vektorsumman (klass Vector) av self och v.



#### metod __sub__
```python
def __sub__(self, v):
```    
Tar in en vektor v och returnerar vektordifferansen (klass Vector) mellan self och v, dvs. man tar self - v.



#### metod __mul__
```python
def __mul__(self, num):
```    
Tar en ett tal num och returnerar skalär multiplikationen mellan self och num (klass Vector), observera att num ej är en vektor.



#### metod __rmul__
```python
def __rmul__(self, num):
```    
Exakt som __mul__ men behövs för att definiera höger multiplikation.



#### metod dot
```python
def dot(self, v):
```    
Tar in en vetkor v och returnerar skalärprodukten mellan self och v (klass Float).



#### metod length
```python
def length(self):
```    
Returnerar längden av vektor self (klass Float).



#### metod norm
```python
def norm(self):
```    
Returnerar den normaliserade vektor self (klass Vector).




### klass Sphere
```python
class Sphere():
```    
Implementerar ett sfär objekt som motsvarar ett matematisk beskrivning av en sfär.


#### metod __init__
```python
def __init__(self, radie, punkt, material):
```   
Skapar en sfär med input radie (av klass Float) som radie på sfär instansen, instansens centrum i input punkten (klass Vector) och sfärens ljusegenskaper efter input material (klass Material). (self.shadow_dots och self.light_dots är privata diktionaries som lagrar punkter och implementerar soft shadows, borde ha lagt till _ framför)


#### metod intersect
```python
def intersect(self, ray):
```   
Tar in en ljusstråle ray (klass Ray) som input och returnerar tiden (klass Float) det tar för strålen att träffa sfären eller self. Om den inte träffar sfären så returnerar intersect metoden None (typen NoneType).



####  metod normal
```python
def normal(self, hit):
```
Tar in en punkt hit (klass Vektor) på sfären och returnerar normalen ut ur sfären i punkten.



### klass Ray
```python
class Ray():
```
Implementerar en ljusstråle objekt.



#### metod __init__
```python
def __init__(self, rikt, punkt):
 ```
 Skapar en stråle med sin origo self.point i input punkt (klass Vector) och riktningen self.directions från input rikt (klass Vector). OBS self.direction normaliseras.

 #### metod hit
```python
def hit(self, sphere):
```
Tar in en sfär eller Sphere objekt (klass Sphere) som input och returnerar (klass Vector) var ljusstrålen self träffar sfären. Returnerar None om den inte träffar något.



### klass Material
```python
class Material():
```
Implementerar en material objekt som lagrar alla egenskaper på ett viss material.


#### metod __init__
```python
def __init__(self, color = RGB(255, 0, 0), ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5):
```
Skapar en instans till material objektet. Tar in color (klass Vector samma som RBG) i RBG format, styrkan på ambientljus ambient (klass Float), en diffuse parameter på material ytan diffuse (klass Float), en specular parameter specular (klass Float) på materialet och en parameter på reflexivitet reflection (klass Float). Standardvärdena på inputvärdena står inom metodparantesen. Dividerar RGB färgerna med 255 så man får ett värde mellan 0 och 1.

#### metod get_color
```python
def get_color(self, hit_pos):
```
Tar in en position (behövs egentligen inte, tar in för att ha samma anrop som Chessboard). Retrunerar self.color, dvs färgen på material instansen.


### klass Chessboard
```python
class Chessboard():
```
Implementerar ett liknande klass som Material, bara att den tar in två färger och annan get_color metod att se ut som en schakbräda.

### metod __init__
```python
def __init__(self, color1 = RGB(255, 255, 255), color2 = RGB(0, 0, 0), ambient=0.0, diffuse=1.0, specular=1.0, reflection=0.5):
```
Skapar ett Chessboard instans med indata som instansvariablerna. Precis som klassen Material men tar in två färger i RGB format (klass Vector). Se metoden __init__ för Material. Standardvärdena på inputvärdena står inom metodparantesen. Dividerar RGB färgerna med 255 så man får ett värde mellan 0 och 1.

#### metod get_color
```python
def get_color(self, hit_pos):
```
Tar in en position (klass Vector) av t.ex. en Sphere objekt och returnerar material Chessboards färg (klass Vector) i punkten.


### klass Light
```python
class Light():
```
Implementerar ljusobjektet som är ljuskällan i rummet.

### metod __init__
```python
def __init__(self, point=Point(), color= RGB(255, 255, 255) * (1/255)):
```
Tar in en punkt (klass Vector eller Point) och sparar den i self.point och en färg i RGB format (klass Vector eller RBG) och sparar den i self.color. Standardvärdena på inputvärdena står inom metodparantesen.




## Funktioner

### func ppm
```python
def ppm(bild_fil, bild):
```
Tar in en bild som består av en lista av formatet [[], [], [], ...] som en ixj matris där varje element i listan är rader och
       varje element i rader är colonn elementet. Varje colonn element består av en RGB färg som klass RGB eller Vector.
       Tar också en bild_fil som är i en tom ppm format och konverterar bild listans RGB färger till ppm format. Bilden får inte vara tom.



### func render
```python
def render(width, height, rum, kamera, lights):
```
Tar in width (klass Float) och height (klass Float) som är bredden och höjden på den färdiga bilden,  rum (klass List) med alla objekt dvs. en lista med Sphere instanser, kamerapunkten (klass Vector) där man vill kolla på 3d rummet igenom det förutbestämda planet med koordinaterna x0, x1, y0, y1. Tar också in lights (klass List) som är en lista med ljuskällor (klass Light) dvs. [Light(), Light(), ...]. Funktionen returnerar en bild lista i ixj matris formatet beskrivet i ppm() med width x height pixel där vi renderar 3d rummet sett från kamerapunkten. Inget av inputs får vara None och listorna måste ha någon objekt.


### func ray_trace
```python
def ray_trace(ray, rum, light, kamera, i, j, depth):
```
En privat funktion som används i render och som tar en ray (klass Ray) och följer hur den rör sig i rummet med olika objekt och en ljuskälla (klass Light) och räknar ut hur den den studsar på och reflekteras.


### func main
```python
def main():
```
Integrerar alla klasser, konstanter, variabler och funktioner och skapar en färdigbild med namnet bild122.ppm i directory.Skriver även ut hur många till det tar att köra progrmmet. I main finns ett exempel på hur biblioteket används.
