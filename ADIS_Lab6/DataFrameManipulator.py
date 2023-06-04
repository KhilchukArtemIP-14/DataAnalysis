import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import lightgbm as lgb
from sklearn.metrics import precision_recall_fscore_support
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier


class DataFrameProcessor:
    def __init__(self):
        pd.set_option('display.max_columns', None)

    def main_task(self):
        """Main task"""
        data=pd.read_csv("titanic.csv")

        #analyze data
        print('\nData samples:')
        print(data)

        print('\nData analysis:')
        print(data.describe())

        print("\nAbsent data:")
        print(data.isnull().sum())


        #clean data
        data=data.drop(["Cabin","Name","Ticket","Embarked","PassengerId"],axis=1)
        data["Age"]=data["Age"].fillna(data["Age"].mean())
        data["Sex"]=data["Sex"].replace({'male': 0, 'female': 1})

        print('\nData analysis after cleaning:')
        print(data)
        print(data.describe())


        #separate data into test and train samples
        data_feed=data["Survived"]
        data_pred=data.loc[:,"Pclass":"Fare"]
        X_train, X_test, y_train, y_test = train_test_split(data_pred, data_feed, test_size=0.2, random_state=42)


        #models themselves
        #naive bayes
        print("\nNaive Bayes:")
        gnb = GaussianNB()
        gnb.fit(X_train, y_train)

        y_pred = gnb.predict(X_test)
        precision, recall, f_score, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        print(f'\tPrecision: {precision:.3f}')
        print(f'\tRecall: {recall:.3f}')
        print(f'\tF-Score: {f_score:.3f}')

        #decision tree
        print("\nDecision tree:")
        decision_tree = DecisionTreeClassifier(max_depth=3, random_state=42)
        decision_tree.fit(X_train, y_train)

        y_pred = decision_tree.predict(X_test)

        precision, recall, f_score, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        print(f'\tPrecision: {precision:.3f}')
        print(f'\tRecall: {recall:.3f}')
        print(f'\tF-Score: {f_score:.3f}')

        #random forest classifier
        print("\nRandom forest classifier:")
        randomforest = RandomForestClassifier(n_estimators=100,max_depth=5,random_state=42)
        randomforest.fit(X_train, y_train)

        y_pred = randomforest.predict(X_test)

        precision, recall, f_score, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        print(f'\tPrecision: {precision:.3f}')
        print(f'\tRecall: {recall:.3f}')
        print(f'\tF-Score: {f_score:.3f}')

        #bagging
        print("\nBagging classifier:")
        base_cls = DecisionTreeClassifier()
        bagging = BaggingClassifier(base_estimator=base_cls,n_estimators=10, random_state=42)
        bagging.fit(X_train, y_train)

        y_pred = bagging.predict(X_test)

        precision, recall, f_score, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        print(f'\tPrecision: {precision:.3f}')
        print(f'\tRecall: {recall:.3f}')
        print(f'\tF-Score: {f_score:.3f}')

        #Gradient boosting classifier
        print("\nGradient boosting classifier:")
        gradboost = GradientBoostingClassifier(learning_rate=0.05,random_state=42)
        gradboost.fit(X_train, y_train)

        y_pred = gradboost.predict(X_test)

        precision, recall, f_score, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        print(f'\tPrecision: {precision:.3f}')
        print(f'\tRecall: {recall:.3f}')
        print(f'\tF-Score: {f_score:.3f}')


        # SVM
        print("\nSupport Vector Machine:")
        svm = SVC(kernel='rbf', random_state=42)
        svm.fit(X_train, y_train)

        y_pred = svm.predict(X_test)

        precision, recall, f_score, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        print(f'\tPrecision: {precision:.3f}')
        print(f'\tRecall: {recall:.3f}')
        print(f'\tF-Score: {f_score:.3f}')

        #LightGBM
        print("\nLightGBM:")
        clf = lgb.LGBMClassifier()
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        precision, recall, f_score, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        print(f'\tPrecision: {precision:.3f}')
        print(f'\tRecall: {recall:.3f}')
        print(f'\tF-Score: {f_score:.3f}')
    def additional_task(self):
        """Additional task"""
        #read, reformat and clean data
        data = pd.read_csv('Data2.csv', sep=';',
                           encoding='cp1252')
        data["GDP per capita"] = data["GDP per capita"] \
            .str.replace(',', '.') \
            .astype(float)

        data["CO2 emission"] = data["CO2 emission"] \
            .str.replace(',', '.') \
            .astype(float)

        data["Area"] = data["Area"] \
            .str.replace(',', '.') \
            .astype(float)


        data.rename(columns={'Populatiion': 'Population'}, inplace=True)

        negative_gdp = data.loc[data["GDP per capita"] < 0]
        negative_area = data.loc[data["Area"] < 0]

        data["GDP per capita"].fillna(data["GDP per capita"].mean(), inplace=True)
        data["CO2 emission"].fillna(data["CO2 emission"].mean(), inplace=True)
        data["Area"].fillna(data["Area"].mean(), inplace=True)
        data["Population"].fillna(data["Population"].mean(), inplace=True)

        data.loc[negative_gdp.index, "GDP per capita"] = data["GDP per capita"].mean()
        data.loc[negative_area.index, "Area"] = data["Area"].mean()

        data["Density"]=data["Population"]/data["Area"]
        print('\n', data)

        print(data.describe())

        #select my data
        X = data[['GDP per capita', 'Density']]
        # and standartize it
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Determine optimal number of clusters using elbow method
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
            kmeans.fit(X_scaled)
            wcss.append(kmeans.inertia_)
        plt.plot(range(1, 11), wcss)
        plt.title('Elbow Method')
        plt.xlabel('Number of Clusters')
        plt.ylabel('WCSS')
        plt.show()

        kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
        kmeans.fit(X_scaled)

        data['Cluster'] = kmeans.labels_

        #determining those regions
        print(f'Clusters and their dominant regions:')
        for i in range(3):
            subset = data[data['Cluster'] == i]
            dominant_region = subset['Region'].value_counts().index[0]
            print(f"\tCluster {i + 1}: Dominant Region is {dominant_region}")

        #frequency histograms
        for col in data.select_dtypes(include=["float64","int64"]).columns:
            plt.hist(data[col], bins=10)
            plt.title(col)
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.show()

        #Function for checking linearity between two lists
        def is_linearly_dependent(arr1, arr2):
            df = pd.DataFrame({'arr1': arr1, 'arr2': arr2})
            corr = df['arr1'].corr(df['arr2'])
            return abs(corr) > 0.8

        A = [1, 2, 3]
        B = [1, 2, 3]
        print("\nCheck for linearity:")
        print("Vector A:", *A)
        print("Vector B:", *B)
        print("Linear correlation found?", is_linearly_dependent(A, B))




