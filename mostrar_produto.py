# --- Importar as bibliotecas --- #
import requests
import streamlit as st


def mostrar_produto(codigo: int):
    """
    Função responsável por mostrar os produtos na tela.
    :param codigo: Código do produto digitado.
    """
    # --- Acessar o banco de dados no Firebase --- #
    link = 'https://entregando-beleza-produtos-out-default-rtdb.firebaseio.com/'

    # --- Obter os códigos do banco --- #
    codigos = list(requests.get(f'{link}/.json').json().keys())

    # --- Verificar se o código informado está presente no banco --- #
    if str(codigo) not in codigos:
        st.warning('O código informado não existe.')

    else:
        # --- Obter o dicionário da classe do produto --- #
        requisicao = requests.get(f'{link}/{codigo}.json')
        dic_requisicao = requisicao.json()

        # --- Mostrar o produto --- #
        with st.container(border=True):
            st.header('Produto:')
            # --- Colocar a foto do produto --- #
            foto = dic_requisicao['foto']

            # --- Colocar o nome do produto --- #
            nome = dic_requisicao['nome']

            # --- Colocar o preço --- #
            preco = dic_requisicao['preco']

            # --- Colocar as informações do produto --- #
            st.image(foto, width=400)
            st.subheader(f'Produto: {nome}')
            st.subheader(f'Preço: R$ {str(preco).replace(".", ",")}0')
            quantidade = st.number_input(
                label=f'Máx: {int(dic_requisicao["estoque"])}',
                min_value=1,
                max_value=int(dic_requisicao['estoque'])
            )

            adicionar = st.button(
                label='Adicionar ao carrinho',
                use_container_width=True
            )
            if adicionar:
                st.session_state.compras[codigo] = {
                    'foto': foto,
                    'nome': nome,
                    'quantidade': quantidade,
                    'preco': preco,
                    'codigo': codigo,
                    'valor_unitario': preco
                }
                st.success(f'O produto {nome} foi adicionado ao carrinho!')
