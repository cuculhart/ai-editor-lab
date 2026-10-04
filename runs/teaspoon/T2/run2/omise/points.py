<<<<<<< SEARCH
def earn_points(amount: int) -> int:
    pass
=======
def earn_points(amount: int) -> int:
    """
    Calculate points for a purchase amount.
    1% of the amount is given as points, rounded down.
    
    Example:
    >>> earn_points(1000)
    10
    >>> earn_points(150)
    1
    """
    return int(amount * 0.01)
>>>>>>> REPLACE
