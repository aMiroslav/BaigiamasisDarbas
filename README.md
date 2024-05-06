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

4. Modelio kūrimas, mokymas ir vertinimas
Iš viso šiame darbe buvo kuriami trys modeliai: Random Forest Regression, Linear Regresion ir dirbtinių neuroninių
tinklų Sequential modeliai.

- Random Forest Regression
  
Naudojamos technologijos

- Python
- Scikit-learn: Biblioteka, skirta mašininio mokymosi modelių kūrimui ir duomenų normalizavimui.
- SQLite3: Integruota duomenų bazė skirta duomenų saugojimui.
- Pandas: Biblioteka duomenų analizei.
- Matplotlib ir Seaborn: Grafikų braižymo bibliotekos.

Pagrindiniai žingsniai

- Duomenų nuskaitymas: Nuskaitomi duomenys iš duomenų bazės ir sudaromas DataFrame.

![code_20240506_180503_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/97198476-9840-4878-90c1-0f6a739a4b5c)

- Duomenų dalijimas: Duomenys dalijami į mokymo ir testavimo rinkinius.
  
![code_20240506_180530_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/1cc6ef77-cd95-4f84-a945-1064ea758aa1)

- Hiperparametrų nustatymas: Nustatomi Random Forest Regresoriaus hiperparametrai naudojant Grid Search metodą.

  ![code_20240506_180729_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/598c5301-1dfd-4106-a030-d25639751524)

- Modelio mokymas: Modelis yra mokomas su mokymo rinkiniu, naudojant geriausius nustatytus hiperparametrus.
  
![code_20240506_180822_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/9664e9ef-8852-4448-81c3-0ca646fe67dd)

- Modelio vertinimas: Modelio veikimas yra įvertinamas naudojant kryžminį patikrinimą ir testavimo rinkinį.

![code_20240506_180913_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/43c7019d-e914-4583-967f-8d3eccffe7d3)

- Rezultatų vizualizavimas: Modelio spėjimų ir realių kainų koreliacija yra vizualizuojama.

  ![code_20240506_181003_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/4a587f97-a278-4c03-8b42-0263d1ec8514)
  ![image](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/e7e3fbd3-3152-4313-ba0a-752d7f9617d7)

Papildomai, bus atvaizduojama savybių svarba aspkaičiuojant prognozuojamą kainą. Kadangi duomenys yra koduoti, 
turime juos sugrupuoti į motinines kategorijas. Tam tisklui padaromas žodynas grupavimui.

![code_20240506_181208_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/b17953ed-9860-485c-a416-0b68819276dc)

Tada suskaičiuojama rodiklių svarba

![code_20240506_192114_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/62d67429-8ae3-4815-af42-1aaca1463171)

Ir pateikiami rezultatai.

![code_20240506_192246_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/49b0486a-095b-4323-b24a-0247b891b6f3)

![image](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/f0cf0945-b5ed-4922-be03-1d907105763b)

Išvados:
Pateiktas grafikas nurodo santyki tarp modelio prognozuotų ir realių kainų. Kiekvienas taškelis reprezentuoja
vieną turto vienetą. Raudona įstriža linija demonstruoja idealią teorinę prognozę (mūsų siekiamybę).
Taškų atstumas iki linijos norodo paklaidos dydį mūsų spėjimuose.

Iš grafiko galima spręsti, kad modelis veikia geriau, prognazuojant pigesnio turto kainas.
Kai kurie taškai, reprezentuojantys labai išsiskiriančius savo kaina, turto vienetus yra labai nutolę nuo 
idealios linijos. Tai reiškia, kad modelis nesugeba deramai įvertini iškirtinio (pagal tam tikras savo savybes)
turto kainos.    

Apibendrinant, galima pasakyti, kad modelis "pagauna" bendrą tendenciją, bet jam yra sunku įvertinti 
kažkuo išskirtinius, ypatingai ženkliai nuo kitų brangesnius turto vienetus. 


- Linear Regression

Naudojamos technologijos

- Python
- Pandas: Biblioteka duomenų analizei.
- Scikit-learn: Biblioteka, skirta mašininio mokymosi modelių kūrimui ir duomenų normalizavimui.
- SQLite3: Integruota duomenų bazė skirta duomenų saugojimui.
- Matplotlib: Biblioteka grafikų braižymui.

Pagrindiniai žingsniai

- Duomenų nuskaitymas: Nuskaitomi duomenys iš duomenų bazės ir sudaromas DataFrame.

- Duomenų dalijimas: Duomenys dalijami į mokymo ir testavimo rinkinius.

