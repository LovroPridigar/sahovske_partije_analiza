Analiza-podatkov
===================================
Najboljši šahisti
===================================


Zajel bom najboljših 175 šahistov s strani 
[Chess.com](https://www.chess.com/players?page=1)
Za vsakega šahista bom zajel:
* ime in priimek
* rating in uvrstitev na lestvici najbolših
* starost
* število vseh odigranih partij
* procent (zmag, porazov, in remijev).

Poleg podatkov o igralcih bom zajel še zadnjih 100 partij vsakega igralca iz zgornjega seznama.
Partije dobimo na strani [Chess.com](https://www.chess.com/games/search?opening=&openingId=&p1=Magnus%Carlsen&p2=&sort=&page=1)
(Zgornji link je primer za šahista Magnusa Carlsena.)
Za vsako partijo bom zajel:

* identifikacijsko število partije
* ime in priimek obeh igralcev
* rating obeh igralcev
* rezultat partije in število odigranih potez
* leto
* prvih 6 odigranih potez.

Iz pridobljenih podatkov bomo razbrali:

* razporejenost igralcev po državah
* kateri izmed igralcev povprečno naredi največ potez
* kateri igralec je pridobil največ ratinga
* v koliko primerih zmaga igralec, ki ima manjši rating
* ali pri najbolših 100 igralcih obstaja povezava med aktivnostjo igralca (koeficient st_vseh_iger/starost) in mestom na lestvici najboljših

Datoteke v repozitoriju vsebujejo:

* nabor_igralcev.py -datoteka za nabor igralcev
* nabor_partij.py -datoteka za nabor partij
* orodja.py -datoteka orodij za nabor podatkov (iz predavanj)
* analiza_podatkov.ipynb -pandas datoteka dejanske analize podatkov
* igralci.csv, partije.csv -obdelani podatki
* v mapah seznam_igralcev in zbrani_podatki -html datoteke