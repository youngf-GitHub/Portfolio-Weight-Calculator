
import sys
from optparse import OptionParser
from calculator import Calculator


def main():

    parser = OptionParser("\n  python  %prog  -f  portfolio_file  [ -e ending_portfolio_file | -h ]")
    parser.add_option("-f", "--file", dest="portfolio_file", help="portfolio input file")
    parser.add_option("-e", "--end", dest="ending_portfolio_file", help="portfolio ending mv file")
    options, args = parser.parse_args()

    start_file, end_file = options.portfolio_file, options.ending_portfolio_file

    if start_file is None or start_file.strip() == "":
        parser.print_help()
        sys.exit(2)

    if end_file is None or end_file.strip() == "":
        end_file = ""

    try:

        calculator = Calculator(start_file, end_file)

        if len(calculator.end_market_tree_map) == 0:

            calculator.print_fund_ratio()

        else:

            calculator.print_weighted_return()

        sys.exit(0)

    except ValueError as e:
        print(e.args)

    except FileNotFoundError as e:
        print(e)

    sys.exit(2)


if __name__ == "__main__":
    main()
