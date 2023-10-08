import pandas as pd


def get_data():
    df = pd.read_csv('monster_list.csv')
    return df


if __name__ == '__main__':
    df = get_data()
    print(df.head())