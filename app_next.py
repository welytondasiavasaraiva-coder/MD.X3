import streamlit as st
import time
import pandas as pd
from datetime import datetime

# =================================================================
# CONFIGURAÇÃO DE ELITE - HOLDING NEXT
# =================================================================
st.set_page_config(
    page_title="HOLDING NEXT | SISTEMA OPERACIONAL",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO PARA APARENCIA DE SOFTWARE PAGO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .css-1offfwp { color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# BANCO DE DADOS EM MEMÓRIA (LÓGICA DA EMPRESA)
# =================================================================
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        'Wellington': {
            'senha': 'ceo', 
            'cargo': 'Dono', 
            'lucro_real': 15450.00, 
            'status': 'Ativo', 
            'aviso': '',
            'vendas_totais': 41
        },
        'Carlos_Vendedor': {
            'senha': 'v1', 
            'cargo': 'Vendedor', 
            'saldo_app': 450.00, 
            'vendas': 2, 
            'status': 'Ativo', 
            'aviso': ''
        },
        'Ana_Next': {
            'senha': 'v2', 
            'cargo': 'Vendedor', 
            'saldo_app': 0.00, 
            'vendas': 0, 
            'status': 'Ativo', 
            'aviso': ''
        }
    }

if 'lista_negra' not in st.session_state:
    st.session_state.lista_negra = []

if 'vendas_recentes' not in st.session_state:
    st.session_state.vendas_recentes = []

# =================================================================
# FUNÇÕES DE COMANDO (WELLINGTON)
# =================================================================
def advertir_usuario(nome):
    st.session_state.usuarios[nome]['aviso'] = "⚠️ VOCÊ VIOLOU AS REGRAS DE OURO. PRÓXIMO ERRO É BANIMENTO."
    st.toast(f"Advertência enviada para {nome}")

def congelar_usuario(nome):
    st.session_state.usuarios[nome]['status'] = "Congelado"
    st.session_state.usuarios[nome]['aviso'] = "❄️ SALDO CONGELADO PELA SEGURANÇA PARA AUDITORIA."
    st.toast(f"Conta de {nome} congelada.")

def banir_permanente(nome):
    saldo = st.session_state.usuarios[nome]['saldo_app']
    st.session_state.lista_negra.append({
        'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'ID': nome,
        'Saldo Retido': f"R$ {saldo:.2f}",
        'Status Final': "BANIDO"
    })
    st.session_state.usuarios[nome]['status'] = "Banido"
    st.toast(f"USUÁRIO {nome} EXPULSO DA HOLDING.")

# =================================================================
# TELAS DO SISTEMA
# =================================================================

def tela_login():
    st.markdown("<h1 style='text-align: center;'>🚀 NEXT HOLDING</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Sistema de Gestão de Vendas de Elite</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        with st.form("login_form"):
            user = st.text_input("Usuário")
            senha = st.text_input("Chave de Acesso", type="password")
            entrar = st.form_submit_button("ACESSAR PAINEL")
            
            if entrar:
                if user in st.session_state.usuarios:
                    if st.session_state.usuarios[user]['senha'] == senha:
                        if st.session_state.usuarios[user]['status'] == "Banido":
                            st.error("🚫 ACESSO BLOQUEADO PELA ADMINISTRAÇÃO NEXT. Violação grave detectada.")
                        else:
                            st.session_state.logado = user
                            st.rerun()
                    else:
                        st.error("Senha incorreta.")
                else:
                    st.error("Usuário não cadastrado.")

def painel_ceo():
    st.sidebar.markdown(f"## 👑 CEO: {st.session_state.logado}")
    aba = st.sidebar.radio("Comandos", ["Dashboard Financeiro", "Gestão de Equipe", "Arquivo de Banidos", "Configuração da Marca"])
    
    if st.sidebar.button("LOGOUT / SAIR"):
        st.session_state.logado = None
        st.rerun()

    if aba == "Dashboard Financeiro":
        st.header("📊 Resumo da Operação Holding")
        c1, c2, c3 = st.columns(3)
        c1.metric("Meu Lucro Real", f"R$ {st.session_state.usuarios['Wellington']['lucro_real']:.2f}")
        c2.metric("Vendedores Ativos", len([u for u in st.session_state.usuarios if st.session_state.usuarios[u]['cargo'] == 'Vendedor']))
        c3.metric("Ticket Médio", "R$ 600,00")

        st.divider()
        st.subheader("📝 Histórico de Split (R$ 375 por Venda)")
        if st.session_state.vendas_recentes:
            st.table(st.session_state.vendas_recentes)
        else:
            st.info("Aguardando primeiras vendas da sessão.")

    elif aba == "Gestão de Equipe":
        st.header("👥 Controle de Funcionários")
        for user, info in st.session_state.usuarios.items():
            if info['cargo'] == "Vendedor" and info['status'] != "Banido":
                with st.container():
                    col_user, col_status, col_btn = st.columns([2, 2, 3])
                    col_user.write(f"**{user}**")
                    col_status.write(f"Status: {info['status']} | Saldo: R$ {info['saldo_app']:.2f}")
                    
                    with col_btn:
                        btn1, btn2, btn3 = st.columns(3)
                        if btn1.button("⚠️ ADV", key=f"adv_{user}"): advertir_usuario(user)
                        if btn2.button("❄️ CONG", key=f"cong_{user}"): congelar_usuario(user)
                        if btn3.button("🚫 BAN", key=f"ban_{user}"): 
                            banir_permanente(user)
                            st.rerun()
                    st.divider()

    elif aba == "Arquivo de Banidos":
        st.header("📂 Lista Negra - Contas Encerradas")
        if st.session_state.lista_negra:
            st.dataframe(pd.DataFrame(st.session_state.lista_negra), use_container_width=True)
        else:
            st.write("Nenhum banimento registrado.")

    elif aba == "Configuração da Marca":
        st.header("🛠️ Ajustes de Identidade")
        nome = st.text_input("Novo Nome da Empresa", "Next Holding")
        if st.button("Salvar"): st.success(f"Nome alterado para {nome}")

def painel_vendedor(user):
    u = st.session_state.usuarios[user]
    st.sidebar.markdown(f"### 🎯 Operador: {user}")
    if st.sidebar.button("SAIR"):
        st.session_state.logado = None
        st.rerun()

    if u['aviso']:
        st.error(u['aviso'])

    st.header("⚡ Painel de Vendas Next")
    st.metric("Meu Saldo App", f"R$ {u['saldo_app']:.2f}", delta="Meta R$ 2.000,00")
    
    progresso = min(u['saldo_app'] / 2000, 1.0)
    st.progress(progresso)
    
    if u['status'] == "Congelado":
        st.warning("⚠️ Seu saldo está bloqueado para retirada. Continue operando enquanto analisamos.")

    st.divider()
    st.subheader("📦 Vitrine de Produtos (R$ 600)")
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.write("**Next Predictor**")
        if st.button("Link 1"): st.code(f"next.com/pay?ref={user}")
    with c2:
        st.write("**Auto-Vendas**")
        if st.button("Link 2"): st.code(f"next.com/pay?ref={user}")
    with c3:
        st.write("**Next Recovery**")
        if st.button("Link 3"): st.code(f"next.com/pay?ref={user}")

    st.divider()
    if st.button("📢 SIMULAR VENDA (TESTE)"):
        st.session_state.usuarios['Wellington']['lucro_real'] += 375.00
        st.session_state.usuarios[user]['saldo_app'] += 225.00
        st.session_state.usuarios[user]['vendas'] += 1
        st.session_state.vendas_recentes.append({'Hora': datetime.now().strftime("%H:%M"), 'Vendedor': user, 'Lucro CEO': 'R$ 375.00'})
        st.balloons()
        st.success("Venda processada com sucesso!")
        time.sleep(1)
        st.rerun()

# =================================================================
# MOTOR PRINCIPAL
# =================================================================
if 'logado' not in st.session_state or st.session_state.logado is None:
    tela_login()
else:
    if st.session_state.usuarios[st.session_state.logado]['cargo'] == "Dono":
        painel_ceo()
    else:
        painel_vendedor(st.session_state.logado)
