import pandas as pd
import json
import date_util

def convert_data(filename):
    data = pd.read_excel(filename, 'Output')
    company_name = raw_input("Enter company id \n")
    epoch = date_util.get_epoch()
    output_file = '{company_name}_*_script_{epoch}_product-data.json'.format(company_name = company_name,
                                                                             epoch = epoch)
    print 'Output file: {name}'.format(name = output_file)
    json.dump(data.T.to_dict().values(), open('data/' + output_file, 'w'))


if __name__ == '__main__':
    filename = raw_input('Enter the file location w/ name \n')
    convert_data(filename)