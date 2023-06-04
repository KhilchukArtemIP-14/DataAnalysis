import pandas as pd
import numpy as np
from scipy.stats import chi2
from scipy.stats import norm

class DataFrameManager:

    def __init__(self):
        pd.set_option('display.max_columns', None)

    def read_data(self):
        """Task 1"""

        """Data read"""
        data = pd.read_csv(r'C:\Users\Artem\PycharmProjects\ADIS_lab4\Data2.csv', sep=';',
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

        """Data investigation"""
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
    def check_for_normality(self):
        # Define the number of bins to use in the histogram
        num_bins = 10

        # Loop over the columns in the DataFrame and test each column for normality
        for col in self.data.columns:
            # Calculate the observed frequency distribution of the column data
            hist, bin_edges = np.histogram(self.data[col], bins=num_bins)

            # Calculate the expected frequency distribution of a normal distribution with the same mean and standard deviation as the column data
            expected_freq = len(self.data[col]) * np.diff(norm.cdf(bin_edges, loc=np.mean(self.data[col]), scale=np.std(self.data[col])))

            # Calculate the Pearson chi-square test statistic for the column data
            chi_squared_stat = np.sum((hist - expected_freq) ** 2 / expected_freq)

            # Calculate the degrees of freedom for the test
            df_chi = num_bins - 1

            # Calculate the p-value for the test
            p_value = 1 - chi2.cdf(chi_squared_stat, df_chi)

            # Print the results for the column
            print(f"Column {col}:")
            print(f"Pearson chi-square test statistic: {chi_squared_stat}")
            print(f"Degrees of freedom: {df_chi}")
            print(f"P-value: {p_value}")

            # Check whether the column data is normally distributed or not
            if p_value < 0.05:
                print("The column data is not normally distributed")
            else:
                print("The column data is normally distributed")
    def find_region_closest_to_normal(self):
        # Filter the dataset to include only the "Region" and "CO2 emission" columns
        co2_by_region = self.data.loc[:, ['Region', 'CO2 emission']]

        # Group the filtered data by region and calculate the mean and standard deviation of CO2 emissions for each region
        co2_stats_by_region = co2_by_region.groupby('Region').agg(['mean', 'std'])

        # Calculate the Pearson chi-square test statistic and p-value for each region
        p_values = {}
        for region, (mean, std) in co2_stats_by_region.iterrows():
            # Calculate the observed frequency distribution of CO2 emissions in the region
            hist, bin_edges = np.histogram(co2_by_region.loc[co2_by_region['Region'] == region, 'CO2 emission'], bins=10)

            # Calculate the expected frequency distribution of a normal distribution with the same mean and standard deviation as the CO2 emissions in the region
            expected_freq = len(co2_by_region.loc[co2_by_region['Region'] == region]) * np.diff(norm.cdf(bin_edges, loc=mean, scale=std))

            # Calculate the Pearson chi-square test statistic for the CO2 emissions in the region
            chi_squared_stat = np.sum((hist - expected_freq) ** 2 / expected_freq)

            # Calculate the degrees of freedom for the test
            df_chi = 10 - 1

            # Calculate the p-value for the test
            p_value = 1 - chi2.cdf(chi_squared_stat, df_chi)

            p_values[region] = p_value

        # Identify the region with the smallest p-value
        closest_region = min(p_values, key=p_values.get)

        print(f"The region with the distribution of CO2 emissions closest to normal is {closest_region}")

