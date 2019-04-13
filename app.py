import sys
sys.dont_write_bytecode = True
import pandas as pd

# Campos selecionados
fields = ["Tipo", "Material de Origem", "pH - H2O", "pH - KCl", "Complexo Sortivo - Cálcio (cmolc/kg)", "Complexo Sortivo - Magnésio", "Complexo Sortivo - Potássio", "Complexo Sortivo - Sódio", "Complexo Sortivo - Valor S (Ca2++Mg2++K++Na+)", "Complexo Sortivo - Hidrogênio (H+)", "Complexo Sortivo - Alumínio Trocável (Al3+)", "Carbono orgânico", "Nitrogênio total"]

# Criação do dataframe com colunas desejadas + filtro por valores nulos
df = pd.read_csv("./data/solo.csv", sep=';', error_bad_lines=False).filter(fields).dropna()

print(df["Complexo Sortivo - Potássio"])
