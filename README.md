# Lego-Store

Skupnij repozitorij za projekt pri podatkovnih bazah za spletno trgovino Lego Store.

Za svoj projekt sem se odločil narediti spletno trgovino Lego Store, kjer lahko uporabniki izvajajo različne ukaze. Uporabnik se lahko registrira in prijavi v trgovino, nato pa je preusmerjen na glavno stran. Tam lahko filtrira izdelke glede na temo, ceno, priporočeno starost in število koščkov v setu. Ko uporabnik prefiltrira izdelke, se mu prikaže nova stran, na kateri so prikazani vsi izdelki, ki jih lahko nato naroči. Vsi izdelki, ki jih uporabnik naroči, se shranijo na posebni strani "naročila" za boljšo preglednost.
Pri izdelavi programa sem delal z bazo, ki je sestavljena iz petih tabel, medsebojno povezanih, kot je prikazano na spodnji sliki.

Povezave med bazami:
- Bazi **Uporabnik** in **Naročilo** sta povezani preko **ID** in **ID_uporabnika**.
- Bazi **Naročilo** in **Ponudba** sta povezani preko **ID_ponudbe** in **ID**.
- Bazi **Ponudba** in **SET** sta povezani preko **ID_seta** in **ID**
- Bazi **SEt** in **Tema** sta povezani preko **ID_teme** in **ID**.

<img width="889" alt="ER_diagram" src="https://github.com/user-attachments/assets/f474c19a-1ece-4224-8e8e-4826a767f811">


Projekt se za delovanja zanaša tudi na knjižnice, ki niso vključene v python, kot npr. bottle, zato jo je potrebno prej naložiti.

 
