# Importăm bibliotecile necesare
import os
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Definim calea fișierului de intrare și fișierul de ieșire
file_path = r'F:\Python\ML\date_sen_agregat.xlsx'  # Calea fișierului care conține datele existente
output_file = r'F:\Python\ML\decembrie_2024.xlsx'  # Calea fișierului de ieșire unde vor fi salvate predicțiile

# Verificăm dacă fișierul de intrare există
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")  # Aruncăm eroare dacă fișierul nu există

# Încercăm să citim fișierul Excel
try:
    data = pd.read_excel(file_path, engine='openpyxl')  # Citim fișierul Excel cu datele
    print("Columns in the DataFrame:", data.columns)  # Afișăm coloanele din DataFrame pentru verificare
except Exception as e:
    raise IOError(f"Error reading the Excel file: {e}")  # Aruncăm eroare în caz de problemă la citire

# Convertim coloana 'Data' în format datetime
data['Data'] = pd.to_datetime(data['Data'], dayfirst=True)  # Convertim formatul datei

# Filtrăm datele pentru luna decembrie
dec_data = data[data['Data'].dt.month == 12]  # Selectăm doar datele din decembrie

# Definim variabilele de intrare și ținta
X = dec_data.drop(['Data', 'Sold[MW]'], axis=1)  # Variabilele de intrare: toate coloanele, cu excepția 'Data' și 'Sold[MW]'
y = dec_data['Sold[MW]']  # Variabila țintă: 'Sold[MW]'

# Convertim toate datele în format numeric și înlocuim valorile lipsă cu 0
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)  # Convertim în format numeric și umplem valorile lipsă cu 0
y = pd.to_numeric(y, errors='coerce').fillna(0)  # Convertim și pentru variabila țintă 'y'

# Împărțim datele în seturi de antrenament și test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # 80% pentru antrenament și 20% pentru testare

# Creăm și antrenăm modelul de regresie folosind un arbore de decizie
tree = DecisionTreeRegressor(criterion='squared_error', random_state=42)  # Definim arborele de decizie
tree.fit(X_train, y_train)  # Antrenăm modelul pe setul de antrenament

# Realizăm predicțiile pe setul de test
y_pred = tree.predict(X_test)  # Predicțiile modelului pe setul de test

# Calculăm eroarea pătratică medie (MSE) pentru evaluarea modelului
mse = mean_squared_error(y_test, y_pred)  # Calculăm eroarea pătratică medie
print(f"Mean Squared Error on test set: {mse:.2f}")  # Afișăm eroarea pe setul de test

# Cream un interval de date pentru luna decembrie 2024
dates_dec_2024 = pd.date_range(start='2024-12-01', end='2024-12-31', freq='D')  # Generăm datele pentru decembrie 2024
placeholder_data = pd.DataFrame({'Data': dates_dec_2024})  # Creăm un DataFrame cu aceste date

# Pentru fiecare zi din decembrie, calculăm media valorilor corespunzătoare
for day in range(1, 32):  # Iterăm pentru fiecare zi din decembrie (1-31)
    day_data = dec_data[dec_data['Data'].dt.day == day]  # Selectăm datele pentru ziua respectivă
    if not day_data.empty:  # Dacă există date pentru ziua respectivă
        for col in X.columns:  # Pentru fiecare coloană de intrare
            placeholder_data.loc[placeholder_data['Data'].dt.day == day, col] = day_data[col].mean()  # Calculăm media pentru acea zi

# Pregătim datele de intrare pentru predicție
december_X = placeholder_data.drop(['Data'], axis=1)  # Eliminăm coloana 'Data'
december_X = december_X.apply(pd.to_numeric, errors='coerce').fillna(0)  # Convertim în numeric și înlocuim valorile lipsă cu 0

# Realizăm predicțiile pentru luna decembrie 2024
placeholder_data['Sold_Pred'] = tree.predict(december_X)  # Adăugăm predicțiile pentru 'Sold[MW]'

# Formatează datele în formatul dorit (dd-mm-yyyy)
placeholder_data['Data'] = placeholder_data['Data'].dt.strftime('%d-%m-%Y')  # Formatăm data pentru afișare

# Verificăm dacă fișierul de ieșire există și, dacă da, îl ștergem
if os.path.exists(output_file):
    os.remove(output_file)  # Ștergem fișierul existent pentru a nu-l suprascrie accidental

# Salvăm predicțiile într-un fișier Excel
placeholder_data.to_excel(output_file, index=False, engine='openpyxl')  # Salvăm rezultatele într-un fișier Excel
print(f"Predicțiile pentru decembrie 2024 au fost salvate în {output_file}")  # Afișăm mesajul că predicțiile au fost salvate
