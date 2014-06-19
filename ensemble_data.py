import pandas as pd
import json
import date_util


class Ensemble():

    def __init__(self):
        self.FILE = raw_input('Enter file location w/ name\n')
        self.bottom_ensembles = pd.read_excel(self.FILE, 'bottom_sku_ensemble_mapping')

    def get_category_positions(self):
        if self.FILE:
            positions = pd.read_excel(self.FILE, 'category_positions')
            self.category_positions = {}
            for positions in positions.T.to_dict().values():
                categories = self.category_positions.get( positions['Position'], [] )
                categories.append(str(positions['Sub_Category']))
                self.category_positions[positions['Position']] = categories

    def get_ensemble_combinations(self):
        combinations = pd.read_excel(self.FILE, 'sku_ensemble_mapping')
        combinations = combinations[ ['sku', 'Sub Category', 'Position', 'is_0', 'is_1', 'is_2', 'is_3', 'is_4'] ]
        combinations.columns = ['sku', 'category', 'position', 0, 1, 2, 3, 4]

        ensembles = combinations[ combinations.position == 'Anchor']
        self.other_positions = combinations[ combinations.position != 'Anchor']
        self.ensembles = ensembles.apply(self.fill_ensemble_combinations, axis=1)

    def fill_ensemble_combinations(self, series):
        for pos in [0, 1, 2, 3, 4]:
            if pos == 0 and series[pos] == 1:
                series[pos] = self.fill_bottom_combinations(series)
                continue

            if series[pos] == 1:
                series[pos] = list(self.other_positions[ self.other_positions.category.isin( self.category_positions[pos] ) ].sku)

            if series[pos] == 0:
                series[pos] = []

        return series

    def fill_bottom_combinations(self, series):
        return [str(sku) for sku in tuple(self.bottom_ensembles[self.bottom_ensembles.sku == series.sku].combination)[0].split(',')]

    def format_ensembles(self):
        ensembles = self.ensembles.T.to_dict().values()
        ensemble_collection = []
        for ensemble in ensembles:
            sku = ensemble['sku']
            for pos in [0, 1, 2, 3, 4]:
                combinations = ensemble[pos]
                for ndx, combination in enumerate(combinations):
                    addition = {'anchor': sku, 'combination': combination,
                                'position': pos, 'association': 'ensemble',
                                'rank': ndx
                    }
                    ensemble_collection.append(addition)

        company_id = raw_input('Enter company_id \n')
        epoch = date_util.get_epoch()
        output_file = '{company_id}_*_script_{epoch}_product-styles.json'.format(company_id = company_id,
                                                                                 epoch = epoch)
        print 'Output file: %s' %output_file
        json.dump(ensemble_collection, open('data/' + output_file, 'w'))

    def get_data(self):
        self.get_category_positions()
        self.get_ensemble_combinations()
        self.format_ensembles()

if __name__ == '__main__':
    Ensemble().get_data()