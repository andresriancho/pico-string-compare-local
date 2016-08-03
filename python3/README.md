# How to measure timing differences in Python 2.7

## Setup

Follow the `Common steps for all languages` from the main README.md file,
and then install tool requirements:

```
pip3 install -r requirements.txt
```

## Capture samples

```
sudo taskset 0x1 python3 measure-str-cmp.py
```

## Monitoring the script

`isolcpus` and `taskset` should reduce the number of context switches for
the `measure-str-cmp.py` script:

```
watch -n1 grep ctxt /proc/`pidof python3`/status
```

# Results
 
## Analysis

The script creates a scatter graph with the data, which can be found
[here](https://plot.ly/~andres.riancho/19.embed).

A very basic analysis of the data tells us that:

  * There is a considerable "bump" in the time consumed to compare strings
   of length 128 with 111 and 112 characters in common.
 
  * [CPython's unicode_compare](https://hg.python.org/cpython/file/c4a86fe52006/Objects/unicodeobject.c#l10633)
   removed the performance enhancement present in CPython 2.7.6 where
   `memcmp` is not called when the first character of each buffer is
   different.

 * [CPython 3.4.3](https://hg.python.org/cpython/file/c4a86fe52006/Objects/unicodeobject.c#l10668)
   uses `memcmp` to compare most strings, but also defines a naive byte-
   per-byte [COMPARE](https://hg.python.org/cpython/file/c4a86fe52006/Objects/unicodeobject.c#l10635)
   macro which could be exploited to get better timing measurements.
  
  * The time it takes to compare two strings of length 128 increases erratically
   between 0 and 111 characters in common. It doesn't seem to be possible
   to easily compare two measurements. For example the time it takes to
   compare 20 chars in common is higher than the one for 21 and 22;
   but lower than the one for 27.

It would be difficult to state the time difference for CPython to compare
strings with N and N+1 chars in common, because it is different for the N
being chosen. Some examples are:

 * Time difference between #8 and #7: 6.223 ns
 * Time difference between #16 and #15: 1.674 ns
 * Time difference between #100 and #7: 9.742 ns

Also note that for some (N, M) tuples where M >> N, the difference is
negative (as explained before with 20 and 21).

Research could be done to identify if the behaviour seen in my workstation
can be reproduced in other 64-bit boxes. If the scatter plot for all analysis
is similar / very similar, then it would be possible to use that fact to
perform a timing attack against the string comparison function using a
custom exploitation algorithm that would only work in this scenario.

## Naive string comparison

The script also has a naive string compare function with a byte-per-byte
comparison. When generating a graph with this function the result is
[a straight line](https://plot.ly/~andres.riancho/21.embed).

Note that it is possible to see this straight line even when setting
the `delay` parameter of `are_equal` to zero; and also commenting out
the `time.sleep(delay)` call. This tells us that a byte-per-byte compare
is very easy to identify and (potentially) exploit.

# Source code

See [CPython 3.4.3](https://hg.python.org/cpython/file/c4a86fe52006/Objects/unicodeobject.c#l10633)
string comparison.

`memcmp` is implemented in `glibc`. The real ASM implementation
used by `glibc` will vary based on the CPU (64bit or 32bit, SSE
capabilities, etc. see [here](https://github.com/kraj/glibc/tree/master/sysdeps/x86_64/multiarch)).
