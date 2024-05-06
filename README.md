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
![code_20240506_164746_via_10015_io.png](..%2F..%2FDownloads%2Fcode_20240506_164746_via_10015_io.png)

scrape_page_data(link) - funkcija skirta išgauti duomenims apie vieną nekilnojamojo turto objektą.
Iškviečiama pagrindinėje funkcijoje ir iteruojamą per kiekvieną atverčiamą puslpapį. 
Funkcija naudoja parametrą 'link' - puslpaio, iš kurio bus išgaunami duomenis, URL.
Funkcija gražiną 'page_data', žodyną, kuriame saugomi duomenys apie vieno NT objekto atributus
![code_20240506_165336_via_10015_io.png](..%2F..%2FDownloads%2Fcode_20240506_165336_via_10015_io.png)