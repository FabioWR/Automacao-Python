import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV = os.path.join(BASE_DIR, 'relatorio_redteam.csv')

load_dotenv()
EMAIL_ORIGEM = os.getenv("EMAIL_USER")
SENHA_APP = os.getenv("EMAIL_PASS")
EMAIL_DESTINO = os.getenv("EMAIL_DEST")

def enviar_alerta(tabela_html):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = EmailMessage()
    msg['Subject'] = f"🚨 RELATÓRIO SOC: Vulnerabilidades - {agora}"
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = EMAIL_DESTINO
    
    conteudo_html = f"""
    <html>
        <body style="font-family: Arial; color: #333;">
            <h2 style="color: #d9534f;">🛡️ Alerta de Segurança Identificado</h2>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f2f2f2;">
                    <th>ID</th><th>Vulnerabilidade</th><th>Severidade</th><th>Status</th>
                </tr>
                {tabela_html}
            </table>
        </body>
    </html>
    """
    msg.add_alternative(conteudo_html, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ORIGEM, SENHA_APP)
        smtp.send_message(msg)

linhas_para_email = ""

try:
    with open(CAMINHO_CSV, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()[1:]

        for linha in linhas:
            dados = linha.strip().split(',')
            
            if len(dados) >= 4:
                vuln_id = dados[0]
                nome = dados[1]
                severidade = dados[2].strip()
                status = dados[3].strip()
                
                if severidade == "Alta" and status == "Aberta":
                    print(f"🔥 Falha encontrada: {nome}")
                    linhas_para_email += f"<tr><td>{vuln_id}</td><td>{nome}</td><td>{severidade}</td><td>{status}</td></tr>"

    if linhas_para_email:
        print("📧 Enviando relatório para o e-mail...")
        enviar_alerta(linhas_para_email)
        print("✅ Sucesso!")
    else:
        print("✅ Nenhuma vulnerabilidade 'Alta' e 'Aberta' no momento.")

except FileNotFoundError:
    print("❌ Erro: O arquivo 'relatorio_redteam.csv' não foi encontrado.")