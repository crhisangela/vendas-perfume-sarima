from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pmdarima import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX


class TimeSeriesModelHandler:
    def __init__(self):
        pass


    # def fit_arima_model(self, db, train_data, test_data, steps, order=(2, 1, 1)):
    #     arima_model = ARIMA(train_data['sold'], order=order)
    #     arima_fitted = arima_model.fit()
    #     arima_pred = arima_fitted.forecast(len(test_data))

    #     # prevendo os próximos dias
    #     arima_future_pred = arima_fitted.forecast(steps=steps)
    #     future_dates = pd.date_range(start=db['date'].max(), periods=11, freq='D')[1:]
    #     future_arima = pd.DataFrame({'date': future_dates, 'previsao_de_vendas': arima_future_pred})
    #     return arima_pred, future_arima
    
    def fit_sarima_model(self, db, train_data, test, steps, order=(2, 1, 2), seasonal_order=(1, 1, 0, 7)):
        sarima_model = SARIMAX(train_data['sold'], order=order, seasonal_order=seasonal_order)
        sarima_fitted = sarima_model.fit()
        sarima_pred = sarima_fitted.forecast(steps=len(test))

        # prevendo os próximos dias
        sarima_future_pred = sarima_fitted.forecast(steps=steps)
        future_dates = pd.date_range(start=db['date'].max(), periods=11, freq='D')[1:]
        future_sarima = pd.DataFrame({'date': future_dates,  'previsao_de_vendas': sarima_future_pred})
        return sarima_pred, future_sarima
    
class Evaluation:
    def __init__(self):
        pass

    def evaluate_model(self, predictions, actual):
        mae = mean_absolute_error(actual, predictions)
        rmse = np.sqrt(mean_squared_error(actual, predictions))

        return {'MAE': mae, 'RMSE': rmse}
    
    def plot_predictions_with_future(self, db, future, model_name, test, pred):
        db['date'] = pd.to_datetime(db['date'])
        test['date'] = pd.to_datetime(test['date'])
        future['date'] = pd.to_datetime(future['date'])

        plt.figure(figsize=(14, 7))
        plt.plot(db['date'], db['sold'], color='grey', label='Real')
        plt.plot(test['date'], pred, label=f'{model_name} (Test)', color='red')
        plt.plot(future['date'], future['pred'], label=f'{model_name} (Future)', color='blue', linestyle='--')
        plt.legend()
        plt.title('Comparação de Modelos de Previsão de Vendas com Previsão Futura')
        plt.xlabel('Data')
        plt.ylabel('Vendas')
        plt.xticks(rotation=45)  
        plt.tight_layout() 
        plt.show()