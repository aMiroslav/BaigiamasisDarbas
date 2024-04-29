import pandas as pd
import re


        # Importuojame duomenis nuskaitydami anksčiau paruoštus CSV failus
df_vilnius = pd.read_csv('Duomenu_isgavimas/namai_vilnius.csv')
df_kaunas = pd.read_csv('Duomenu_isgavimas/namai_kaunas.csv')
df_klaipeda = pd.read_csv('Duomenu_isgavimas/namai_klaipeda.csv')
df_siauliai = pd.read_csv('Duomenu_isgavimas/namai_siauliai.csv')
df_panevezys = pd.read_csv('Duomenu_isgavimas/namai_panevezys.csv')
df_alytus = pd.read_csv('Duomenu_isgavimas/namai_alytus.csv')
df_palanga = pd.read_csv('Duomenu_isgavimas/namai_palanga.csv')
print('Duomenys nuskaityti.')

        # Sujungiame visus duomenis į vieną DataFrame
df = pd.concat([df_vilnius, df_kaunas, df_klaipeda, df_siauliai, df_panevezys, df_alytus, df_palanga],
               ignore_index=True)
print('Duomenų rinkiniai sujungti.')

        # Pašaliname besidubliuojančiu įrašus
df_no_duplicates = df.drop_duplicates()
df_no_duplicates.reset_index(drop=True, inplace=True)
print('Besidubliuojančios reokšmės pašalintos.')

        # Ištriname stulpelius, kurie nebus naudojami analizėje
df_cleaned = df_no_duplicates.drop(['Artimiausias vandens telkinys:', 'Iki vandens telkinio (m):', 'Ypatybės:',
                                    'Papildomos patalpos:', 'Papildoma įranga:', 'Apsauga:', 'Reklama:',
                                    'Reklama/pasiūlymas:', 'Namo numeris:', 'Kambarių sk.:', 'Aukštų sk.:',
                                    'Unikalus daikto numeris(RC numeris):'], axis=1)
print('Pašalinti analizėje nenaudojami stulpeliai.')

        # Kategoriniuose stulpeliuose, kuriuose trūksta verčių, įvedame naują kategoriją apie nepateiktus duomenys
df_cleaned.fillna({'Pastato energijos suvartojimo klasė:': 'nepateikta'}, inplace=True)
df_cleaned.fillna({'Vanduo:': 'nepateikta'}, inplace=True)
df_cleaned.fillna({'Šildymas:': 'nepateikta'}, inplace=True)
print('Sutvarkytos trūkstamos reikšmės.')

        # Patikriname ar duomenų rinkinyje neliko celių be reikšmių
nan_number = df_cleaned.isna().sum()
print("Trūkstamų reikšmių kiekis skirtinguose stulpeliuose:.")
print(nan_number)


    # Funkcija, skirta pašalinti nereikalingus ženklus iš langelių
def cleen_cell_to_number(text):
        numbers = re.sub(r'[^\d.,]', '', text)
        numbers = numbers.replace(',', '.')
        return numbers

  # Pritaikome funkciją ir konvertuojame duomenys į skaičius pasirinktuose stulpeliuose
df_cleaned['Kaina'] = df_cleaned['Kaina'].apply(cleen_cell_to_number)
df_cleaned['Kaina'] = pd.to_numeric(df_cleaned['Kaina'])

df_cleaned['Plotas:'] = df_cleaned['Plotas:'].apply(cleen_cell_to_number)
df_cleaned['Plotas:'] = pd.to_numeric(df_cleaned['Plotas:'])
df_cleaned['Plotas:'] = pd.to_numeric(df_cleaned['Plotas:']).round(2)

df_cleaned['Sklypo plotas:'] = df_cleaned['Sklypo plotas:'].apply(cleen_cell_to_number)
df_cleaned['Sklypo plotas:'] = pd.to_numeric(df_cleaned['Sklypo plotas:']).round(2)

print("Stulpelių 'Kaina', 'Plotas:' ir 'Sklypo plotas:' reikšmės pakeistos į skaitines.")

    # Sutvarkome datos stulpelį
df_cleaned['Statybos Metai:'] = df['Metai:'].apply(lambda x: int(re.search(r'\d+', x).group()))
df_cleaned.drop(['Metai:'], axis=1, inplace=True)
print("Sutvarkytas stulpelis 'Metai:', pakesitas į 'Statybos Metai:'.")

    # Adreso stulpelį pertvarkome į du atskirus: Miestas ir Rajonas
df_cleaned['Miestas:'] = df['Adresas'].str.split(',').str[0].str.strip()
df_cleaned['Rajonas:'] = df['Adresas'].str.split(',').str[1].str.strip()
df_cleaned.drop(['Adresas'], axis=1, inplace=True)
print("Sutvarkytas stulpelis 'Adresas', pakeistas į du naujus stulpelius: 'Miestas:', 'Rajonas:'.")