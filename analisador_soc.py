with open('relatorio_redteam.csv', 'r', encoding='utf-8') as arquivo:

    tab = arquivo.readlines()[1:]

    print("--- ALERTAS DE CRITICIDADE ALTA IDENTIFICADOS ---")
    
    
    for linha in tab:
        
        dados = linha.strip().split(',')
        
        vuln = dados[0]
        nome = dados[1]
        severidade = dados[2]
        status = dados[3]
        
        if severidade == "Alta" and status == "Aberta":
            print(f"ALERTA: Corrigir imediatamente: {nome} (ID: {vuln})")

print("--- FIM DA ANÁLISE ---")