import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import qrcode
import base64
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("Loja Virtual para Alunos EAD")
st.subheader("Selecione os serviços que você precisa")

servicos = [
    "Resumo",
    "Prova do",
    "Pesquisa",
    "Dissertação",
    "Correção ABNT",
    "Relatório Científico",
    "Prova em Plataforma",
    "Atividade em Plataforma",
    "Cuidar da Plataforma de Disciplina",
    "Projeto de Extensão",
    "Slide de Qualquer Tema",
    "Mini Resumo",
    "Relatório de Estágio"
]

selecao_servicos = st.multiselect("Escolha os serviços:", servicos)

# Definir os serviços que requerem informações adicionais
servicos_requerem_info_adicional = [
    "Dissertação",
    "Relatório de Estágio",
    "Projeto de Extensão",
    "Prova do",
    "Cuidar da Plataforma de Disciplina"
]

# Funções de cálculo de preço
def preco_resumo():
    return 40

def preco_provadol():
    return 15

def preco_pesquisa(paginas):
    if paginas == 5:
        return 25
    elif paginas == 10:
        return 35
    else:
        return 25 + ((paginas - 5) * 2)

def preco_dissertacao():
    return 25

def preco_correcao_abnt():
    return 30

def preco_relatorio_cientifico(tamanho):
    base = 30
    if tamanho == "Pequeno":
        return base
    elif tamanho == "Médio":
        return base + 20
    else:
        return base + 40

def preco_prova_em_plataforma():
    return 15

def preco_atividade_em_plataforma():
    return 25

def preco_cuidar_plataforma(qtd_disciplinas):
    return 100 + (qtd_disciplinas - 1) * 50

def preco_projeto_extensao():
    return 150

def preco_slide():
    return 25

def preco_mini_resumo():
    return 25

def preco_relatorio_estagio():
    return 30

total = 0
detalhes_servicos = {}

# Loop para calcular o preço e coletar detalhes
for servico in selecao_servicos:
    if servico == "Pesquisa":
        paginas = st.number_input(f"Quantas páginas para {servico}?", min_value=1, step=1)
        preco = preco_pesquisa(paginas)
        st.write(f"Preço para {servico} com {paginas} páginas: R$ {preco}")
        detalhes_servicos[servico] = f"{paginas} páginas"
    elif servico == "Relatório Científico":
        tamanho = st.selectbox(f"Tamanho do {servico}:", ["Pequeno", "Médio", "Grande"])
        preco = preco_relatorio_cientifico(tamanho)
        st.write(f"Preço para {servico} ({tamanho}): R$ {preco}")
        detalhes_servicos[servico] = f"Tamanho: {tamanho}"
    elif servico == "Cuidar da Plataforma de Disciplina":
        qtd_disciplinas = st.number_input("Quantidade de disciplinas:", min_value=1, step=1)
        preco = preco_cuidar_plataforma(qtd_disciplinas)
        st.write(f"Preço para {servico} com {qtd_disciplinas} disciplinas: R$ {preco}")
        detalhes_servicos[servico] = f"{qtd_disciplinas} disciplinas"
    else:
        preco_func = {
            "Resumo": preco_resumo,
            "Prova do": preco_provadol,
            "Dissertação": preco_dissertacao,
            "Correção ABNT": preco_correcao_abnt,
            "Prova em Plataforma": preco_prova_em_plataforma,
            "Atividade em Plataforma": preco_atividade_em_plataforma,
            "Projeto de Extensão": preco_projeto_extensao,
            "Slide de Qualquer Tema": preco_slide,
            "Mini Resumo": preco_mini_resumo,
            "Relatório de Estágio": preco_relatorio_estagio
        }
        preco = preco_func[servico]()
        st.write(f"Preço para {servico}: R$ {preco}")
        detalhes_servicos[servico] = "N/A"
    total += preco

st.write(f"### Preço Total: R$ {total}")

st.header("Finalize seu Pedido")

with st.form("form_pedido"):
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")
    observacoes = st.text_area("Observações")

    # Verificar se serviços selecionados requerem informações adicionais
    requer_info_adicional = any(servico in servicos_requerem_info_adicional for servico in selecao_servicos)

    if requer_info_adicional:
        st.subheader("Informações Adicionais")
        matricula = st.text_input("Matrícula")
        nome_completo = st.text_input("Nome Completo")
        nome_universidade = st.text_input("Nome da Universidade")
        polo_universidade = st.text_input("Polo da Universidade")
        st.info("Se necessário, entraremos em contato para obter informações adicionais de forma segura.")
    else:
        matricula = ''
        nome_completo = ''
        nome_universidade = ''
        polo_universidade = ''

    submitted = st.form_submit_button("Enviar Pedido")

