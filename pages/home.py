# --- Importar as bibliotecas --- #
from PIL import Image
from imagens import *
import streamlit as st

# --- Importar a string com os elementos para esconder no menu --- #
from menu_css import css

# --- Importar o módulo para mostrar o produto pesquisado --- #
from mostrar_produto import mostrar_produto

# --- Configurações da página --- #
st.set_page_config(
    page_title='Entregando Beleza',
    page_icon=Image.open(FAVICON),
    layout='wide'
)

# --- Estilo de alguns elementos --- #
st.html(css)

# --- Banner do site --- #
st.image(BANNER)

# --- Logo da side bar --- #
st.logo(image=LOGO_MENU_ABERTO, icon_image=LOGO_MENU_FECHADO)

# --- Compras na sessão do site --- #
if 'compras' not in st.session_state:
    st.session_state.compras = {'produtos': 0}

# --- Código do produto salvo na sessão --- #
if 'codigo_pesquisado' not in st.session_state:
    st.session_state.codigo_pesquisado = None

# --- Informações do cliente na sessão --- #
if 'cliente' not in st.session_state:
    st.session_state.cliente = {}

# --- Título da página --- #
st.title('Entregando Beleza')

# --- Descrição da página --- #
st.write('<p class="fonte">Bem-vindo(a) ao <b>Entregando Beleza</b>! Aqui você pode realizar as sua compras '
         'diretamente do site. Basta digitar o código do produto, clicar no botão <b>Pesquisar</b> e verificar '
         'se o produto é o que você tem em mãos. Após isso, clique no botão <b>Adicionar ao carrinho</b> '
         'e quando quiser finalizar as suas compras, basta clicar no botão <b>Finalizar</b> que você será '
         'redirecionado(a) à página de finalização da compra.</p>', unsafe_allow_html=True)

# --- Campo para digitar o código --- #
st.subheader('Código do produto:')
codigo = st.number_input(
    label='',
    label_visibility='hidden',
    placeholder='Digite o código do produto',
    min_value=0,
    max_value=9999,
    value=None,
)

# --- Botão para mostra o produto --- #
pesquisar = st.button(
    label='Pesquisar',
    use_container_width=True
)

# --- Verificar se o código é válido --- #
if pesquisar:
    if codigo is not None:
        st.session_state.codigo_pesquisado = codigo
    else:
        st.warning('Por favor, informe o código.')

# --- Mostrar o produto pesquisado --- #
if st.session_state.codigo_pesquisado is not None:
    mostrar_produto(st.session_state.codigo_pesquisado)

# --- Botão para finalizar a compra --- #
if len(st.session_state.compras) > 1:
    finalizar = st.button(
        label='Finalizar compra',
        use_container_width=True
    )
    if finalizar:
        st.switch_page('./pages/finalizar_compra.py')
