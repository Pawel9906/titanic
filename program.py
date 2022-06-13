'''
Pierwszym zastosowanym algorytmem będzie analiza najbliższego sąsiada.
Rozpatrzymy tutaj takie cechy, jak rok urodzenia, liczba rodzeństwa/małżonka
liczba rodziców/dzieci i klasa. Tym sposobem każdemu pasażerowi
odpowiadać będzie punkt w przestrzeni 4D. Na każdej z osi możliwa wartoć
niech będzie należeć do przedziału od -10 do 10. Taki sam rozstęp na każdej z osi
sprawi, że nie powinno być sytuacji, w której jedna cecha zdecydowanie zdominuje pozostałe.

Rozważane parametry mogą przyjmować stosunkowo zróżnicowane wartosci, dlatego
metoda analizy sąsiada powinna być sensowna. Cecha płci przyjmuje tylko
2 wartosci, więc lepiej może jej nie dawać przy tym algorytmie. Cechy przyjmujące 3, 4, 5 wartości
myślę, że już można przeanalizowac.

Najpierw stworzymy klasę dot. pasażerów.
 Potem wytworzymy odpowiednią liczbę obiektów odpowiadających pasażerom,
 początkowo z pustymi wartosciami cech. Potem przydzielimy pasażerom
 odpowiednie wartosci
 '''

#przyda się math
import math

class Passenger:
    def __init__(self):
        self.sex = None
        self.survived = None
        self.pclass = None
        self.sib = None
        self.par = None
        self.embarked = None
        self.born = None
        
        #Zdefiniujmy też dwie metody, które się przydzadzą do algorytmów
        #Najpierw metoda przyporządkowywująca pasażerowi punkt w przestrzeni 4D
        
    def point(self):
        #wiek należy do przedziału od 1850, do 1912 - 
        #liczbom z tego zakresu przyporządkować trzeba liczby z zakresu od -10 do 10
        if (self.born == 1881):
            a = 0
        elif (self.born == 0): #niektórzy nie mają podanego wieku
            a = 0
        else:
            a = (self.born - 1881) / 31 * 10
            
        #wspólczynnik sib wynosi od 0 do 4
        b = -10 + self.sib * 5
        
        #współczynnik par wynosi od 0 do 5
        c = -10 + self.par * 4
        
        #są 3 klasy
        if (self.pclass == '1st'):
            d = 10
        elif (self.pclass == '2nd'):
            d = 0
        else:
            d = -10

        #i teraz możemy zwrócić krotkę ze współrzędnymi punktu w 4D
        return (a, b, c, d)            
        
#Teraz tworzymy listę wszystkich pasażerów

passengers = []

for i in range(0,891): #jest 891 pasażerów
    passengers.append(Passenger())
        
#Czas poprzydzielać pasażerom cechy. Pomoże nam w tym funkcja giveAttribute
#Najpierw jednak ułatwmy sobie przekształcanie danych tworząc funkcję int2

def int2(x):
    if (x == ''):
        return 0
    else:
        return int(x)
    
#rok urodzenia pewnych pasażerów nie jest znany i ma postać pustego ciągu ''
#a z '' funkcja int sobie nie radzi - dlatego tworzymy pomocniczo int2

#teraz czas na giveAttribute

def giveAttribute(attributeName, intNum):
    file = open(attributeName + '.txt')
    attributeValues = file.read()
    attributeValues = attributeValues.split('\n')
    if intNum:
        for i in range(0,891):
            setattr(passengers[i], attributeName, int2(attributeValues[i]))
    else: 
        for i in range(0,891):
            setattr(passengers[i], attributeName, attributeValues[i])
      
#teraz można przydzielić wszystko po kolei
giveAttribute('sex', False)
giveAttribute('survived', True) #tu int będzie lepsze niż bool, co się wyjasni w dalszej czesci
giveAttribute('pclass', False) #to się w metodzie point() zmieni w int
giveAttribute('sib', True)
giveAttribute('par', True)
giveAttribute('embarked', False)
giveAttribute('born', True)

#Stwórzmy teraz metodę, co sprawdza dystans w metryce euklidesowej między 2 różnymi punktami w 4D

def distance(x, y):
    return math.sqrt( (x[0]-y[0])**2 + (x[1]-y[1])**2 + (x[2]-y[2])**2 + (x[3]-y[3])**2     )

#Stwórzmy teraz funkcję, która, po podaniu kilku parametrów, znajdzie nam najbliższego sąsiada

def f1(born, sib, par, pclass):
    present = Passenger()
    present.born = born
    present.sib = sib
    present.par = par
    present.pclass = pclass
    
    nearestDistance = distance(present.point(), passengers[0].point())
    nearestPassenger = passengers[0]
    
    for i in range (1, 891):
        presentDistance = distance(present.point(), passengers[i].point())
        if (presentDistance < nearestDistance):
            nearestDistance = presentDistance
            nearestPassenger = passengers[i]
            
    return nearestPassenger.survived()

'''Teraz czas na drugi algorytm. Podzielimy pasażerów na 6 podzbiorów, 
według płci i klasy. Dla każdego podzbioru obliczymy, czy więcej przeżyło,
czy zginęło. Potem utworyzmy funkcję, która na podstawie danych przydzieli
człowieka do jednego z 6 podzbiorów i zwróci częstszy los w danym podzbiorze.
'''
male1 = []
male2 = []
male3 = []
female1 = []
female2 = []
female3 = []

for i in range (0, 891):
    if (passengers[i].sex == 'male'):
        if (passengers[i].pclass == '1st'):
            male1.append(passengers[i])
        elif (passengers[i].pclass == '2nd'):
            male2.append(passengers[i])
        else:
            male3.append(passengers[i])
            
    else:
        if (passengers[i].pclass == '1st'):
            female1.append(passengers[i])
        elif (passengers[i].pclass == '2nd'):
            female2.append(passengers[i])
        else:
            female3.append(passengers[i])
            
#mamy już 6 podzbiorów, opracujmy funkcję co podzbiorowi przypisze dominujący los pasażera

#tu włanie przyda się, że los jest w formacie int, nie bool

def findCommonerDestiny(l):
    sumOfDestinies = 0
    for i in range (0,len(l)):
        sumOfDestinies += l[i].survived
    
    return round(sumOfDestinies / len(l))

#Teraz funkcja, której podajemy płeć i klasę, 
#i uzyskujemy częstszy los w danej grupie pasażerów

def f2(sex, pclass):
    if (sex == 'male'):
        if (pclass == '1st'):
            return findCommonerDestiny(male1)
        elif (pclass == '2nd'):
            return findCommonerDestiny(male2)
        else:
           return findCommonerDestiny( male3)
            
    else:
        if (pclass == '1st'):
            return findCommonerDestiny(female1)
        elif (pclass == '2nd'):
            return findCommonerDestiny(female2)
        else:
            return findCommonerDestiny(female3)
    



    
            
