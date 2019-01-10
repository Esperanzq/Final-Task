# -*- coding: utf-8 -*-
from final_staff import Staff
from final_parser import create_parser

if __name__ == '__main__':
    parser = create_parser()
    if parser.name:
        user = Staff(name=parser.name.capitalize(), position=parser.position)
        assert parser.name.isalpha(), "Name should consist only from letters"
        assert 36 > len(parser.name) >= 3, "The len of name can`t be less than 3 symbols and more than 36 symbols"
    else:
        user = Staff(name=parser.name, position=parser.position)
    user.admittance()
