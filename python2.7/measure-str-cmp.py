#!/bin/env python2.7

import time

TESTS = '../tests.csv'
SAMPLES = 10000000


def load_tests():
    """
    Load tests from file
    :return: A list of tuples with the tests to run
    """
    tests = []

    for line in file(TESTS):
        line = line.strip()
        str_a, str_b = line.split(',')
        tests.append((str_a, str_b))

    return tests


def measure_str_cmp(str_a, str_b, samples):
    total = 0.0

    for _ in xrange(samples):
        start = time.time()

        str_a == str_b

        end = time.time()
        total += end - start

    return total


def measure_all_str_cmp(tests):
    # discard the first measurement, the first one seems to always take more
    # time
    str_a, str_b = tests[0]
    measure_str_cmp(str_a, str_b, SAMPLES)

    for str_a, str_b in tests:
        result = measure_str_cmp(str_a, str_b, SAMPLES)
        print('%s,%s,%s,%s' % (str_a, str_b, SAMPLES, result))


if __name__ == '__main__':
    tests = load_tests()
    measure_all_str_cmp(tests)
