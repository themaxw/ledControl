import fastrand

def randInt(start, stop):
    """returns a random int in the range [start, stop)

    Args:
        start (int): start of interval, inclusive
        stop (int): end of interval, exclusive

    Returns:
        int: random int
    """
    return fastrand.pcg32bounded(stop - start) + start

def randFloat(start, stop):
    """returns a random Float Between 0 and 1, further bound by [start, stop)

    Args:
        start (float): must be between 0 and 1
        stop (float): must be between 0 and 1
    """
    assert(0 <= start <= stop <= 1)

    precision = 10000
    start = int(start * precision)
    stop = int(stop * precision)
    randFloat = randInt(start, stop)
    return float(randFloat) / precision