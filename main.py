from playwright.sync_api import sync_playwright
import pandas as pd

from leitor_planilha import carregar_planilha
from analisador import analisar_dia

planilha = "planilha_escala_limpa.xlsx"

profissionais = carregar_planilha(planilha)

relatorio = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for prof in profissionais:

        try:

            page.goto(prof["link"])

            linhas = page.query_selector_all("table tr")

            for linha in linhas:

                texto = linha.inner_text().split("\n")

                if len(texto) < 2:
                    continue

                data = texto[0]

                horarios = [h for h in texto[1:] if ":" in h]

                entradas = []
                saidas = []

                for i,h in enumerate(horarios):

                    if i % 2 == 0:
                        entradas.append(h)
                    else:
                        saidas.append(h)

                erros = analisar_dia(
                    data,
                    entradas,
                    saidas,
                    prof["horario"],
                    prof["dias"]
                )

                if erros:
                    relatorio.append({
                        "Nome": prof["nome"],
                        "Data": data,
                        "Erro": ",".join(erros)
                    })

        except Exception as e:

            relatorio.append({
                "Nome": prof["nome"],
                "Data": "ERRO",
                "Erro": str(e)
            })

    browser.close()

df = pd.DataFrame(relatorio)
df.to_excel("relatorio_inconsistencias.xlsx", index=False)

print("Relatório gerado com sucesso.")