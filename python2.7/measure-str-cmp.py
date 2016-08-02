#!/bin/env python2.7

import time
import random

import plotly.plotly as py
import plotly.graph_objs as go

from tqdm import tqdm
from collections import OrderedDict

TESTS = '../tests.csv'
SAMPLES = 500000
CHAR_OK = 'A'
CHAR_FAIL = 'X'


def load_tests():
    """
    Load tests from file
    :return: A list of tuples with the tests to run
    """
    tests = []

    for line in file(TESTS):
        line = line.strip()

        if not line:
            continue

        str_a, str_b = line.split(',')
        tests.append((str_a, str_b))

    return tests


def generate_strings(num_tests):
    tests = []
    base_string = CHAR_OK * num_tests

    for i in xrange(num_tests):
        test = (CHAR_OK * i) + (CHAR_FAIL * (num_tests - i))
        tests.append((base_string, test))

    return tests


def measure_all_str_cmp(tests):
    ltime = time.time
    temp_measurements = OrderedDict()

    # Init output
    for str_a, str_b in tests:
        temp_measurements[str_b] = 0.0

    # discard the first measurement, the first one seems to always take more
    # time
    str_a, str_b = tests[0]
    for _ in xrange(SAMPLES / 2):
        str_a == str_b

    # Now we measure the str compare function. Take interleaved measurements
    # to account for CPU load / other processes / kernel using our core, context
    # switching, etc.
    pbar = tqdm(total=SAMPLES * len(tests))

    for _ in xrange(SAMPLES):

        random.shuffle(tests)

        for str_a, str_b in tests:
            start = ltime()

            if str_a == str_b:
                temp = True
            else:
                temp = False

            end = ltime()
            temp_measurements[str_b] += end - start

        pbar.update(len(tests))

    pbar.close()

    # Convert the output to the expected format
    measurements = []

    for str_b in temp_measurements:
        result = temp_measurements[str_b]
        measurements.append((str_a, str_b, SAMPLES, result))

    return measurements


def are_equal(str_a, str_b, delay=0.001):
    """
    Slow (when compared with memcmp) string equal implementation used to
    test if the rest of my code is working properly.

    If you replace `str_a == str_b` with `are_equal(str_a, str_b)` and run this
    script you'll get a straight line in the output scatter graph.

    >>> are_equal('a', 'b')
    False

    >>> are_equal('a', 'a')
    True

    >>> start = time.time()
    >>> are_equal('aaaaaaaaa', 'aaaaaaaab')
    False
    >>> end = time.time()
    >>> long = end-start

    >>> start = time.time()
    >>> are_equal('aaaa', 'aaab')
    False
    >>> end = time.time()
    >>> short = end-start

    >>> assert short * 2 < long

    :return: True if the two strings are equal
    """
    if len(str_a) != len(str_b):
        return False

    for i in xrange(len(str_a)):
        time.sleep(delay)
        if str_a[i] != str_b[i]:
            return False

    return True


def print_to_stdout(measurements):
    for measurement in measurements:
        print('%s,%s,%s,%s' % measurement)


def create_graph(measurements):
    x_axys = []
    y_axys = []

    for i, (str_a, str_b, SAMPLES, result) in enumerate(measurements):
        x_axys.append(i)
        y_axys.append(result)

    # Create a trace
    trace = go.Scatter(
        x=x_axys,
        y=y_axys,
        mode='markers'
    )

    data = [trace]

    plot_url = py.plot(data, filename='python-str-cmp', fileopt='new')
    print('Plot URL: %s' % plot_url)

    # Plot offline
    #plotly.offline.plot(data, filename='python-str-cmp.html')


if __name__ == '__main__':
    #tests = load_tests()
    tests = generate_strings(128)

    measurements = measure_all_str_cmp(tests)

    print_to_stdout(measurements)
    create_graph(measurements)
