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

![code_20240506_172734_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/af21db66-aaf0-4e3c-9146-978984890b3f)


- 'remove_extreme_values' - funkcija, skirta pašalinti ribinėms reikšmės (minimalioms ir maksimalioms), 
  kurios gali turėti įtakos modelio tiklsumui

![code_20240506_172809_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/b9f5cf46-6a02-4bb3-873a-4300fd9e07b6)


- 'calculate_room_count' - funkcija, skirta užpildyti tuštiems laukeliams, stulpelyje 'Kambarių sk.'.
  Šis stulpelis turėjo daug tuščių reikšmių, tad jo užpildymas vidutiniu kambarių skaičiaus dydžiu
  galėtų turėti neigiamos įtakos modelio tikslumui. Buvo pasirinktas kitas būdas: remiantis turimais
  duomenimis iš pradžių apskaičiuotas vidutinis vieno kambario plotas. Tad tusčios vietos užpildytos
  suapvalinta verte, gauta padalinus namo plotą iš vidutinio kambario ploto

![code_20240506_173313_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/92fff7bc-3f21-46bd-88d8-1edf37d47358)
![code_20240506_172834_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/d9ab93a6-a7da-45d2-abd2-c8fc58ef126a)


Pagrindiniai žingsniai

- Duomenų nuskaitymas: nuskaitomi duomenys iš CSV failų, sukurtų duomenų gavybos metu ir sukūriami 
  DF objektai, kurie galiausiai yra sujungiamį į vieną.
  
![code_20240506_172927_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/96728763-9df8-4bd1-9a52-952a135eb097)

- Duomenų valymas ir transformavimas: pašalinami nereikalingi simboliai ir ribinės kainų reikšmės. 
  Taip pat pašalinami dublikatai ir stulpeliai, kurie nebus naudojami tolimesnėje analizėje.
  Skaitinės reikšmės konvertuojamos į skaičius. Užpildomos trūkstamos vertės.
  
![code_20240506_173110_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/a615be74-c5b4-4e54-aa63-09ccba62f20e)

- Statybos metų stulpelis turėjo eilutes, kuriose buvo nurodyta daugiau nei viena data ir papildomas tekstas.
  Pasirinkome pirmą datą, tekstą pašalinome

![code_20240506_173607_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/39695abf-28b3-4abf-92dc-9de3f1eb3b91)

- Iš adreso stulpelio išgavome tik miestą (arbą rajoną) ir suvienodinome pavadinimus

  ![code_20240506_173716_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/9bdb5a16-9374-4088-8dcc-bcd616495f87)

- Kai kurie kategoriniai atribūtai (Šildymo tipas, Vanduo) turėjo daug unikalių kategorijų, arba pasikartojimų,
  tad buvo nuspręsta palikti tik pirmu pasirinkimu įrašytą opciją

![code_20240506_173958_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/986d56ec-53e8-4cda-bf98-0e1849f97d7e)

- Patikriname ar duomenų rinkinyje neliko tuščių reikšmių.

![code_20240506_173438_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/11743daf-a809-4cf9-aa15-5360c7387db6)

- Duomenų kodavimas ir normalizavimas: Kategoriniai kintamieji yra koduojami naudojant One-Hot Encoder'į, 
  o skaitiniai kintamieji yra normalizuojami naudojant Min-Max Scaler'į.

  ![code_20240506_174057_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/3d8f71fa-2051-4b9d-ac59-7d12a7b5e78c)

- Duomenų išsaugojimas: Koduoti ir normalizuoti duomenys yra išsaugomi duomenų bazėje, 
  taip pat papildomai išsaugomi ir naudoti normalizavimo parametrai.

![code_20240506_174153_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/975532a1-090e-47f3-8751-01c6adeaf86f)
