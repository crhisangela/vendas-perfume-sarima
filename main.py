from fastapi import FastAPI, Header
from src.data_handler import CleaningData
from src.model_handler import TimeSeriesModelHandler
from src.project_handler import PredictHandler

app = FastAPI()

predict= PredictHandler()
df = predict.process_data()
cleaning_data = CleaningData()
predict = PredictHandler()
comum_sales, outlier_sales = cleaning_data.split_outliers(df)

@app.get('/')
def helth():
    return {"message": "API is running"}

@app.get('/comum_sales')
def comum_days_predict(days_to_predict: int):
    train, test = predict.train_test_split(comum_sales)
    predict.sarima_predict(comum_sales, train, test, days_to_predict)
    return (f"✅ Arquivo salvo com sucesso na sua área de trabalho")

@app.get('/outlier_sales')
def outliers_days_predict(days_to_predict: int):
    train, test = predict.train_test_split(outlier_sales)
    predict.sarima_predict(comum_sales, train, test, days_to_predict)
    return (f"✅ Arquivo salvo com sucesso na sua área de trabalho")
