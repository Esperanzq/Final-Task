import argparse


def create_parser():
    """Parse for optional argument:
    '-n' '--name' to get name
    '-p' '--position' to get position (variants are 'salesman', 'manager')
    if combination of name and position is not found in database, new user will be created
    """
    parser = argparse.ArgumentParser(prog='CoffeeForMe', description='Great Description To Be Here')
    parser.add_argument(
        '-n', '--name', type=str, default=None, help='Username of employee')
    parser.add_argument(
        '-p', '--position', type=str, default=None, help='Position of employee', choices=["manager", "salesman"])
    return parser.parse_args()
