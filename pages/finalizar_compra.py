# --- Importar as bibliotecas --- #
import time
from PIL import Image
from imagens import *
import streamlit as st

# --- Importar a string com os elementos para esconder no menu --- #
from menu_css import css

# --- Importar o módulo para atualizar o estoque --- #
from atualizar_banco import atualizar_banco

# --- Importar o módulo para pagar pelo Mercado Pago --- #
from pagamento import pagamento

# --- Configurações da página --- #
st.set_page_config(
    page_title='Finalizar compra',
    page_icon=Image.open(FAVICON),
    layout='wide',
    initial_sidebar_state='collapsed'
)

# --- Estilo de alguns elementos --- #
st.html(css)

# --- Logo da side bar --- #
st.logo(image=LOGO_MENU_ABERTO, icon_image=LOGO_MENU_FECHADO)

# --- Título da página --- #
st.title('Finalizar compra')

# --- Descrição da página --- #
st.write('<p class="fonte">Aqui você poderá realizar o pagamento dos seus produtos. Ao clicar no botão '
         '<b>Pagar</b>, um botão abaixo escrito <b>Ir ao Mercado Pago</b> aparecerá. Clique-o e você será redirecionado ao site do <b>Mercado Pago</b>; podendo pagar por '
         '<b>PIX</b> ou <b>cartão de crédito</b>!',
         unsafe_allow_html=True)

# --- Produtos comprados --- #
compras = st.session_state.compras

# --- Lista com os produtos --- #
produtos = [produto for produto in compras.keys() if produto != 'produtos']

# --- Dicionário com o carrinho --- #
dic_carrinho = dict.fromkeys(produtos)

# --- Valor total da compra --- #
total = 0

# --- Colocar cada bloco como um produto --- #
for produto in produtos:
    with st.container(border=True):
        # --- Dicionário com as informações do produto --- #
        dic_produto = compras[produto]

        # --- Chaves do dicionário --- #
        chaves = [chave for chave in dic_produto.keys()]

        # --- Dicionário do carrinho atualizado --- #
        dic_carrinho[produto] = {}

        # --- Foto do produto --- #
        st.subheader('Foto:')
        foto = dic_produto['foto']
        st.image(foto, width=250)

        # --- Nome do produto --- #
        nome = dic_produto['nome']
        st.subheader(f'Produto: {nome}')
        dic_carrinho[produto]['nome'] = nome

        # --- Quantidade desejada --- #
        quantidade = dic_produto['quantidade']
        st.subheader(f'Quantidade: {quantidade}')
        dic_carrinho[produto]['quantidade'] = quantidade

        # --- Preço unitário --- #
        preco = dic_produto['preco']
        st.subheader(f'Preço (unid.): R$ {str(preco).replace(".", ",")}0')
        dic_carrinho[produto]['preco'] = preco

        # --- Valor total --- #
        preco_quantidade_str = f'{preco * quantidade:.1f}0'
        st.subheader(f'Valor: R$ {preco_quantidade_str.replace(".", ",")}')
        dic_carrinho[produto]['total'] = preco * quantidade

        # --- Adicionar o código do produto --- #
        codigo = dic_produto['codigo']
        dic_carrinho[produto]['codigo'] = codigo

        # --- Total da compra --- #
        total += preco * quantidade

# --- Mostrar o total da compra --- #
total_str = f'{total:.1f}0'
st.subheader(f'Total: R$ {total_str.replace(".", ",")}')

# --- Botão para pagar a compra --- #
pagar = st.button(
    label='Pagar',
    use_container_width=True
)

# --- Clicar no botão para pagar --- #
if pagar:
    # --- Informações do cliente --- #
    cliente = st.session_state.cliente
    cliente['produtos'] = list()
    cliente['quantidade'] = list()
    cliente['codigos'] = list()
    cliente['valor_unitario'] = list()

    # --- Colocar os produtos e o valor dos produtos --- #
    for produto in produtos:
        dic_produto = dic_carrinho[produto]
        produto = dic_produto['nome']
        cliente['produtos'].append(produto)
        quantidade = dic_produto['quantidade']
        cliente['quantidade'].append(quantidade)
        codigo = dic_produto['codigo']
        cliente['codigos'].append(codigo)
        valor_unitario = dic_produto['total'] / dic_produto['quantidade']
        cliente['valor_unitario'].append(valor_unitario)

    # --- Atualizar a quantidade do produto no JSON --- #
    for quantidade, chave in zip(cliente['quantidade'], produtos):
        for codigo in cliente['codigos']:
            atualizar_banco(codigo, quantidade)
        break

    # --- Botão para ir ao Mercado Pago --- #
    st.success('Clique no botão abaixo para realizar o pagamento no pelo Mercado Pago')
    pagamento()
    time.sleep(15)
    st.switch_page('./pages/home.py')
