import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures


class DataFrameManager:
    def __init__(self):
        pd.set_option('display.max_columns', None)

    def initialize_data(self):
        """Read and investigate data"""
        self.data=pd.read_csv("winequality-red.csv")

        #print('\nData samples:')
        #print(self.data)

        print('\nData analysis:')
        print(self.data.describe())

        print("\nAbsent data:")
        print(self.data.isnull().sum())

    def prepare_for_regressional_analysis(self):
        corr = self.data.corr()

        sns.heatmap(corr, annot=True)
        plt.show()

        #removing predictors that have weak correlation with our main factor
        print("Deleted columns which have weak correaltion with quality:",','.join(['fixed acidity',"residual sugar",'chlorides',  'free sulfur dioxide',  'total sulfur dioxide',"pH","density"]))
        self.data = self.data.drop(['fixed acidity',"residual sugar",'chlorides',  'free sulfur dioxide',  'total sulfur dioxide',"pH","density"], axis=1)

        #checking for multicolinearity
        print("Investigate correlations for multicolinearity")
        corr = self.data.loc[:, "volatile acidity":"alcohol"].corr()
        print(corr)

        corr_flag=False
        for index, row in corr.iterrows():
            for col in corr.columns:
                if abs(row[col])>0.7 and col!=index:
                    corr_flag=True
        if corr_flag:
            print("Multicolinearity detected")
        else:
            print("Multicolinearity not detected")
        print('\n')

    def split_into_samples(self):
        self.feedback=self.data["quality"]
        self.predictors = self.data.loc[:, "volatile acidity":"alcohol"]
        self.predictors_train, self.predictors_test, self.feedback_train, self.feedback_test = train_test_split(self.predictors, self.feedback, test_size=0.2, random_state=42)

    def build_regressions(self):
        """Building regressions"""

        # linear single-factor regression
        lin_reg = LinearRegression()
        lin_reg.fit(self.predictors_train['alcohol'].values.reshape(-1, 1), self.feedback_train)
        feedback_pred_lin = lin_reg.predict(self.predictors_test['alcohol'].values.reshape(-1, 1))
        plt.scatter(self.predictors_test['alcohol'],self.feedback_test)
        plt.plot(self.predictors_test['alcohol'],feedback_pred_lin,color='red')
        plt.xlabel('alcohol %')
        plt.ylabel('quality')
        plt.show()

        #analyzing model efficiency
        mse_lin = mean_squared_error(self.feedback_test, feedback_pred_lin)
        r2_lin = r2_score(self.feedback_test, feedback_pred_lin)
        print("\nMSE for linear single-factor regression is : {}".format(mse_lin))
        print("R-squared for linear single-factor regression is: {}".format(r2_lin))

        for degr in range(1,5):
            poly = PolynomialFeatures(degree=degr)
            predictors_train_polyfeat = poly.fit_transform(self.predictors_train)
            predictors_test_polyfeat = poly.transform(self.predictors_test)

            poly_reg = LinearRegression()
            poly_reg.fit(predictors_train_polyfeat, self.feedback_train)

            feedback_pred_poly = poly_reg.predict(predictors_test_polyfeat)

            # analysing efficiency of regressions
            mse = mean_squared_error(self.feedback_test, feedback_pred_poly)
            r2 = r2_score(self.feedback_test, feedback_pred_poly)
            print("\nMSE for polynomial regression of {} degree is : {}".format(degr, mse))
            print("R-squared for polynomial regression of {} degree is: {}".format(degr, r2))

    def additional_task(self):

        #reading data
        data=pd.read_csv("Data4.csv",sep=';',encoding="cp1252")
        data.rename(columns={'Unnamed: 0': 'Eng'}, inplace=True)
        print(data)
        print(data.describe())
        print(data.isnull().sum())
        #format data
        for col in data.loc[:, "Cql":"Is"].columns:
            data[col] = data[col].str.replace(',', '.').astype(float)

        #looking for multicolinearity
        print("Multicolinearity check:")
        numeric=data.select_dtypes(include=['float64','int64'])
        numeric_corr=numeric.corr()
        correlations=dict()
        print(numeric_corr)
        for index, row in numeric_corr.iterrows():
            correlations[index]=[]
            for col in numeric_corr.columns:
                if abs(row[col])>0.7  and col!=index:
                    correlations[index].append(col)
        counter=0
        for i in correlations.values():
            if len(i)>1:
                counter+=1
        if counter>1:
            print("Multicolinearity found")
        else:
            print("Multicolinearity not found")

        #building scatter plots
        fig, axs = plt.subplots(nrows=len(numeric.columns), ncols=(len(numeric.columns)-1), figsize=(90, 90))
        num=0
        for col_x in numeric.columns:
            for col_y in numeric.columns:
                if col_y!=col_x:
                    axs[num%(len(numeric.columns)),num//(len(numeric.columns))].scatter(numeric[col_x],numeric[col_y])
                    axs[num%(len(numeric.columns)),num//(len(numeric.columns))].set_title(f"{col_x} and {col_y}")
                    num+=1
        plt.show()

        #separating data
        predictors_train=data.loc[:,'Ie':'Is']
        feedback_train=data['Cql']

        test_csv=pd.read_csv("Data4t.csv",sep=';',encoding='cp1252')

        #formatting test input
        for col in test_csv.loc[:, "Cql":"Is"].columns:
            test_csv[col] = test_csv[col].str.replace(',', '.').astype(float)

        #building models
        for degr in range(1,7):
            poly = PolynomialFeatures(degree=degr)
            predictors_train_polyfeat = poly.fit_transform(predictors_train)
            predictors_test_polyfeat = poly.transform(test_csv.loc[:,'Ie':'Is'])

            poly_reg = LinearRegression()
            poly_reg.fit(predictors_train_polyfeat, feedback_train)

            feedback_pred_poly = poly_reg.predict(predictors_test_polyfeat)

            #analysing efficiency of regressions
            mse_lin_multi = mean_squared_error(test_csv['Cql'], feedback_pred_poly)
            r2_lin_multi = r2_score(test_csv['Cql'], feedback_pred_poly)
            print("\nMSE for polynomial regression of {} degree is : {}".format(degr,mse_lin_multi))
            print("R-squared for polynomial regression of {} degree is: {}".format(degr,r2_lin_multi))




