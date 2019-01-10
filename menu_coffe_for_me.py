# -*- coding: utf-8 -*-
import json
from final_logger import logger

class LoadMenu(object):
    def __init__(self, file_='menu_coffee_for_me.json'):
        self.file_ = file_
        self.load_data()

    def load_data(self):
        try:
            logger.info('Reading menu json file << {} >>'.format(self.file_))
            with open(self.file_) as menu_file:
                self.file_data = json.load(menu_file)
        except Exception as error:
            logger.exception(error)
            raise


class Menu(LoadMenu):

    def coffee_types_and_prices(self):
        for coffee_types in self.file_data['COFFEE']:
            yield coffee_types

    def ingredients_and_prices(self):
        for ingredients in self.file_data['INGREDIENTS']:
            yield ingredients
