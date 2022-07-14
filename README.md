#  PROJETO HOUSE ROCKET
<img src="https://raw.githubusercontent.com/felipejaguiar/hr_project/main/img/hrf.png" alt="logo" style="zoom:80%;" />
# # # PROJETO FICTÍCIO # # #

# Questão de Negócio
A House Rocket é uma empresa do ramo imobiliário com foco na compra e venda de imóveis. Visando a maximização de seus resultados, a empresa requisitou o projeto como forma de otimizar o processo de tomada de decisão de quais negócios devem ser concretizados. Para isso, disponibilizou um conjunto de dados contendo alguns atributos de cada imóvel, como por exemplo: localização, preço, data de construção, entre outros. Além disso, a empresa definiu seu objetivo com o projeto em três perguntas, que são:

👉 Quais os 300 imóveis que deveriam ser adquiridos e por qual preço?

👉 Para os imóveis adquiridos, qual seria o preço da venda?

👉 Quais os meses mais indicados para comprar e vender?

# Premissas do Negócio
As premissas são alterações feitas nos dados originais a fim de melhorar a qualidade da análise. Para o projeto, tomou-se as seguintes premissas:

🟪 Os valores duplicados da coluna ID (identificação do imóvel) foram removidos considerando a compra mais recente;

🟪 Por se tratar de um erro, o imóvel de 33 quartos foi alterado para 3 quartos;

🟪 Excluídos os atributos que não seriam utilizados nas análises;

🟪 Caso o preço seja menor que a mediana de preços por região, o imóvel esteja em boas condições e tenha boa qualidade de construção e design, deve ser adquirido;

🟪 Preço de venda varia de acordo com a sazonalidade.

# Planejamento da Solução
Passos do planejamento:

1️⃣ Coleta dos dados (Kaggle);

2️⃣ Análise das questões de negócio (demandas do cliente e insights);

3️⃣ Tratamento de dados (limpeza e ajustes);

4️⃣ Demonstração da solução para as demandas da empresa e insights;

5️⃣ Demonstração de resultados obtidos;

Ferramentas:

🟣 Python 3.9, PyCharm, Jupyter (manipulação dos dados);

🟣Streamlit (construção das visualizações);

🟣Heroku (disponibilização das visualizações).

# Insights de Negócio

H1: Imóveis reformados são 45% mais caros, na média.

✅ Válida: Imóveis reformados apresentam um valor superior em média, o que impactaria a tomada de decisão sobre comprar imóveis reformados ou comprar imóveis e reformá-los.

H2: Imóveis com data de construção menor que 1955, são 20% mais baratos, na média.

❌ Inválida: Imóveis mais recentes tem praticamente a mesma média de preço que os antigos. Portanto, neste caso, o ano de construção tende a apresentar pouco impacto sobre os preços de compra dos imóveis.

H3: Imóveis sem porão são 15% maiores do que os imóveis com porão.

✅ Válida: Imóveis com porão tem relativamente menores áreas construídas. Logo, focar em imóveis sem porão quando a área construída for um fator decisivo.

H4: Imóveis com grade low/avg são 45% mais baratos que com grade good/high, na média.

✅ Válida: Os imóveis com baixo grau de construção e design são mais baratos, o que possibilitaria a compra e reforma, ou aproveitamento do terreno para novas construções.

H5: 10% dos imóveis em piores condições tem os maiores grades.

✅ Válida: 19 imóveis de alto nível de construção apresentam nível baixo de condição atual, sendo propícios para reformas e revendas futuras.

H6: O crescimento do preço dos imóveis MoM (month over month) é de 10%.

❌ Inválida: Após uma sequência de queda entre Jun/2014 e Jan/2015, o preço médio de vendas cresceu. O que configura uma tendência de equilíbrio dos preços durante os meses analisados.

# Resultados financeiros
|  Preço total de compra dos 300 imóveis  |  Preço total de venda dos 300 imóveis  |   Lucratividade total   |
|-----------------------------------------|----------------------------------------|-------------------------|
|            $263.037.725,00               |            $341.949.042,00            |      $78.911.318,00     |

A lucratividade em porcentagem foi de 30%!

# Conclusão

Por fim, o objetivo do projeto foi alcançado, pois conseguiu-se indicar os imóveis certos para compra, o preço de venda para as futuras negociações e qual a melhor época do ano para negociá-los. Para projetos futuros, focar na expanção dos dados, agora através da ótica do cliente, analisando quais pontos e atributos mais impactam para adquirir ou não um imóvel.

