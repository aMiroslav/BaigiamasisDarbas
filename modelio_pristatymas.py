from flask import Flask, render_template, request
from flask_caching import Cache
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
import joblib
from Statistine_analize import (calculate_mean_values, df, show_price_per_m2, show_avg_area, show_avg_land_area,
                                avg_price_per_m2, avg_area, avg_land_area)


# Inicializuojame flask aplikaciją.
app = Flask(__name__, static_url_path='/static')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    # Užkrauname išsaugotą modelį.
model = load_model('price_prediction_sequential.keras')

    # Duomenys tinkamam vartotojo įvesties kodavimui.
miestai = ['Alytaus r.', 'Alytus','Kaunas', 'Kauno r.', 'Klaipėda', 'Klaipėdos r.', 'Panevėžio r.',  'Panevėžys',
           'Vilniaus r.', 'Vilnius', 'Šiauliai', 'Šiaulių r.']
irengimo_lygiai = ['Dalinė apdaila', 'Kita', 'Nebaigtas statyti',  'Neįrengtas',  'Pamatai', 'Įrengtas']

namo_tipas =['Kita (nukeliamas, projektas, kt.)', 'Namas (gyvenamasis)', 'Namo dalis', 'Sodo namas',  'Sodyba',
             'Sublokuotas namas']

vanduo = ['Artezinis',  'Kita', 'Miesto vandentiekis',  'Vietinis vandentiekis', 'nepateikta', 'Šulinys']

sildymas = ['Aeroterminis',  'Centrinis', 'Centrinis kolektorinis', 'Dujinis', 'Elektra', 'Geoterminis', 'Kietu kuru',
            'Kita', 'Saulės energija', 'Skystu kuru',]

energijos_klase = ['A', 'A+', 'A++',  'B',  'C', 'D',  'E',  'F',  'G', 'nepateikta']

pastato_tipas = ['Blokinis', 'Karkasinis', 'Kita', 'Medinis', 'Monolitinis', 'Mūrinis', 'Rąstinis', 'Skydinis']

    # Kodojuoma kategorinius stulpelius, kad viskas sutaptų su mokymo duomenimis.

encoder_miestas = OneHotEncoder(sparse_output=False)
encoder_miestas.fit(np.array(miestai).reshape(-1, 1))

encoder_irengimas = OneHotEncoder(sparse_output=False)
encoder_irengimas.fit(np.array(irengimo_lygiai).reshape(-1, 1))

encoder_namo_tipas = OneHotEncoder(sparse_output=False)
encoder_namo_tipas.fit(np.array(namo_tipas).reshape(-1, 1))

encoder_vanduo = OneHotEncoder(sparse_output=False)
encoder_vanduo.fit(np.array(vanduo).reshape(-1, 1))

encoder_sildymas = OneHotEncoder(sparse_output=False)
encoder_sildymas.fit(np.array(sildymas).reshape(-1, 1))

encoder_energijos_klase = OneHotEncoder(sparse_output=False)
encoder_energijos_klase.fit(np.array(energijos_klase).reshape(-1, 1))

encoder_pastato_tipas = OneHotEncoder(sparse_output=False)
encoder_pastato_tipas.fit(np.array(pastato_tipas).reshape(-1, 1))

    # Užkrauname išsaugotą skaitinių reikšmių "scaler'į".
scaler = joblib.load('minmax_scaler.pkl')

    # Inicializuojame testines skaitmenių reikšmių vertes, kad turėtume tinkamą jų formą.
numerical_features = np.array([[0.0, 0.0, 0, 0]])
scaler.fit(numerical_features)


    # Generuojame pradinį puslapį, kuris gražina vartotojo įvestas reikšmes.
@app.route('/')
def index():
    return render_template('index.html',
                           cities=miestai,
                           irengimai=irengimo_lygiai,
                           namo_tipai=namo_tipas,
                           pastato_tipai=pastato_tipas,
                           energijos_klases=energijos_klase,
                           sildymai=sildymas,
                           vandens=vanduo)



