import heapq
import time

class Uzol:
    def __init__(self, mapa, pred, g):              #konstruktor na objekt uzol
        self.mapa = mapa                            #v uzle si pamatam mapu, index predchadzajuceho prvku v poli sprac, dlzku uz prejdenej cesty a hodnotu f (predchadzajuca cesta + heuristickou funkcou vypocitana priblizna dlzka dalsej cesty) 
        self.pred = pred                                                #mapa predstavuje n-hlavolam
        self.g = g
        self.f = self.hodnotaF()              #hned pri definovani objektu sa vyrata hodnota F = (g+h)

    def __lt__(self, other):                        #pri vkladani do min haldy sa vklada podla hodnoty F
        return self.f < other.f

    def generovaniePotomkov(self):                  #generovanie potomkov z aktualneho objektu
        x,y = self.hladanieCisla(0)                 #najskor vyhladam medzeru v mapke, potom zacnem presuvat prvky cim generujem potomkov
                                                    #3 verzie kontroly predkov
        suradnice = []
        suradnice.append([x+1, y])
        suradnice.append([x-1, y])                  #suradnice prvkov ktore idem prehadzovat
        suradnice.append([x, y+1])
        suradnice.append([x, y-1])

        for i in suradnice:
            potomok = self.presuvanie(x, y, i[0], i[1])         #presuvanie a nasledne si vyberiem 1 z kontrol
            self.kontrolaPredkov1(potomok)
            #self.kontrolaPredkov2(potomok)
            #self.kontrolaPredkov3(potomok)

    def kontrolaPredkov1(self, potomok):                                                    #1.funkcia kontroly - prechadzajuci nebol rovnaky
        if (potomok is not None) and (self.pred < 0 or potomok != sprac[self.pred].mapa):   #kontrola ci potomok a predchadzajuci existuju a ci nebol predchadzajuci rovnaky ako potomok
            heapq.heappush(vygen, Uzol(potomok, len(sprac), self.g + 1))                    


    def kontrolaPredkov2(self, potomok):                                                    #2.funkcia na kontrolu predkov - vsetky predchadzajuce neboli rovnake
        if potomok is not None:                                                             #pokial potomok neexistuje skonci funkcia bez pridania do heapu
            if self.pred < 0:
                heapq.heappush(vygen, Uzol(potomok, len(sprac), self.g + 1))                #pokial predok neexistuje, pridam uzol do heapu
            else:    
                act = sprac[self.pred]                                                      #ak predok existuje kontrolujem v cykle, ci sa potomok nerovna predkovi
                while True:
                    if potomok == act.mapa:                                                 #ak sa rovna skoncim cyklus bez pridania do heapu
                        break
                    else:
                        if act.pred > 0 and sprac[act.pred].pred >= 0:                      #ak sa nerovna kontrolujem ci existuje predok (staci mi kontrolovat kazdy druhy lebo na rovnake miesto sa dostaneme len parnym poctom tahov) 
                            act = sprac[sprac[act.pred].pred]
                        else:        
                            heapq.heappush(vygen, Uzol(potomok, len(sprac), self.g + 1))    #ak neexistuje cyklus konci a pridam uzol do haldy, kedze som nenasiel rovnakeho predka
                            break


    def kontrolaPredkov3(self, potomok):                                                    #3.funkcia na kontrolu predkov - vsetky uzly neboli rovnake
        jetam = False                                                                       
        if potomok is not None:                                                             #kontrola ci v spracovanych sa nenachadza duplikat
            for uzol in sprac:
                if uzol.mapa == potomok:
                    jetam = True
                    break
            if not jetam:
                for uzol in vygen:                                                          #kontrola ci vo vygenerovanych sa nenachadza duplikat
                    if uzol.mapa == potomok:
                        jetam = True
                        break
                if not jetam:                                                               #ak ani v jednej nie je duplikat vlozenie do haldy
                    heapq.heappush(vygen, Uzol(potomok, len(sprac), self.g + 1))
                    
            
    def presuvanie(self, x, y, a, b):                   #presuvanie prvkov na volne miesto
        if a >= vyska or b >= sirka or a < 0 or b < 0:  #pokial prvok, ktory sa ma presuvat neexistuje, funkcia vrati nic 
            return None
        
        nova = []                                       #inak nakopirujem aktualnu mapu
        for i in range(vyska):                          ###vo vsetkych cykloch pouzivam globalne premenne vyska a sirka
            pole = []                                   ###pretoze je to rychlejsie ako len(mapa), len(mapa[i]), ktore musia zakazdym merat dlzku pola
            for j in range(sirka):                      ###a bolo by zbytocne si ich pamatat v objekte
                pole.append(self.mapa[i][j])            
            nova.append(pole)

        nova[x][y] = self.mapa[a][b]                    #zmenim indexy medzery a prvku ktory posuvam
        nova[a][b] = self.mapa[x][y]
    
        return nova                                     #funkcia vrati novu mapu

    def hladanieCisla(self, z):                         #hladanie znaku v mape 
        for i in range(vyska):
            for j in range(sirka):
                if (self.mapa[i][j] == z):              #ak najdem zadany znak vratim jeho suradnice v mape
                    return i,j

    def hodnotaF(self):                                 #vypocet hodnoty F - mam 2 verzie heuristickej funkcie 
        suc = 0  

        """
        for i in range(vyska):                                        #prva kontroluje pocet nespravne umiestnenych znakov v mape (aktualny stav oproti koncovemu)
            for j in range(sirka):
                if self.mapa[i][j] != koniec[i][j] and koniec[i][j] != 0:       #neratam medzeru
                    suc += 1
        """
            
        for i in range(vyska):                                  #druha kontroluje vzdialenost znakov od miesta, kam sa potrebuju dosta 
            for j in range(sirka):                      
                if koniec[i][j] != 0:                           #opat neratam medzeru (keby ju ratam, heuristicka funkcia by nebola dobra, mohla by udavat vyssi pocet ako je skutocny)
                    x,y = self.hladanieCisla(koniec[i][j])      #pri kazdom znaku v koncovom stave, skontrolujem o kolko je posunuty od aktualneho
                    suc += abs(i-x) + abs(j-y)
        
        
        return self.g + suc                                     #hodnota f = g + h
        

