# Lego-Store
Skupnij repozitorij za projekt pri podatkovnih bazah za spletno trgovino Lego Store.

Avtorja:
* Ivo Peterka in Aljaž Remžgar

Za najin projekt sva se odločila narediti spletno trgovino Lego Store, na kateri lahko uporabnik izvaja različne ukaze. Lahko se registrira in prijavi v samo trgovino in potem je poslan na glavno stran trgovine. Tam lahko filtrira izdelke po temi, ceni, primerni starosti in število koščkov samega seta. Ko uporabnik prefiltrira izdelke se mu odpre nova stran, kjer so prikazani vsi izdelki katere lahko potem naroči. Vse izdelke, ki jih je uporabnik naročil se potem shranijo na posebni strani "naročila", za boljšo preglednost. 
Pri izdelavi samega programa sva delala s petimi bazami, ki so med seboj povezane tako kot je prikazano na spodnji sliki.

Povezave med bazami:
- Bazi **Uporabnik** in **Naročilo** sta povezani preko **ID** in **ID_uporabnika**.
- Bazi **Naročilo** in **Ponudba** sta povezani preko **ID_ponudbe** in **ID**.
- Bazi **Ponudba** in **SET** sta povezani preko **ID_seta** in **ID**
- Bazi **SEt** in **Tema** sta povezani preko **ID_teme** in **ID**.

<img width="889" alt="ER_diagram" src="https://github.com/user-attachments/assets/f474c19a-1ece-4224-8e8e-4826a767f811">


Najin projekt se za delovanja zanaša tudi na knjižnice, ki niso vključene v python, kot npr. bottle, zato jo je potrebno prej naložiti.
