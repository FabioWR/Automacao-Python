import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ORIGEM = os.getenv("EMAIL_USER")
SENHA_APP = os.getenv("EMAIL_PASS")
EMAIL_DESTINO = os.getenv("EMAIL_DEST")

def enviar_alerta(conteudo):
    msg = EmailMessage()
    msg['Subject'] = "ALERTA DE SEGURANÇA: Relatório Red Team"
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = EMAIL_DESTINO
    msg.set_content(f"Atenção Analista Fabio,\nForam encontradas algumas vulnerabilidades críticas:\n{conteudo}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ORIGEM, SENHA_APP)
        smtp.send_message(msg)
    print("E-mail enviado com sucesso!")

vulnerabilidades_encontradas = ""

try:
    with open('relatorio_redteam.csv', 'r') as arquivo:
        linhas = arquivo.readlines()[1:]
        for linha in linhas:
            dados = linha.strip().split(',')
            if dados[2] == "Alta":
                vulnerabilidades_encontradas += f"- {dados[1]} (ID: {dados[0]})\n"

    if vulnerabilidades_encontradas:
        enviar_alerta(vulnerabilidades_encontradas)
    else:
        print("Tudo limpo. Nenhuma vulnerabilidade alta hoje.")

except FileNotFoundError:
    print("Erro: O arquivo de relatório não foi encontrado.")