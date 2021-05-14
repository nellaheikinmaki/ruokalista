import csv
import json
    
def lueRuokalista():
    tiedosto = open("csv/ruokalista.csv", "r")
    ruokalista = csv.DictReader(tiedosto, delimiter=",")
    lista = []
    for row in ruokalista:
        lista.append(row)
    return lista

def lueReseptit():
    with open("reseptit.json", "r") as tiedosto:
        reseptit = json.load(tiedosto)
        return reseptit

def kysyViikko(ruokalista):
    viikko = input("Minkä viikon ostoslistan haluat luoda? --> ")
    for row in ruokalista:
        if viikko == row["Vko"]:
            return viikko
    return kysyViikko(ruokalista)


def teeOstoslista(ruokalista, reseptit, viikko, ostoslista):
    ostoslista = ostoslista + "Vko " + viikko + "\n"
    for row in ruokalista:
        kysyseuraava = True
        if row["Vko"] == viikko:
            ruuat = list(row.values())[1:]
            ruokienmaara = {}
            for ruoka in ruuat:
                if ruoka == "":
                    continue
                if not ruoka in ruokienmaara.keys():
                    ruokienmaara[ruoka] = 0
                ruokienmaara[ruoka] = ruokienmaara[ruoka]+1
            for ruoka in ruuat:
                if ruoka == "":
                    continue
                if ruokienmaara[ruoka] == 2:
                    ruokienmaara[ruoka] = 0.5
                if ruokienmaara[ruoka] == 3:
                    ruokienmaara[ruoka] = 1
            ostoslista = mitaTarvitaan(reseptit, ruokienmaara, ostoslista)
            ostoslista = lisaaMuut(ostoslista)
            return ostoslista

def mitaTarvitaan(reseptit, ruokienmaara, ostoslista):
    for ruoka in ruokienmaara:
        ostoslista = ostoslista + ruoka + "\n"
        for resepti in reseptit:
            try:   
                if resepti["Ruoka"] == ruoka:
                    if resepti["Raaka-aineet"] == "":
                        break
                    pisin = 0
                    for row in resepti["Raaka-aineet"]:
                        if pisin < len(row["ainesosa"]):
                            pisin = len(row["ainesosa"])
                    pisin = pisin +2
                    for row in resepti["Raaka-aineet"]:
                        todellinen = float(row["maara"]) * ruokienmaara[ruoka]
                        vali = pisin - len(row["ainesosa"])
                        ostoslista = ostoslista + "    - " + row["ainesosa"] + vali*" " + str(todellinen) + row["yksikko"] + "\n"           
            except KeyError:
                ostoslista = ostoslista + "    - Raaka-aineet puuttuu" + "\n"
    return ostoslista
            
def lisaaMuut(ostoslista):
    muut = []
    kysyLisaa = True
    while kysyLisaa:
        muut.append(input("Lisää ostoslistalle muuta --> "))
        if input("Lisätäänkö muuta? (e = ei) --> ") == "e":
            break
    ostoslista = ostoslista + "Muut" + "\n"
    for row in muut:
        ostoslista = ostoslista + "    - " + row + "\n"
    return ostoslista

def tallennaOstoslista(ostoslista, viikko):
    with open("ostoslista" + viikko + ".txt", "w") as ostokset:
        ostokset.write(ostoslista)
            

def main():
    ostoslista = ""
    ruokalista = lueRuokalista()
    reseptit = lueReseptit()
    viikko = kysyViikko(ruokalista)
    ostoslista = teeOstoslista(ruokalista, reseptit, viikko, ostoslista)
    tallennaOstoslista(ostoslista, viikko)

main()