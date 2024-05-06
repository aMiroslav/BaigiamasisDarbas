import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
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

    # Nustatome mūsų duomenys ir tikslą (features, target)
X = df.drop(['Kaina'], axis=1)
y = df['Kaina']

    # Padaliname duoemnų rinkinį į mokymo ir testavimo dalis
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Sukuriame modelį
model = LinearRegression()
model.fit(X_train, y_train)

    # Išvedame modelio tikslumo parametrus
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Vidutinė absoliuti paklaida (MAE): {mae}')
print(f'R2 rodiklis: {r2}')

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

    # Išvados
"""  
Įveritnus gautą grafiką, ir modelio veikimo rodiklių rezultatus, galima daryti išvadas, kad
modelis duoda panašų, bet kiek prastesnį rezultatą, nei Random Forest Regresssion modelis.
Bendra tendencija yra pagaunama, modeliui sekasi neblogai prognozuoti žemėsnės kainos ir standartinį 
turtą, bet sunkiau yra su brangesniu turtu. Matome, kad tokios prognozės yra netikslios. """