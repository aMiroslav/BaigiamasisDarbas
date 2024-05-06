import tensorflow as tf
from sklearn.metrics import r2_score, mean_absolute_error, explained_variance_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.callbacks import EarlyStopping

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
    # Nustatome X ir y
X = df.drop(['Kaina'], axis=1)
y = df['Kaina']

    # Padaliname duomenų rinkinį į testatavimo ir mokymo dalis
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.31, random_state=42)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

    # Sukuriame modelį su įvairiais sluoksniais
model = Sequential()
model.add(Dense(63, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(126, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(252, activation='relu'))
model.add(Dense(504, activation='relu'))
model.add(Dense(252, activation='relu'))
model.add(Dense(126, activation='relu'))
model.add(Dense(63, activation='relu'))
model.add(Dense(1))

    # Nustatome early stopping parametrus
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Kompiliuojame modelį
model.compile(optimizer='adam', loss='mae')
model.fit(x=X_train, y=y_train.values, validation_data=(X_test, y_test.values), batch_size=256, epochs=400,
          callbacks=[early_stopping])

    # Apskaičiuojame ir vizualizuojame modelio mokymo nuostolius
loss = pd.DataFrame(model.history.history)
plt.figure(figsize=(15, 5))
sns.lineplot(data=loss, lw=3)
plt.xlabel('Epocha')
plt.ylabel('Nuostoliai')
plt.title('Mokymosi nuostoliai pagal Epochas')
sns.despine()
plt.show()

    # Apskaičiuojame modelio veikimo, tikslumo rodiklius
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
evs = explained_variance_score(y_test, y_pred)
print(f'Vidutinė absoliuti paklaida (MAE): {mae}')
print(f'R2 rodiklis: {r2}')
print(f'Variance Regression rodiklis: {evs}')



    # Vizualizuojame modelio prognozes
y_pred = model.predict(X_test)
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.5, label='Modelio spėjimai')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Ideali prognozė')
plt.title(f'Santykis tarp tikros ir prognozuotos kainos. R2 = {r2:.2f}')
plt.xlabel('Tikra kaina, EUR')
plt.ylabel('Prognozuota kaina, EUR')
plt.ticklabel_format(style='plain')
plt.legend()
plt.show()

    # Išsaugome modelį
model.save('price_prediction_sequential.keras')
print("Modelio konfigūracija išsaugota")

    # Išvados
"""
Apibendrinant šio modelio veikimą, matome, kad rezultatas yra labai panašus į gautą
naudojant Random Forest regresijos modelį. Tiek grafikai, tiek rodikliai yra labai 
panašūs. Tiesa šis modelis parodė minimaliai geresnį rezultatą, ko pasekoje galime gauti
šiek tiek tikslesnį spėjimą. Šis modelis (kaip ir kiti, anksčiau apžvelgti), geriau prognozuoja pigesnės ir 
vidutinės klasės namų kainas, sunkiai sekasi su brangesnio turto vertinimu.

Tačiau įvertinant nekilnojamojo turto rinkos specifiką, galima teigti, jog prabangių 
NT vienetų kainai didžiausią įtaką turi veiksniai, kurie nėra skaitiškai įvardinti tarp požymių,
randamų mūsų duomenų rinkinyje. Tai gali būti ypatinga vieta mieste ar kokios nors kitos unikalios
savybės, realybėje nulemiančios ženkliai aukštesnę kainą. Tokie dalykai, savo ruožtu, nėra vertinami mūsų modelių.
Šios objektyvios priežastys nulemia galutinį pateiktų skaičiavimų rezultatų tiklsumą."""
