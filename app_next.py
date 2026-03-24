import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="HOLDING NEXT | Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- ESTILO CUSTOMIZADO (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS EM MEMÓRIA ---
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        'Wellington': {'senha': 'ceo', 'cargo': 'Dono', 'lucro_real': 15450.00, 'status': 'Ativo'},
        'Carlos_Vendedor': {'senha': 'v1', 'cargo': 'Vendedor', 'saldo_app': 450.00, 'vendas': 2, 'status': 'Ativo'},
        'Ana_Next': {'senha': 'v2', 'cargo': 'Vendedor', 'saldo_app': 0.00, 'vendas': 0, 'status': 'Ativo'}
    }

# --- SISTEMA DE LOGIN ---
def tela_login():
    st.title("🚀 Holding Next - Portal de Operações")
    with st.container():
        user = st.text_input("ID do Operador")
        senha = st.text_input("Chave de Acesso", type="password")
        
        if st.button("AUTENTICAR"):
            if user in st.session_state.usuarios and st.session_state.usuarios[user]['senha'] == senha:
                if st.session_state.usuarios[user]['status'] == 'Banido':
                    st.error("🚨 CONTA BLOQUEADA POR VIOLAÇÃO DE TERMOS.")
                else:
                    st.session_state.logado = user
                    st.rerun()
            else:
                st.error("Credenciais inválidas.")

# --- INTERFACE DO CEO (WELLINGTON) ---
def painel_ceo():
    st.sidebar.success(f"Logado como: {st.session_state.logado} (CEO)")
    if st.sidebar.button("LOGOUT"):
        st.session_state.logado = None
        st.rerun()

    st.header("👑 Comando Central - Holding Next")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Meu Lucro Acumulado", f"R$ {st.session_state.usuarios['Wellington']['lucro_real']:.2f}")
    m2.metric("Vendedores na Equipe", len([u for u in st.session_state.usuarios if st.session_state.usuarios[u]['cargo'] == 'Vendedor']))
    m3.metric("Status do Servidor", "ONLINE", delta="100%")

    st.divider()

    st.subheader("📋 Monitoramento de Funcionários")
    for user, info in st.session_state.usuarios.items():
        if info['cargo'] == 'Vendedor':
            with st.expander(f"👤 {user} | Vendas: {info['vendas']} | Status: {info['status']}"):
                col_data, col_btn = st.columns([3, 1])
                col_data.write(f"**Saldo a Receber:** R$ {info['saldo_app']:.2f}")
                if info['status'] == 'Ativo':
                    if col_btn.button(f"BANIR {user}", key=f"ban_{user}"):
                        st.session_state.usuarios[user]['status'] = 'Banido'
                        st.rerun()

# --- INTERFACE DO VENDEDOR ---
def painel_vendedor(user):
    dados = st.session_state.usuarios[user]
    st.sidebar.info(f"Operador: {user}")
    if st.sidebar.button("SAIR"):
        st.session_state.logado = None
        st.rerun()

    st.header("⚡ Painel de Vendas Next")
    
    # Meta de Saque
    st.subheader(f"Progresso para Saque (R$ 2.000,00)")
    prog = min(dados['saldo_app'] / 2000, 1.0)
    st.progress(prog)
    st.write(f"Saldo: **R$ {dados['saldo_app']:.2f}**")

    st.divider()

    # Ferramentas de Venda
    st.subheader("🔗 Meus Links de Checkout")
    produtos = ["Next Predictor", "Next Auto-Vendas", "Next Recovery"]
    cols = st.columns(3)
    
    for idx, prod in enumerate(produtos):
        with cols[idx]:
            st.info(f"**{prod}**")
            if st.button(f"Link {idx+1}"):
                st.code(f"https://checkout.next.com/ref={user}")

    st.divider()
    if st.button("📢 SIMULAR VENDA (TESTE)"):
        st.session_state.usuarios['Wellington']['lucro_real'] += 375.00
        st.session_state.usuarios[user]['saldo_app'] += 225.00
        st.session_state.usuarios[user]['vendas'] += 1
        st.balloons()
        st.success("Venda registrada! Split: R$ 375 (CEO) / R$ 225 (Você)")
        st.rerun()

# --- LÓGICA PRINCIPAL ---
if 'logado' not in st.session_state or st.session_state.logado is None:
    tela_login()
else:
    cargo = st.session_state.usuarios[st.session_state.logado]['cargo']
    if cargo == 'Dono':
        painel_ceo()
    else:
        painel_vendedor(st.session_state.logado)
    
