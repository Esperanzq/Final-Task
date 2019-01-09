try:
    import final_parser as pars
    import final_logger as log
    from final_db import connect as db
    from datetime import datetime
except ImportError as err:
    print ("{}. Check if file exists.".format(err))

parser = pars.create_parser()
local_logger = log.final_logger()


try:
    get_input = raw_input
except NameError:
    get_input = input


class Staff(object):
    def __init__(self, name=None, position=None):
        self.name = name
        self.position = position
        if not self.name:
            self.add_name()
        if not self.position:
            self.add_position()
            self.add_employee_to_db()
            self.define_position_of_employee()

    def add_name(self, name_=parser.name):
        if not name_:
            res = get_input("What is your name?\n").capitalize()
            self.name = res
            return self.add_position()

    def add_position(self, position_=parser.position):
        if not position_:
            position = get_input("Hello! What is your position?\n1.manager 2.salesman\n")
            if position == '1' or position == "manager":
                self.position = "manager"
                return self.add_employee_to_db()
            if position == '2' or position == "salesman":
                self.position = "salesman"
                return self.add_employee_to_db()
            else:
                local_logger.error("There is no such position, choose from available variants")
                self.add_position()

    def define_position_of_employee(self):
        if self.position == "salesman":
            return Salesmans(name=self.name, position=self.position)
        if self.position == "manager":
            return Managers(name=self.name, position=self.position)

    def add_employee_to_db(self):
        user_info = (self.name, self.position)
        db.add_employee(user_info)
        return self.define_position_of_employee()


class Managers(Staff):
    def __init__(self, name, position):
        super(Managers, self).__init__(name, position)
        self.show_statistic()

    def show_statistic(self):
        results = get_input("Do you want to see statistic?\n1.Yes 2.No\n")
        if results in ('1', "yes", "y"):
            db.show_statistic()
            return self.show_statistic()
        if results in ('2', "no", "n"):
            print ("Exiting...\n")
            return Staff()
        else:
            print ("You need to press '1' or '2'")
            return self.show_statistic()


class Salesmans(Staff):
    def __init__(self, name, position):
        super(Salesmans, self).__init__(name, position)
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
            Staff()

    def make_order(self):
        print (db.show_coffee_types_menu())
        order = get_input("Select ID number of what do you want to sell? Press 0 to QUIT\n")
        if order in self.coffee_dictionary.keys():
            coffeetype = self.coffee_dictionary[order]
            self.order_list.append(coffeetype)
            print ("You choose {} {} BYN".format(coffeetype.name, coffeetype.price))
            self.add_ingredient()
        if order in ('0', 'quit', 'q'):
            Staff()

    def add_ingredient(self):
        question = get_input("Do you want to add sugar, cream or milk?\n1.yes\n2.no\n")
        if question in ('1', "yes", "y"):
            print (db.show_ingredients_menu())
            order = get_input("What ingredient do you want to add? Choose ID number\nPress 0 to QUIT\n")
            if order in self.ingredient_dictionary.keys():
                ingredient = self.ingredient_dictionary[order]
                self.order_list.append(ingredient)
                print ("You choose {} {} BYN".format(ingredient.name, ingredient.price))
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
        dt = date.strftime("%H_%M_%S_%m.%d.%y")
        filename = "bill_" + dt
        with open(filename, "w") as file_:
            file_.write("\n***Your bill:***\n")
        with open(filename, "a") as file_:
            for order in self.order_list:
                file_.write("\n" + order.name + " - " + str(order.price) + " BYN " + "\n")
        with open(filename, "a") as file_:
            file_.write("\nTotal price: {} BYN\n".format(db.get_overall_price(order_list)))
        with open(filename) as file_:
            file_contents = file_.read()
            print (file_contents)

    def save_sales_details_to_db(self):
        db.update_table_sales(self.name, self.order_list)
        return self.bill_request(self.order_list)

    def bill_request(self, order_list):
        choice = get_input("Do you want to see bill?\n1.yes\n2.no")
        if choice in ('1', "y", "yes"):
            self.save_the_sales_details_into_file(order_list)
        if choice in ('2', "no", "n"):
            print ("\nTotal price is {} BYN ".format(db.get_overall_price(order_list)))
        self.order_list = []
        self.salesman_menu()
