import re
import numpy as np
import pandas as pd

class CleaningData:
    def __init__(self):
        self.path1 = 'C:\\Users\\Cliente\\Documents\\Git\\case\\docs\\ebay_womens_perfume.csv'
        self.path2 = 'C:\\Users\\Cliente\\Documents\\Git\\case\\docs\\ebay_mens_perfume.csv'
        self.df = self.concat_data()
    
    def concat_data(self):
        data1 = pd.read_csv(self.path1)
        data2 = pd.read_csv(self.path2)
        return pd.concat([data1, data2], axis=0)
    
    def convert_canadian_to_usd(self, price):
        return price * 0.69

    def adjusting_price_to_usd(self):
        self.df.loc[self.df['priceWithCurrency'].str.contains('C'), 'price'] = self.df.loc[self.df['priceWithCurrency'].str.contains('C'), 'price'].apply(self.convert_canadian_to_usd)
        
        self.df['price'] = self.df['price'].round(2)
        return self.df
    
    def drop_columns(self):
        return self.df.drop(columns=['availableText', 'priceWithCurrency'], axis=1)
    
    def split_state_country(self):
        self.df['country'] = self.df['itemLocation'].str.split(', ').str[-1]
        self.df['state'] = self.df['itemLocation'].str.split(', ').str[-2]
        self.df['city'] = self.df['itemLocation'].str.split(', ').str[0]
        self.df = self.df.drop(columns=['itemLocation'], axis=1)
    
    def treat_values(self):
        self.df = self.df.dropna(subset=['lastUpdated'])
        self.df['brand'] = self.df['brand'].fillna('Unknown')
        self.df['state'] = self.df['state'].fillna('Unknown')
        self.df['type'] = self.df['type'].fillna('Eau de Parfum')
        self.df['available'] = self.df['available'].fillna(int(0))
        self.df['sold'] = self.df['sold'].fillna(int(0))

        self.df['sold'] = self.df['sold'].astype(int)
        self.df['available'] = self.df['available'].astype(int)
        return self.df
    
    @staticmethod
    def extract_date_parts(date_str):
        month = date_str[:3]
        year = date_str[7:12]
        day_match = re.search(r'(\d{1,2}),', date_str)
        day = day_match.group(1) if day_match else None
        return pd.Series([month, day, year])

    # def get_weeknames(self):
    #     self.df = self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    #     self.df['date'] = pd.to_datetime(self.df['year'] + '-' + self.df['month'] + '-' + self.df['day'], format='%Y-%b-%d')
    #     self.df['weekday'] = self.df['date'].dt.day_name()
    #     self.df[['month', 'day', 'year']] = self.df[['month', 'day', 'year']].apply(lambda col: col.str.strip())

    #     self.df = self.df.drop(columns=['date'], axis=1)
    #     return self.df

    
    def process_dates(self):
        self.df[['month', 'day', 'year']] = self.df[['month', 'day', 'year']].astype(str).apply(lambda col: col.str.strip())

        month_mapping = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
            'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }

        self.df['day'] = self.df['day'].replace({None: 1, 'None': 1, 'nan': 1, np.nan: 1}) 
        self.df['day'] = pd.to_numeric(self.df['day'], errors='coerce').fillna(1).astype(int)
        self.df['year'] = self.df['year'].astype(int)
        self.df['month'] = self.df['month'].map(month_mapping)
        
        self.df['date'] = pd.to_datetime(
            self.df['year'].astype(str) + '-' + self.df['month'].astype(str) + '-' + self.df['day'].astype(str),
            format='%Y-%m-%d',
            errors='coerce'
        )

        self.df = self.df[self.df['year']==2024]
        self.df = self.df.drop(columns=['lastUpdated'], errors='ignore')
        self.df = self.df.dropna(subset=['date'])
        
        return self.df
    
    
    def split_outliers(self, df):
        df = df[df['sold'] != 0]
        outlier_sales = df[df['sold'] >= 200]
        comum_sales = df[df['sold'] < 100]
        return comum_sales, outlier_sales

    

    

