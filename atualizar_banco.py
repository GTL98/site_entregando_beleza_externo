# --- Importar as bibliotecas --- #
import json
import requests
import streamlit as st


def atualizar_banco(codigo: str, quantidade: int):
    """
    Função responsável por atualizar a quantidade de produtos do banco de dados.
    :param codigo: Código do produto.
    :param quantidade: Quantidade comprada.
    """
    # --- Acessar o banco de dados no Firebase --- #
    link = 'https://entregando-beleza-produtos-out-default-rtdb.firebaseio.com/'

    # --- Obter o dicionário da classe do produto --- #
    requisicao = requests.get(f'{link}/{codigo}/.json')
    dic_requisicao = requisicao.json()
    dic_copia = dic_requisicao

    # --- Atualizar o valor da quantidade --- #
    if dic_copia['estoque'] > 0:
        dic_copia['estoque'] -= quantidade
        if dic_copia['estoque'] < 0:
            dic_copia['estoque'] = 0
        requests.patch(f'{link}/{codigo}//.json', data=json.dumps(dic_copia))
