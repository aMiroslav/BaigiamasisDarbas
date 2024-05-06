import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

STATIC_DIR = 'static'

    # Prisijungiame prie duomenų bazės
conn = sqlite3.connect('nt_lt.db')
c = conn.cursor()

    # Pasirenkame visus duomenys iš lentelės
c.execute("""SELECT * FROM namai_pardavimui_not_scaled""")
column_names = [description[0] for description in c.description]

    # Sukūriame DF ir uždarome prisijungimą prie DB
df = pd.DataFrame(c.fetchall(), columns=column_names)
c.close()
conn.close()

def calculate_mean_values(city):
    avg_house_price = df[df['Miestas:'] == city]['Kaina'].mean()
    avg_city_price_per_m2 = df[df['Miestas:'] == city]['Kaina už m2.:'].mean()

    return int(avg_house_price), int(avg_city_price_per_m2)

    # Skaičiuojame vidutinę kiekvieno miesto kvadratinio metro kainą
df['Kaina už m2.:'] = (df['Kaina'] / df['Plotas:']).round(2)
avg_price_per_m2 = df.groupby('Miestas:')['Kaina už m2.:'].mean().astype(int)
print('Vidutinė kvadratinio metro kaina pagal miestus:')
print(avg_price_per_m2)

def show_price_per_m2(avg_price_per_m2):
    try:
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=avg_price_per_m2.index, y=avg_price_per_m2.values, color='blue')
        plt.title('Vidutinė kvadratinio metro kaina')
        plt.xlabel('Miestas')
        plt.ylabel('kaina (EUR/m2)')
        plt.xticks(rotation=45)

        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        xytext=(0, 10),
                        textcoords='offset points')

        plt.tight_layout()

        # Generate a unique filename for each image
        image_filename = 'avg_price_per_m2.png'
        image_path = os.path.join(STATIC_DIR, image_filename)
        plt.savefig(image_path)
        plt.clf()

        # Return the path to the saved image
        return image_path
    except Exception as e:
        print(f"Error occurred while generating the plot: {e}")


    # Skaičiuojame vidutinį kiekvieno namo plotą, pagal miestą
avg_area = df.groupby('Miestas:')['Plotas:'].mean().astype(int)
print('Vidutinis namo dydis pagal miestus:')
print(avg_area)


def show_avg_area(avg_area):
    try:
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=avg_area.index, y=avg_area.values, color='green')
        plt.title('Vidutinis namo dydis')
        plt.xlabel('Miestas')
        plt.ylabel('Plotas (m2)')
        plt.xticks(rotation=45)

        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        xytext=(0, 10),
                        textcoords='offset points')

        plt.tight_layout()

        # Generate a unique filename for each image
        image_filename = 'avg_area.png'
        image_path = os.path.join(STATIC_DIR, image_filename)
        plt.savefig(image_path)
        plt.clf()

        # Return the path to the saved image
        return image_path
    except Exception as e:
        print(f"Error occurred while generating the plot: {e}")


    # Skaičiuojame vidutinį sklypo plotą, pagal miestą
avg_land_area = df.groupby('Miestas:')['Sklypo plotas:'].mean().astype(int)
print('Vidutinis sklypo dydis pagal miestus:')
print(avg_land_area)


def show_avg_land_area(avg_land_area):
    try:
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=avg_land_area.index, y=avg_land_area.values, color='orange')
        plt.title('Vidutinis sklypo dydis')
        plt.xlabel('Miestas')
        plt.ylabel('Plotas (a)')
        plt.xticks(rotation=45)

        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        xytext=(0, 10),
                        textcoords='offset points')

        plt.tight_layout()

        # Generate a unique filename for each image
        image_filename = 'avg_land_area.png'
        image_path = os.path.join(STATIC_DIR, image_filename)
        plt.savefig(image_path)
        plt.clf()

        # Return the path to the saved image
        return image_path
    except Exception as e:
        print(f"Error occurred while generating the plot: {e}")