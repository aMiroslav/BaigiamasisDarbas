Darbo pavadinimas: NT kainų prognozavimo sistema

Projektas skirtas namų kainų prognozavimui, remiantis įvairiomis savybėmis.

Prejektas sudarytas iš kelių dalių:

1. Įvadas
2. Duomenų surinkimas 
3. Duomenų paruošimas ir apdorojimas 
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

'accept_cookies()' - funkcija skirta paspausti slapukų sutikimo mygtukui. Funkcija iškviečiama 
pagrindinėje funkcijoje, kad būtų galima uždaryti slapukų sutikimo langą norint atlikti kitas 
operacijas puslapyje. 

![code_20240506_164746_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/74aea71a-7604-46d6-bf4b-2af2b9f2fc7c)


'scrape_page_data(link)' - funkcija skirta išgauti duomenims apie vieną nekilnojamojo turto objektą.
Iškviečiama pagrindinėje funkcijoje ir iteruojamą per kiekvieną atverčiamą puslapį. 
Funkcija naudoja parametrą 'link' - puslpaio, iš kurio bus išgaunami duomenis, URL.
Funkcija gražiną 'page_data', žodyną, kuriame saugomi duomenys apie vieno NT objekto atributus

![code_20240506_165336_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/1204ea94-e088-44f5-b5a8-0ec9846772ff)

'scrape_and_save(start_page, end_page)' - funkcija, skirta nuorodų, apie kiekvieną NT objoktą išgavimui, 
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


3. Duomenų paruošimas ir apdorojimas
Prieš atliekant tolimesnius žingsniu, gautus duomenis svarbu tinkamai paruošti. Šis procesas
apima duomenų nuskaitymą iš CSV failų, duomenų valymą, transformavimą ir kodavimą bei galutinių 
duomenų išsaugojimą duomenų bazėje.

Naudojamos technologijos

- Python
- SQLite3: Integruota duomenų bazė skirta duomenų saugojimui.
- Pandas: Biblioteka duomenų analizei.
- Regular Expressions (re): Python modulis teksto šablonų atpažinimui.
- Scikit-learn: Biblioteka, skirta mašininio mokymosi modelių kūrimui ir duomenų normalizavimui.

Nauodojamos funkcijos:

-'cleen_cell_to_number' - funkcija, skirta pašalinti nereikalingus ženklus iš duomenų langelių, kadangi
  iš puslapio gauti duomenis turi mums nereikalingų simbolių. Taip pat ',' skaičiuose keičiami į '.'.


- 'remove_extreme_values' - funkcija, skirta pašalinti ribinėms reikšmės (minimalioms ir maksimalioms), 
  kurios gali turėti įtakos modelio tiklsumui


- 'calculate_room_count' - funkcija, skirta užpildyti tuštiems laukeliams, stulpelyje 'Kambarių sk.'.
  Šis stulpelis turėjo daug tuščių reikšmių, tad jo užpildymas vidutiniu kambarių skaičiaus dydžiu
  galėtų turėti neigiamos įtakos modelio tikslumui. Buvo pasirinktas kitas būdas: remiantis turimais
  duomenimis iš pradžių apskaičiuotas vidutinis vieno kambario plotas. Tad tusčios vietos užpildytos
  suapvalinta verte, gauta padalinus namo plotą iš vidutinio kambario ploto



Pagrindiniai žingsniai

- Duomenų nuskaitymas: nuskaitomi duomenys iš CSV failų, sukurtų duomenų gavybos metu ir sukūriami 
  DF objektai, kurie galiausiai yra sujungiamį į vieną.


- Duomenų valymas ir transformavimas: pašalinami nereikalingi simboliai ir ribinės kainų reikšmės. 
  Taip pat pašalinami dublikatai ir stulpeliai, kurie nebus naudojami tolimesnėje analizėje


- Duomenų kodavimas ir normalizavimas: Kategoriniai kintamieji yra koduojami naudojant One-Hot Encoder'į, 
  o skaitiniai kintamieji yra normalizuojami naudojant Min-Max Scaler'į.


- Duomenų išsaugojimas: Koduoti ir normalizuoti duomenys yra išsaugomi duomenų bazėje, 
  taip pat papildomai išsaugomi ir naudoti normalizavimo parametrai.

