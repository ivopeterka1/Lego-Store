import sqlite3
from model import Uporabnik, Teme, Set, Ponudba, Narocilo
from enum import Enum

def vnesi_izbiro(moznosti):
    """
    Uporabniku da na izbiro podane možnosti.
    """
    moznosti = list(moznosti)
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    izbira = None
    while True:
        try:
            izbira = int(input('> ')) - 1
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira!")

def izpisi_narocila(uporabnik):
    """
    Izpiše vsa naročila podanega uporabnika.
    """
    narocila = Narocilo.dobi_narocila_uporabnika(uporabnik)
    if narocila:
        for narocilo in narocila:
            print(f'{narocilo[0]} - {narocilo[1]}€ x {narocilo[2]}')
    else:
        print('Ni naročil.')

def dodaj_narocilo(uporabnik):
    """
    Doda novo naročilo za uporabnika.
    """
    print("Izberite set:")
    seti = Set.dobi_sete_z_imenom_teme()
    izbrani_set = vnesi_izbiro(seti)
    
    if izbrani_set:
        if Narocilo.preveri_ze_naroceno(uporabnik.id, izbrani_set.id):
            print("Ta set ste že naročili.")
        else:
            ponudbe = Ponudba.dobi_vse_ponudbe(izbrani_set.id)
            if ponudbe:
                izbrana_ponudba = vnesi_izbiro(ponudbe)
                narocilo = Narocilo(id_ponudbe=izbrana_ponudba.id, id_uporabnika=uporabnik.id)
                narocilo.dodaj_v_bazo()
                print("Naročilo je bilo uspešno dodano.")
            else:
                print("Izbrani set ni na voljo.")

def registracija():
    """
    Registracija novega uporabnika.
    """
    uporabnisko_ime = input("Vnesite uporabniško ime: ")
    geslo = input("Vnesite geslo: ")
    geslo_md5 = hashlib.md5(geslo.encode('utf-8')).hexdigest()
    nov_uporabnik = Uporabnik(uporabnisko_ime, geslo_md5)
    nov_uporabnik.shrani_v_bazo()
    print("Registracija uspešna.")

def prijava():
    """
    Prijava obstoječega uporabnika.
    """
    uporabnisko_ime = input("Vnesite uporabniško ime: ")
    geslo = input("Vnesite geslo: ")
    geslo_md5 = hashlib.md5(geslo.encode('utf-8')).hexdigest()
    uporabnik = Uporabnik.pravilen_vnos(uporabnisko_ime, geslo_md5)
    if uporabnik:
        return Uporabnik.dobi_uporabnika(uporabnisko_ime).fetchone()
    else:
        print("Napačno uporabniško ime ali geslo.")
        return None

def glavni_meni(uporabnik):
    """
    Glavni meni za interakcijo z uporabnikom.
    """
    while True:
        print("\nGlavni meni:")
        print("1) Preglej naročila")
        print("2) Dodaj naročilo")
        print("3) Odjava")
        izbira = input("> ")
        if izbira == '1':
            izpisi_narocila(uporabnik)
        elif izbira == '2':
            dodaj_narocilo(uporabnik)
        elif izbira == '3':
            print("Odjava uspešna.")
            break
        else:
            print("Napačna izbira!")

def main():
    print("Dobrodošli v LEGO trgovini!")
    while True:
        print("\n1) Prijava")
        print("2) Registracija")
        print("3) Izhod")
        izbira = input("> ")
        if izbira == '1':
            uporabnik = prijava()
            if uporabnik:
                glavni_meni(uporabnik)
        elif izbira == '2':
            registracija()
        elif izbira == '3':
            print("Nasvidenje!")
            break
        else:
            print("Napačna izbira!")

if __name__ == '__main__':
    main()
