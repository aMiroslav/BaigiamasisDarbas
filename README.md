Darbo pavadinimas: NT kainų prognozavimo sistema

Projektas skirtas namų kainų prognozavimui, remiantis įvairiomis savybėmis.

Prejektas sudarytas iš kelių dalių:

1. Įvadas
2. Duomenų surinkimas 
3. Duomenų apdorojimas 
4. Modelio kūrimas, mokymas ir vertinimas 
5. Prognozių generavimas 
6. Vizualinis pateikimas 
7. Išvados

1. Įvadas
Projektas buvo orientuotas į Lietuvos rinką, tad projektui buvo pasirinkta analizuoti
nekilnojomojo turto, o kenkrečiau namų kainas Lietuvoje. Buvo orientuojamasi į didžiausius 
miestus, tad objektu buvo pasirinkti: Vilnius, Kaunas, Klaipėda, Šiauliai, Panevėžys ir 
Alytus. Peržvelgus nekilnojamo turto sklebimų portalus, šie miestai turėjo daugiausiai 
duomenų. Duomenų rinkimui buvo pasirinktas didžiausias ir populiariausias skelbimų portaslas
aruodas.lt.

2. Duomenų rinkimas

Naudotos technologijos:

- Python
- BeautifulSoup: 
- Selenium: Nešiojama karkaso testavimui interneto programoms.
- WebDriver Manager: Įrankis, skirtas valdyti interneto draiverius.
- Pandas: 

Naudotos funkcijos:

accept_cookies() - funkcija skirta paspausti slapukų sutikimo mygtukui. Funkcija iškviečiama 
pagrindinėje funkcijoje, kad būtų galima uždaryti slapukų sutikimo langą norint atlikti kitas 
operacijas puslapyje. 

![code_20240506_164746_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/74aea71a-7604-46d6-bf4b-2af2b9f2fc7c)


scrape_page_data(link) - funkcija skirta išgauti duomenims apie vieną nekilnojamojo turto objektą.
Iškviečiama pagrindinėje funkcijoje ir iteruojamą per kiekvieną atverčiamą puslapį. 
Funkcija naudoja parametrą 'link' - puslpaio, iš kurio bus išgaunami duomenis, URL.
Funkcija gražiną 'page_data', žodyną, kuriame saugomi duomenys apie vieno NT objekto atributus

![code_20240506_165336_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/1204ea94-e088-44f5-b5a8-0ec9846772ff)

scrape_and_save(start_page, end_page) - funkcija, skirta nuorodų, apie kiekvieną NT objoktą išgavimui, 
duomenų išsaugojimui CSV formatu, iteruojant per visus puslapius iš atitinkamų skelbimų filtro
kategorijos. Funkcija iškviečiama kaip pagrindinė funkcija, kad būtų pradėtas duomenų išgavimo procesas.
Naudojami parametrai:     'start_page' - pradinis puslapio numeris, nuo kurio 
'end_page' - paskutinis puslapio numeris, ties kuriuo baigiamas duomenų išgavimas.

![code_20240506_170311_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/87a1e48f-5a16-40e3-845c-f0bdce4408ad)

Duomenų išgavimą pradedame paprasta komanda, kuria iškviečiama pagrindinė funkcija, pradedama
duomenų gavyba ir galiausiai duomenys išsaugomi. 

![code_20240506_170424_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/de3b8c0d-6604-4d9e-a73a-73ffcc2f5f94)

Šis procesas atliekamas atskirai kiekvienam miestui (įtraukus ir rajoną). Kiekvienam miestui yra 
paruoštas atitinkamas kodas, su konkrečia pradine nuorodą, galutinio failo pavadinimu ir
galutinio puslapio skaičiumi

