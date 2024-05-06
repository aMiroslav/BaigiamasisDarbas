from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, cross_val_score
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


    # Prisijungiame prie duomenų bazės
conn = sqlite3.connect('nt_lt.db')
c = conn.cursor()

    # Pasirenkame visus duomenys iš lentelės
c.execute("""SELECT * FROM namai_pardavimui""")
column_names = [description[0] for description in c.description]

    # Sukūriame DF ir uždarome prisijungimą prie DB
df = pd.DataFrame(c.fetchall(), columns=column_names)
c.close()
conn.close()

    # Nustatome mūsų duomenys ir tikslą (features, target)
X = df.drop(['Kaina'], axis=1)
y = df['Kaina']

    # Padaliname duoemnų rinkinį į mokymo ir testavimo dalis
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)

    # Nustatome hiperparamtrų tinklelį
param_grid = {
    'n_estimators': [150], # [25, 50, 100, 125, 150],
    'max_depth': [None], #[None, 5, 10, 15, 20],
    'min_samples_split': [2], #[2, 3, 5, 7, 10],
    'min_samples_leaf': [5] #[1, 2, 3, 4, 5]
}

    # Sukuriame Grid Search objektą
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                           param_grid=param_grid,
                           cv=6,
                           verbose=2,
                           n_jobs=-1)

    # Atliekame geriausių parametrų paiešką
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
print("Geriausi hiperparametrai:", best_params)

    # Pritaikome geriausius hiperparamtrus regresijos modeliui
best_regressor = RandomForestRegressor(random_state=42, **best_params)

    # Atliekame kryžminį patikrinimą
cv_scores = cross_val_score(best_regressor, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
cv_mse = -cv_scores.mean()
print("Kryžminio patikrinimo Vidutinė Kvadratine Paklaida (MSE):", cv_mse)

    # Apmokome modelį
best_regressor.fit(X_train, y_train)

    # Įvertiname modelio veikima su testiniais duomenimis
y_pred = best_regressor.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Testinio duomenų rinkinio Vidutinė Kvadratine Paklaida (MSE): {mse:.2f}")
r2 = r2_score(y_test, y_pred)
print(f"R2: {r2}")

    # Vizualizuojame modelio spėjimų ir tikrųjų verčių koreliaciją
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.5, label="Modelio spėjimai")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Ideali prognozė')
plt.title(f'Santykis tarp tikros ir prognozuotos kainos. R2 = {r2:.2f}')
plt.xlabel('Tikra kaina, EUR')
plt.ylabel('Prognozuota kaina, EUR')
plt.ticklabel_format(style='plain')
plt.legend()
plt.show()

    # Skaičiuojame rodiklių svarbą galutiniam modelio sprendimui
    # Sukuriame žodyna, kodotiems stulpeliams sujungti
cat_features = {
    'Miestas:': ['Miestas:_Alytaus r.', 'Miestas:_Alytus','Miestas:_Kaunas', 'Miestas:_Kauno r.', 'Miestas:_Klaipėda',
                 'Miestas:_Klaipėdos r.', 'Miestas:_Panevėžio r.',  'Miestas:_Panevėžys',
                 'Miestas:_Vilniaus r.', 'Miestas:_Vilnius', 'Miestas:_Šiauliai', 'Miestas:_Šiaulių r.'],
'Įrengimas:': ['Įrengimas:_Dalinė apdaila', 'Įrengimas:_Kita', 'Įrengimas:_Nebaigtas statyti',  'Įrengimas:_Neįrengtas',
               'Įrengimas:_Pamatai', 'Įrengimas:_Įrengtas'],
'Namo tipas:': ['Namo tipas:_Kita (nukeliamas, projektas, kt.)', 'Namo tipas:_Namas (gyvenamasis)',
                'Namo tipas:_Namo dalis', 'Namo tipas:_Sodo namas',  'Namo tipas:_Sodyba',
                'Namo tipas:_Sublokuotas namas'],
'Vanduo:': ['Vanduo:_Artezinis',  'Vanduo:_Kita', 'Vanduo:_Miesto vandentiekis',  'Vanduo:_Vietinis vandentiekis',
            'Vanduo:_nepateikta', 'Vanduo:_Šulinys'],
'Šildymas:': ['Šildymas:_Aeroterminis',  'Šildymas:_Centrinis', 'Šildymas:_Centrinis kolektorinis', 'Šildymas:_Dujinis',
              'Šildymas:_Elektra', 'Šildymas:_Geoterminis', 'Šildymas:_Kietu kuru',
              'Šildymas:_Kita', 'Šildymas:_Saulės energija', 'Šildymas:_Skystu kuru'],
'Energijos kl.:': ['Pastato energijos suvartojimo klasė:_A',
                                         'Pastato energijos suvartojimo klasė:_A+',
                                         'Pastato energijos suvartojimo klasė:_A++',
                                         'Pastato energijos suvartojimo klasė:_B',
                                         'Pastato energijos suvartojimo klasė:_C',
                                         'Pastato energijos suvartojimo klasė:_D',
                                         'Pastato energijos suvartojimo klasė:_E',
                                         'Pastato energijos suvartojimo klasė:_F',
                                         'Pastato energijos suvartojimo klasė:_G',
                                         'Pastato energijos suvartojimo klasė:_nepateikta'],
'Patato tipas:': ['Pastato tipas:_Blokinis', 'Pastato tipas:_Karkasinis', 'Pastato tipas:_Kita',
                  'Pastato tipas:_Medinis', 'Pastato tipas:_Monolitinis', 'Pastato tipas:_Mūrinis',
                  'Pastato tipas:_Rąstinis', 'Pastato tipas:_Skydinis']
}
cat_importance = {}

    # Verčių apskaičiavimas