- Modelio sukurimas: Sukuriamas tiesinės regresijos modelis ir yra yra mokomas naudojant mokymo rinkinį

![code_20240506_193112_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/c72ee9c2-48ba-4e45-83b9-850e87ff237b)

- Modelio vertinimas: Modelio veikimas yra įvertinamas naudojant testavimo rinkinį.

![code_20240506_193222_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/f77d167e-0a3d-433f-be5a-9aba8d1c7cea)

- Rezultatų vizualizavimas: Modelio spėjimų ir realių kainų koreliacija yra vizualizuojama grafike.

![code_20240506_193256_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/52d1e4ce-266d-4d70-a41d-78c6fd59cd2a)
![image](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/368e0a4b-41e7-4784-89cc-8c31bdb09d3b)

Išvados
Įveritnus gautą grafiką, ir modelio veikimo rodiklių rezultatus, galima daryti išvadas, kad
modelis duoda panašų, bet kiek prastesnį rezultatą, nei Random Forest Regresssion modelis.
Bendra tendencija yra pagaunama, modeliui sekasi neblogai prognozuoti žemėsnės kainos ir standartinį 
turtą, bet sunkiau yra su brangesniu turtu. Matome, kad tokios prognozės yra netikslios. 

![Screenshot 2024-05-06 at 19 39 12](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/4a11b7c8-2aa4-4f54-963e-d21e96bfdeef)

- Sequential

Šis modelis yra sukurtas naudojant giliojo mokymosi techniką ir apmokomas naudojant tuos pačius
mokymo ir testavimo duomenų rinkinius.

Naudojamos technologijos

- Python
- TensorFlow: Giliojo mokymosi įrankių biblioteka.
- Scikit-learn: Biblioteka modelių vertinimui.
- SQLite3: Integruota duomenų bazė skirta duomenims saugoti.
- Pandas: Biblioteka duomenų  analizei.
- Matplotlib ir Seaborn: Bibliotekos vizualizacijai.

Pagrindiniai žingsniai

- Duomenų nuskaitymas: Duomenys yra nuskaitomi iš duomenų bazės ir sudaromas DataFrame.
- Duomenų dalijimas: Duomenys yra padalinami į mokymo ir testavimo rinkinius.
  Pirmieji du žingsniai analogiški prieš tai aprašytuose modeliuose
- Modelio kūrimas: Sukuriamas tiesinio regresijos modelis naudojant gilųjį mokymąsi.
- 
![code_20240506_210747_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/f9e8b6a8-274e-4a2b-be11-19ef2c0caae9)
  
- Modelio mokymas: Modelis yra mokomas su mokymo rinkiniu.
- 
![code_20240506_210845_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/5a27470d-efa9-4d29-9661-0218c4f92fdc)

- Modelio vertinimas: Modelio veikimas yra įvertinamas naudojant testavimo rinkinį.

  ![code_20240506_210919_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/f87d443d-1062-4f70-939b-458b72ae7ca9)

- Rezultatų vizualizavimas: Modelio spėjimų ir realių kainų koreliacija yra vizualizuojama.
  
![code_20240506_211223_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/f6748fa0-a01b-4b54-8cf3-e28dccc8d942)

![image](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/68f8a685-0f52-40d2-9854-aeb725161790)

![Screenshot 2024-05-06 at 21 33 38](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/55f4fdd2-5a09-4218-8e58-c1d3a100f5cc)

- Taip pat vizualizuojame mokymosi proceso nuostolių kreivė. Šis grafikas parodo, kad mokymo procesas vyksta 
sklandžiai, ir gaunamas tolygus rezultatas.

![code_20240506_210957_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/3fdfeb95-c109-4d50-8eb3-928cc062f1b9)

![image](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/8bb88842-86a5-4e82-99dd-7103fb8c04b5)

Išvados
Apibendrinant šio modelio veikimą, matome, kad rezultatas yra labai panašus į gautą
naudojant Random Forest regresijos modelį. Tiek grafikai, tiek rodikliai yra labai 
panašūs. Tiesa šis modelis parodė minimaliai geresnį rezultatą, ko pasekoje galime gauti
šiek tiek tikslesnį spėjimą. Šis modelis (kaip ir kiti, anksčiau apžvelgti), geriau prognozuoja pigesnės ir 
vidutinės klasės namų kainas, sunkiai sekasi su brangesnio turto vertinimu.

