from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, cross_val_score
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

    # Surušiuojame duomenis į kategorinius ir skaitinius kintamuosius
categorical_features = ['Įrengimas:','Miestas:']
numerical_features = ['Plotas:', 'Kambarių sk.:', 'Sklypo plotas:', 'Statybos Metai:']

    # Nustatome kodavimo kintamuosius
encoder = LabelEncoder()
scaler = StandardScaler()

    # Nustatome mūsų duomenys ir tikslą (features, target)
X = df.drop(['Kaina'], axis=1)
y = df['Kaina']

    # Padaliname duoemnų rinkinį į mokymo ir testavimo dalis
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)

    # Koduojame kategorinius kintamuosius mokymo ir testavimo rinkiniuose
X_combined = pd.concat([X_train, X_test])

for feature in categorical_features:
    X_combined[feature] = encoder.fit_transform(X_combined[feature])

X_train_encoded = X_combined[:len(X_train)]
X_test_encoded = X_combined[len(X_train):]

    # Standartizuojame skaitinius duomenis
X_train_encoded.loc[:, numerical_features] = scaler.fit_transform(X_train_encoded[numerical_features]).astype(np.float64)
X_test_encoded.loc[:, numerical_features] = scaler.transform(X_test_encoded[numerical_features]).astype(np.float64)

    # Nustatome hiperparamtrų tinklelį
param_grid = {
    'n_estimators': [25, 50, 100, 125, 150],
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 3, 5, 7, 10],
    'min_samples_leaf': [1, 2, 3, 4, 5]
}

    # Sukuriame Grid Search objektą
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                           param_grid=param_grid,
                           cv=6,
                           verbose=2,
                           n_jobs=-1)

    # Atliekame geriausių parametrų paiešką
grid_search.fit(X_train_encoded, y_train)
best_params = grid_search.best_params_
print("Geriausi hiperparametrai:", best_params)

    # Pritaikome geriausius hiperparamtrus regresijos modeliui
best_regressor = RandomForestRegressor(random_state=42, **best_params)

    # Atliekame kryžminį patikrinimą
cv_scores = cross_val_score(best_regressor, X_train_encoded, y_train, cv=5, scoring='neg_mean_squared_error')
cv_mse = -cv_scores.mean()
print("Kryžminio patikrinimo Vidutinė Kvadratine Paklaida (MSE):", cv_mse)

    # Pritaikome geriausius hiperparametrus modeliui
best_regressor.fit(X_train_encoded, y_train)

    # Įvertiname modelio veikima su testiniais duomenimis
y_pred = best_regressor.predict(X_test_encoded)
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
feature_importances = best_regressor.feature_importances_
feature_importance_df = pd.DataFrame({'Rodiklis': X.columns, 'Svarba': feature_importances})
feature_importance_df = feature_importance_df.sort_values(by='Svarba', ascending=False)
print('Rodiklių svarba prognozuojant kainą:')
print(feature_importance_df)

    # Atvaizduojame rodiklių svarbą grafike
plt.figure(figsize=(18, 6))
plt.barh(feature_importance_df['Rodiklis'], feature_importance_df['Svarba'], color='skyblue', height=0.5)
plt.xlabel('Svarba')
plt.ylabel('Rodiklis')
plt.title('Rodiklių įtaka namo kainai')
plt.gca().invert_yaxis()
plt.show()

    # Išvados
"""
Pateiktas grafikas nurodo santyki tarp modelio prognozuotų ir realių kainų. Kiekvienas taškelis reprezentuoja
vieną turto vienetą. Raudona įstriža linija demonstruoja idealią teoriną prognozę (mūsų siekiamybę).
Taškų atstumas iki linijos norodo paklaidos dydį mūsų spėjimuose.

Iš grafiko galima spręsti, kad modelis veikia geriau, prognazuojant pigesnio turto kainas.
Kai kurie taškai, reprezentuojantys labai išsiskiriančius savo kaina, turto vienetus yra labai nutolę nuo 
idelaios linijos. Tai reiškia, kad modelis nesugeba deramai įvertini iškirtinio (pagal tam tikras savo savybes)
turto kainos.    

Apibendrinant, galima pasakyti, kad modelis "pagauna" bendrą tendenciją, bet jam yra sunku įvertinti 
kažkuo išskirtinius, ypatingai ženkliai nuo kitų brangesnius turto vienetus. 
"""