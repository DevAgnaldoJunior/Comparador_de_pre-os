from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import streamlit as st
import pandas as pd

# Função para inicializar o driver do Selenium
def init_driver():
    options = Options()
    #options.headless = False  #para não abrir o navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Função para buscar produtos
def buscar_produtos(produto_name):
    url_base = "https://www.americanas.com.br/busca/"
    
    driver = init_driver()
    driver.get(url_base + produto_name)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Espera um pouco para garantir que o conteúdo seja carregado
    time.sleep(3) 

    # Obter o HTML da página carregada
    site = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()  # Fechar o navegador após a requisição

    # Agora, continue com o mesmo processo de extração de dados com BeautifulSoup
    produtos = site.find_all('div', attrs={'class': "src__Wrapper-sc-1l8mow4-0"})

    lista_produtos = []

    for produto in produtos:
        nome_do_produto = produto.find('h3')
        if nome_do_produto is None:
            nome_do_produto = produto.select_one('product-name')


        # Link do produto
        link_tag = produto.find('a', href=True)
        link = link_tag['href'] if link_tag else None

        # Certifique-se de que o link não seja nulo e que esteja completo
        if link and not link.startswith('http'):
            link = f'https://www.americanas.com.br{link}'

        # Preço
        preco = produto.find('span', attrs={'class': 'src__Text-sc-154pg0p-0'})

        if preco:  # Verifica se o preço foi encontrado
            preco_texto = preco.text.strip()  # Obtém o texto do preço
            preco_limpo = preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip()  # Limpeza
            try:
                preco_value = float(preco_limpo)  # Tenta converter para float
            except ValueError:
                preco_value = None  # Se não conseguir converter, atribui None
        else:
            preco_value = None  # Se não encontrar o preço, atribui None

        lista_produtos.append([ 
            nome_do_produto.text.strip() if nome_do_produto else "Nome não disponivel",
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

    st.title('Comparador de Preços da americanas')

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

                with col1:
                    st.markdown(f'''
                    <div style="border: 2px solid green; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 128, 0, 0.2); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                        <h3 style="color: green;">Produto com Menor Preço:</h3>
                        <p><strong>Nome:</strong> {produto_menor_preco.iloc[0]["Nome"]}</p>
                        <p><strong>Preço:</strong> R${menor_preco:.2f}</p>
                        <p><a href="{produto_menor_preco.iloc[0]['Link']}" target="_blank">Link para o produto</a></p>
                    </div>
                    ''', unsafe_allow_html=True)

                with col2:
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
                st.markdown(f"**Preço**: R${row['Preço']:.2f}" if row['Preço'] is not None else "Preço não disponível")
                st.markdown(f"[Link para o produto]({row['Link']})")
                st.write('---')
        else:
            st.write("Nenhum produto encontrado para a pesquisa.")

if __name__ == "__main__":
    app()
