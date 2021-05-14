import csv
import json

ruokalista = None
    
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


def teeOstoslista(ruokalista, reseptit, viikko):
    print("Vko", viikko)
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
            mitaTarvitaan(reseptit, ruokienmaara)
            print(ruokienmaara)

def mitaTarvitaan(reseptit, ruokienmaara):
    for ruoka in ruokienmaara:
        print(ruoka)
        for resepti in reseptit:
            try:   
                if resepti["Ruoka"] == ruoka:
                    if resepti["Raaka-aineet"] == "":
                        break
                    for row in resepti["Raaka-aineet"]:
                        todellinen = float(row["maara"]) * ruokienmaara[ruoka]
                        print("    - ", row["ainesosa"], todellinen, row["yksikko"])
                    #print(resepti["Raaka-aineet"])
            except KeyError:
                print("Raaka-aineet puuttuu")
            

def main():
    ruokalista = lueRuokalista()
    reseptit = lueReseptit()
    viikko = kysyViikko(ruokalista)
    teeOstoslista(ruokalista, reseptit, viikko)

if __name__ == "__main__":
    main()