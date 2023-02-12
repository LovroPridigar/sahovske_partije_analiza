import orodja
import re

seznam = []

# vzorca (i) in (ii) pobereta informacije o igralcih s strani https://www.chess.com/players?page={PAGE_NUMBER}

vzorec_bloka = re.compile(r'<span class="post-author-name">.*?'
                         r'<p class="post-author-about">',flags=re.DOTALL)

podatki_igralca = re.compile(r'<span class="post-author-name">\n\s*'
                             r'(?P<ime>.*?)'
                             r'\n\s*?</span>.*?'
                             r'href="https://www.chess.com/ratings">\n\s*'
                             r'(?P<rating>\d\d\d\d)\s\|\s#(?P<mesto>\d*).*?'
                             r'<div class="post-author-meta">\n\s*'
                             r'(?P<drzava>\w*)',flags=re.DOTALL)

# vzorca (iii) in (iv) pobereta za vsakega igralca posebej še nekaj dodatnih informacij

blok_dodatnih_podatkov = re.compile(r'<div class="master-players-description">.*?'
                         r'<div class="master-games-table-responsive">',flags=re.DOTALL)

dodatni_podatki = re.compile(r'<span class="master-players-age">\(.*?(?P<age>\d*)\).*?'
                             r'Total Games <span class="master-games-distribution-count">(?P<total_games>\d*?)</span>.*?'
                             r'<span class="master-games-percent-label">.*?(?P<winrate_win>\d*?)%\sWin.*?</span>.*?'
                             r'<span class="master-games-percent-label">.*?(?P<winrate_draw>\d*?)%\sDraw.*?</span>.*?'
                             r'<span class="master-games-percent-label">.*?(?P<winrate_loss>\d*?)%\sLoss.*?</span>.*?', flags=re.DOTALL)
                            
orodja.pripravi_imenik("seznam_igralcev")

# poberemo top ((ST_TOP_STRANI) * 25) igralcev

ST_TOP_STRANI = 7

for stran in range(ST_TOP_STRANI):
    url = f'https://www.chess.com/players?page={stran + 1}'
    datoteka = f'seznam_igralcev/top_igralci_{stran + 1}.html' 
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)

    for blok in vzorec_bloka.finditer(vsebina):
        igralec_info = podatki_igralca.search(blok.group(0))
        if igralec_info:
          seznam.append(igralec_info.groupdict())
    print(seznam)

orodja.pripravi_imenik("dodatek")

# sprehodimo se po vseh igralcih in pri vsakemu dodamo še informacijo o starosti, številu vseh iger, procentu zmag, ...

for igralec in seznam:
    ime = igralec["ime"].replace(" ","%20")
    url = f'https://www.chess.com/games/search?opening=&openingId=&p1={ime}&p2=&sort=&page=1'
    datoteka = f'dodatek/dodatni_podatki_{ime}.html'
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)

    for blok in blok_dodatnih_podatkov.finditer(vsebina):
        starost = dodatni_podatki.search(blok.group(0))
        if starost:
            for key in starost.groupdict():
                igralec[key] = starost.groupdict()[key]

orodja.zapisi_csv(seznam, ["ime", "rating", "mesto", "drzava", "age", "total_games", "winrate_win", "winrate_draw", "winrate_loss"], "obdelani_podatki/igralci.csv")