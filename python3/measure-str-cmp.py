#!/bin/env python3

import sys
import time
import random

from tqdm import tqdm

TESTS = '../tests.csv'
SAMPLES = 5000000
CHAR_OK = 'A'
CHAR_FAIL = 'X'


def load_tests():
    """
    Load tests from file
    :return: A list of tuples with the tests to run
    """
    tests = []
    test_num = 0

    for line in open(TESTS, encoding='utf-8'):
        line = line.strip()

        if not line:
            continue

        str_a, str_b = line.split(',')
        tests.append((test_num, str_a, str_b))

        test_num += 1

    return tests


def generate_strings(num_tests):
    tests = []
    base_string = CHAR_OK * num_tests

    for i in range(num_tests):
        test = (CHAR_OK * i) + (CHAR_FAIL * (num_tests - i))
        tests.append((base_string, test))

    return tests


def measure_all_str_cmp(tests, title):
    ltime = time.time
    zero_time_spent_count = 0
    temp_measurements = {}

    output_filename = 'db-%s.csv' % title
    db = open(output_filename, 'w')

    # Init temp measurement store
    for test_num, str_a, str_b in tests:
        temp_measurements[test_num] = []

    # discard the first measurement, the first one seems to always take more
    # time
    test_num, str_a, str_b = tests[0]
    for _ in range(int(SAMPLES / 100)):
        str_a == str_b

    # Now we measure the str compare function. Take interleaved measurements
    # to account for CPU load / other processes / kernel using our core, context
    # switching, etc.
    pbar = tqdm(total=SAMPLES * len(tests))

    for i in range(SAMPLES):

        random.shuffle(tests)

        for test_num, str_a, str_b in tests:
            # Multiply by 10000000 to get rid of all decimals, this is a neat
            # trick that reduces zero_time_spent_count to zero.
            start = ltime() * 10000000

            if str_a == str_b:
                temp = True
            else:
                temp = False

            end = ltime() * 10000000
            time_spent = end - start

            if not time_spent:
                zero_time_spent_count += 1
                continue

            if time_spent < 0:
                print('Ignore negative time spent.')
                continue

            temp_measurements[test_num].append(time_spent)

        pbar.update(len(tests))

        #
        #   Move the items from memory to disk only once every N samples to
        #   reduce the disk-io and make the test faster
        #
        if i % 50000 == 0:
            save_to_db(temp_measurements, db)

    save_to_db(temp_measurements, db)
    pbar.close()

    if zero_time_spent_count:
        msg = 'Ignored %s measurements because they were zero!'
        print(msg % zero_time_spent_count)


def save_to_db(temp_measurements, db):
    for key in temp_measurements:
        for data_point in temp_measurements[key]:
            # Save
            db.write('%s,%s\n' % (key, data_point))

        # Clear
        temp_measurements[key] = []


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

    for i in range(len(str_a)):
        time.sleep(delay)
        if str_a[i] != str_b[i]:
            return False

    return True


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: ./measure-str-cmp.py <title>')
        sys.exit(1)

    title = sys.argv[1]

    tests = load_tests()
    measure_all_str_cmp(tests, title)
