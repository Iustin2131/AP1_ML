import pandas as pd

# Citim fișierul cu datele agregate
file_path = 'date_sen_agregat.xlsx'  # Modifică cu calea fișierului tău
data = pd.read_excel(file_path, engine='openpyxl')

# Convertim coloana de date în format datetime
data['Data'] = pd.to_datetime(data['Data'], dayfirst=True)

# Filtrăm doar datele pentru luna decembrie
data_decembrie = data[data['Data'].dt.month == 12].copy()

# Grupăm după ziua lunii și calculăm media
data_decembrie.loc[:, 'Ziua'] = data_decembrie['Data'].dt.day  # Extragem ziua lunii
medie_istorica_decembrie = data_decembrie.groupby('Ziua')['Sold[MW]'].mean()

# Afișăm rezultatele
print("Media istorică a soldului energetic pentru fiecare zi din decembrie:")
print(medie_istorica_decembrie)

# Salvăm rezultatele într-un fișier Excel (opțional)
medie_istorica_decembrie.to_excel('medie_istorica_decembrie.xlsx', sheet_name='Medie Istorică')