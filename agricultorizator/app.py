from source import open_csv, drop_column

def app():
    invalid_columns = ['Datum', 'Northing', 'Easting', 'Fase de Substrato', 'Forma de Relevo', 'Cronologia', 'Gaussen', '2ª Ocorrência', '3ª Ocorrência', '4ª Ocorrência', 'Caráter Sodico/Solodico', 'Caráter Sálico/Salino', 'Caráter Plíntico/Plânico', 'Caráter Concrecionário/Litoplíntico/Dúrico', 'Caráter Ácrico', 'Caráter Flúvico', 'Caráter Argilúvico', 'Caráter Coeso', 'Caráter Vértico', 'Caráter Epiáquico', 'Caráter Crômico', 'Caráter Ebânico', 'Caráter Rúvico', 'Caráter Êutrico', 'Classe de erosão', 'Frequência de Erosão - 2ª Ocorrência', 'Profundidade de Erosão - 1ª Ocorrência', 'Profundidade de Erosão - 2ª Ocorrência', 'Presença de Fase Erodida', 'Presença de Fase Rochosa', 'Presença Contato lico-fragmentário', 'Presença de Nódulos', 'Presença Petroplintita', 'Superfície de compressão - Grau de desenvolvimento', 'Superfície de compressão - Quantidade', 'Superfície fosca - Grau de desenvolvimento', 'Superfície fosca - Quantidade', 'Nódulos e concreções minerais - Quantidade', 'Nódulos e concreções minerais - Tamanho', 'Nódulos e concreções minerais - Dureza', 'Nódulos e concreções minerais - Forma', 'Nódulos e concreções minerais - Cor', 'Nódulos e concreções minerais - Natureza', 'Poros - Quantidade', 'Poros - Diâmetro', 'Macroporosidade (%)', 'Umidade atual gravimétrica (g/100g ou %)', 'Umidade atual volumétrica (g/cm3)', 'Agregados via seca (g/kg)', 'Agregação (g/kg)', 'Estabilidade Agregados (g/kg)', 'Superfície específica (m2/g)', 'Condutividade hidráulica (mm/h)', 'Percentagem de saturação (g/cm3)', 'Limite de liquidez (%)', 'Limite de plasticidade (%)', 'Limite de pegajosidade (%)', 'Retenção de Umidade - 0,006 (MPa)', 'Retenção de Umidade - 0,100 (MPa)', 'Ataque sulfúrico - MnO', 'Água da pasta de saturação', 'Condutividade Elétrica', 'Sais Solúveis do Extrato da Saturação - Sódio', 'Sais Solúveis do Extrato da Saturação - Carbonatos', 'Sais Solúveis do Extrato da Saturação - Cloretos', 'Sais Solúveis do Extrato da Saturação - Bicarbonatos', 'Sais Solúveis do Extrato da Saturação - Sulfatos', 'Ponto de Carga Zero', 'Adsorção de Fosfato', 'Enxofre', 'Equivalente de Carbonato de Cálcio', 'CDB - Ferro (g/kg)', 'CDB - Alumínio (g/kg)', 'CDB - Manganês (g/kg)', 'Oxalato de Amônio - Ferro', 'Oxalato de Amônio - Alumínio', 'Oxalato de Amônio - Sílica', 'Pirofosfato de Sódio - Ferro', 'Pirofosfato de Sódio - Alumínio', 'Microelementos - Ferro', 'Microelementos - Manganês', 'Microelementos - Cobre', 'Microelementos - Zinco', 'Microelementos - Níquel', 'Microelementos - Boro', 'Microelementos - Molibidênio', 'Microelementos - Cobalto', 'Microelementos – Cádmio', 'Microelementos - Cromo', 'Microelementos - Selênio', 'Microelementos - Chumbo', 'Microelementos - Mercúrio', 'Microelementos - Arsênio', 'Microelementos - Silício', 'Informações adicionais da análise química']
    
    df = open_csv('solo')
    
    print(df)
    
    for value in invalid_columns:
        df = drop_column(df, value)
    print(df)
    return df
app()

