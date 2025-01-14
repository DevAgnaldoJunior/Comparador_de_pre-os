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

# Função para encontrar o menor e maior preço
def encontrar_menor_maior_preco(produtos):
    df_produtos = pd.DataFrame(produtos, columns=['Nome', 'Link', 'Preço'])
    
    if not df_produtos['Preço'].isnull().all():  # Verifica se há preços válidos
        menor_preco = df_produtos['Preço'].min()
        maior_preco = df_produtos['Preço'].max()

        # Filtrar os produtos correspondentes aos preços encontrados
        produto_menor_preco = df_produtos[df_produtos['Preço'] == menor_preco]
        produto_maior_preco = df_produtos[df_produtos['Preço'] == maior_preco]

        return produto_menor_preco, produto_maior_preco, menor_preco, maior_preco
    else:
        return None, None, None, None

# Frontend com Streamlit
def app():
    st.title('Comparador de Preços do Mercado Livre')

    produto_name = st.text_input('Qual produto você deseja?')

    if produto_name:
        st.write(f'Buscando por **"{produto_name}"**...')

        # Buscar os produtos
        produtos = buscar_produtos(produto_name)

        if produtos:
            # Encontrar menor e maior preço
            produto_menor_preco, produto_maior_preco, menor_preco, maior_preco = encontrar_menor_maior_preco(produtos)

            if produto_menor_preco is not None and produto_maior_preco is not None:
                # Criar colunas lado a lado para o produto mais barato e o mais caro
                col1, col2 = st.columns(2)

                # Envolvendo as colunas com bordas e garantindo altura igual
                with col1:
                    # Usando HTML e CSS para aplicar uma borda à coluna inteira
                    st.markdown(f'''
                    <div style="border: 2px solid green; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 128, 0, 0.2); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                        <h3 style="color: green;">Produto com Menor Preço:</h3>
                        <p><strong>Nome:</strong> {produto_menor_preco.iloc[0]["Nome"]}</p>
                        <p><strong>Preço:</strong> R${menor_preco:.2f}</p>
                        <p><a href="{produto_menor_preco.iloc[0]['Link']}" target="_blank">Link para o produto</a></p>
                    </div>
                    ''', unsafe_allow_html=True)

                with col2:
                    # Usando HTML e CSS para aplicar uma borda à coluna inteira
                    st.markdown(f'''
                    <div style="border: 2px solid red; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(255, 0, 0, 0.2); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                        <h3 style="color: red;">Produto com Maior Preço:</h3>
                        <p><strong>Nome:</strong> {produto_maior_preco.iloc[0]["Nome"]}</p>
                        <p><strong>Preço:</strong> R${maior_preco:.2f}</p>
                        <p><a href="{produto_maior_preco.iloc[0]['Link']}" target="_blank">Link para o produto</a></p>
                    </div>
                    ''', unsafe_allow_html=True)

                

            else:
                st.write("Nenhum produto com preço válido encontrado.")
            
            # Exibir todos os outros produtos
            st.markdown("## Todos os Produtos Encontrados:")
            for index, row in pd.DataFrame(produtos, columns=['Nome', 'Link', 'Preço']).iterrows():
                st.markdown(f"**Nome**: {row['Nome']}")
                st.markdown(f"**Preço**: R${row['Preço']:.2f}")
                st.markdown(f"[Link para o produto]({row['Link']})")
                st.write('---')
        else:
            st.write("Nenhum produto encontrado para a pesquisa.")

if __name__ == "__main__":
    app()