feature_importances = best_regressor.feature_importances_
feature_importance_df = pd.DataFrame({'Rodiklis': X.columns, 'Svarba': feature_importances})
feature_importance_df = feature_importance_df.sort_values(by='Svarba', ascending=False)

    # Grupuojame kategorinius stulpelius
for feat, values in cat_features.items():
    importance_sum = 0
    for value in values:
        if value in feature_importance_df['Rodiklis'].values:
            importance_sum += feature_importance_df.loc[feature_importance_df['Rodiklis'] == value, 'Svarba'].values[0]
    cat_importance[feat] = importance_sum

    # Sukuriame kategorinių ir skaitinių rodiklių DF
cat_importance_df = pd.DataFrame(cat_importance.items(), columns=['Rodiklis', 'Svarba'])

num_features = ['Plotas:', 'Sklypo plotas:', 'Kambarių sk.:', 'Statybos Metai:']
num_importance_df = feature_importance_df[feature_importance_df['Rodiklis'].isin(num_features)]

    # Sujungiame kategorinį ir skaitinį DF, bei surūšiuojame
feat_importances_grouped = pd.concat([cat_importance_df, num_importance_df])
feat_importances_grouped = feat_importances_grouped.sort_values(by='Svarba', ascending=False)
print('Rodiklių svarba prognozuojant kainą:')
print(feat_importances_grouped)


    # Atvaizduojame rezultatus
plt.figure(figsize=(10, 6))
plt.barh(feat_importances_grouped['Rodiklis'], feat_importances_grouped['Svarba'], color='skyblue', height=0.5)
plt.xlabel('Svarba')
plt.ylabel('Rodiklis')
plt.title('Rodiklių įtaka namo kainai')
plt.gca().invert_yaxis()
plt.show()

    # Išvados
"""
Pateiktas grafikas nurodo santyki tarp modelio prognozuotų ir realių kainų. Kiekvienas taškelis reprezentuoja
vieną turto vienetą. Raudona įstriža linija demonstruoja idealią teorinę prognozę (mūsų siekiamybę).
Taškų atstumas iki linijos norodo paklaidos dydį mūsų spėjimuose.

Iš grafiko galima spręsti, kad modelis veikia geriau, prognazuojant pigesnio turto kainas.
Kai kurie taškai, reprezentuojantys labai išsiskiriančius savo kaina, turto vienetus yra labai nutolę nuo 
idealios linijos. Tai reiškia, kad modelis nesugeba deramai įvertini iškirtinio (pagal tam tikras savo savybes)
turto kainos.    

Apibendrinant, galima pasakyti, kad modelis "pagauna" bendrą tendenciją, bet jam yra sunku įvertinti 
kažkuo išskirtinius, ypatingai ženkliai nuo kitų brangesnius turto vienetus. 
"""