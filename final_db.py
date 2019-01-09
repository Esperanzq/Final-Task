try:
    from final_products import Products
    from menu_coffee_for_me import Menu
    import final_logger
except ImportError as err:
    print ("{}. Check if file exists.".format(err))

local_logger = final_logger.final_logger()

try:
    import sqlite3
    from tabulate import tabulate
except ImportError as err:
    local_logger.error("Import error {}.Use command -'pip install requirements.txt'".format(err))


class DataBaseWorkaround(object):
    """Creating a database with a tables of employees."""

    def __init__(self, db_file="CoffeeForMeDB.db"):
        try:
            self.conn = sqlite3.connect(db_file)
        except sqlite3.Error as error:
            local_logger.error("Error {}".format(error))
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """ create a database tables if they are not exist"""

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees(position TEXT, name TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS coffeetypes(product TEXT, price REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients(product TEXT, price REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales(\"Seller name\" TEXT,
                                                                \"Number of sales\" REAL, 
                                                                \"Total value (BYN)\" REAL)''')

    def init_products_tables(self, menu_):
        """ init tables coffetypes and ingredients"""
        for coffee_types_and_prices in menu_.coffee_types_and_prices():
            self.fill_table_coffeetypes(coffee_types_and_prices)
        for ingredients_and_prices in menu_.ingredients_and_prices():
            self.fill_table_ingredients(ingredients_and_prices)

    def fill_table_employees(self, user_info):
        """ filling table employees"""
        if not self.employee_exist(user_info):
            self.cursor.execute('''INSERT INTO employeees VALUES (?,?)''', user_info)
            self.conn.commit()

    def check_if_employee_in_db(self, user_info):
        position, name = user_info
        self.cursor.execute('SELECT * FROM employees WHERE position = ? AND name = ?', (position, name,))
        return self.cursor.fetchall()

    def employee_exist(self, user_info):
        return bool(self.check_if_employee_in_db(user_info))

    def fill_table_coffeetypes(self, coffeetypes):
        """ filling table coffeetypes"""
        if not self.coffeetype_exist(coffeetypes):
            self.cursor.execute('''INSERT INTO coffeetypes VALUES (?, ?)''', coffeetypes)
            self.conn.commit()

    def check_if_coffee_types_in_db(self, coffeetypes):
        coffee, price = coffeetypes
        self.cursor.execute('SELECT * FROM coffeetypes WHERE product = ? AND price = ?', (coffee, price,))
        return self.cursor.fetchall()

    def coffeetype_exist(self, coffeetypes):
        return bool(self.check_if_coffee_types_in_db(coffeetypes))

    def fill_table_ingredients(self, ingredients):
        if not self.ingredient_exist(ingredients):
            self.cursor.execute('''INSERT INTO ingredients VALUES(?, ?)''', ingredients)
            self.conn.commit()

    def check_ingredients_in_db(self, ingredients):
        ingredient, price = ingredients
        self.cursor.execute('SELECT * FROM ingredients WHERE product = ? AND price = ?', (ingredient, price,))
        return self.cursor.fetchall()

    def ingredient_exist(self, ingredients):
        return bool(self.check_ingredients_in_db(ingredients))

    def fill_table_sales(self, user_info):
        name, position = user_info
        if not self.sales_exist(user_info) and position == 'salesman':
            self.cursor.execute("INSERT INTO sales VALUES (?,?,?)", (name, 0, 0,))
            self.conn.commit()

    def check_if_salesman_in_db(self, user_info):
        name, position = user_info
        self.cursor.execute('SELECT * FROM sales WHERE \"Seller name\" = ?', (name,))
        return self.cursor.fetchall()

    def sales_exist(self, user_info):
        return bool(self.check_if_salesman_in_db(user_info))

    def update_table_sales(self, name, order_list):
        price = self.get_overall_price(order_list)
        self.cursor.execute('SELECT \"Number of sales\", \"Total value (BYN)\" FROM sales WHERE \"Seller name\" = ?',
                            (name,))
        number_of_sales, total_value = self.cursor.fetchone()
        number_of_sales += 1
        total_value += price
        self.cursor.execute(
            'UPDATE sales SET \"Number of sales\" = ?, \"Total value (BYN)\" = ? WHERE \"Seller name\" = ? ',
            (number_of_sales, total_value, name,))
        self.conn.commit()

    def add_employee(self, user_info):
        if self.employee_exist(user_info):
            print('You were logged as {} position {}'.format(user_info[0], user_info[1]))
        else:
            self.fill_table_employees(user_info)
            self.fill_table_sales(user_info)
            print ('User {} as {} was successfully added!'.format(user_info[0], user_info[1]))

    def look_sales_results(self, position):
        if position == "manager":
            self.cursor.execute('''SELECT * FROM sales''')
            columns = ['Seller name', 'Number of sales', 'Total value(BYN)']
            print (tabulate(self.cursor.fetchall(), headers=columns, tablefmt="pipe", ) + '\n')

    def coffee_types_menu(self):
        self.cursor.execute('SELECT ROWID,* FROM coffeetypes')
        coffee_menu = self.cursor.fetchall()
        return [Products(rowid, name, price) for rowid, name, price in coffee_menu]

    @property
    def ingredients_menu(self):
        self.cursor.execute('SELECT ROWID,* FROM ingredients')
        ingredients_menu = self.cursor.fetchall()
        return [Products(rowid, name, price) for rowid, name, price in ingredients_menu]

    def show_coffee_types_menu(self):
        sourse = self.coffee_types_menu()
        menu_ = [coffee.product_info() for coffee in sourse]
        columns = ['ID', 'COFFEE TYPES', 'PRICE']
        return tabulate(menu_, headers=columns, tablefmt="pipe", )

    def show_ingredients_menu(self):
        sourse = self.ingredients_menu
        menu_ = [ingredient.product_info() for ingredient in sourse]
        columns = ['ID', 'INGREDIENT', 'PRICE']
        return tabulate(menu_, headers=columns, tablefmt="pipe", )

    def coffee_dict(self):
        return {str(coffee.rowid): coffee for coffee in self.coffee_types_menu()}

    def ingredient_dict(self):
        return {str(ingredient.rowid): ingredient for ingredient in self.ingredients_menu}

    def show_statistic(self):
        self.cursor.execute('SELECT * FROM sales')
        columns = ['Seller name', 'Number of sales', 'Total value(BYN)']
        print (tabulate(self.cursor.fetchall(), headers=columns, tablefmt="pipe", ) + '\n')

    @staticmethod
    def get_overall_price(order):
        return sum(product.price for product in order)


connect = DataBaseWorkaround()
menu = Menu()
connect.create_tables()
connect.init_products_tables(menu)
