import pandas as pd
import traceback

def procesare_csv(input_file, output_file):
    try:
        # Încărcăm datele din fișierul Excel
        data = pd.read_excel(input_file, engine='openpyxl')

        # Convertim coloana 'Data' într-un format datetime
        data['Data'] = pd.to_datetime(data['Data'], format='%d-%m-%Y %H:%M:%S')

        # Selectăm coloanele ce trebuie convertite în tip numeric
        cols_to_convert = [
            'Consum[MW]', 'Medie Consum[MW]', 'Productie[MW]', 'Carbune[MW]',
            'Hidrocarburi[MW]', 'Ape[MW]', 'Nuclear[MW]', 'Eolian[MW]',
            'Foto[MW]', 'Biomasa[MW]', 'Sold[MW]'
        ]

        # Convertim coloanele selectate în tip numeric
        data[cols_to_convert] = data[cols_to_convert].apply(pd.to_numeric, errors='coerce')

        # Setăm 'Data' ca index pentru a facilita agregarea
        data.set_index('Data', inplace=True)

        # Agregăm datele pe baza frecvenței zilnice (D) și realizăm sumarizări
        data_agregata = data.resample('D').agg({
            'Consum[MW]': 'sum',
            'Medie Consum[MW]':'mean',
            'Productie[MW]': 'sum',
            'Carbune[MW]': 'sum',
            'Hidrocarburi[MW]': 'sum',
            'Ape[MW]': 'sum',
            'Nuclear[MW]': 'sum',
            'Eolian[MW]': 'sum',
            'Foto[MW]': 'sum',
            'Biomasa[MW]': 'sum',
            'Sold[MW]':'sum'
        }).reset_index()

        # Formatăm data pentru a fi mai ușor citibilă
        data_agregata['Data'] = data_agregata['Data'].dt.strftime('%d-%m-%Y')

        # Salvăm datele agregate într-un fișier Excel nou
        data_agregata.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Fișierul a fost salvat ca {output_file}")

    except Exception as e:
        # Gestionăm erorile care pot apărea în procesul de citire sau prelucrare
        print(f"Error processing the file: {e}")
        traceback.print_exc()

# Setăm fișierele de intrare și ieșire
input_file = r'F:\Python\ML\Grafic_SEN.xlsx'
output_file = r'F:\Python\ML\date_sen_agregat.xlsx'

# Apelăm funcția de procesare
procesare_csv(input_file, output_file)
