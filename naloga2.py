import json
from math import log2
from collections import Counter
import heapq

    
def main():
    podatki = {
        "ime": "Kolesarjenje",
        "znacilke": {
            "Nebo": ["j", "j", "j", "j", "j", "j", "o", "o", "o", "o"],
            "Temp": ["h", "h", "t", "h", "h", "t", "t", "t", "t", "t"],
            "Veter": ["v", "v", "v", "m", "m", "m", "v", "v", "m", "m"]
        },
        "razredi": {
            "Kolo": ["d", "n", "d", "d", "d", "d", "n", "n", "d", "n"]
        }
    }

    koraki = 1  # defined outside the dict

    znacilke = podatki["znacilke"]
    razredi = podatki["razredi"]["Kolo"]

    naloga2(znacilke, razredi, koraki)

def H(verjetnosti: list):
    ent = 0
    for item in verjetnosti:
        ent -= item * log2(item)
    
    return ent

                                        
def tocnost(t, locilke_list, locilke_dict, nivo, koraki, stVseh):
    if not t: # ce nobena pot ne vodi sem je verjetnost 0 in tudi ta clen entropije je 0
        return 0
    
    if nivo == koraki:
        # mora vrnit clen za izracun entropije(verjetnost*entropija ...)
        # da se potem sestavi v vecji rezultat
        return
    
    attr = locilke_list[nivo]
    opcije = locilke_dict[attr]
    # print(attr)
    # print(opcije)
    # print(t)
    dd = {}
    for i in opcije:
        dd[i] = []

    for i in range(len(t)):
        o = t[i][attr]
        dd[o].append(t[i])
    
    for key, seznam in dd.items():
        tocnost(seznam, locilke_list, locilke_dict, nivo+1, koraki, stVseh)

        
            

def naloga2(znacilke: dict, razredi: list, koraki: int) -> tuple:

    razredi_set = set(razredi)
    
    minHeap = []
    stVseh = len(razredi)
    d = {} # atribut(str): opcija(str): razred(str): stPojavitev(int)  
    
    for atribut, seznam in znacilke.items():
        d[atribut] = {}
        opcije = set(seznam)
        terke = []
        i = 0
        for item in seznam:
            t = (item, razredi[i])
            terke.append(t)
            i += 1
        
        countTerke = Counter(terke)

        # init drevesa ker morda bo kje nicna vrednost ...
        for item in opcije:
            d[atribut][item] = {}
            for r in razredi_set:
                d[atribut][item][r] = 0
        
        for terka, vrednost in countTerke.items():
            d[atribut][terka[0]][terka[1]] = vrednost
            
        # zdej treba izracunat POGOJNE entropije in jih po vrsti od min do max razvrstit
        
        prehodna_ent = 0.0
        for item in opcije:
            veja_count = 0
            verjetnosti = []
            
            for r in razredi_set:
                veja_count += d[atribut][item][r]

            for r in razredi_set:
                verjetnosti.append(d[atribut][item][r] / veja_count)
                
            clen = (veja_count / stVseh) * H(verjetnosti)
            prehodna_ent += clen
        
        heapq.heappush(minHeap, (prehodna_ent, atribut) ) # v min heap, da so po vrsti od najmanjse nedol. do najvecje
    # print(d)

#######################################################################################################
    # 2. del algoritma, kjer dejansko simuliramo
    # treba je zgradit drevo (st nivojev dano) po vrsti po narascajocih entropijah
    vsiStolpci = []
    for i in range(len(razredi)):
        dd = {}
        for atribut, seznam in znacilke.items():
            dd[atribut] = seznam[i]
        dd["Razred"] = razredi[i]
        vsiStolpci.append(dd)

    # zdej mam list dictov - vsak stolpec tabele atributov in razredov
    # ideja je da jih bom razporedil v koshe da ne bom vsakic rabu it cez celo tabelo ... 
    tt = heapq.nsmallest(koraki, minHeap)
    locilke_dict = {}
    locilke_list = []
    for item in tt:
        l = item[1]
        locilke_list.append(l)
        locilke_dict[l] = list(d[l].keys())
    # locilke so po vrsti kot morajo bit zaradi heapa

    rez = tocnost(vsiStolpci, locilke_list, locilke_dict, 0, koraki, stVseh)           
    # mora bit tuple (entropija, tocnost)
    return rez

#delete at the end
if __name__ == "__main__":
    main()