import pandas as pd
import streamlit as st
from americanas.americanas import buscar_produtos as buscar_americanas
from mercadolivre.mercadolivre import buscar_produtos as buscar_mercadolivre

# Função para encontrar o menor e maior preço
def comparar_precos(produtos_americanas, produtos_mercadolivre):
    df_americanas = pd.DataFrame(produtos_americanas, columns=['Nome', 'Link', 'Preço'])
    df_mercadolivre = pd.DataFrame(produtos_mercadolivre, columns=['Nome', 'Link', 'Preço'])
    
    if not df_americanas['Preço'].isnull().all() and not df_mercadolivre['Preço'].isnull().all():
        menor_preco_americanas = df_americanas['Preço'].min()
        maior_preco_americanas = df_americanas['Preço'].max()

        menor_preco_mercadolivre = df_mercadolivre['Preço'].min()
        maior_preco_mercadolivre = df_mercadolivre['Preço'].max()

        # Comparando qual site tem o menor preço
        if menor_preco_americanas < menor_preco_mercadolivre:
            menor_produto_americanas = df_americanas[df_americanas['Preço'] == menor_preco_americanas]
            st.markdown(f'<p style="font-size: 18px; color: #008000;">O menor preço está na Americanas: <strong>R${menor_preco_americanas:.2f}</strong></p>', unsafe_allow_html=True)
            st.markdown(f"**Produto**: {menor_produto_americanas.iloc[0]['Nome']}")
            st.markdown(f"[Link para o produto]( {menor_produto_americanas.iloc[0]['Link']} )")
        else:
            menor_produto_mercadolivre = df_mercadolivre[df_mercadolivre['Preço'] == menor_preco_mercadolivre]
            st.markdown(f'<p style="font-size: 18px; color: #FF5733;">O menor preço está no Mercado Livre: <strong>R${menor_preco_mercadolivre:.2f}</strong></p>', unsafe_allow_html=True)
            st.markdown(f"**Produto**: {menor_produto_mercadolivre.iloc[0]['Nome']}")
            st.markdown(f"[Link para o produto]( {menor_produto_mercadolivre.iloc[0]['Link']} )")

        # Comparando qual site tem o maior preço
        if maior_preco_americanas > maior_preco_mercadolivre:
            maior_produto_americanas = df_americanas[df_americanas['Preço'] == maior_preco_americanas]
            st.markdown(f'<p style="font-size: 18px; color: #FF5733;">O maior preço está na Americanas: <strong>R${maior_preco_americanas:.2f}</strong></p>', unsafe_allow_html=True)
            st.markdown(f"**Produto**: {maior_produto_americanas.iloc[0]['Nome']}")
            st.markdown(f"[Link para o produto]( {maior_produto_americanas.iloc[0]['Link']} )")
        else:
            maior_produto_mercadolivre = df_mercadolivre[df_mercadolivre['Preço'] == maior_preco_mercadolivre]
            st.markdown(f'<p style="font-size: 18px; color: #FF5733;">O maior preço está no Mercado Livre: <strong>R${maior_preco_mercadolivre:.2f}</strong></p>', unsafe_allow_html=True)
            st.markdown(f"**Produto**: {maior_produto_mercadolivre.iloc[0]['Nome']}")
            st.markdown(f"[Link para o produto]( {maior_produto_mercadolivre.iloc[0]['Link']} )")

    else:
        st.write("Nenhum preço válido encontrado para comparação.")

def app():
    st.title('🔍 Comparador de Preços: Americanas vs Mercado Livre')

    produto_name = st.text_input('Qual produto você deseja?')

    if produto_name:
        st.write(f'Buscando por **"{produto_name}"**...')

        # Buscar os produtos nos dois sites
        produtos_americanas = buscar_americanas(produto_name)
        produtos_mercadolivre = buscar_mercadolivre(produto_name)

        if produtos_americanas and produtos_mercadolivre:
            # Comparar os preços
            comparar_precos(produtos_americanas, produtos_mercadolivre)

            # Exibir todos os outros produtos encontrados
            st.markdown("## Produtos Encontrados")

            # Usando colunas para exibir os produtos lado a lado
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🛍️ Americanas")
                for index, row in pd.DataFrame(produtos_americanas, columns=['Nome', 'Link', 'Preço']).iterrows():
                    st.markdown(f'''
                    <div style="border: 2px solid #008000; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 128, 0, 0.2);">
                        <p><strong>{row['Nome']}</strong></p>
                        <p><strong>Preço:</strong> R${row['Preço']:.2f}</p>
                        <p><a href="{row['Link']}" target="_blank" style="color: #008000;">Ver Produto</a></p>
                    </div>
                    ''', unsafe_allow_html=True)

            with col2:
                st.markdown("### 🛒 Mercado Livre")
                for index, row in pd.DataFrame(produtos_mercadolivre, columns=['Nome', 'Link', 'Preço']).iterrows():
                    st.markdown(f'''
                    <div style="border: 2px solid #FF5733; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(255, 87, 51, 0.2);">
                        <p><strong>{row['Nome']}</strong></p>
                        <p><strong>Preço:</strong> R${row['Preço']:.2f}</p>
                        <p><a href="{row['Link']}" target="_blank" style="color: #FF5733;">Ver Produto</a></p>
                    </div>
                    ''', unsafe_allow_html=True)

        else:
            st.write("Nenhum produto encontrado em um dos sites.")

if __name__ == "__main__":
    app()
