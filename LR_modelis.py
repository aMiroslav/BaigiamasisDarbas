import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import sqlite3


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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    # Koduojame kategorinius kintamuosius mokymo ir testavimo rinkiniuose
X_combined = pd.concat([X_train, X_test])

for feature in categorical_features:
    X_combined[feature] = encoder.fit_transform(X_combined[feature])

X_train_encoded = X_combined[:len(X_train)]
X_test_encoded = X_combined[len(X_train):]

    # Standartizuojame skaitinius duomenis
X_train_encoded.loc[:, numerical_features] = scaler.fit_transform(X_train_encoded[numerical_features])
X_test_encoded.loc[:, numerical_features] = scaler.transform(X_test_encoded[numerical_features])

    # Sukuriame modelį
model = LinearRegression()
model.fit(X_train_encoded, y_train)

    # Išvedame modelio tikslumo parametrus
y_pred = model.predict(X_test_encoded)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'MSE: {mse}')
print(f"R2: {r2}")

    # Vizualizuojame modelio spėjimų ir tikrųjų verčių koreliaciją
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.5, label='Modelio spėjimai')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Ideali prognozė')
plt.title(f'Santykis tarp tikros ir prognozuotos kainos. R2 = {r2:.2f}')
plt.xlabel('Tikra kaina, EUR')
plt.ylabel('Prognozuota kaina, EUR')
plt.ticklabel_format(style='plain')
plt.legend()
plt.show()