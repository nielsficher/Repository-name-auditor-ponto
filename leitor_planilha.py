import pandas as pd

def carregar_planilha(caminho):
    df = pd.read_excel(caminho)

    profissionais = []
    for _, row in df.iterrows():
        profissionais.append({
            "nome": row["NOME"],
            "dias": str(row["DIAS_TRABALHO"]).split(","),
            "horario": row["HORARIO"],
            "link": row["LINK"]
        })

    return profissionais