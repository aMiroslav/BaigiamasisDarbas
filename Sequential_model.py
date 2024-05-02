import tensorflow as tf
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping
from keras import optimizers


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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    # Koduojame kategorinius kintamuosius mokymo ir testavimo rinkiniuose
categorical_features = ['Miestas:', 'Įrengimas:']
encoder = OneHotEncoder()
X_train_encoded = encoder.fit_transform(X_train[categorical_features])
X_test_encoded = encoder.transform(X_test[categorical_features])

    # Standartizuojame skaitinius kintamuosius
numerical_features = ['Plotas:', 'Sklypo plotas:', 'Statybos Metai:', 'Kambarių sk.:']
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[numerical_features])
X_test_scaled = scaler.transform(X_test[numerical_features])

    # Ssujungiame koduotus ir standartizuotus duomenis
X_train_final = np.hstack((X_train_encoded.toarray(), X_train_scaled))
X_test_final = np.hstack((X_test_encoded.toarray(), X_test_scaled))

    # Sukuriame modelį su įvairiais sluoksniais
model = Sequential()
model.add(Dense(1024, activation='relu', input_shape=(X_train_final.shape[1],)))
model.add(Dropout(0.4))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))


    # Nustatome Early stopping parametrus
early_stopping = EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True)

    # Mokome modelį
opt = optimizers.Adam(learning_rate=0.007)
model.compile(optimizer=opt, loss='mean_squared_error')
history = model.fit(X_train_final, y_train, epochs=200, batch_size=100, validation_split=0.05, callbacks=[early_stopping])

    # Išvedame modelio tikslumo parametrus
loss= model.evaluate(X_test_final, y_test)
print(f"Modelio praradimai: {loss}")
y_pred = model.predict(X_test_final)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'MSE: {mse}')
print(f"R2: {r2}")

    # Vizualizuojame modelio prognozes
y_pred = model.predict(X_test_final)
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.5, label='Modelio spėjimai')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Ideali prognozė')
plt.title(f'Santykis tarp tikros ir prognozuotos kainos. R2 = {r2:.2f}')
plt.xlabel('Tikra kaina, EUR')
plt.ylabel('Prognozuota kaina, EUR')
plt.ticklabel_format(style='plain')
plt.legend()
plt.show()