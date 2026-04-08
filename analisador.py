def analisar_dia(data_texto, entradas, saidas, horario, dias_trabalho):

    resultado = []

    partes = data_texto.split()
    if len(partes) < 2:
        return resultado

    data = partes[0]
    dia_semana = partes[1]

    mapa = {
        "SEGUNDA-FEIRA":"SEG",
        "TERCA-FEIRA":"TER",
        "QUARTA-FEIRA":"QUA",
        "QUINTA-FEIRA":"QUI",
        "SEXTA-FEIRA":"SEX",
        "SABADO":"SAB",
        "DOMINGO":"DOM"
    }

    dia = mapa.get(dia_semana.upper(), "")

    if dia not in dias_trabalho:
        if entradas:
            resultado.append("TRABALHO_FORA_ESCALA")
        return resultado

    if not entradas:
        resultado.append("SEM_REGISTRO")
        return resultado

    entrada = min(entradas)
    saida = max(saidas)

    inicio_escala, fim_escala = horario.split("-")

    if entrada > inicio_escala:
        resultado.append("ATRASO")

    if saida < fim_escala:
        resultado.append("SAIDA_ANTECIPADA")

    if saida > fim_escala:
        resultado.append("HORA_EXTRA")

    return resultado