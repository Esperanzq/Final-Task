import unittest
from final_db import connect


class TestDatabaseClient(unittest.TestCase):
    def setUp(self):
        self.user_info = ('Micky', 'manager')
        self.non_existing_user_info = ('salesman', 'Wydie')
        self.not_existing_coffee = ("Capuccino", 10)
        self.existing_coffee = ("Raf", 10)

    def test_add_employee(self):
        connect.add_employee(self.user_info)
        self.assertTrue(connect.check_if_employee_in_db(self.user_info))

    def test_user_not_in_db(self):
        self.assertFalse(connect.check_if_employee_in_db(self.non_existing_user_info))

    def test_coffee_types_in_db(self):
        connect.fill_table_coffeetypes(self.existing_coffee)
        self.assertTrue(connect.check_if_coffee_types_in_db(self.existing_coffee))

    def test_coffee_types_not_in_db(self):
        self.assertFalse(connect.check_if_coffee_types_in_db(self.not_existing_coffee))


if __name__ == '__main__':
    unittest.main()
