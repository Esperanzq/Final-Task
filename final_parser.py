import argparse


def create_parser():
    parser = argparse.ArgumentParser(prog='CoffeeForMe')
    parser.add_argument(
        '-n', '--name', type=str, help='Username of employee')
    parser.add_argument(
        '-p', '--position', type=str, help='Position of employee', choices=["manager", "salesman"])
    return parser.parse_args()
