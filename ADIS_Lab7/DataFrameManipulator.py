import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.tsa.api as smt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from datetime import datetime,timedelta
import statsmodels.graphics.tsaplots as tsaplots
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import numpy as np
import seaborn as sns
from statsmodels.tsa.stattools import adfuller


class DataFrameProcessor:
    def __init__(self):
        pd.set_option('display.max_columns', None)

    def exploratory_time_series_data_analysis(self,df, name, name_of_checked_value):
        print(f"\nPerforming analysis of {name}:")
        print(df.describe())

        # build rolling mean trend for window size=10
        fig, ax = plt.subplots(figsize=(15, 10))
        df.plot(ax=ax)
        plt.plot(df.rolling(window=10).mean())
        plt.legend([name_of_checked_value, "Rolling mean trend"])
        plt.title("Window size=10")
        plt.show()

        # decompose to basic layers
        fig = smt.seasonal_decompose(df).plot()

        fig.set_size_inches(15, 10)

        plt.show()

        # build autocorrelation and partial autocorrelation
        fig, ax = plt.subplots(2, figsize=(15, 10))
        ax[0] = plot_acf(df[~df.isna()], ax=ax[0], lags=120)
        ax[1] = plot_pacf(df[~df.isna()], ax=ax[1], lags=120)
        plt.show()

        # stationarity check
        adfuller_test = adfuller(df[~df.isna()])
        print('ADF Statistic: %f' % adfuller_test[0])
        print('p-value: %f' % adfuller_test[1])
        print('Critical Values:')
        for key, value in adfuller_test[4].items():
            print('\t%s: %.3f' % (key, value))
        if adfuller_test[0]>adfuller_test[4]['5%']:
            print('Series is non-stationary')
        else:
            print('Series is stationary')


        print("\n")
    def poland_slovakia_covid(self):
        data=pd.read_csv('owid-covid-data.csv', index_col=['date'], parse_dates=['date'])
        data=data[["iso_code","new_cases"]]

        poland_df=data[data["iso_code"]=="POL"]
        poland_df=poland_df["new_cases"]

        slovakia_df=data[data["iso_code"]=="SVK"]
        slovakia_df=slovakia_df["new_cases"]

        fig, ax = plt.subplots(figsize=(15, 10))
        poland_df.plot(ax=ax)
        slovakia_df.plot(ax=ax)
        plt.legend(["Poland","Slovakia"])
        ax.grid()
        plt.show()
        self.exploratory_time_series_data_analysis(poland_df,"Poland","new_cases")
        self.exploratory_time_series_data_analysis(slovakia_df,"Slovakia","new_cases")

    def euro_to_hryvna(self):
        print("Checking euro to hryvna")
        data=pd.read_csv("euro-to-hryvna.csv", index_col=['Date'], parse_dates=['Date'],encoding="cp1252")
        print(data)
        three_years_ago = datetime(year=2023, month=5, day=5)- timedelta(days=3*365)
        last_3_years_data = data[data.index >= three_years_ago]
        last_3_years_data=last_3_years_data[["Kurs"]]
        self.exploratory_time_series_data_analysis(last_3_years_data,'Euro to hryvna','Kurs')


    def additional_task(self):
        data=pd.read_csv("seattleWeather_1948-2017.csv",index_col=["DATE"],parse_dates=["DATE"])
        data=data.drop("RAIN",axis=1)
        print(data)
        print(data.isna().sum())
        data["PRCP"]=data["PRCP"].fillna(data["PRCP"].mean())

        # first let's look at all the data
        data["PRCP"].plot()
        plt.show()

        last_three_year=datetime(year=2017,month=12,day=14)-timedelta(days=3*365)
        last_three_year_data = data[data.index >= last_three_year].resample('W').mean()
        last_three_year_data["PRCP"].plot()
        plt.legend(["PRCD", "Rolling mean trend"])
        plt.show()

        decompose = smt.seasonal_decompose(data['PRCP'].loc[data.index[-4*365:]].resample('W').mean())
        fig = decompose.plot()

        fig.set_size_inches(15, 10)

        plt.show()

        plot_acf(data["PRCP"].loc[data.index[-4*365:]].resample('W').mean())
        plt.show()
        plot_pacf(data["PRCP"].loc[data.index[-4*365:]].resample('W').mean())
        plt.show()


        #farenheit to celsius
        def farenheit_to_celsius(original,col_name):
            original[col_name]=round((original[col_name] - 32) * 5/9,2)

        farenheit_to_celsius(data,"TMAX")
        farenheit_to_celsius(data,"TMIN")
        print(data)

        #checking for correlations
        correlations=data.corr()
        sns.heatmap(correlations,annot=True)
        plt.show()

        #percipation prediciton

        #ARIMA

        #how to pick p d q :  https://analyticsindiamag.com/quick-way-to-find-p-d-and-q-values-for-arima/

        adfuller_test = adfuller(data["PRCP"])
        print('ADF Statistic: %f' % adfuller_test[0])
        print('p-value: %f' % adfuller_test[1])
        print('Critical Values:')
        for key, value in adfuller_test[4].items():
            print('\t%s: %.3f' % (key, value))
        if adfuller_test[0] > adfuller_test[4]['5%']:
            print('Series is non-stationary')
        else:
            print('Series is stationary')

        model = ARIMA(data['PRCP'], order=(3, 0, 6))
        result = model.fit()
        last_two_years=datetime(year=2017,month=12,day=14)-timedelta(days=2*365)
        last_two_years_data = data[data.index >= last_two_years]
        fig, ax = plt.subplots(figsize=(10, 6))
        last_two_years_data["PRCP"].plot(ax=ax)
        tsaplots.plot_predict(result,ax=ax,
                                start=datetime(year=2017,month=12,day=15),
                                end=datetime(year=2018, month=12, day=31))
        plt.show()

        #model evaluation
        actual_data=pd.read_csv("seattle-weather-december2017-2018.csv",index_col=['DATE'],parse_dates=['DATE'])
        actual_data=actual_data[actual_data.index>datetime(year=2017,month=12,day=14)]
        fig, ax = plt.subplots(figsize=(10, 6))
        tsaplots.plot_predict(result, ax=ax,
                              start=datetime(year=2017, month=12, day=15),
                              end=datetime(year=2018, month=12, day=31))
        actual_data['PRCP'].plot(ax=ax,label='Actual data')
        ax.legend()
        plt.show()
        predicted_values = result.predict(start=datetime(year=2017, month=12, day=15),
                                          end=datetime(year=2018, month=12, day=31))
        mae = mean_absolute_error(actual_data['PRCP'], predicted_values)
        mse = mean_squared_error(actual_data['PRCP'], predicted_values)
        rmse = np.sqrt(mean_squared_error(actual_data['PRCP'], predicted_values))
        print('ARIMA prediction analysis:')
        print(f'\tMAE: {mae}')
        print(f'\tMSE: {mse}')
        print(f'\tAIC: {result.aic}')
