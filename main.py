import argparse
import re
import database

parser = argparse.ArgumentParser(description='ASIN Inspector database')
parser.add_argument('--add', '-a', help='Add an ASIN to the database')
parser.add_argument('--remove', '-r', help='Remove an ASIN from the database')
parser.add_argument('--list', '-l', action='store_true', help='List all ASINs in the database')
parser.add_argument('--scrape', '-s', action='store_true', help='Scrapes data for all ASINs and store raw data in database')
parser.add_argument('--process', '-p', action='store_true', help='Processes raw data to extract key data')
args = parser.parse_args()

def validate_asin(asin):
    pattern = re.compile("B[\dA-Z]{9}|\d{9}(X|\d)$/")
    if(pattern.match(asin.upper())):
        print(asin + " valid ASIN")
        return(True)
    else:
        print(asin + " not a valid ASIN")
        return(False)

if __name__ == '__main__':
    if args.add != None:
        if validate_asin(args.add.upper()):
            database.add(args.add.upper())

    if args.remove != None:
        database.remove(args.remove.upper())

    if args.list:
        database.list()

    if args.scrape:
        database.scrape()

    if args.process:
        print("Not implemented")
