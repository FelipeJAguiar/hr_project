import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from folium.plugins import MarkerCluster
from PIL import Image
import folium
import geopandas

# Configure layout.
st.set_page_config(layout='wide')

# Images used.
image=Image.open('img/hrf.png')
image2=Image.open('img/r3.gif')
image3=Image.open('img/hrf1.png')

st.image(image3, use_column_width=True)
selected= option_menu(menu_title="Selecione:",
             options= ['Página Inicial', 'Descrição dos Dados', 'Insights de Negócio', 'Resultados'],
             icons=['house','braces','bar-chart', 'calendar2-check'],
             menu_icon='rocket',
             default_index = 0,
             orientation='horizontal',
            styles={"container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "rgba(204, 189, 217, 1)", "font-size": "18px"},
                    "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px",
                                       "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "rgba(127,90,159,255)"},})
st.markdown("""
<style>
MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if selected == 'Página Inicial':
    st.image(image,use_column_width=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Seja bem vindo(a) ao projeto House Rocket!</h1>", unsafe_allow_html=True)
    st.header(' Descrição')
    st.write('A House Rocket é uma empresa do ramo imobiliário com foco na compra e venda de imóveis. Visando a maximização de seus resultados, a empresa requisitou o projeto como forma de otimizar o processo de tomada de decisão de quais negócios devem ser concretizados. Para isso, disponibilizou um conjunto de dados contendo alguns atributos de cada imóvel, como por exemplo: localização, preço, data de construção, entre outros. Além disso, a empresa definiu seu objetivo com o projeto em três perguntas, que são:')
    st.write(':point_right: Quais os 300 imóveis que deveriam ser adquiridos e por qual preço?')
    st.write(':point_right: Para os imóveis adquiridos, qual seria o preço da venda?')
    st.write(':point_right: Quais os meses mais indicados para comprar e vender?')
    st.header('Premissas adotadas')
    st.write('As premissas são alterações feitas nos dados originais a fim de melhorar a qualidade da análise. Para o projeto, tomou-se as seguintes premissas:')
    st.write('- Os valores duplicados da coluna ID (identificação do imóvel) foram removidos considerando a compra mais recente;')
    st.write('- Por se tratar de um erro, o imóvel de 33 quartos foi alterado para 3 quartos;')
    st.write('- Excluídos os atributos que não seriam utilizados nas análises.')
    st.write('- Caso o preço seja menor que a mediana de preços por região, o imóvel esteja em boas condições e tenha boa qualidade de construção e design, deve ser adquirido.')
    st.write('- Preço de venda varia de acordo com a sazonalidade.')
    st.header('Planejamento da Solução')
    st.subheader(' Passos do planejamento:')
    st.write(':one:  Coleta dos dados (Kaggle);')
    st.write(':two:  Análise das questões de negócio (demandas do cliente e insights);')
    st.write(':three:  Tratamento de dados (limpeza e ajustes);')
    st.write(':four:  Demonstração da solução para as demandas da empresa e insights;')
    st.write(':five:  Demonstração de resultados obtidos;')
    st.subheader(' Ferramentas')
    st.write('- Python 3.9, PyCharm, Jupyter (manipulação dos dados)')
    st.write('- Streamlit  (construção das visualizações)')
    st.write('- Heroku (disponibilização das visualizações)')

    st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    z1, z2, z3 = st.columns((1, 1, 1))
    z2.markdown("![Alt Text](https://media.giphy.com/media/hNWmkvCgaj6SxgABYl/giphy.gif)")

    cont = '[LinkedIn](https://www.linkedin.com/in/felipejaguiar) | [GitHub](https://github.com/felipejaguiar)'
    st.caption('Desenvolvido por Felipe Aguiar, Cientista de Dados e Engenheiro de Produção.')
    st.caption(cont)

@st.cache(allow_output_mutation=True)
def get_data(path):
   data = pd.read_csv(path)
   return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
   geofile = geopandas.read_file(url)
   return geofile

@st.cache(allow_output_mutation=True)
# Transforming data.
def transf_data(data):
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    data = data.rename(columns={'sqft_basement':'basement'})

    #===== Define column price/ft²:
    data['price_sqft'] = data['price'] / data['sqft_lot']

    #===== Solve the error of bedrooms column:
    data['bedrooms'] = data['bedrooms'].apply(lambda x: 3 if x==33 else x)

    #===== Exclude columns not used and duplicates ids:
    data.drop(['sqft_living15', 'sqft_lot15'], axis=1, inplace=True)
    data.drop_duplicates(subset=['id'], keep='first', inplace=True)

    return data

@st.cache(allow_output_mutation=True)
# Loading on data.
def load_data(data):
    #===== Median price by zipcode.
    df = data[['price', 'zipcode']].groupby('zipcode').median()
    data = pd.merge(data, df, on='zipcode', how='inner')
    data = data.rename(columns={'price_x': 'price', 'price_y': 'price_median'})

    #===== Seasons of year.
    data['season'] = data['date'].apply(lambda x: 'fall' if (x < '2014-06-21') else
                                                    'winter' if (x >= '2014-06-21') & (x < '2014-09-23') else
                                                    'spring' if (x >= '2014-09-23') & (x < '2014-12-21') else
                                                    'summer' if (x >= '2014-12-21') & (x < '2015-03-21') else
                                                    'fall')

    #===== Median price by season.
    dfs = data[['price', 'season']].groupby('season').median()
    data['price_season'] = data['season'].apply(lambda x: dfs['price']['fall'] if x == 'fall' else
                                                            dfs['price']['spring'] if x == 'spring' else
                                                            dfs['price']['summer'] if x == 'summer' else
                                                            dfs['price']['winter'])

    #===== Buy column.
    data['buy'] = 0
    for i in range(len(data)):
        if (data.loc[i, 'condition'] >= 3) & (data.loc[i, 'grade'] >= 8) & (data.loc[i, 'price'] < data.loc[i, 'price_median']):
            data.loc[i, 'buy'] = "yes"
        else:
            data.loc[i, 'buy'] = "no"

    #===== Price sell column.
    data['price_sell'] = 0
    for i in range(len(data)):
        if data.loc[i, 'price_season'] > data.loc[i, 'price']:
            data.loc[i, 'price_sell'] = (data.loc[i, 'price'] * 0.1) + data.loc[i, 'price']
        else:
            data.loc[i, 'price_sell'] = (data.loc[i, 'price'] * 0.3) + data.loc[i, 'price']


    #===== Profit column.
    data['profit'] = 0
    for i in range(len(data)):
        if data.loc[i, 'buy'] == "yes":
            data.loc[i, 'profit'] = data.loc[i, 'price_sell'] - data.loc[i, 'price']
        else:
            data.loc[i, 'profit'] = 0

    return data

def data_description(data2):
    if selected == 'Descrição dos Dados':

        st.markdown("<h1 style='text-align: center; color: black;'>Descrição dos Dados</h1>", unsafe_allow_html=True)

        # Data attributes.
        text = """
        | ATRIBUTOS | DESCRIÇÃO |
        |-----------|-----------|
        | id | ID exclusivo para cada casa vendida |
        | date | Data da venda da casa |
        | price | Preço de cada casa vendida |
        | bedrooms | Número de quartos |
        | bathrooms | Número de banheiros, onde 0.5 indicam banheiros sem chuveiro |
        | sqft_living | Área construída em pés |
        | sqft_lot | Área do terreno em pés |
        | floors | Número de pisos, onde os decimais indicam a porcentagem da construção baseada no térreo |
        | waterfront | Define se o imóvel tem vista para água |
        | view | Escala de 0 a 4 que define quão boa é a vista do imóvel |
        | condition | Escala de 1 a 5 que define a condição atual do imóvel |
        | grade | Escala de 1 a 13, que define o grau de construção e design |
        | sqft_above | Área das construções acima do 1º piso, em pés |
        | sqft_basement | Área do porão em pés|
        | yr_built | Ano de construção do imóvel |
        | yr_renovated | Ano da última reforma do imóvel |
        | zipcode | Código postal |
        | lat | Coordenada latidudinal do imóvel |
        | long | Coordenada longitidudinal do imóvel |
        """
        if st.checkbox('Clique para ver descrição dos atributos.'):
            st.write(text)

        b1, b2, b3, b4 = st.columns((1, 1, 1, 1))
        # Price filter.
        min_price = int(data2['price'].min())
        max_price = int(data2['price'].max())
        f_price = b1.slider('Preço:', max_price, min_price)

        # Zipcode filter.
        f_zipcode = b2.multiselect('Códigos postais:', data2['zipcode'].sort_values().unique())

        # Histogram filter by price.
        filter_p = data2[data2['price'] < f_price]

        # Histogram filter by zipcode.
        if (f_zipcode != []):
            filter_p = filter_p.loc[filter_p['zipcode'].isin(f_zipcode), :]
        else:
            filter_p = filter_p.copy()

        # Metric filter.
        d = (len(filter_p) / len(data2))
        d1 = "{:.0%}".format(d)
        b3.metric(label="Total de imóveis", value=(len(filter_p)), delta=("{} dos imóveis".format(d1)), delta_color="normal")

        # Metric 2 filter.
        f = filter_p['price_sqft'].mean()
        f2 = "{:.2f}".format(f)
        fd = filter_p['price_sqft'].median()
        fd2 = "{:.2f}".format(fd)
        if f2 > fd2:
            b4.metric(label="Preço/ft² médio", value="USD$ {}".format(f2), delta="Acima da mediana", delta_color="inverse")
        else:
            b4.metric(label="Preço/ft² médio", value="USD$ {}".format(f2), delta="Abaixo da mediana", delta_color="inverse")

        # Price histogram chart.
        fig = px.histogram(filter_p, x='price', nbins=50)
        fig.update_traces(textposition='inside')
        fig.update_yaxes(showticklabels=False)
        fig.update_traces(marker_color='rgba(127,90,159,255)')

        d1, d2 = st.columns((1, 1))
        d1.subheader('Casas por faixa de preço (quantidade)')
        d1.plotly_chart(fig, use_container_width=True)

        # Descriptive analysis.
        stat_des = data2.select_dtypes(include=['int64','float64']).drop(['id', 'lat', 'long', 'price_median',
                                                                          'yr_built','yr_renovated','price_season',
                                                                          'price_sell','profit','price_sqft',], axis=1)

        # Descriptive analysis filter by Price.
        stat_des = (stat_des.loc[stat_des['price'] <= f_price])

        # Descriptive analysis filter by Zipcode.
        if (f_zipcode != []):
            stat_des = stat_des.loc[stat_des['zipcode'].isin(f_zipcode), :]
        else:
            stat_des = stat_des.copy()

        media = pd.DataFrame(stat_des.apply(np.mean))
        mediana = pd.DataFrame(stat_des.apply(np.median))
        stdev = pd.DataFrame(stat_des.apply(np.std))
        maxi = pd.DataFrame(stat_des.apply(np.max))
        mini = pd.DataFrame(stat_des.apply(np.min))
        stdes = pd.concat([maxi, mini, media, mediana, stdev], axis=1).reset_index()
        stdes.columns = ['attributes', 'max', 'min', 'mean', 'median','std']

        d2.subheader('Análise Descritiva')
        d2.dataframe(stdes)

        # Map.
        st.subheader('Mapa de Densidade')
        st.write('Mapa com as localizações de cada imóvel e seus respectivos preços. Onde as cores e tamanhos dos pontos representam a relevância do preço.')
        houses = data2[['id', 'lat', 'long', 'price', 'zipcode', 'bedrooms', 'bathrooms','floors']].copy()

        # Map filter by Price.
        dt = (houses.loc[houses['price'] <= f_price])

        # Map filter by Zipcode.
        if (f_zipcode != []):
            dt = houses.loc[houses['zipcode'].isin( f_zipcode ), : ]
        else:
            houses = houses.copy()

        # Map plot.
        fig1 = px.scatter_mapbox(dt,
                                lat="lat",
                                lon="long",
                                color="price",
                                color_continuous_scale=px.colors.sequential.Agsunset,
                                size_max=15,
                                zoom=10)
        fig1.update_layout(mapbox_style="open-street-map")
        fig1.update_layout(width=600, height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig1,use_container_width=True)

        z1,z2,z3=st.columns((1,1,1))
        z2.markdown("![Alt Text](https://media.giphy.com/media/hNWmkvCgaj6SxgABYl/giphy.gif)")

        return None

def get_hips(data2):
    if selected == 'Insights de Negócio':

        st.markdown("<h1 style='text-align: center; color: black;'>Insights de Negócio</h1>", unsafe_allow_html=True)
        st.write('Nesta seção são levantadas hipóteses que podem ser úteis em análises complementares para a tomada de decisão, no negócio.')

        c1, c2 = st.columns((1,1))
        c3, c4 = st.columns((1,1))
        c5, c6 = st.columns((1,1))
        
        datah = data2.copy()
        datah['yr_built'] = datah['yr_built'].astype(int)
        
        c1.subheader('H1: Imóveis reformados são 45% mais caros, na média.')
        c1.write(':white_check_mark: Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar imóveis e reformá-los.')
        datah['yr_renovated'] = datah['yr_renovated'].apply(lambda x: "no" if x == 0 else "yes")
        h1 = datah[['price', 'yr_renovated']].groupby('yr_renovated').mean()
        fig = px.bar(h1, x=h1.index, y=h1.columns)
        fig.update_traces(marker_color='rgba(127,90,159,255)')
        c1.plotly_chart(fig, use_container_width=True)

        c2.subheader('H2: Imóveis com data de construção menor que 1955, são 20% mais baratos, na média.')
        c2.write(':x: Inválida: Imóveis mais recentes tem praticamente a mesma média de preço que os antigos. Portanto, neste caso, o ano de construção tende a apresentar pouco impacto sobre os preços de compra dos imóveis.')
        datah['yr_built'] = datah['yr_built'].apply(lambda x: "pre-1955" if x < 1955 else "pos-1955")
        h2 = datah[['price', 'yr_built']].groupby('yr_built').mean().reset_index()
        fig2 = px.pie(h2, values=h2['price'], names=h2['yr_built'],color_discrete_sequence=['rgba(127,90,159,255)','rgb(111,64,112)'])
        c2.plotly_chart(fig2, use_container_width=True)

        c3.subheader('H3: Imóveis sem porão são 15% maiores do que os imóveis com porão.')
        c3.write(':white_check_mark: Válida: Imóveis com porão tem relativamente menores áreas construídas. Logo, focar em imóveis sem porão quando a área construída for um fator decisivo.')
        datah['basement'] = datah['basement'].apply(lambda x: "no" if x != 0 else "yes")
        h3 = datah[['sqft_living', 'basement']].groupby('basement').mean()
        fig3 = px.bar(h3, x=h3.index, y=h3.columns)
        fig3.update_traces(marker_color='rgba(127,90,159,255)')
        c3.plotly_chart(fig3, use_container_width=True)

        c4.subheader('H4: Imóveis com grade low/avg são 45% mais baratos que com grade good/high, na média.')
        c4.write(':white_check_mark: Válida: Os imóveis com baixo grau de construção e design são mais baratos, o que possibilitaria a compra e reforma, ou aproveitamento do terreno para novas construções.')
        datah['grade'] = datah['grade'].apply(lambda x: "low_avg" if x < 8 else "good_high")
        h4 = datah[['price', 'grade']].groupby('grade').mean().round(3)
        fig4 = px.bar(h4, x=h4.index, y=h4.columns)
        fig4.update_traces(marker_color='rgba(127,90,159,255)')
        c4.plotly_chart(fig4, use_container_width=True)

        c5.subheader('H5: 10% dos imóveis em piores condições tem os maiores grades.')
        c5.write(':white_check_mark: Válida: 19 imóveis de alto nível de construção apresentam nível baixo de condição atual, sendo propícios para reformas e revendas futuras.')
        dt2 = datah[['condition', 'grade']]
        h5 = (dt2.loc[dt2['condition'] <= 2]).groupby('grade').count()
        fig5 = px.bar(h5, x=h5.index, y=h5.columns)
        fig5.update_traces(marker_color='rgba(127,90,159,255)')
        c5.plotly_chart(fig5, use_container_width=True)

        c6.subheader('H6: O crescimento do preço dos imóveis MoM (month over month) é de 10%.')
        c6.write(':x: Inválida: Após uma sequência de queda entre Jun/2014 e Jan/2015, o preço médio de vendas cresceu. O que configura uma tendência de equilíbrio dos preços durante os meses analisados.')
        dt = datah[['date', 'price']]
        dt['date'] = pd.to_datetime(datah['date']).dt.strftime('%Y-%m')
        h6 = dt[['price', 'date']].groupby('date').mean().round(2)
        fig6 = px.line(h6, x=h6.index, y=h6.columns)
        fig6['data'][0]['line']['color'] = 'rgba(127,90,159,255)'
        fig6['data'][0]['line']['width'] = 5
        c6.plotly_chart(fig6, use_container_width=True)

        z1, z2, z3 = st.columns((1, 1, 1))
        z2.markdown("![Alt Text](https://media.giphy.com/media/hNWmkvCgaj6SxgABYl/giphy.gif)")

        return None

def results (data2):
    if selected == 'Resultados':

        st.markdown("<h1 style='text-align: center; color: black;'>Resultados</h1>", unsafe_allow_html=True)

        c1, c2, c3= st.columns((1, 1, 1))
        # Values metrics.
        metrics = data2.sort_values('profit', ascending=False).head(300)
        prc = metrics['price'].sum().round(0)
        dol = "${:,.2f}".format(prc).replace(",", "X").replace(".", ",").replace("X", ".")
        c1.metric(label="Preço total de compra dos 300 imóveis", value=(dol))

        prc_v = metrics['price_sell'].sum().round(0)
        dol0 = "${:,.2f}".format(prc_v).replace(",", "X").replace(".", ",").replace("X", ".")
        c2.metric(label="Preço total de venda dos 300 imóveis", value=(dol0))

        lcr = metrics['profit'].sum().round(0)
        dol1 = "${:,.2f}".format(lcr).replace(",", "X").replace(".", ",").replace("X", ".")
        prf = (lcr/prc)
        prf1 = "{:.0%}".format(prf)
        c3.metric(label="Lucratividade total",value=(dol1), delta=(prf1))

        # Houses to buy.
        st.header('Imóveis indicados para compra')
        st.write('Os imóveis sugeridos para a compra são os dispostos no mapa e estão devidamente identificados com seus IDs e alguns de seus atributos.')
        df3 = data2.sort_values('profit',ascending=False).head(300)
        df4 = df3[['lat','long','id','zipcode','sqft_living','sqft_lot','bedrooms','bathrooms','floors','waterfront','price_sell','profit']]

        buy_map = folium.Map(location=[data2['lat'].mean(),data2['long'].mean()],use_container_width=True,default_zoom_start=20)
        mc = MarkerCluster().add_to(buy_map)
        for name, row in df4.iterrows():
            folium.Marker([row['lat'], row['long']],
                            popup='ID: {8}, CEP: {9} Vendendo por USD$ {0:,.2f} terá lucro de USD$ {1:,.2f}. Área construída - {2:.2f} ft²; Área do terreno - {3:.2f} ft²; Quartos - {4:,.0f}; Banheiros - {5:,.0f}; Pisos - {6:,.2f}; Vista para água - {7}'
                          .format( row['price_sell'],row['profit'],
                                   row['sqft_living'],row['sqft_lot'],
                                   row['bedrooms'],row['bathrooms'],
                                   row['floors'],row['waterfront'],
                                   row['id'], row['zipcode']),icon=folium.Icon(color='purple',icon="home", prefix='fa')).add_to(mc)
        folium_static(buy_map)

        # Deals by months.
        st.subheader('Negócios por mês')
        st.write('A observação de negociações mensais nos ajuda a identificar os melhores meses pra se fazer negócio. Logo, os meses indicados para compra e venda, são:')

        c4, c5 = st.columns((1, 1))
        c4.metric(label="MÊS", value=("Junho, Julho, Abril"), delta=('VENDER'), delta_color="inverse")
        c5.metric(label="MÊS", value=("Janeiro, Fevereiro"), delta=('COMPRAR'))

        # Histogram chart.
        df5 = pd.to_datetime(data2['date']).dt.strftime("%Y-%m")
        fig7 = px.histogram(df5, x="date")
        fig7.update_traces(marker_color='rgba(127,90,159,255)')
        fig7.update_traces(textposition='inside')
        fig7.update_yaxes(showticklabels=False)
        st.plotly_chart(fig7,use_container_width=True)
        st.write(':white_check_mark:  Portanto, o projeto chega ao final com seu objetivo cumprido, respondendo à todas as demandas do cliente, indicando os imóveis, o preço de venda e quando negociá-los.')

        z1, z2, z3 = st.columns((1, 1, 1))
        z2.markdown("![Alt Text](https://media.giphy.com/media/hNWmkvCgaj6SxgABYl/giphy.gif)")

        st.caption('Desenvolvido por Felipe Aguiar, Cientista de Dados e Engenheiro de Produção.')
        cont = '[LinkedIn](https://www.linkedin.com/in/felipejaguiar) | [GitHub](https://github.com/felipejaguiar)'
        st.caption(cont)

        return None

if __name__ =='__main__':

    #Extract
    url = 'https://services2.arcgis.com/I7NQBinfvOmxQbXs/arcgis/rest/services/sps_geo_zone_ES_2021_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'
    path = 'kc_house_data.csv'
    geofile = get_geofile(url)
    data = get_data(path)

    #Transform and Load
    data = transf_data(data)
    data2 = load_data(data)

    #Visualizations
    descript = data_description(data2)
    hipo = get_hips(data2)
    rslt = results(data2)

