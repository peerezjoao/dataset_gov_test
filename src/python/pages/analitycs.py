import pandas as pd
import os

def cross_datasets(download_dir, dataset_1, dataset_2):

    # read datasets 
    df_1 = pd.read_csv(dataset_1)
    print(f'Dataset 1:')
    print(df_1.head())

    df_2 = pd.read_csv(dataset_2)
    print(f'Dataset 2:')
    print(df_2.head())

    #  calculate the obesity percentage of DS1
    obesity_percentage = df_1['Obesity'].mean()

    # add new column - df_2
    df_2['Obesity Percentage'] = obesity_percentage

    # save new report
    output_path = os.path.join(download_dir, 'result.xlsx')
    df_2.to_excel(output_path, index=False)





