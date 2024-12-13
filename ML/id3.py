import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pydotplus
from IPython.display import Image

# Calea către fișierul de date de intrare
file_path = r'F:\Python\ML\date_sen_agregat.xlsx'
# Calea către fișierul cu datele din decembrie 2024
decembrie_2024_path = r'F:\Python\ML\decembrie_2024.xlsx'

# Verificăm dacă fișierul de intrare există
print(f"File exists: {os.path.exists(file_path)}")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

try:
    # Încărcăm datele din fișierul Excel
    data = pd.read_excel(file_path, engine='openpyxl')
    print("Columns in the DataFrame:", data.columns)
except Exception as e:
    raise IOError(f"Error reading the Excel file: {e}")

# Convertim coloana 'Data' într-un tip datetime
data['Data'] = pd.to_datetime(data['Data'], dayfirst=True)
# Excludem datele din luna decembrie pentru antrenare
data = data[data['Data'].dt.month != 12]

# Definim coloanele de interes
columns = ['Consum[MW]', 'Medie Consum[MW]', 'Productie[MW]',
           'Carbune[MW]', 'Hidrocarburi[MW]', 'Ape[MW]', 'Nuclear[MW]',
           'Eolian[MW]', 'Foto[MW]', 'Biomasa[MW]', 'Sold[MW]']

# Verificăm dacă toate coloanele necesare există
missing_columns = [col for col in columns if col not in data.columns]
if missing_columns:
    raise KeyError(f"Missing columns in the DataFrame: {missing_columns}")

# Selectăm doar coloanele relevante
data = data[columns]

# Convertim coloana 'Sold[MW]' într-un tip numeric
data['Sold[MW]'] = pd.to_numeric(data['Sold[MW]'], errors='coerce')

# Creăm variabila categorică pentru 'Sold[MW]'
sold_categoric = []
for sold in data['Sold[MW]']:
    if pd.isna(sold):
        sold_categoric.append(np.nan)
    elif sold < -500:
        sold_categoric.append('Foarte mic')
    elif -500 <= sold < 0:
        sold_categoric.append('Mic')
    elif 0 <= sold < 500:
        sold_categoric.append('Mediu')
    elif 500 <= sold < 1000:
        sold_categoric.append('Mare')
    else:
        sold_categoric.append('Foarte mare')

sold_categoric = pd.Series(sold_categoric, index=data.index)

# Eliminăm valorile lipsă
data = data.dropna(subset=['Sold[MW]'])
sold_categoric = sold_categoric.dropna()

# Împărțim datele în seturi de intrare (X) și țintă (y)
X = data.drop(['Sold[MW]'], axis=1)
y = sold_categoric

# Convertim toate datele într-un format numeric valid
X = X.apply(pd.to_numeric, errors='coerce')
X = X.fillna(0)
y = y.astype(str)

# Împărțim setul de date în seturi de antrenament și testare
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creăm și antrenăm un model de arbore de decizie
tree = DecisionTreeClassifier(criterion='entropy', random_state=42)
tree.fit(X_train, y_train)

# Facem predicții și evaluăm acuratețea modelului
y_pred = tree.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuratețe pe setul de test: {accuracy:.2f}")

# Exportăm arborele de decizie într-un fișier PNG
dot_data = export_graphviz(tree, out_file=None,
                           feature_names=list(X.columns),
                           class_names=tree.classes_,
                           filled=True, rounded=True,
                           special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_png("decision_tree.png")
Image(graph.create_png())

# Dacă există date pentru decembrie 2024, le procesăm și facem predicții
if os.path.exists(decembrie_2024_path):
    december_data = pd.read_excel(decembrie_2024_path, engine='openpyxl')
    december_data['Data'] = pd.to_datetime(december_data['Data'], dayfirst=True)
    december_data = december_data[december_data['Data'].dt.month == 12]

    if not december_data.empty:
        december_X = december_data[columns[:-1]]
        december_X = december_X.apply(pd.to_numeric, errors='coerce').fillna(0)

        december_data['Sold_Pred'] = tree.predict(december_X)

        print("\n Predicții pentru luna decembrie 2024: \n")
        for index, row in december_data.iterrows():
            print(f"Ziua: {row['Data'].strftime('%d-%m-%Y')}, Predicție Sold[MW]: {row['Sold_Pred']}")
    else:
        print("Nu sunt date disponibile pentru decembrie 2024.")
else:
    print(f"Fișierul {decembrie_2024_path} nu a fost găsit.")
