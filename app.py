import bottle
import hashlib
import baza
import importlib
from model import Uporabnik, Teme, Set, Ponudba, Narocilo
from urllib import parse

secret = 'skrivnost'

def geslo_md5(s):
    '''Vrne MD5 hash danega UTF-8 niza.'''
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

@bottle.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='./static')

@bottle.route('/registracija')
def registracija():
    '''Vrne stran za registracijo'''
    return bottle.template('templates\\registracija.html', napaka=None)

@bottle.post('/registracija')
def registracija_post():
    '''Obdelaj izpolnjeno formo za registracijo'''
    uporabnisko_ime = bottle.request.forms.uname
    geslo = geslo_md5(bottle.request.forms.psw)

    if Uporabnik.dobi_uporabnika(uporabnisko_ime) is not None:
        return bottle.template('templates\\registracija.html', napaka='Uporabniško ime že obstaja!')

    nov_uporabnik = Uporabnik(uporabnisko_ime, geslo)
    nov_uporabnik.shrani_v_bazo()

    bottle.response.set_cookie('uporabniskoIme', uporabnisko_ime, path='/', secret=secret)
    bottle.redirect('/')

@bottle.route('/prijava')
def prijava():
    '''Vrne stran za prijavo'''
    return bottle.template('templates\\prijava.html', napaka=None)
    

@bottle.post('/prijava')
def prijava_post():
    '''Obdelaj izpolnjeno formo za prijavo'''
    uporabnisko_ime = bottle.request.forms.uname
    geslo = geslo_md5(bottle.request.forms.psw)
    poizvedba = Uporabnik.pravilen_vnos(uporabnisko_ime, geslo)

    if poizvedba is None:
        return bottle.template('templates\\prijava.html', napaka='Uporabnik ne obstaja ali je geslo napačno!')
    else:
        bottle.response.set_cookie('uporabniskoIme', uporabnisko_ime, path='/', secret=secret)
        bottle.redirect('/')

@bottle.route('/odjava', method='POST')
def odjava():
    '''Odjavi uporabnika in preusmeri na prijavno stran'''
    bottle.response.delete_cookie('uporabniskoIme', path='/', secret=secret)
    bottle.redirect('/prijava')

@bottle.route('/')
def glavna_stran():
    '''Vrne glavno stran'''
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    if trenutni_uporabnik is None:
        bottle.redirect('/prijava')
        return
    
    starosti = Set.dobi_vse_sete_starost()
    teme = Teme.dobi_vse_teme()
    narocila = Narocilo.dobi_narocila_uporabnika(trenutni_uporabnik)
    
    for tema in teme:
        tema.tema_url = tema.tema.lower().replace(' ', '')
    
    max_cena = Ponudba.MAX_CENA  # Nastavimo privzeto maksimalno ceno
    min_koscki = Set.MIN_KOSCKI  # Nastavimo privzeto minimalno število koščkov
    
    return bottle.template('templates\\glavna.html', starosti=starosti, teme=teme, trenutni_uporabnik=trenutni_uporabnik, napaka=None, narocila=narocila, max_cena=max_cena, min_koscki=min_koscki)

@bottle.post('/')
def glavna_stran_post():
    '''Obdelaj izpolnjen obrazec za filtriranje setov'''
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    if trenutni_uporabnik is None:
        bottle.redirect('/prijava')
        return

    starost = bottle.request.forms.get('starost')
    id_teme = bottle.request.forms.get('tema')
    max_cena = bottle.request.forms.get('max_cena')
    koscki = bottle.request.forms.get('koscki')

    # Filtri bodo nastavljeni samo, če imajo vrednost
    filtri = {}
    if starost:
        filtri['starost'] = starost
    if id_teme:
        filtri['id_teme'] = id_teme
    if max_cena:
        filtri['max_cena'] = max_cena
    if koscki:
        filtri['koscki'] = koscki

    bottle.redirect('/rezultati?' + parse.urlencode(filtri))

