# elite-knapsack
Dynamic programming solver for the Knapsack problem in 2 dimensions.
Designed to solve the problem of "what commodities do I buy?" in Elite
Dangerous.

## Usage
Create a .csv file for the profitable items for your trade route,
similar to the `example.csv` file in the repository.

Run the script:

    ./knapsack.py -h

Or, for example:

    ./knapsack.py -c 36 -b 78139 -i example.csv

For very large holds/very large budgets, it can be slow. This tool is
designed to be used when you don't have enough credits to buy a full hold
of your most profitable item.

## Licensing
See LICENSE file.
