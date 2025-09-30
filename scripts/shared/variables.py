from dataclasses import dataclass

@dataclass
class BasePaths:

    raw_data_path = './data/'
    processed_data_path = './processed/'

    train_data_name = 'train.csv'
    test_data_name = 'test.csv'