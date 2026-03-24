import streamlit as st

st.title("Meu Primeiro App com Streamlit 🚀")
st.write("Olá, este é um aplicativo rodando direto do GitHub!")

nome = st.text_input("Qual é o seu nome?")
if nome:
    st.write(f"Bem-vindo ao mundo da programação, {nome}!")
  
