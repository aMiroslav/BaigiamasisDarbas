import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd

    # Inicializuojame WebDriver'į
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)


    # Funkcija skirta nuspausti sutikimo su slapukais mygtukui
def accept_cookies():
    try:
        accept_cookies_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler'))
        )
        accept_cookies_btn.click()
        print('Slapukų sutikimo mygtukas paspaustas')
    except TimeoutException:
        print('Slapukų sutikimo mygtukas nerastas.')


    # Funkcija, skirta  duomenims paimti iš puslapio
def scrape_page_data(link):
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Surandame adresą ir kainą
    address = soup.find('h1', class_='obj-header-text')
    if address:
        address_text = address.text.strip()
    else:
        print("Objekto adresas nerastas")

    price = soup.find('span', class_='price-eur')
    if price:
        price_text = price.text.strip()
    else:
        print("Objekto kaina nerasta")

    # Surandame aprašymo lauką su visais atributai
    description = soup.find('dl')
    if description:

        # Ištraukiame atribūtų pavadinimus ir jų vertes
        att_names = [dt.get_text(strip=True) for dt in description.find_all('dt')]
        att_values = [dd.get_text(strip=True) for dd in description.find_all('dd')]

        # Sukuriame žodyną išgautiems duomenims
        page_data = {'Adresas': address_text, 'Kaina': price_text}
        page_data.update(zip(att_names, att_values))

        return page_data
    else:
        print("Objekto aprašymas nerastas")


    # Pagrindinė funkcija skirta duomenims išgauti ir išsaugoti
def scrape_and_save(start_page, end_page):
    all_pages_data = []

    # Naudojame for loop, ir iteruojame per visus puslapius su mus dominančiais paieškos rezultatais
    for page_number in range(start_page, end_page + 1):

        # Pradinis puslapis, nuo kurio pradedame
        target = f'https://www.aruodas.lt/namai/kaune/puslapis/{page_number}/?FRegionArea=63'
        links = []

        # nuskaitome puslapio html
        driver.get(target)
        accept_cookies()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if soup:
            # randame eilutes, kuriose saugomos nuorodos į objektus
            rows = soup.find_all('div', class_='list-adress-v2')[2:]

            # Ištraukiame ir išsaugome nuorodas
            if rows:
                for row in rows:
                    link_part = row.find('h3')
                    if link_part:
                        link = link_part.find('a')['href']
                        links.append(link)
                    else:
                        print('Nerasta HTML eilutė su linku.')
            else:
                print("Nerasta <'div', class_='list-adress-v2'> eilute")

            # Kiekvienai išsaugotai nuorodai pritaikome duomenų paėmimo funkciją ir sukuriame atskirą DataFrame objektą
            # kiekvienam puslapiui
            page_df = []
            for link in links:
                page_data = scrape_page_data(link)
                one_page_df = pd.DataFrame([page_data])
                page_df.append(one_page_df)

            # Sujungiame naujai išgauto puslapio DF su jau prieš tai sukurtu
            if page_df:
                df = pd.concat(page_df, ignore_index=True)
                all_pages_data.append(df)
                print(f'Puslapis {page_number} išsaugotas')
            else:
                print(f'Puslapio {page_number} nepavyko išsaugoti')
        else:
            print('Nepavyko nuskaityti puslapio HTML')

    # Sudarome galutinį DF
    final_df = pd.concat(all_pages_data, ignore_index=True)

    # Išsaugome CSV
    final_df.to_csv('namai_kaunas.csv', index=False)
    print(f'Duomenys sėkmingai išsaugoti')


    # Nustatome puslapius, iš kurių trauksime duomenys
start_page = 1
end_page = 47

    # Paleidžiame pagrindinę funkciją
scrape_and_save(start_page, end_page)

    # Atlikus užduotį, uždarome WebDraiverį
driver.quit()