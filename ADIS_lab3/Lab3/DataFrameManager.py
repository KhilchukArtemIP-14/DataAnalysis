import pandas as pd
import matplotlib.pyplot as plt

class DataFrameManager:

    def __init__(self):
        pd.set_option('display.max_columns', None)

    def read_data(self):
        """Task 1"""
        data = pd.read_csv(r'C:\Users\Artem\source\repos\ADIS_Labs\ADIS_Labs\Lab3\Data2.csv', sep=';',
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
        self.data=data
        print('\n', self.data)

    def investigate_data(self):
        """Task 2"""
        print(self.data.describe())

        self.data.rename(columns={'Populatiion':'Population'},inplace=True)

        gdpPerCapitaNaNs = self.data.loc[self.data["GDP per capita"].isna()]
        co2NaNs = self.data.loc[self.data["CO2 emission"].isna()]
        areaNaNs = self.data.loc[self.data["Area"].isna()]
        popNaNs = self.data.loc[self.data["Population"].isna()]

        print("Total Nans occurences in data:\n\tGdp per capita:{}\n\tCO2 emission:{}\n\tArea:{}\n\tPopulation:{}\n"
              .format(len(gdpPerCapitaNaNs), len(co2NaNs), len(areaNaNs), len(popNaNs)))

        negativeGdp = self.data.loc[self.data["GDP per capita"] < 0]
        negativeArea = self.data.loc[self.data["Area"] < 0]

        print("Total negative values occurences in data:\n\tGdp per capita:{}\n\tArea:{}\n".format(len(negativeGdp),
                                                                                                   len(negativeArea)))
    def fix_corupted_data(self):
        """Task 3"""
        gdp_per_capita_NaNs = self.data.loc[self.data["GDP per capita"].isna()]
        co2_NaNs = self.data.loc[self.data["CO2 emission"].isna()]
        area_NaNs = self.data.loc[self.data["Area"].isna()]
        pop_NaNs = self.data.loc[self.data["Population"].isna()]

        negative_gdp = self.data.loc[self.data["GDP per capita"] < 0]
        negative_area = self.data.loc[self.data["Area"] < 0]

        for index in gdp_per_capita_NaNs.index:
            self.data.loc[index, "GDP per capita"] = self.data["GDP per capita"].mean()

        for index in co2_NaNs.index:
            self.data.loc[index, "CO2 emission"] = self.data["CO2 emission"].mean()

        for index in area_NaNs.index:
            self.data.loc[index, "Area"] = self.data["Area"].mean()

        for index in pop_NaNs.index:
            self.data.loc[index, "Population"] = self.data["Population"].mean()

        for index in negative_gdp.index:
            self.data.loc[index, "GDP per capita"] = self.data["GDP per capita"].mean()

        for index in negative_area.index:
            self.data.loc[index, "Area"] = self.data["Area"].mean()

        print("\nData after fix:")
        print('\n', self.data)
        print('\n', self.data.describe())

    def show_plots(self):
        """Task 4"""
        plt.boxplot(self.data["GDP per capita"])
        plt.show()

        plt.hist(self.data["GDP per capita"])
        plt.show()

    def add_density(self):
        """Task 5"""
        self.data["Population density"] = self.data["GDP per capita"] / self.data["Area"];
        print("\nData after adding density:")
        print(self.data.describe(), '\n')

    def additional_questions(self):
        """Additional tasks"""

        """Highest gdp"""
        max_GDP_per_capita = self.data["GDP per capita"].max()
        top_gdp_per_capita = self.data.loc[self.data["GDP per capita"] == max_GDP_per_capita]
        print("Country with the highest GDP per capita is {} (Gdp per capita - {})\n"
              .format(top_gdp_per_capita["Country Name"].values[0], max_GDP_per_capita))

        """Lowest are"""
        min_area = self.data["Area"].min()
        min_area_country = self.data.loc[self.data["Area"] == min_area]

        print("Country with the smallest area is {} (Area - {})\n".format(min_area_country["Country Name"].values[0],
                                                                          min_area))

        """Largest average area region"""
        grouped = self.data.groupby("Region")
        regions_averages = grouped["Area"].mean()

        print("Largest average area is {} owned by {}\n".format(regions_averages.max(), regions_averages.idxmax()))

        """Highest population density in the world and europe and central asia"""
        print("Highest population density in the world is {} owned by {}\n"
              .format(self.data["Population density"].max(), self.data.loc[self.data['Population density'].idxmax()]['Country Name']))

        europe_and_asia = grouped.get_group("Europe & Central Asia")
        print("Highest population density in Europe and central asia is {} owned by {}\n"
              .format(europe_and_asia["Population density"].max(),
                      europe_and_asia.loc[self.data['Population density'].idxmax()]['Country Name']))

        """Countries with coinciding mean and median gdp"""
        averages = grouped["GDP per capita"].mean()
        medians = grouped["GDP per capita"].median()

        result = []

        for region in grouped.groups:
            mean = averages.loc[region]
            med = medians.loc[region]
            if (med == mean):
                result.append(region)

        print("Median and average GDP per capita coincide in {} regions\n".format(len(result)))

        """Top 5's"""
        print("Top 5 countries with highest GDP per capita")

        for i in self.data.nlargest(5, "GDP per capita")['Country Name'].values:
            print('\t{}'.format(i))

        print("\nTop 5 countries with lowest GDP per capita")

        for i in self.data.nsmallest(5, "GDP per capita")['Country Name'].values:
            print('\t{}'.format(i))

        print("\nTop 5 countries with highest CO2 per capita")

        temp = pd.DataFrame()
        temp['Country'] = self.data['Country Name']
        temp['CO2 per capita'] = self.data['CO2 emission'] / self.data['Population']

        for i in temp.nlargest(5, 'CO2 per capita')['Country'].values:
            print('\t{}'.format(i))

        print("\nTop 5 countries with lowest CO2 per capita")

        for i in temp.nsmallest(5, 'CO2 per capita')['Country'].values:
            print('\t{}'.format(i))