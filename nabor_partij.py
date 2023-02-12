from dataclasses import replace
import orodja
import re
import csv

seznam_igralcev = []
seznam = []

with open("obdelani_podatki/igralci.csv") as igralci:
    reader = csv.reader(igralci)
    for igralec in reader:
        if igralec == []:
            None
        else:
            seznam_igralcev.append(igralec[0])

# pomozne funkcije

def pripravi_igralca_za_url(seznam):
    sez = []
    for igralec in seznam:
        sez.append(igralec.replace(" ","%20"))
    return sez

def vrni_igralca(ime):
    return ime.replace("%20","_")

def popravi_igralca(ime):
    return ime.replace(" ","_")

# vzorca za nabor informacij o partijah top šahistov

vzorec_bloka = re.compile(r'class="master-games-clickable-link master-games-td-user".*?'
                          r'<tr class="master-games-master-game v-board-popover"', 
                          flags=re.DOTALL)

podatki_partije = re.compile(r'href="https://www.chess.com/games/view/(?P<id>\d*)">.*?'
                             r'<span class="master-games-username">(?P<ime_beli>.*?)</span>.*?'
                             r'<span class="master-games-user-rating">\((?P<rating_beli>\d\d\d\d)\).*?'
                             r'<span class="master-games-username">(?P<ime_crni>.*?)</span>.*?'
                             r'<span class="master-games-user-rating">\((?P<rating_crni>\d\d\d\d)\).*?'
                             r'title="(?P<poteze>.*?)">.*?'
                             r'title="(?P<rezultat>.*?)">.*?'
                             r'title="(?P<st_potez>.*?)">.*?'
                             r'title="(?P<leto>.*?)">',
                             flags=re.DOTALL)

# poberemo podatke in jih shranimo

for igralec in pripravi_igralca_za_url(seznam_igralcev[1:]):
    for stran in range(4):
        url = f'https://www.chess.com/games/search?opening=&openingId=&p1={igralec}&p2=&sort=&page={stran + 1}'
        datoteka = f'zbrani_podatki/{vrni_igralca(igralec)}_partije/{vrni_igralca(igralec)}_stran_{stran + 1}.html' 
        orodja.shrani_spletno_stran(url, datoteka)

# iz html datotek izluščimo informacije

for igralec in seznam_igralcev[1:]:
    for stran in range(4):
        datoteka = f'zbrani_podatki/{popravi_igralca(igralec)}_partije/{popravi_igralca(igralec)}_stran_{stran + 1}.html'
        vsebina = orodja.vsebina_datoteke(datoteka)

        for blok in vzorec_bloka.finditer(vsebina):
           match = podatki_partije.search(blok.group(0))
           if match is not None:
              podatki = match.groupdict()
              seznam.append(podatki)

# po FIDE pravilih za vsako partijo izračunamo spremembo ratinga (Za top igralce se uporabi koeficient K = 10)

K = 10

def elo_calc(rating1, rating2):
    return 1/(1 + pow(10,((rating2 - rating1)/400)))

for igra in seznam:
    if igra['rezultat'] == '1-0':
        igra['rezultat'] = int(1)
        igra["rating_spr"] = (igra["rezultat"] - elo_calc(int(igra["rating_beli"]), int(igra["rating_crni"]))) * K
    elif igra['rezultat'] == '0-1':
        igra['rezultat'] = int(0)
        igra["rating_spr"] = (igra["rezultat"] - elo_calc(int(igra["rating_beli"]), int(igra["rating_crni"]))) * K
    else:
        igra['rezultat'] = 0.5
        igra["rating_spr"] = (igra["rezultat"] - elo_calc(int(igra["rating_beli"]), int(igra["rating_crni"]))) * K

for igra in seznam:
    if igra['rating_beli'] > igra['rating_crni'] and igra['rezultat'] == 1:
        igra['underdog'] = 0
    elif igra['rating_beli'] > igra['rating_crni'] and igra['rezultat'] != 1:
        igra['underdog'] = 1
    elif igra['rating_beli'] < igra['rating_crni'] and igra['rezultat'] != 0:
        igra['underdog'] = 1
    else:
        igra['underdog'] = 0

for igra in seznam:
    if igra['rating_beli'] > igra['rating_crni'] and igra['rezultat'] == 1:
        igra['pravi_underdog'] = 0
    elif int(igra['rating_beli']) - int(igra['rating_crni']) > 99 and igra['rezultat'] != 1:
        igra['pravi_underdog'] = 1
    elif 99 < int(igra['rating_crni']) - int(igra['rating_beli']) and igra['rezultat'] != 0:
        igra['pravi_underdog'] = 1
    else:
        igra['pravi_underdog'] = 0


# lahko se zgodi, da smo kakšno partijo dvakrat zabeležili (za vsakega izmed igralcev), zato dvojne ponovitve izbrišemo!

def delete_doubles(seznam):
    sez = []
    for element in seznam:
        if element in sez:
            None
        else:
            sez.append(element)
    return sez

orodja.zapisi_csv(delete_doubles(seznam), ["id", "ime_beli", "ime_crni", "rating_beli", "rating_crni", "rezultat", "rating_spr", "poteze", "st_potez", "leto", "underdog", "pravi_underdog"], "obdelani_podatki/partije.csv")