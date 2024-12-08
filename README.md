# Predicția Soldului Total în Sistemul Energetic Național (SEN) pentru Decembrie 2024

## Descrierea Proiectului

Acest proiect vizează predicția soldului total din Sistemul Energetic Național (SEN) al României pentru luna decembrie 2024. Folosind un set de date disponibil pe site-ul Transelectrica, proiectul utilizează algoritmi de învățare automată pentru a prezice soldul total, respectând constrângerea de a nu utiliza datele din luna decembrie pentru antrenarea modelelor.

### Scopul Proiectului
- Predicția soldului total pentru decembrie 2024 folosind metode de învățare automată, incluzând algoritmi de tip ID3 (arbore de decizie) și clasificare bayesiană adaptată pentru regresie.
- Compararea performanței modelului pe date istorice și implementarea unor tehnici de preprocesare și adaptare a algoritmilor pentru a îmbunătăți precizia predicțiilor.

## Date disponibile

Datele utilizate sunt disponibile pe site-ul oficial Transelectrica: [SEN Grafic](https://www.transelectrica.ro/) (verificați secțiunea de date istorice).

Setul de date conține următoarele coloane principale:
- **Data:** Timpul specific al înregistrării.
- **Consum[MW]:** Consumul total de energie electrică.
- **Medie Consum[MW]:** Media consumului de energie electrică.
- **Producție[MW]:** Producția totală de energie electrică.
- **Carbune[MW]:** Producție pe bază de cărbune.
- **Hidrocarburi[MW]:** Producție pe bază de hidrocarburi.
- **Ape[MW]:** Producție hidro.
- **Nuclear[MW]:** Producție nucleară.
- **Eolian[MW]:** Producție eoliană.
- **Foto[MW]:** Producție solară.
- **Biomasă[MW]:** Producție din biomasă.
- **Sold[MW]:** Diferența între producție și consum (soldul energetic).

## Algoritmi de Învațare Automată

Pentru această problemă, am utilizat următorii algoritmi de învățare automată:
1. **ID3 (Arbore de decizie):** Adaptat pentru regresie prin utilizarea tehnicii de bucketizare pentru valoarea "Sold[MW]".
2. **Clasificare Bayesiană:** Adaptat pentru regresie prin discretizarea intervalelor pentru variabilele continue.

### Adaptări necesare:
- Algoritmul ID3 a fost adaptat pentru a face regresie, utilizând intervale pentru a prezice valori continue ale soldului.
- Clasificarea bayesiană a fost adaptată pentru a permite regresia prin discretizarea variabilelor de intrare.

## Restricții
- **Datele din luna decembrie 2024 nu pot fi utilizate pentru antrenarea modelelor.**
- **Algoritmii folosiți sunt ID3 și Bayes, adaptându-i pentru o problemă de regresie.**

## Pași pentru rularea soluției

### Preprocesare:
1. Încărcarea setului de date din fișierul Excel sau CSV.
2. Filtrarea datelor pentru luna decembrie 2024.
3. Se împart datele în seturi de antrenare și testare (fără a folosi decembrie 2024 pentru antrenare).
4. Aplicarea tehnicilor de preprocesare necesare (de exemplu, normalizarea datelor sau tratarea valorilor lipsă).

### Antrenarea modelelor:
1. Antrenarea modelului de tip **ID3** pe datele istorice.
2. Antrenarea unui **model bayesian adaptat** pentru regresie pe aceleași date.

### Evaluarea Performanței:
- Evaluarea modelelor folosind metrici precum RMSE (Root Mean Square Error), MAE (Mean Absolute Error).
- Compararea performanței fiecărui model pentru a determina cea mai bună abordare.