@bottle.route('/rezultati')
def prikazi_rezultate():
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    if trenutni_uporabnik is None:
        bottle.redirect('/prijava')
        return

    starost = bottle.request.query.get('starost')
    id_teme = bottle.request.query.get('id_teme')
    max_cena = bottle.request.query.get('max_cena')
    koscki = bottle.request.query.get('koscki')

    filtri = {'starost': starost, 'id_teme': id_teme, 'max_cena': max_cena, 'koscki': koscki}
    rezultati = filtriraj_sete(filtri)

    return bottle.template('templates\\rezultati.html', rezultati=rezultati, trenutni_uporabnik=trenutni_uporabnik)

def filtriraj_sete(filtri):
    '''Filtrira sete glede na dane filtre'''
    starost = filtri.get('starost')
    id_teme = filtri.get('id_teme')
    max_cena = filtri.get('max_cena')
    koscki = filtri.get('koscki')

    rezultati = Set.dobi_sete_z_imenom_teme(id_teme)
    if starost:
        rezultati = [set for set in rezultati if set.starost == starost]
    if max_cena:
        ponudbe = Ponudba.dobi_ponudbe_cena_do(max_cena)
        ponudba_ids = [int(ponudba.id_seta) for ponudba in ponudbe]
        rezultati = [set for set in rezultati if set.id in ponudba_ids]
    if koscki:
        rezultati = [set for set in rezultati if set.koscki >= int(koscki)]

    return rezultati


# Podrobnosti seta
@bottle.route('/set/<id_seta:int>')
def prikazi_set(id_seta):
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    if trenutni_uporabnik is None:
        bottle.redirect('/prijava')
        return

    set = Set.dobi_vse_podatke_za_set(id_seta)
    if set:
        set = set[0]  # Predpostavimo, da dobimo samo en rezultat
        return bottle.template('templates\\podrobnosti.html', set=set, trenutni_uporabnik=trenutni_uporabnik)
    else:
        return bottle.template('templates\\napaka.html', sporocilo="Set ni bil najden.")

@bottle.post('/naroci')
def naroci():
    '''Obdelaj naročilo in shrani v bazo'''
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    if trenutni_uporabnik is None:
        bottle.redirect('/prijava')
        return
    
    id_seta = bottle.request.forms.id_seta

    if trenutni_uporabnik and id_seta:
        id_uporabnika = int(Uporabnik.dobi_id_up(trenutni_uporabnik))
        
        # Preveri, ali je uporabnik že naročil ta set
        ze_narocil = Narocilo.preveri_ze_naroceno(id_uporabnika, id_seta)
        if ze_narocil:
            return bottle.template('templates\\napaka.html', sporocilo="Ta set ste že naročili. Večkratno naročanje istega seta ni dovoljeno.", trenutni_uporabnik=trenutni_uporabnik)
        
        ponudbe = Ponudba.dobi_vse_ponudbe(id_seta)
        if ponudbe:
            ponudba = ponudbe[0]
            narocilo = Narocilo(id_ponudbe=ponudba.id, id_uporabnika=id_uporabnika)
            narocilo.dodaj_v_bazo()
            return bottle.template('templates\\uspesno.html', sporocilo="Vaše naročilo je bilo uspešno oddano.", trenutni_uporabnik=trenutni_uporabnik)
    
    return bottle.template('templates\\napaka.html', sporocilo="Naročilo ni bilo uspešno. Prosimo, poskusite znova.", trenutni_uporabnik=trenutni_uporabnik)


@bottle.route('/narocila')
def prikazi_narocila():
    trenutni_uporabnik = bottle.request.get_cookie('uporabniskoIme', secret=secret)
    if trenutni_uporabnik is None:
        bottle.redirect('/prijava')
        return

    narocila = Narocilo.dobi_narocila_uporabnika(trenutni_uporabnik)
    skupna_cena = Narocilo.dobi_skupno_ceno_uporabnika(trenutni_uporabnik)
    print(narocila)

    return bottle.template('templates\\narocila.html', narocila=narocila, trenutni_uporabnik=trenutni_uporabnik, skupna_cena=skupna_cena)

bottle.run(host='localhost', port=8080, debug=True, reloader=True)




