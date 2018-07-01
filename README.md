Portfolio Weight Calculator
===

This project is an implementation of a Portfolio Weight Calculator which was described in

    <https://gist.github.com/rprabhat/3b8cc6e47a822d63b844e3d3d0d67ea7>


### Solution

    Load the portfolio data from an input file, and build a tree structure to represent the fund relationship.

    The class definition:

        Fund:
            name,
            parent,
            has_child,
            mv,
            aggregated_mv,
            weight

        Calculator:
            start_file_name
            end_file_name
            start_market_tree_map
            end_market_tree_map
            current_file_name

    The Fund A = { B(1000), C(2000) } will be presented as below in the tree_map:

    {  
        A: name=A, parent='', has_child=True, mv=3000, aggregated_mv=3000, weight=0  
        B: name=B, parent=A,  has_child=True, mv=1000, aggregated_mv=1000, weight=0  
        C: name=C, parent=A,  has_child=True, mv=2000, aggregated_mv=2000, weight=0  
    }   

    To print out the weight for each of the base funds:  

    1) Validate (re-calculate) the market value for each tree node (including root).  
    2) Find the Root fund(s) and the corresponding base funds.  
    3) Calculate the weight (ratio) for each base fund.  

    When ending market value (file) is provided, load the ending market file into a separate tree map,  
    then calculate the weighted return.  


### Development Environment:
      Python 3.7


### Source Code:  
        `calculator.py`
        `fund.py`
        `weight-calc.py`


### Command Line Usage:
        `python  weight-calc.py  -f portfolio_file  [  -e  portfolio_file   |   -h  ]`
        Options:  
            -h, --help            show this help message and exit  

            -f PORTFOLIO_FILE, --file=PORTFOLIO_FILE  
                                portfolio input file  

            -e ENDING_PORTFOLIO_FILE, --end=ENDING_PORTFOLIO_FILE  
                                portfolio ending mv file  

### Test
    1. Calculator
        `python  weight-calc.py   -f ./test_data/sample_portfolio.txt`

        input file:  
            A,B,1000  
            A,C,2000  
            B,D,500  
            B,E,250  
            B,F,250  
            C,G,1000  
            C,H,1000  

        output:  
            A,D,0.167  
            A,E,0.083  
            A,F,0.083  
            A,G,0.333  
            A,H,0.333  

    2. Extended Calculator
        `python  weight-calc.py   -f ./test_data/sample_portfolio.txt      -e  ./test_data/ending_portfolio.txt`

        input file:  

          sample__portfolio.txt      ending_portfolio.txt  
       _____________________________________________________  

            A,B,1000                     A,B,1040  
            A,C,2000                     A,C,2000  
            B,D,500                      B,D,490  
            B,E,250                      B,E,300  
            B,F,250                      B,F,250  
            C,G,1000                     C,G,1000  
            C,H,1000                     C,H,1000  

        output:  
            weighted return of A: 1.33 %  

### To Be Improved
        The tree map for the ending market value could be omitted, and share the tree map with the starting market value instead.  
