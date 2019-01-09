from final_staff import Staff
from final_parser import create_parser

if __name__ == '__main__':
    parser = create_parser()
    user = Staff(name=parser.name, position=parser.position)
