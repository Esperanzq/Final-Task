# -*- coding: utf-8 -*-
from datetime import datetime

try:
    from final_logger import logger
    from final_db import connect as db
except ImportError as err:
    print ("{}. Check if file exists.".format(err))

try:
    get_input = raw_input
except NameError:
    get_input = input


class Staff(object):
    def __init__(self, name=None, position=None):
        self.name = name
        self.position = position

    def admittance(self):
        if not self.name:
            self.add_name()
        if not self.position:
            self.add_position()
        self.add_employee_to_db()

    def add_name(self):
        res = get_input("Hello! What is your name?\n").capitalize()
        self.name = res
        assert self.name.isalpha(), "Name should consist only of letters"
        assert 36 > len(self.name) >= 3, "The len of name can`t be less 3 symbols and more 36 symbols"
        return self.add_position()

    def add_position(self):
        position = get_input("What is your position?\n1.manager 2.salesman\n")
        if position == '1' or position == "manager":
            self.position = "manager"
            logger.info("User {} position {} logged in".format(self.name, self.position))
            return self.add_employee_to_db()
        if position == '2' or position == "salesman":
            self.position = "salesman"
            logger.info("User {} position {} logged in".format(self.name, self.position))
            return self.add_employee_to_db()
        else:
            print ("There is no such position, choose from available variants")
            logger.error("There is no such position, choose from available variants")
            self.add_position()

    def define_position_of_employee(self):
        if self.position == "salesman":
            return Salesman(name=self.name, position=self.position)
        if self.position == "manager":
            return Manager(name=self.name, position=self.position)

    def add_employee_to_db(self):
        user_info = (self.name, self.position)
        db.add_employee(user_info)
        return self.define_position_of_employee()


class Manager(Staff):
    def __init__(self, name, position):
        super(Manager, self).__init__(name, position)
        self.show_statistic()

    def show_statistic(self):
        results = get_input("Do you want to see statistic?\n1.Yes 2.No\n")
        if results in ('1', "yes", "y"):
            db.show_statistic()
            print ("\nExiting to main menu....\n")
            return self.add_name()
        if results in ('2', "no", "n"):
            logger.info("Manager {} logged out".format(self.name))
            print ("Exiting to main menu...\n")
            return self.add_name()
        else:
            logger.info("Wrong choice! Need to press 1 or 2")
            print ("You need to press '1' or '2'")
            return self.show_statistic()


class Salesman(Staff):
    def __init__(self, name, position):
        super(Salesman, self).__init__(name, position)
        self.order_list = []
        self.coffee_dictionary = db.coffee_dict()
        self.ingredient_dictionary = db.ingredient_dict()
        self.salesman_menu()

    def salesman_menu(self):
        input_ = get_input("What do you want to do?\n 1.See prices\n 2.Make order\n 0.exit\n")
        if input_ in ('1', "see prices"):
            self.get_price()
        if input_ in ('2', "make order"):
            self.make_order()
        if input_ in ('0', "exit"):
            print ("Exiting to main menu...\n")
            logger.info("Salesman {} logged out".format(self.name))
            self.add_name()
        else:
            print ("Wrong choice! Press 1, 2 or 0")
            self.salesman_menu()

    def make_order(self):
        print (db.show_coffee_types_menu())
        order = get_input("Select ID number of what do you want to sell?\nPress 0 to QUIT\n")
        if order in self.coffee_dictionary.keys():
            coffee_type = self.coffee_dictionary[order]
            self.order_list.append(coffee_type)
            print ("\nYour choice: {} {} BYN\n".format(coffee_type.name, coffee_type.price))
            self.add_ingredient()
        if order in ('0', 'quit', 'q'):
            print ("Exiting to main menu...")
            self.admittance()

    def add_ingredient(self):
        question = get_input("Do you want to add sugar, cream or milk?\n1.yes\n2.no\n")
        if question in ('1', "yes", "y"):
            print (db.show_ingredients_menu())
            order = get_input("What ingredient do you want to add? Choose ID number\nPress 0 to QUIT\n")
            if order in self.ingredient_dictionary.keys():
                ingredient = self.ingredient_dictionary[order]
                self.order_list.append(ingredient)
                print ("\nYour choice: {} {} BYN\n".format(ingredient.name, ingredient.price))
                self.save_sales_details_to_db()
            if order in ('0', "quit", "q"):
                self.add_ingredient()
        if question in ('2', "no", "n"):
            print ("Saving your order...")
            self.save_sales_details_to_db()

    def get_price(self):
        print ("\nCoffeeTypes prices:\n")
        print (db.show_coffee_types_menu())
        print ("\nIngredient prices:\n")
        print (db.show_ingredients_menu())
        self.salesman_menu()

    def save_the_sales_details_into_file(self, order_list):
        date = datetime.now()
        dt = date.strftime("%d.%m.%y_%H_%M_%S")
        dt2 = date.strftime("%d.%m.%y     %H:%M:%S")
        filename = "bill_" + dt
        file_ = open(filename, "a")
        file_.write("CoffeeForMe Shop\n***Your bill***\n")
        for order in self.order_list:
            file_.write("{} - {} BYN\n".format(order.name, str(order.price)))
        file_.write(
            "\nTotal price: {} BYN\nSalesman: {}\n{}\n".format(db.get_overall_price(order_list), self.name, dt2))
        file_.close()
        with open(filename) as file_:
            print(file_.read())

    def save_sales_details_to_db(self):
        db.update_table_sales(self.name, self.order_list)
        return self.bill_request(self.order_list)

    def bill_request(self, order_list):
        print("Printing bill...\n")
        self.save_the_sales_details_into_file(order_list)
        self.order_list = []
        print ("Exiting to salesman menu...\n")
        self.salesman_menu()
