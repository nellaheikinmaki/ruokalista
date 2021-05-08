import csv
import json

ruuat = None
    
def lueruuat():
    tiedosto = open("csv/ruuat.csv", "r")
    ruuat = csv.DictReader(tiedosto, delimiter=",")
    ruuatlista = []
    for row in ruuat:
        ruuatlista.append(row)
    return ruuatlista

def kysyainekset(ruuat):
    
    for row in ruuat:
        kysyseuraava = True
        print(row["Ruoka"])
        row["Raaka-aineet"] = []
        while kysyseuraava:
            raakaaine = dict()
            raakaaine["ainesosa"] = input("Mitä tarvitaan? --> ")
            raakaaine["maara"] = input("Kuinka paljon? --> ")
            raakaaine["yksikko"] = input("Mitä yksikköä? --> ")
            row["Raaka-aineet"].append(raakaaine)
            toiminto = input("Onko lisää raaka-aineita? (k/e) --> ")
            if toiminto == "k":
                kysyseuraava = True
                continue
            if toiminto == "e":
                kysyseuraava = False
                
    with open("reseptit.json", "w") as reseptit:
        json.dump(ruuat, reseptit, indent=4)


def main():
    ruuat = lueruuat()
    kysyainekset(ruuat)


if __name__ == "__main__":
    main()