def kresli(akt):                                                #funkcia na zaverecne nakreslenie postupnosti krokov
    while True:
        for i in range(vyska):
            for j in range(sirka):
                print(akt.mapa[i][j], end = ' ')
            print()
        print("Hodnota g = ", akt.g, "hodnota f = ", akt.f, "hodnota h = ", akt.f - akt.g)      #pre kazdy uzol vypisujem aj hodnoty, ktore mozu byt pre cloveka 
        print()
        
        if akt.pred >= 0:
            akt = sprac[akt.pred]
        else:
            break
    


start = []
koniec = []
"""
start.append([0, 1, 2, 3])
start.append([4, 5, 6, 7])
start.append([8, 9, 'A', 'B'])

koniec.append([0, 2, 7, 6])
koniec.append([1, 9, 4, 3])
koniec.append(['A', 8, 5, 'B'])


start.append([0, 1, 2])                    #priklady zaciatocnych a koncovych stavov
start.append([3, 4, 5])
start.append([6, 7, 8])

koniec.append([8, 0, 6])
koniec.append([5, 4, 7])
koniec.append([2, 3, 1])


start.append([0,1, 2, 3, 4])
start.append([5, 6, 7, 8, 9])

koniec.append([5, 1, 9, 8, 7])
koniec.append([2, 4, 0, 3, 6])
"""

with open('hlavolam.txt', 'r') as f:
    i, j = [int(x) for x in next(f).split()]
    for line in f:
        if i > 0:
            start.append([int(x) for x in line.split()])
        elif i < 0:
            koniec.append([int(x) for x in line.split()])
        i -= 1

vyska = len(start)                          #definovanie premennych vyska a sirka mapy 
sirka = len(start[0])


#zaciatok programu
akt = Uzol(start, -1, 0)                    #prvy uzol - pociatocna pozicia je startovna, predok neexistuje preto -1, a dlzka uz prejdenej cesty 0

sprac = []                                  #definovanie pola spracovanych prvkov a heapu vygenerovanych
vygen = []
heapq.heapify(vygen)

heapq.heappush(vygen, akt)

riesenie = False
tic = time.perf_counter()                   #meranie casu kvoli zdokumentovaniu efektivnosti jednotlivych heuristik / kontrol predkov

while True:                                 #hlavny cyklus programu
        if akt.mapa == koniec:              #pokial sa aktualny uzol rovna cielovemu koncim cyklus s najdenym riesenim
            riesenie = True
            print("Nasiel som riesenie")    
            break

        akt.generovaniePotomkov()           #inak generujem potomkov aktualneho uzla
        sprac.append(akt)                   #aktualny uzol zaradim na koniec uz spracovanych

        if len(vygen) == 0:
            break
        akt = heapq.heappop(vygen)          #vyberiem prvok s najmensou hodnotou f a pokracujem v cykle

toc = time.perf_counter()

if (riesenie):
    kresli(akt)

print(f"Trvanie: {toc -tic:0.4f}")    
print("spracovane = ", len(sprac))          #pocet vygenerovanych a spracovanych uzlov pouzivam pre zdokumentovanie pamatovej efektivnosti jednotlivych verzii heurstik / kontrol
print("vygenerovane = ", len(vygen))
input()
