# -*- coding: utf-8 -*-
import contextlib
import sqlite3

try:
    from final_products import Products
    from menu_coffee_for_me import Menu
    from final_logger import logger
except ImportError as err:
    print ("{}. Check if file exists.".format(err))

try:
    from tabulate import tabulate
except ImportError as err:
    logger.error("Import error {}.Use command -'pip install requirements.txt'".format(err))


class DataBaseWorkaround(object):
    """Creating a database with a tables of employees, coffeetypes, ingredients, sales."""

    def __init__(self, db_file="CoffeeForMeDB.db"):
        self.database = db_file
        try:
            self.conn = sqlite3.connect(db_file)
        except sqlite3.Error as error:
            logger.error("Error {}".format(error))
        self.cursor = self.conn.cursor()

    def run_query(self, query, param=None):
        msg = 'Execute query: {}, {}'.format(query, param) if param else 'Execute query: {}'.format(query)
        logger.info(msg)
        try:
            with contextlib.closing(sqlite3.connect(self.database)) as conn:
                with conn:
                    cursor = conn.cursor()
                    if param:
                        cursor.execute(query, param)
                    else:
                        cursor.execute(query)
                    result = cursor.fetchall()
            logger.info('Success!')
            return result
        except Exception as error:
            logger.exception(error)
            raise

    def create_tables(self):
        """ create a database tables if they are not exist"""
        logger.info('Creating database << {} >>.'.format(self.database))
        query1 = 'CREATE TABLE IF NOT EXISTS employees(position TEXT, name TEXT)'
        query2 = 'CREATE TABLE IF NOT EXISTS coffeetypes(product TEXT, price REAL)'
        query3 = 'CREATE TABLE IF NOT EXISTS ingredients(product TEXT, price REAL)'
        query4 = 'CREATE TABLE IF NOT EXISTS sales(\"Seller name\" TEXT,\"Number of sales\" ' \
                 'REAL,\"Total value (BYN)\" REAL)'

        for query in (query1, query2, query3, query4):
            result = self.run_query(query)
        logger.info('Database << {} >> {} created.'.format(self.database, 'was not' if result else 'was'))
        return result

    def init_products_tables(self, menu_):
        """ init tables coffee_types and ingredients"""
        for coffee_types_and_prices in menu_.coffee_types_and_prices():
            self.fill_table_coffeetypes(coffee_types_and_prices)
        for ingredients_and_prices in menu_.ingredients_and_prices():
            self.fill_table_ingredients(ingredients_and_prices)

    def fill_table_employees(self, user_info):
        """ filling table employees"""
        if not self.check_if_employee_in_db(user_info):
            query = 'INSERT INTO employees VALUES (?,?)'
            param = user_info
            result = self.run_query(query, param)
            logger.info('User << {} >> {} created.'.format(user_info[0], 'was not' if result else 'was'))
            return result

    def check_if_employee_in_db(self, user_info):
        position, name = user_info
        query = 'SELECT * FROM employees WHERE position = ? AND name = ?'
        param = (position, name,)
        result = self.run_query(query, param)
        logger.info('User << {} >> position << {} >> {}.'.format(user_info[0], user_info[1],
                                                                 'exists' if result else 'does not exist'))
        return bool(result)

    def fill_table_coffeetypes(self, coffeetypes):
        """ filling table coffeetypes"""
        if not self.check_if_coffee_types_in_db(coffeetypes):
            query = 'INSERT INTO coffeetypes VALUES (?, ?)'
            param = coffeetypes
            result = self.run_query(query, param)
            logger.info('Coffetype {} added.'.format('was not' if result else 'was'))

    def check_if_coffee_types_in_db(self, coffeetypes):
        coffee, price = coffeetypes
        query = 'SELECT * FROM coffeetypes WHERE product = ? AND price = ?'
        param = (coffee, price,)
        result = self.run_query(query, param)
        logger.info('Coffetype {}.'.format('exists' if result else 'is not exist'))
        return bool(result)

    def fill_table_ingredients(self, ingredients):
        if not self.check_ingredients_in_db(ingredients):
            query = 'INSERT INTO ingredients VALUES(?, ?)'
            param = ingredients
            result = self.run_query(query, param)
            logger.info('Ingredient {} added.'.format('was not' if result else 'was'))

    def check_ingredients_in_db(self, ingredients):
        ingredient, price = ingredients
        query = 'SELECT * FROM ingredients WHERE product = ? AND price = ?'
        param = (ingredient, price,)
        result = self.run_query(query, param)
        logger.info('Ingredient {}.'.format('exists' if result else 'is not exist'))
        return bool(result)

    def fill_table_sales(self, user_info):
        name, position = user_info
        if not self.check_if_salesman_in_db(user_info) and position == 'salesman':
            query = 'INSERT INTO sales VALUES (?,?,?)'
            param = (name, 0, 0,)
            result = self.run_query(query, param)
            logger.info('Salesman`s values {} added.'.format('were not' if result else 'were'))

    def check_if_salesman_in_db(self, user_info):
        name, position = user_info
        query = 'SELECT * FROM sales WHERE \"Seller name\" = ?'
        param = (name,)
        result = self.run_query(query, param)
        logger.info('User {}.'.format('exists' if result else 'is not exist'))
        return bool(result)

    def update_table_sales(self, name, order_list):
        price = self.get_overall_price(order_list)
        query = 'SELECT \"Number of sales\", \"Total value (BYN)\" FROM sales WHERE \"Seller name\" = ?'
        param = (name,)
        self.cursor.execute(query, param)
        logger.info('Execute query: {}, {}'.format(query, param))
        number_of_sales, total_value = self.cursor.fetchone()
        number_of_sales += 1
        total_value += price
        query2 = 'UPDATE sales SET \"Number of sales\" = ?, \"Total value (BYN)\" = ? WHERE \"Seller name\" = ? '
        param2 = (number_of_sales, total_value, name,)
        self.cursor.execute(query2, param2)
        logger.info('Execute query: {}, {}'.format(query, param2))
        self.conn.commit()

    def add_employee(self, user_info):
        if self.check_if_employee_in_db(user_info):
            print('You were logged as {} position {}\n'.format(user_info[0], user_info[1]))
        else:
            self.fill_table_employees(user_info)
            self.fill_table_sales(user_info)
            print ('User {} as {} was successfully added!'.format(user_info[0], user_info[1]))
            logger.info('User {} position: {} was successfully added to db!'.format(user_info[0], user_info[1]))

    def look_sales_results(self, position):
        if position == "manager":
            self.cursor.execute('''SELECT * FROM sales''')
            columns = ['Seller name', 'Number of sales', 'Total value(BYN)']
            print (tabulate(self.cursor.fetchall(), headers=columns, tablefmt="pipe", ) + '\n')

    @property
    def coffee_types_menu(self):
        query = 'SELECT ROWID,* FROM coffeetypes'
        self.cursor.execute(query)
        logger.info('Execute query: {}'.format(query))
        coffee_menu = self.cursor.fetchall()
        return [Products(rowid, name, price) for rowid, name, price in coffee_menu]

    @property
    def ingredients_menu(self):
        query = 'SELECT ROWID,* FROM ingredients'
        self.cursor.execute(query)
        logger.info('Execute query: {}'.format(query))
        ingredients_menu = self.cursor.fetchall()
        return [Products(rowid, name, price) for rowid, name, price in ingredients_menu]

    def show_coffee_types_menu(self):
        sourse = self.coffee_types_menu
        menu_ = [coffee.product_info() for coffee in sourse]
        columns = ['ID', 'COFFEE TYPES', 'PRICE']
        return tabulate(menu_, headers=columns, tablefmt="pipe", )

    def show_ingredients_menu(self):
        sourse = self.ingredients_menu
        menu_ = [ingredient.product_info() for ingredient in sourse]
        columns = ['ID', 'INGREDIENT', 'PRICE']
        return tabulate(menu_, headers=columns, tablefmt="pipe", )

    def coffee_dict(self):
        return {str(coffee.rowid): coffee for coffee in self.coffee_types_menu}

    def ingredient_dict(self):
        return {str(ingredient.rowid): ingredient for ingredient in self.ingredients_menu}

    def show_statistic(self):
        query = 'SELECT * FROM sales'
        self.cursor.execute(query)
        logger.info('Execute query: {}'.format(query))
        columns = ['Seller name', 'Number of sales', 'Total value(BYN)']
        print (tabulate(self.cursor.fetchall(), headers=columns, tablefmt="pipe", ) + '\n')

    @staticmethod
    def get_overall_price(order):
        return sum(product.price for product in order)


connect = DataBaseWorkaround()
menu = Menu()
connect.create_tables()
connect.init_products_tables(menu)
