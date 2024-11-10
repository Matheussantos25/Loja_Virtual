import streamlit as st

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

# Funções de cálculo de preço (definidas anteriormente)
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

for servico in selecao_servicos:
    if servico == "Pesquisa":
        paginas = st.number_input(f"Quantas páginas para {servico}?", min_value=1, step=1)
        preco = preco_pesquisa(paginas)
        st.write(f"Preço para {servico} com {paginas} páginas: R$ {preco}")
    elif servico == "Relatório Científico":
        tamanho = st.selectbox(f"Tamanho do {servico}:", ["Pequeno", "Médio", "Grande"])
        preco = preco_relatorio_cientifico(tamanho)
        st.write(f"Preço para {servico} ({tamanho}): R$ {preco}")
    elif servico == "Cuidar da Plataforma de Disciplina":
        qtd_disciplinas = st.number_input("Quantidade de disciplinas:", min_value=1, step=1)
        preco = preco_cuidar_plataforma(qtd_disciplinas)
        st.write(f"Preço para {servico} com {qtd_disciplinas} disciplinas: R$ {preco}")
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
    
    submitted = st.form_submit_button("Enviar Pedido")

    if submitted:
        st.success("Pedido enviado com sucesso! Entraremos em contato em breve.")
        # Aqui você pode adicionar o código para enviar um email ou salvar as informações em um banco de dados
        # As informações coletadas estão disponíveis nas variáveis correspondentes
