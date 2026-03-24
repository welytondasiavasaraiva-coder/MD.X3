import streamlit as st
import time

# --- CONFIGURAÇÃO MASTER DA HOLDING ---
st.set_page_config(page_title="HOLDING NEXT - SISTEMA CENTRAL", layout="wide", initial_sidebar_state="expanded")

# --- BANCO DE DADOS (SIMULADO) ---
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        'Wellington': {'senha': 'ceo', 'cargo': 'Dono', 'lucro_real': 15450.00, 'status': 'Ativo', 'aviso': ''},
        'Carlos_Vendedor': {'senha': 'v1', 'cargo': 'Vendedor', 'saldo_app': 450.00, 'vendas': 2, 'status': 'Ativo', 'aviso': ''},
        'Ana_Next': {'senha': 'v2', 'cargo': 'Vendedor', 'saldo_app': 0.00, 'vendas': 0, 'status': 'Ativo', 'aviso': ''}
    }
if 'lista_negra' not in st.session_state:
    st.session_state.lista_negra = []

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #00ff00; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
def tela_login():
    st.title("🚀 NEXT HOLDING - PORTAL DE ELITE")
    with st.container():
        user = st.text_input("ID do Operador")
        senha = st.text_input("Chave de Acesso", type="password")
        
        if st.button("AUTENTICAR"):
            if user in st.session_state.usuarios:
                u = st.session_state.usuarios[user]
                if u['status'] == 'Banido':
                    st.error("🚨 ACESSO BLOQUEADO PELA ADMINISTRAÇÃO NEXT. Sua conta foi encerrada por violação grave das Regras de Ouro. O saldo acumulado foi retido. Esta decisão é irreversível.")
                elif u['senha'] == senha:
                    st.session_state.logado = user
                    st.rerun()
                else:
                    st.error("Chave de acesso incorreta.")
            else:
                st.error("ID não encontrado no sistema.")

# --- PAINEL DO DONO (WELLINGTON) ---
def painel_wellington():
    st.sidebar.title(f"👑 CEO: {st.session_state.logado}")
    menu = st.sidebar.radio("Comando Central", ["Painel Geral", "Gestão de Equipe", "Arquivo de Banimentos", "Configuração da Holding"])
    
    if st.sidebar.button("LOGOUT"):
        st.session_state.logado = None
        st.rerun()

    if menu == "Painel Geral":
        st.header("📊 Dashboard de Faturamento")
        m1, m2, m3 = st.columns(3)
        m1.metric("Meu Lucro Real (R$ 375/venda)", f"R$ {st.session_state.usuarios['Wellington']['lucro_real']:.2f}")
        m2.metric("Operadores Ativos", len([u for u in st.session_state.usuarios if st.session_state.usuarios[u]['status'] != 'Banido' and u != 'Wellington']))
        m3.metric("Contas Deletadas", len(st.session_state.lista_negra))

    elif menu == "Gestão de Equipe":
        st.subheader("👥 Controle de Vendedores e Gerentes")
        for user, info in st.session_state.usuarios.items():
            if info['cargo'] != 'Dono' and info['status'] != 'Banido':
                with st.expander(f"👤 {user} | Vendas: {info['vendas']} | Saldo: R$ {info['saldo_app']:.2f}"):
                    col1, col2, col3 = st.columns(3)
                    
                    # OPÇÃO 1: ADVERTÊNCIA
                    if col1.button(f"⚠️ Advertir", key=f"adv_{user}"):
                        st.session_state.usuarios[user]['aviso'] = "Você violou as Regras de Ouro. Próximo erro será banimento."
                        st.toast(f"Advertência enviada para {user}")

                    # OPÇÃO 2: CONGELAR SALDO
                    status_btn = "❄️ Descongelar" if info['status'] == 'Congelado' else "❄️ Congelar Saldo"
                    if col2.button(status_btn, key=f"cong_{user}"):
                        st.session_state.usuarios[user]['status'] = 'Congelado' if info['status'] == 'Ativo' else 'Ativo'
                        st.rerun()

                    # OPÇÃO 3: BANIR E DELETAR
                    if col3.button(f"🚫 BANIR E DELETAR", key=f"banir_{user}"):
                        saldo_perdido = info['saldo_app']
                        st.session_state.lista_negra.append({
                            'Usuário': user, 
                            'Saldo Retido': f"R$ {saldo_perdido:.2f}", 
                            'Motivo': 'Violação das Regras de Ouro',
                            'Data': time.strftime("%d/%m/%Y")
                        })
                        st.session_state.usuarios[user]['status'] = 'Banido'
                        st.error(f"Usuário {user} expulso. R$ {saldo_perdido} voltaram para o caixa da Holding.")
                        st.rerun()

    elif menu == "Arquivo de Banimentos":
        st.subheader("📂 Lista Negra (Histórico de Expulsões)")
        if st.session_state.lista_negra:
            st.table(st.session_state.lista_negra)
        else:
            st.info("Nenhum banimento registrado até o momento.")

    elif menu == "Configuração da Holding":
        st.subheader("🛠️ Ferramentas do Patrão")
        novo_nome = st.text_input("Mudar Nome da Empresa", "Next Holding")
        if st.button("Aplicar Novo Nome"):
            st.success(f"Empresa renomeada para {novo_nome}!")

# --- PAINEL DO VENDEDOR ---
def painel_vendedor(user):
    u = st.session_state.usuarios[user]
    st.sidebar.title(f"Operador: {user}")
    if st.sidebar.button("SAIR"):
        st.session_state.logado = None
        st.rerun()

    if u['aviso']:
        st.error(f"⚠️ AVISO DA ADMINISTRAÇÃO: {u['aviso']}")

    st.header("🎯 Minha Meta de Saque")
    
    # Barra de Progresso para os R$ 2.000,00
    progresso = min(u['saldo_app'] / 2000, 1.0)
    st.progress(progresso)
    st.write(f"Saldo Atual: **R$ {u['saldo_app']:.2f}** / Meta para Saque: **R$ 2.000,00**")
    
    if u['status'] == 'Congelado':
        st.warning("⚠️ Sua conta está sob investigação. Os saques estão bloqueados.")

    st.divider()
    st.subheader("📦 Minha Vitrine (Vendas de R$ 600)")
    c1, c2, c3 = st.columns(3)
    produtos = [("Next Predictor", "🎯"), ("Next Auto-Vendas", "🤖"), ("Next Recovery", "🛡️")]
    
    for i, (nome, icon) in enumerate(produtos):
        with [c1, c2, c3][i]:
            st.info(f"{icon} **{nome}**")
            if st.button(f"Link de Venda {i+1}"):
                st.code(f"checkout.next.holding/ref={user}")

    st.divider()
    if st.button("📢 SIMULAR VENDA REALIZADA (Teste de Split)"):
        # Lógica: R$ 375 pro Wellington, R$ 225 pro Vendedor
        st.session_state.usuarios['Wellington']['lucro_real'] += 375.00
        st.session_state.usuarios[user]['saldo_app'] += 225.00
        st.session_state.usuarios[user]['vendas'] += 1
        st.balloons()
        st.success("Venda processada! R$ 375 enviados ao CEO Wellington.")
        st.rerun()

# --- MOTOR PRINCIPAL ---
if 'logado' not in st.session_state:
    tela_login()
else:
    if st.session_state.usuarios[st.session_state.logado]['cargo'] == 'Dono':
        painel_wellington()
    else:
        painel_vendedor(st.session_state.logado)