if submitted:
    st.success("Pedido enviado com sucesso! Entraremos em contato em breve.")

    # Gerar um ID único para o pedido
    pedido_id = str(uuid.uuid4())

    # Função para salvar o pedido
    def salvar_pedido(dados_pedido):
        try:
            # Tenta carregar o arquivo existente
            df_existente = pd.read_csv('pedidos.csv')
            df_novo = pd.DataFrame([dados_pedido])
            df_final = pd.concat([df_existente, df_novo], ignore_index=True)
        except FileNotFoundError:
            # Se o arquivo não existir, cria um novo DataFrame
            df_final = pd.DataFrame([dados_pedido])

        # Salva o DataFrame atualizado no arquivo CSV
        df_final.to_csv('pedidos.csv', index=False)

    # Montar o dicionário com os dados do pedido
    dados_pedido = {
        'Pedido ID': pedido_id,
        'Data': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'Nome': nome,
        'Email': email,
        'Telefone': telefone,
        'Serviços Selecionados': ', '.join(selecao_servicos),
        'Detalhes dos Serviços': str(detalhes_servicos),
        'Observações': observacoes,
        'Preço Total': total,
        'Matrícula': matricula,
        'Nome Completo': nome_completo,
        'Nome da Universidade': nome_universidade,
        'Polo da Universidade': polo_universidade,
        'Status': 'Pendente'
    }

    # Salvar o pedido na planilha
    salvar_pedido(dados_pedido)

    # Enviar o email (mantém o código existente)
    # Montar o conteúdo do email
    mensagem = MIMEMultipart()
    mensagem["From"] = st.secrets["email"]["user"]
    mensagem["To"] = st.secrets["email"]["user"]  # Seu email
    mensagem["Subject"] = "Novo Pedido Recebido"

    # Construir a lista de serviços com detalhes
    servicos_detalhados = ""
    for servico in selecao_servicos:
        detalhe = detalhes_servicos.get(servico, "")
        servicos_detalhados += f"- {servico}: {detalhe}\n"

    # Conteúdo do email
    corpo_email = f"""
    Novo pedido recebido:

    Pedido ID: {pedido_id}
    Nome: {nome}
    Email: {email}
    Telefone: {telefone}
    Serviços Selecionados:
    {servicos_detalhados}
    Observações: {observacoes}
    Preço Total: R$ {total}
    """

    if requer_info_adicional:
        corpo_email += f"""
        Informações Adicionais:
        Matrícula: {matricula}
        Nome Completo: {nome_completo}
        Nome da Universidade: {nome_universidade}
        Polo da Universidade: {polo_universidade}
        """

    mensagem.attach(MIMEText(corpo_email, "plain"))

    # Enviar o email
    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(st.secrets["email"]["user"], st.secrets["email"]["password"])
        servidor.send_message(mensagem)
        servidor.quit()
        st.info("Detalhes do pedido enviados por email.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao enviar o email: {e}")

    # Gerar o código Pix e QR Code
    def gerar_codigo_pix(valor, chave_pix, nome_recebedor, cidade_recebedor, pedido_id):
        valor_str = f"{valor:.2f}"
        # Limitar o nome e a cidade ao tamanho máximo permitido
        nome_recebedor = nome_recebedor[:25]
        cidade_recebedor = cidade_recebedor[:15]
        pedido_id = pedido_id[:25]
        # Montar o código Pix conforme o padrão
        payload = (
            "000201"  # Payload Format Indicator
            + "010212"  # Ponto de entrada do merchant (virtual payment address)
            + "26" + f"{14 + len(chave_pix):02d}" + "0014BR.GOV.BCB.PIX"  # GUI do Pix
            + "01" + f"{len(chave_pix):02d}" + chave_pix  # Chave Pix
            + "52040000"  # Merchant Category Code
            + "5303986"   # Transaction Currency (986 = BRL)
            + "54" + f"{len(valor_str):02d}" + valor_str  # Transaction Amount
            + "5802BR"  # Country Code
            + "59" + f"{len(nome_recebedor):02d}" + nome_recebedor  # Merchant Name
            + "60" + f"{len(cidade_recebedor):02d}" + cidade_recebedor  # Merchant City
            + "62" + f"{4 + 13 + len(pedido_id):02d}"  # Additional Data Field Template
            + "05" + "03" + "***"  # TxID (*** indica que não está sendo usado)
            + "04" + f"{len(pedido_id):02d}" + pedido_id  # Pedido ID
            + "6304"  # CRC16
        )
        # Calcula o CRC16 do payload
        crc = calcular_crc16(payload)
        codigo_pix = payload + crc
        return codigo_pix

    # Função para calcular o CRC16
    def calcular_crc16(payload):
        polinomio = 0x1021
        resultado = 0xFFFF
        for byte in bytearray(payload.encode('utf-8')):
            resultado ^= (byte << 8)
            for _ in range(8):
                if (resultado & 0x8000):
                    resultado = (resultado << 1) ^ polinomio
                else:
                    resultado = resultado << 1
                resultado &= 0xFFFF
        return f"{resultado:04X}"

    # Dados para o código Pix
    chave_pix = "sua_chave_pix"  # Substitua pela sua chave Pix
    nome_recebedor = "Seu Nome"  # Seu nome ou nome da sua empresa (até 25 caracteres)
    cidade_recebedor = "Sua Cidade"  # Sua cidade (até 15 caracteres)

    codigo_pix = gerar_codigo_pix(total, chave_pix, nome_recebedor, cidade_recebedor, pedido_id)

    # Gerar o QR Code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(codigo_pix)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    # Exibir o QR Code no aplicativo
    st.subheader("Pagamento via Pix")
    st.write("Escaneie o QR Code abaixo para realizar o pagamento:")
    st.image(f"data:image/png;base64,{img_str}")

    # Exibir o código Pix Copia e Cola
    st.write("Ou copie o código Pix abaixo:")
    st.code(codigo_pix, language='text')

    st.info("Após realizar o pagamento, por favor, envie o comprovante para nosso email ou WhatsApp.")
