import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Função para buscar os produtos no Mercado Livre
def buscar_produtos(produto_name):
    url_base = "https://lista.mercadolivre.com.br/"
    response = requests.get(url_base + produto_name)
    site = BeautifulSoup(response.text, 'html.parser')

    # Busca por todos os produtos
    produtos = site.find_all('li', attrs={'class': "ui-search-layout__item"})

    lista_produtos = []

    for produto in produtos:
        # Título
        nome_do_produto = produto.find('h2')
        if nome_do_produto is None:
            nome_do_produto = produto.select_one('h2.ui-search-item__title')

        # Link do produto
        link_tag = produto.find('a', href=True)
        link = link_tag['href'] if link_tag else None

        # Certifique-se de que o link não seja nulo e que esteja completo
        if link and not link.startswith('http'):
            link = f'https://www.mercadolivre.com.br{link}'

        # Preço
        preco = produto.find('span', attrs={'class': 'andes-money-amount__fraction'})

        # Adiciona os dados à lista
        preco_value = float(preco.text.replace('.', '').replace(',', '.')) if preco else None

        lista_produtos.append([ 
            nome_do_produto.text.strip() if nome_do_produto else None,
            link,
            preco_value
        ])

    return lista_produtos

