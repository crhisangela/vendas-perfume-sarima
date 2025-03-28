
from email.message import EmailMessage
from io import StringIO
import os
import smtplib
from src.data_handler import CleaningData
from src.model_handler import TimeSeriesModelHandler, Evaluation
import warnings
warnings.filterwarnings("ignore")


class PredictHandler:
    def __init__(self):
        self.cleaning_data = CleaningData()
        self.models = TimeSeriesModelHandler()
        self.evaluation = Evaluation()

    def process_data(self):
        self.df = self.cleaning_data.concat_data()
        self.df = self.cleaning_data.adjusting_price_to_usd()
        self.df = self.cleaning_data.drop_columns()
        self.df = self.cleaning_data.split_state_country()
        self.df = self.cleaning_data.treat_values()
        self.df[['month', 'day', 'year']] = self.df['lastUpdated'].apply(self.cleaning_data.extract_date_parts)
        self.df = self.cleaning_data.process_dates()
        self.df = self.df.sort_values(by='date')

        return self.df
    
    def train_test_split(self, df):
        train_size = int(len(df) * 0.7)
        train = df[:train_size]
        test = df[train_size:]
        return train, test

    def save_df_to_desktop(self, df, filename="previsao.csv"):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop, filename)
        df.to_csv(file_path, index=False, encoding="utf-8")

    def sarima_predict(self,df,  train, test, days_to_predict):
        sarima_pred, future_sarima = self.models.fit_sarima_model(df, train, test, days_to_predict)
        self.save_df_to_desktop(df = future_sarima)