Tačiau įvertinant nekilnojamojo turto rinkos specifiką, galima teigti, jog prabangių 
NT vienetų kainai didžiausią įtaką turi veiksniai, kurie nėra skaitiškai įvardinti tarp požymių,
randamų mūsų duomenų rinkinyje. Tai gali būti ypatinga vieta mieste ar kokios nors kitos unikalios
savybės, realybėje nulemiančios ženkliai aukštesnę kainą. Tokie dalykai, savo ruožtu, nėra vertinami mūsų modelių.
Šios objektyvios priežastys nulemia galutinį pateiktų skaičiavimų rezultatų tiklsumą.

5. Prognozių generavimas

Prognozės bus generuojamos išsagojus geriausius tikslumo rodiklius pasiekusio modelio konfigūraciją (Sequential).
R2 rodiklis = 0.60, Vidutinė absoliuti paklaida = 60532.59. Tai reiškia, kad modelio suprognozuota kaina gali turėti
apie 60 tūkstančių eur. paklaidą.

Duomenys skaičiavimams pateiks vartotojai per interaktyvią sąsają. Tam, kad galėtų būti atlikti tisklūs skaičiavimai, 
pateiktus duomenys reikės apdoroti taip pat, kaip ir mūsų mokymui naudotą duomenų rinkinį. Tam tisklui ir buvo išsaugota
MinMax Scaler konfigūracija. 

Interaktyviai sąsajai sukurti naudosime Python web aplikacijų kurimo karkasą Flask. Taip vartotojai galės suvesti duomenys, 
matyti gautus rezultatus, ir susipažinti su tam tikrais statistiniais rodikliais.

6. Vizualinis pateikimas

Kaip ir aprašyta aukščiau, rezultatų ir skaičiavimų pateikimui bus naudojamas Flask. Šio įrankio pagalba
sukurta paprasta WEB aplikacija, sukuriančia paprastą sąsają informacijai vartotojui pateikti.

Naudojamos technologijos

- Python
- Flask: Python web aplikacijų karkasas.
- TensorFlow: Giliojo mokymosi įrankių biblioteka.
- Scikit-learn: Biblioteka modelių vertinimui.
- SQLite3: Integruota duomenų bazė skirta duomenims saugoti.
- Pandas: Biblioteka duomenų analizei.
- NumPy:
- Matplotlib ir Seaborn: Bibliotekos vizualizacijai.

Pagrindiniai žingsniai

- Duomenų užkrovimas: Užkraunami išsaugoti modelis ir normalizacijos skalė.

![code_20240506_215649_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/c215b66c-a9e3-4214-b54e-3c4d9bee9d78)

- Vartotojo sąsaja: Sukuriama vartotojo sąsaja, kurioje vartotojas gali įvesti namo charakteristikas.

![code_20240506_215743_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/722c33f3-346f-4ee4-be5e-a5b86d11c2e4)

- Duomenų apdorojimas: Įvesti duomenys koduojami ir normalizuojami, kad būtų galima juos naudoti modelyje.

![code_20240506_223311_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/1afb18e2-b1ac-4dea-90fe-3d18b6a4dfb4)

- Prognozavimas: Prognozuojama namo kaina pagal įvestus duomenis. Ir prognozes išvedame naujame lange, kartu nurodant
  ir to paties miesto vidutinę namų kainą, bei vidutinę kainą už kvadratinį metrą, kad vartotjas galėtų palyginti,
  kaip jo įvestos reikšmes daro įtaką galutinei prognozuotai kainai, lyginant su vidurkiu. Kartu atvaizduojami
  pasirinkti parametrai
  
![code_20240506_223613_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/b82f14ff-eb60-4ea4-b189-e18429b304bc)


- Statistika: Vartotojas gali peržiūrėti statistinius duomenis apie nekilnojamąjį turtą iš naudojamo duomenų rinkinio.
  Statistiniai duomenys išvedami naujame lape, pateikia grafikus apie vidutinę kvadratinio metro kainą, vidutinį namų dydį bei vidutinį
  sklypo dydi.

  ![code_20240506_223901_via_10015_io](https://github.com/aMiroslav/BaigiamasisDarbas/assets/163419923/c7e0126b-c353-4922-969b-ba01219ff06f)

Siekiant neapsunkinti kodo, statistiniai rodiklai yra skaičiuojami atskirame faile: Statisne_analize.py

Pagrindiniai failai, užtikrinantys Flask aplikacijos veikimą:

- index.html: Pagrindinis puslapis, kuriame vartotojas įveda duomenis.
- result.html: Puslapis, kuriame pateikiama prognozuojama kaina.
- statistics.html: Puslapis, kuriame vartotojas gali peržiūrėti statistinius duomenis.
- error.html: Puslapis, kuriame rodomas klaidos pranešimas, jei įvyksta klaida vykdant prognozę.
 