# generuojame prognozavimo puslapį, kuris leidžia vartotojui įvesti parametrus. Parametrai koduojami ir normalizuojami
# taip pat, kaip ir buvo apdorojami mokymo duomenys.
@app.route('/predict', methods=['POST'])
def predict():
    try:
        scaler = joblib.load('minmax_scaler.pkl')

        # Vartotojo įvestys.
        plotas = float(request.form['Plotas:'])
        sklypo_plotas = float(request.form['Sklypo plotas:'])
        kambariai = int(request.form['Kambarių sk.:'])
        statybos_metai = int(request.form['Statybos Metai:'])
        miestas = request.form['Miestas:']
        irengimas = request.form['Įrengimas:']
        namo_tipas = request.form['Namo tipas:']
        vanduo = request.form['Vanduo:']
        sildymas = request.form['Šildymas:']
        energijos_klase = request.form['Energijos suvartojimo klase:']
        pastato_tipas = request.form['Pastato tipas:']

        avg_house_price, avg_city_price_per_m2 = calculate_mean_values(miestas)

        # Kodojuome kategorinius kintamuosius.
        miestas_encoded = encoder_miestas.transform(np.array(miestas).reshape(-1, 1))
        irengimas_encoded = encoder_irengimas.transform(np.array(irengimas).reshape(-1, 1))
        namo_tipas_encoded = encoder_namo_tipas.transform(np.array(namo_tipas).reshape(-1, 1))
        vanduo_encoded = encoder_vanduo.transform(np.array(vanduo).reshape(-1, 1))
        sildymas_encoded = encoder_sildymas.transform(np.array(sildymas).reshape(-1, 1))
        energijos_klase_encoded = encoder_energijos_klase.transform(np.array(energijos_klase).reshape(-1, 1))
        pastato_tipas_encoded = encoder_pastato_tipas.transform(np.array(pastato_tipas).reshape(-1, 1))

        # Sujungiame koduotus kategorinius duomenys.
        categorical_features_encoded = np.concatenate([miestas_encoded, irengimas_encoded, namo_tipas_encoded,
                                             vanduo_encoded, sildymas_encoded, energijos_klase_encoded,
                                             pastato_tipas_encoded], axis=1)

        # Sujungiame skaitinius duomenys.
        numerical_features = np.array([[plotas, sklypo_plotas, kambariai, statybos_metai]])

        # Sujungiame skaitinius ir kategorinius duomenys.
        features = np.concatenate([numerical_features, categorical_features_encoded], axis=1)

        # Normalizuojame skaitines reikšmes.
        features_scaled = scaler.transform(features)

        # Perduodame normalizuotus duomenys modeliui, darome prognozę.
        prediction = model.predict(features_scaled)
        round_prediction = int(prediction[0])

        price_m2 = int(round_prediction / plotas)

        # Grąžiname prognozės reikšmę.
        return render_template('result.html', prediction=round_prediction, miestas=miestas,
                               avg_house_price=avg_house_price, avg_city_price_per_m2=avg_city_price_per_m2,
                               selected_features={
                                   'Plotas, m²': plotas,
                                   'Sklypo plotas, a': sklypo_plotas,
                                   'Kambarių sk.': kambariai,
                                   'Statybos Metai': statybos_metai,
                                   'Miestas': miestas,
                                   'Įrengimas': irengimas,
                                   'Namo tipas': namo_tipas,
                                   'Vanduo': vanduo,
                                   'Šildymas': sildymas,
                                   'Energijos suvartojimo klase': energijos_klase,
                                   'Pastato tipas': pastato_tipas},
                               price_m2=price_m2,
                               )

    except Exception as e:
        # Jei ivyktų klaidą, hžgeneruojame klaidos pranešimą
        error_message = f"Įvyko klaida: {str(e)}"
        return render_template('error.html', error_message=error_message), 500

    # Generuojame statistikos rodiklių iįvedimo puslapį
@app.route('/statistics', methods=['GET', 'POST'])
def preview_statistics():
    if request.method == 'POST':
        selected_statistic = request.form['statistic']
        image_path = None
        if selected_statistic == 'avg_price_per_m2':
            image_path = show_price_per_m2(avg_price_per_m2)
        elif selected_statistic == 'avg_house_area':
            image_path = show_avg_area(avg_area)
        elif selected_statistic == 'avg_land_area':
            image_path = show_avg_land_area(avg_land_area)

        # Gražiname šabloną sugenerutiems statistiniams rodikliams atvaizduoti
        return render_template('statistics.html', selected_statistic=selected_statistic,
                               image_path=image_path)
    else:
        # Gražiname pradinį statistikos atvaizdavimo puslapį
        return render_template('statistics.html')


# Paleidžiame pagrindinę funkciją.
if __name__ == '__main__':
    app.run(port=8080)