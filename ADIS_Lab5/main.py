from DataFrameManipulator import DataFrameManager

if __name__=="__main__":
    dfm=DataFrameManager()
    dfm.initialize_data()
    dfm.prepare_for_regressional_analysis()
    dfm.split_into_samples()
    dfm.build_regressions()
    dfm.additional_task()