import numpy

from stats import midhinge as midhinge_impl
from scipy import stats


def median(samples):
    """
    Calculate the median

    https://en.wikipedia.org/wiki/Median

    In [9]: median([0,1,2,3,4,5,6,7,8,9,10,11])
    Out[9]: 5.5

    In [10]: median([0,1,2,3,4,5,6,7,8,9,10,11,12])
    Out[10]: 6.0

    In [11]: median([0,1,2,3,4,5,6,7,8,9,10,50])
    Out[11]: 5.5

    In [12]: median([0,1,2,3,4,5,6,7,8,9,10,50,50])
    Out[12]: 6.0

    In [13]: median([0,1,2,3,4,5,6,7,8,9,10,50,50,100])
    Out[13]: 6.5

    :param samples: All the samples
    :return: One number representing the whole sample series
    """
    return numpy.median(samples)


def midhinge(samples):
    """
    The midhinge is halfway between the first and second hinges. It is a
    better measure of central tendency than the midrange, and more robust
    than the sample mean (more resistant to outliers).

    https://en.wikipedia.org/wiki/Midhinge

    In [3]: midhinge([0,1,2,3,4,5,6,7,8,9,10])
    Out[3]: 5.0

    In [4]: midhinge([0,1,2,3,4,5,6,7,8,9,10,50])
    Out[4]: 5.5

    In [5]: midhinge([0,1,2,3,4,5,6,7,8,9,10,50,50])
    Out[5]: 6.0

    In [6]: midhinge([0,1,2,3,4,5,6,7,8,9,10,50,50,100])
    Out[6]: 6.5

    :param samples: All the samples
    :return: One number representing the whole sample series
    """
    return midhinge_impl(samples)


def trimean(samples, trim=0.10):
    """
    Trim the top and bottom `trim`% of the samples and then calculate the mean
    This is a good way to remove outliers.

    In [15]: trimean([0,1,2,3,4,5,6,7,8,9,10])
    Out[15]: 5.0

    In [16]: trimean([0,1,2,3,4,5,6,7,8,9,10,11])
    Out[16]: 5.5

    In [17]: trimean([0,1,2,3,4,5,6,7,8,9,10,50])
    Out[17]: 5.5

    In [18]: trimean([0,1,2,3,4,5,6,7,8,9,10,50,50])
    Out[18]: 9.545454545454545

    In [19]: trimean([0,1,2,3,4,5,6,7,8,9,10,50,50,50])
    Out[19]: 12.916666666666666

    In [20]: trimean([0,1,2,3,4,5,6,7,8,9,10,50,50,50,100])
    Out[20]: 15.76923076923077

    :param samples: All the samples
    :param trim: % to trim from top and bottom
    :return: One number representing the whole sample series
    """
    return stats.trim_mean(samples, trim)