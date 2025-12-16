# --- Importar o Streamlit --- #
import streamlit as st

# --- Criar o menu de navegação das páginas --- #
pg = st.navigation(
    [st.Page('./pages/home.py', title='Página Inicial'),
     st.Page('./pages/finalizar_compra.py', title='Finalizar')],
    position='hidden'
)
pg.run()