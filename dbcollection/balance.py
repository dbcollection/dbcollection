"""
Balances the data between sets of the dataset.

Allocating/moving data between two or more sets can be done using the balance
property in the load() API. To do this, simply select the name of the sets you
want to balance, and then provide the total amount per set. 

This allows the user to move data around, even depleting a set of data if needed. 
Moving the entire data of a dataset into one set is not only possible but also 
doable and easy.
"""


def parse_inputs(sets, distributions):
    """
    Description
    """
    # check the inputs have the same size
    assert len(sets) == len(distributions)

    # check if the distribution have a correct range of values
    assert min(distributions) >= 0
    assert max(distributions) <= 100
    assert sum(distributions) == 100


def balance(handler, sets, split_distribution):
    """
    Balance sets w.r.t. a range of distributions.

    The distributions must be all positive and sum to 1.
    """
    # assert if the splits are valid
    parse_inputs(sets, split_distribution)

    # concat data
    

    # shuffle if required

    # define index range for each split

    # split the data for each set

    


