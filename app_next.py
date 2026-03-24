import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO MASTER ---
st.set_page_config(page_title="HOLDING NEXT - COMANDO CENTRAL", layout="wide")

# --- BANCO DE DATOS (Simulado em Session State) ---
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        'Wellington': {'senha': 'ceo', 'cargo': 'Dono', 'lucro_real': 15450.00, 'status': 'Ativo', 'aviso': ''},
        'Carlos_Vendedor': {'senha': 'v1', 'cargo': 'Vendedor', 'saldo_app': 450.00, 'vendas': 2, 'status': 'Ativo', 'aviso': ''},
        'Ana_Next': {'senha': 'v2', 'cargo': 'Vendedor', 'saldo_app': 0.00, 'vendas': 0, 'status': 'Ativo', 'aviso': ''}
    }
if 'lista_negra' not in st.session_state:
    st.session_state.lista_negra = []

# --- LÓGICA DE LOGIN ---
def tela_login():
    st.title("🎯 NEXT HOLDING - LOGIN DE ELITE")
    user = st.text_input("ID do Operador")
    senha = st.text_input("Chave de Acesso", type="password")
    if st.button("AUTENTICAR"):
        if user in st.session_state.usuarios:
            u = st.session_state.usuarios[user]
            if u['senha'] == senha:
                if u['status'] == 'Banido':
                    st.error("🚫 ACESSO BLOQUEADO PELA ADMINISTRAÇÃO NEXT. Sua conta foi encerrada por violação grave.")
                else:
                    st.session_state.logado = user
                    st.rerun()
        else:
            st.error("Credenciais Inválidas.")

# --- PAINEL DO DONO (WELLINGTON) ---
def painel_wellington():
    st.sidebar.title(f"👑 CEO: {st.session_state.logado}")
    aba = st.sidebar.radio("Navegação", ["Dashboard", "Gestão de Equipe", "Arquivo de Banimentos", "Configuração Holding"])
    
    if st.sidebar.button("Sair"):
        st.session_state.logado = None
        st.rerun()

    if aba == "Dashboard":
        st.header("📊 Resumo da Holding")
        c1, c2, c3 = st.columns(3)
        c1.metric("Meu Lucro Real", f"R$ {st.session_state.usuarios['Wellington']['lucro_real']:.2f}")
        c2.metric("Membros Ativos", len([x for x in st.session_state.usuarios if st.session_state.usuarios[x]['status'] == 'Ativo']))
        c3.metric("Contas Banidas", len(st.session_state.lista_negra))

    elif aba == "Gestão de Equipe":
        st.subheader("👥 Controle de Operadores")
        for user, info in st.session_state.usuarios.items():
            if info['cargo'] != 'Dono' and info['status'] != 'Banido':
                with st.expander(f"👤 {user} | Saldo: R$ {info['saldo_app']:.2f} | Status: {info['status']}"):
                    col1, col2, col3 = st.columns(3)
                    if col1.button(f"⚠️ Advertência", key=f"adv_{user}"):
                        st.session_state.usuarios[user]['aviso'] = "Você violou as Regras de Ouro. Próximo erro será banimento."
                        st.warning(f"Advertência enviada para {user}")
                    
                    if col2.button(f"❄️ Congelar Saldo", key=f"cong_{user}"):
                        st.session_state.usuarios[user]['status'] = 'Congelado'
                        st.info(f"Saldo de {user} congelado para investigação.")

                    if col3.button(f"🚫 BANIR E DELETAR", key=f"ban_{user}"):
                        saldo_retido = info['saldo_app']
                        st.session_state.lista_negra.append({'usuario': user, 'saldo_retido': saldo_retido, 'motivo': 'Violação Grave'})
                        st.session_state.usuarios[user]['status'] = 'Banido'
                        st.error(f"Usuário {user} foi expulso. R$ {saldo_retido} retidos no caixa.")
                        st.rerun()

    elif aba == "Arquivo de Banimentos":
        st.subheader("📂 Lista Negra da Next")
        if st.session_state.lista_negra:
            st.table(st.session_state.lista_negra)
        else:
            st.write("Nenhum banimento registrado.")

    elif aba == "Configuração Holding":
        st.subheader("🛠️ Ferramentas do Patrão")
        nome_empresa = st.text_input("Mudar Nome da Empresa", "Next Holding")
        if st.button("Salvar Alterações"):
            st.success(f"Empresa atualizada para {nome_empresa}!")

# --- PAINEL DO VENDEDOR ---
def painel_vendedor(user):
    u = st.session_state.usuarios[user]
    st.sidebar.title(f"Operador: {user}")
    if st.sidebar.button("Sair"):
        st.session_state.logado = None
        st.rerun()

    if u['aviso']:
        st.warning(f"🚨 MENSAGEM DA ADMINISTRAÇÃO: {u['aviso']}")

    st.header("⚡ Painel de Vendas")
    st.write(f"Status da Conta: **{u['status']}**")
    
    st.metric("Meu Saldo (R$)", f"{u['saldo_app']:.2f}")
    if u['status'] == 'Congelado':
        st.error("⚠️ Seu saldo está sob análise. Saques temporariamente bloqueados.")

    if st.button("📢 Simular Venda de R$ 600"):
        st.session_state.usuarios['Wellington']['lucro_real'] += 375.00
        st.session_state.usuarios[user]['saldo_app'] += 225.00
        st.success("Venda processada! R$ 375 foram para o cofre do Wellington.")
        st.rerun()

# --- NAVEGAÇÃO PRINCIPAL ---
if 'logado' not in st.session_state:
    tela_login()
else:
    if st.session_state.usuarios[st.session_state.logado]['cargo'] == 'Dono':
        painel_wellington()
    else:
        painel_vendedor(st.session_state.logado)
        
