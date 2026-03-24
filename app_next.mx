import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Holding Next - Portal Oficial", layout="wide")

# --- BANCO DE DADOS SIMULADO (Em um app real, usaríamos SQL) ---
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        'Wellington': {'senha': '123', 'cargo': 'Dono', 'lucro_real': 15450.00, 'status': 'Ativo'},
        'Carlos_Vendedor': {'senha': 'v1', 'cargo': 'Vendedor', 'saldo_app': 450.00, 'vendas': 2, 'status': 'Ativo'},
        'Ana_Next': {'senha': 'v2', 'cargo': 'Vendedor', 'saldo_app': 0.00, 'vendas': 0, 'status': 'Ativo'}
    }

# --- FUNÇÃO DE LOGIN ---
def login():
    st.title("🚀 Holding Next - Login de Elite")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Acessar Painel"):
        if user in st.session_state.usuarios and st.session_state.usuarios[user]['senha'] == senha:
            if st.session_state.usuarios[user]['status'] == 'Banido':
                st.error("ACESSO BLOQUEADO PELA SEGURANÇA NEXT. Violação das Regras de Ouro.")
            else:
                st.session_state.logado = user
                st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

# --- PAINEL DO DONO (WELLINGTON) ---
def painel_dono():
    st.sidebar.title(f"Olá, CEO {st.session_state.logado}")
    if st.sidebar.button("Sair"):
        st.session_state.logado = None
        st.rerun()

    st.header("👑 Painel de Controle - Holding Next")
    
    # Métricas de Topo
    col1, col2 = st.columns(2)
    col1.metric("Meu Lucro Real (R$ 375/venda)", f"R$ {st.session_state.usuarios['Wellington']['lucro_real']:.2f}")
    col2.metric("Vendedores Ativos", len([u for u in st.session_state.usuarios if st.session_state.usuarios[u]['cargo'] == 'Vendedor']))

    st.divider()

    # Gestão de Funcionários e Banimento
    st.subheader("👥 Gestão de Equipe e Ranking")
    for user, dados in st.session_state.usuarios.items():
        if dados['cargo'] == 'Vendedor':
            col_nome, col_vendas, col_saldo, col_acao = st.columns([2,1,2,1])
            col_nome.write(f"**{user}** ({dados['status']})")
            col_vendas.write(f"{dados['vendas']} vendas")
            col_saldo.write(f"Saldo App: R$ {dados['saldo_app']:.2f}")
            
            if dados['status'] == 'Ativo':
                if col_acao.button(f"🚫 BANIR", key=user):
                    st.session_state.usuarios[user]['status'] = 'Banido'
                    st.warning(f"Usuário {user} foi expulso da Next.")
                    st.rerun()

# --- PAINEL DO VENDEDOR ---
def painel_vendedor(user):
    dados = st.session_state.usuarios[user]
    st.sidebar.title(f"Vendedor: {user}")
    if st.sidebar.button("Sair"):
        st.session_state.logado = None
        st.rerun()

    st.header("🎯 Minha Meta - Próximo ao Saque de 2k")
    
    # Barra de Progresso para os 2k
    progresso = min(dados['saldo_app'] / 2000, 1.0)
    st.progress(progresso)
    st.write(f"Saldo Atual: **R$ {dados['saldo_app']:.2f}** / Meta: **R$ 2.000,00**")

    st.divider()

    # Vitrine de Vendas
    st.subheader("📦 Vitrine de Aplicativos (R$ 600,00)")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image("https://img.icons8.com/fluency/96/bullseye.png")
        st.write("**Next Predictor**")
        if st.button("Gerar Link Predictor"):
            st.code(f"next.holding/checkout?ref={user}&prod=predictor")
            
    with c2:
        st.image("https://img.icons8.com/fluency/96/bot.png")
        st.write("**Next Auto-Vendas**")
        if st.button("Gerar Link Auto-Vendas"):
            st.code(f"next.holding/checkout?ref={user}&prod=autovendas")

    with c3:
        st.image("https://img.icons8.com/fluency/96/shield.png")
        st.write("**Next Recovery**")
        if st.button("Gerar Link Recovery"):
            st.code(f"next.holding/checkout?ref={user}&prod=recovery")

    # Simulação de Venda para teste do sistema
    st.divider()
    if st.button("🛠️ Simular Venda Realizada (R$ 600)"):
        # Lógica do Split: R$ 375 para o Dono, R$ 225 para o Vendedor
        st.session_state.usuarios['Wellington']['lucro_real'] += 375.00
        st.session_state.usuarios[user]['saldo_app'] += 225.00
        st.session_state.usuarios[user]['vendas'] += 1
        st.success("Venda processada! R$ 375 foram para o Wellington e R$ 225 para seu saldo.")
        st.rerun()

# --- LÓGICA DE NAVEGAÇÃO ---
if 'logado' not in st.session_state or st.session_state.logado is None:
    login()
else:
    cargo = st.session_state.usuarios[st.session_state.logado]['cargo']
    if cargo == 'Dono':
        painel_dono()
    else:
        painel_vendedor(st.session_state.logado)
