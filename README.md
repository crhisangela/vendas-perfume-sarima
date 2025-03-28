#  Previsão de Vendas de Perfumes  

Este projeto utiliza o algoritmo **SARIMA** para prever as vendas de perfumes em um e-commerce. Os dados utilizados são provenientes do [Kaggle](https://www.kaggle.com/datasets/kanchana1990/perfume-e-commerce-dataset-2024?select=ebay_womens_perfume.csv).  

---

### Instalação e Configuração  

#### 1. Clone o repositório e entre no diretório do projeto:  
```bash
git clone https://github.com/seuusuario/projeto.git
cd projeto
```

####  2. Instale as dependências necessárias:  
```bash
pip install -r requirements.txt
```

---

### Funcionamento da API  

O projeto disponibiliza uma API com os seguintes endpoints:  

#### **1. Verificar o status da API**  
- _Endpoint:_ `/`  
- _Método:_ `GET`  
- _Descrição:_ Verifica se a API está rodando corretamente.  

#### **2. Previsão de vendas para dias Comuns**  
- _Endpoint:_ `/comum_sales`  
- _Método:_ `GET`  
- _Parâmetro:_ `days_to_predict` -> Número de dias à frente para prever.  
- _Descrição:_ Retorna a previsão de vendas para dias considerados comuns **salvando estes dados em um arquivo csv na área de trabalho**.  

#### **3. Previsão de vendas para dias atípicos e picos de venda (Outliers)**  
- _Endpoint:_ `/outlier_sales`  
- _Método:_ `GET`  
- _Parâmetro:_ `days_to_predict` -> Número de dias à frente para prever.  
- _Descrição:_ Retorna a previsão de vendas para dias que podem apresentar comportamentos atípicos **salvando estes dados em um arquivo csv na área de trabalho**.  

---

### Como Executar a API  

Para rodar a API localmente, utilize o comando abaixo:  
```bash
uvicorn main:app --reload
```
A API estará disponível no endereço:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)  

---

### Observações
Na pasta [crispdm](crispdm), você pode visualizar todo o fluxo de decisão adotado nos testes e na escolha do algoritmo para este projeto.

[_Preparação de Dados:_](crispdm/01_data_preparation.ipynb) Processamento e limpeza dos dados para prepará-los para análise e modelagem.

[_Análise e Visualização de Dados:_](crispdm/02_data_visualization.ipynb) Exploração e visualização dos dados para entender padrões e insights.

[_Testes e Modelagem com Avaliação:_](crispdm/03_modeling.ipynb) Implementação dos modelos, testes e avaliações para prever as vendas com base nas séries temporais (arima, sarima, xgboost, orbita, prophet).
