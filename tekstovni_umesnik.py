from model import Uporabnik, Teme, Set, Ponudba, Narocilo

def vnesi_izbiro(moznosti):
    """
    Uporabniku da na izbiro podane možnosti.
    """
    moznosti = list(moznosti)
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    while True:
        try:
            izbira = int(input('> ')) - 1
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira!")

def main():
    while True:
        uporabnik = input('Vnesite ime: ')
        if uporabnik:
            glavni_meni(uporabnik)
            break
        else:
            print("Poskusite znova.")

def glavni_meni(uporabnik):
    """
    Glavni meni za interakcijo z uporabnikom.
    """
    while True:
        print("\nGlavni meni:")
        print("1) Poišči izdelke")
        print("2) Odjava")
        izbira = input("> ")
        if izbira == '1':
            poisci_izdelke()
        elif izbira == '2':
            print("Odjava uspešna.")
            break
        else:
            print("Napačna izbira!")

def poisci_izdelke():
    """
    Poišče izdelke glede na uporabnikov izbor.
    """
    print("Izberite način iskanja:")
    print("1) Poišči glede na temo")
    print("2) Poišči glede na starost")
    print("3) Poišči glede na ceno")
    izbira = input("> ")
    
    if izbira == '1':
        poisci_izdelke_po_tematicnih()
    elif izbira == '2':
        poisci_izdelke_po_starosti()
    elif izbira == '3':
        poisci_izdelke_po_ceni()
    else:
        print("Napačna izbira iskanja.")

def poisci_izdelke_po_tematicnih():
    """
    Poišče izdelke glede na temo.
    """
    print("Izberite temo:")
    teme = Teme.dobi_vse_teme()
    if teme:
        for i, tema in enumerate(teme, 1):
            print(f"{i}) {tema.tema}")
        izbira = int(input("> ")) - 1
        if 0 <= izbira < len(teme):
            izbrana_tema = teme[izbira]
            izdelki = Set.dobi_sete_po_temi(izbrana_tema.id)
            if izdelki:
                for i, izdelek in enumerate(izdelki, 1):
                    print(f"{i}) Izdelek: {izdelek.ime}, Cena: {izdelek.cena}€")
                izdelek_izbira = int(input("Izberite izdelek za dodajanje v naročilo (številka): ")) - 1
                if 0 <= izdelek_izbira < len(izdelki):
                    id_seta = izdelki[izdelek_izbira].id
                    kolicina = int(input("Vnesite količino: "))
                    print("Izdelek je bil uspešno naročen.")
                else:
                    print("Napačna izbira!")
            else:
                print("Ni izdelkov za izbrano temo.")
        else:
            print("Napačna izbira!")
    else:
        print("Ni razpoložljivih tem.")

def poisci_izdelke_po_starosti():
    """
    Poišče izdelke glede na starost.
    """
    try:
        minimalna_starost = int(input('Vnesite minimalno starost: ').strip())
        izdelki = Set.dobi_po_starosti(minimalna_starost)
        if izdelki:
            print(f"Izdelki za starost {minimalna_starost}+ let:")
            for i, izdelek in enumerate(izdelki, 1):
                print(f'{i}) Izdelek: {izdelek.ime}, Cena: {izdelek.cena}€, Starost: {izdelek.starost}')
            izdelek_izbira = int(input("Izberite izdelek za dodajanje v naročilo (številka): ")) - 1
            if 0 <= izdelek_izbira < len(izdelki):
                id_seta = izdelki[izdelek_izbira].id
                kolicina = int(input("Vnesite količino: "))
                print("Izdelek je bil uspešno naročen.")
            else:
                print("Napačna izbira!")
        else:
            print(f"Ni izdelkov, ki bi ustrezali starostni skupini {minimalna_starost}+.")
    except ValueError:
        print("Napačen vnos starosti. Prosimo, vnesite veljavno številko.")

def poisci_izdelke_po_ceni():
    """
    Poišče izdelke glede na ceno.
    """
    try:
        minimalna_cena = float(input('Vnesite minimalno ceno: ').strip())
        maksimalna_cena = float(input('Vnesite maksimalno ceno: ').strip())
        izdelki = Set.dobi_sete_po_ceni(minimalna_cena, maksimalna_cena)
        if izdelki:
            for i, izdelek in enumerate(izdelki, 1):
                print(f'{i}) Izdelek: {izdelek.ime}, Cena: {izdelek.cena}€')
            izdelek_izbira = int(input("Izberite izdelek za dodajanje v naročilo (številka): ")) - 1
            if 0 <= izdelek_izbira < len(izdelki):
                id_seta = izdelki[izdelek_izbira].id
                kolicina = int(input("Vnesite količino: "))
                print("Izdelek je bil uspešno naročen.")
            else:
                print("Napačna izbira!")
        else:
            print("Ni izdelkov v izbranem cenovnem razponu.")
    except ValueError:
        print("Napačen vnos cene. Prosimo, vnesite številke.")

if __name__ == '__main__':
    main()
