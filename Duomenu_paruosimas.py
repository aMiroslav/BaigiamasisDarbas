import sqlite3
import pandas as pd
import re


    # Importuojame duomenis nuskaitydami anksčiau paruoštus CSV failus
df_vil = pd.read_csv('Duomenu_isgavimas/namai_vilnius.csv')
df_kau = pd.read_csv('Duomenu_isgavimas/namai_kaunas.csv')
df_kl = pd.read_csv('Duomenu_isgavimas/namai_klaipeda.csv')
df_siau = pd.read_csv('Duomenu_isgavimas/namai_siauliai.csv')
df_pan = pd.read_csv('Duomenu_isgavimas/namai_panevezys.csv')
df_al = pd.read_csv('Duomenu_isgavimas/namai_alytus.csv')
print('Duomenys nuskaityti.')


    # Funkcija, skirta pašalinti nereikalingus ženklus iš langelių
def cleen_cell_to_number(text):
    numbers = re.sub(r'[^\d.,]', '', text)
    numbers = numbers.replace(',', '.')
    return numbers


    # Funkcija, skirta pašalinti ribinėms kainų reikšmėms
def remove_extreme_values(df):
    df['Kaina'] = df['Kaina'].apply(cleen_cell_to_number)
    df['Kaina'] = pd.to_numeric(df['Kaina'])
    df_sorted = df.sort_values(by='Kaina')
    df_trimmed = df_sorted.iloc[20:-20]
    return df_trimmed

    # Pritaikome funkciją ir pašaliname ribines reikšmes
df_vilnius = remove_extreme_values(df_vil)
df_kaunas = remove_extreme_values(df_kau)
df_klaipeda = remove_extreme_values(df_kl)
df_siauliai = remove_extreme_values(df_siau)
df_panevezys = remove_extreme_values(df_pan)
df_alytus = remove_extreme_values(df_al)

    # Sujungiame visus duomenis į vieną DataFrame
df = pd.concat([df_vilnius, df_kaunas, df_klaipeda, df_siauliai, df_panevezys, df_alytus],
               ignore_index=True)
print('Duomenų rinkiniai sujungti.')

    # Pašaliname besidubliuojančiu įrašus
df_no_duplicates = df.drop_duplicates()
df_no_duplicates.reset_index(drop=True, inplace=True)
print('Besidubliuojančios reokšmės pašalintos.')

    # Ištriname stulpelius, kurie nebus naudojami analizėje
df_cleaned = df_no_duplicates.drop(['Artimiausias vandens telkinys:', 'Iki vandens telkinio (m):', 'Ypatybės:',
                                    'Papildomos patalpos:', 'Papildoma įranga:', 'Apsauga:', 'Reklama:',
                                    'Reklama/pasiūlymas:', 'Namo numeris:', 'Aukštų sk.:',
                                    'Unikalus daikto numeris(RC numeris):', 'Pastato energijos suvartojimo klasė:',
                                    'Vanduo:', 'Šildymas:', 'Namo tipas:', 'Pastato tipas:'], axis=1)
print('Pašalinti analizėje nenaudojami stulpeliai.')

    # Pritaikome funkciją ir konvertuojame duomenys į skaičius pasirinktuose stulpeliuose

df_cleaned['Plotas:'] = df_cleaned['Plotas:'].apply(cleen_cell_to_number)
df_cleaned['Plotas:'] = pd.to_numeric(df_cleaned['Plotas:']).round(2)

df_cleaned['Sklypo plotas:'] = df_cleaned['Sklypo plotas:'].apply(cleen_cell_to_number)
df_cleaned['Sklypo plotas:'] = pd.to_numeric(df_cleaned['Sklypo plotas:']).round(2)

print("Stulpelių 'Plotas:' ir 'Sklypo plotas:' reikšmės pakeistos į skaitines.")

    # Apskaičiuojame vidutinį kambario plotą, remiantis esamais duomenimis
df_cleaned['Kambario plotas'] = df_cleaned['Plotas:'] / df_cleaned['Kambarių sk.:']
avg_room_space = df_cleaned['Kambario plotas'].mean()

    # Funkcija, skirta trūkstamoms stulpelio 'Kambarių sk.:' reikšmėms apskaičiuoti
def calculate_room_count(row):
    if pd.isna(row['Kambarių sk.:']):
        return round(row['Plotas:'] / avg_room_space)
    else:
        return row['Kambarių sk.:']
    # Pritaikome funkciją trūkstamoms reikšmėms užpildyti
df_cleaned['Kambarių sk.:'] = df_cleaned.apply(calculate_room_count, axis=1)
df_cleaned.drop(['Kambario plotas'], axis=1, inplace=True)
print("Sutvarkytas stulpelis 'Kambarių sk.:', trūkstamos reikšmės apskaičiuotos pagal vidutinį kambario plotą.")

    # Patikriname ar duomenų rinkinyje neliko celių be reikšmių
nan_number = df_cleaned.isna().sum()
print("Trūkstamų reikšmių kiekis skirtinguose stulpeliuose:.")
print(nan_number)

    # Sutvarkome datos stulpelį
df_cleaned['Statybos Metai:'] = df['Metai:'].apply(lambda x: int(re.search(r'\d+', x).group()))
df_cleaned.drop(['Metai:'], axis=1, inplace=True)
print("Sutvarkytas stulpelis 'Metai:', pakesitas į 'Statybos Metai:'.")

    # Adreso stulpelį pertvarkome į du atskirus: Miestas ir Rajonas
df_cleaned['Miestas:'] = df['Adresas'].str.split(',').str[0].str.strip()
df_cleaned.drop(['Adresas'], axis=1, inplace=True)
print("Sutvarkytas stulpelis 'Adresas', pakeistas į stulpelį: 'Miestas:'.")

    # Sutvarkome miestų pavadinimus stulpeliuose
all_cities = df_cleaned['Miestas:'].unique()
print("Unikalių reikšmių sąrašas stulpelyje 'Miestas:'")
print(all_cities)

df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Vilniaus m. sav.', 'Vilnius')
df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Šiaulių m. sav.', 'Šiauliai')
df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Alytaus k.', 'Alytaus r. sav.')
df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Vilniaus r. sav.', 'Vilniaus r.')
df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Kauno r. sav.', 'Kauno r.')
df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Klaipėdos r. sav.', 'Klaipėdos r.')
df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Panevėžio r. sav.', 'Panevėžio r.')
df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Šiaulių r. sav.', 'Šiaulių r.')
df_cleaned['Miestas:'] = df_cleaned['Miestas:'].replace('Alytaus r. sav.', 'Alytaus r.')


    #Sutvarkytų duomenų išsaugojimas duomenų bazėje
conn = sqlite3.connect('nt_lt.db')
c = conn.cursor()

df_cleaned.to_sql('namai_pardavimui', conn, if_exists='replace', index=False)
print('Duomenys išsaugoti duomenų bazėje.')
