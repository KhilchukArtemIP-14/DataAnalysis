from Lab3.DataFrameManager import DataFrameManager

if __name__ == "__main__":

    data = DataFrameManager()

    data.read_data()
    data.investigate_data()
    data.fix_corupted_data()
    data.show_plots()
    data.add_density()
    data.additional_questions()