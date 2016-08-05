#!/bin/env python2.7

import sys

from tqdm import tqdm

from common.stats import midhinge, median, trimean
from common.common import (load_results_from_csv,
                           analyze_differences,
                           create_graph)

STATS_METHODS = {'midhinge': midhinge,
                 'median': median,
                 'trimean': trimean}


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: ./graph.py <results-file> <stats-method> <language> <title>')
        sys.exit(1)

    # Load results from file
    file_name = sys.argv[1]
    stats_method_name = sys.argv[2]
    language = sys.argv[3]
    title = sys.argv[4]

    try:
        stats_method = STATS_METHODS[stats_method_name]
    except KeyError:
        valid_methods = ', '.join(STATS_METHODS.keys())
        print('Invalid stats method. Choose one of %s.' % valid_methods)
        sys.exit(1)

    measurements = []
    samples = 0

    pbar = tqdm(total=128)

    # Load and process one test result at the time to avoid consuming a lot
    # of memory
    for test_num, test_n_samples in load_results_from_csv(file_name):
        summarized_result = stats_method(test_n_samples)
        samples += len(test_n_samples)

        measurements.append((test_num, summarized_result))

        args = (len(test_n_samples), stats_method_name, summarized_result)
        print('Read %s samples from file. %s is %s' % args)

        pbar.update(1)

    pbar.close()

    # Graph
    create_graph(measurements, samples, language, title, stats_method_name)
