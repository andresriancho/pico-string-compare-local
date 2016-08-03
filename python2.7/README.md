# How to measure timing differences in Python 2.7

## Setup

Follow the `Common steps for all languages` from the main README.md file,
and then install tool requirements:

```
pip install -r requirements.txt
```

## Capture samples

```
sudo taskset 0x1 python2.7 measure-str-cmp.py
```

## Monitoring the script

`isolcpus` and `taskset` should reduce the number of context switches for
the `measure-str-cmp.py` script:

```
watch -n1 grep ctxt /proc/`pidof python2.7`/status
```

# Results

## Analysis

The script creates a scatter graph with the data, which can be found
[here](https://plot.ly/~andres.riancho/1.embed).

A very basic analysis of the data tells us that:

 * For some unknown reason (potentially glibc performance enhancements)
   comparing strings of length 128 with 3 and 7 characters in common requires 
   considerable more time than the same operation with 2 and 6 characters
   in common
    
 * Comparing strings of length 128 with 0 to 15 chars in common is *almost*
   constant in time (see previous point)
 
 * [CPython's string_richcompare](https://hg.python.org/cpython/file/2.7/Objects/stringobject.c#l1192)
   does not call `memcmp` when the first character is different, this makes
   comparisons of strings where the first character is different much faster.
  
 * There is a considerable "bump" in the time consumed to compare strings
   of length 128 with 107 and 108 characters in common.
 
 * The time it takes to compare two strings of length 128 increases erratically
   between 16 and 107 characters in common. It doesn't seem to be possible
   to easily compare two measurements. For example the time it takes to
   compare 16 chars in common is higher than the one for 22; but lower
   than the one for 23.

It would be difficult to state the time difference for CPython to compare
strings with N and N+1 chars in common, because it is different for the N
being chosen. Some examples are:

 * N: 9, 0.505 ns
 * N: 15, 6.065 ns

Also note that for some (N, M) tuples where M >> N, the difference is
negative (as explained before with 16 and 22).

Research could be done to identify if the behaviour seen in my workstation
can be reproduced in other 64-bit boxes. If the scatter plot for all analysis
is similar / very similar, then it would be possible to use that fact to
perform a timing attack against the string comparison function using a
custom exploitation algorithm that would only work in this scenario.

## Naive string comparison

The script also has a naive string compare function with an artificial
delay. When generating a graph with this function the result is [a straight
line](https://plot.ly/~andres.riancho/3.embed).

# Source code

When comparing two strings using `==` CPython 2.7 uses [string_richcompare](https://hg.python.org/cpython/file/2.7/Objects/stringobject.c#l1192):

```c
    if (op == Py_EQ) {
        /* Supporting Py_NE here as well does not save
           much time, since Py_NE is rarely used.  */
        if (Py_SIZE(a) == Py_SIZE(b)
            && (a->ob_sval[0] == b->ob_sval[0]
            && memcmp(a->ob_sval, b->ob_sval, Py_SIZE(a)) == 0)) {
            result = Py_True;
        } else {
            result = Py_False;
        }
        goto out;
    }
```

Then, `memcmp` is implemented in `glibc`. The real ASM implementation
used by `glibc` will vary based on the CPU (64bit or 32bit, SSE
capabilities, etc. see [here](https://github.com/kraj/glibc/tree/master/sysdeps/x86_64/multiarch)).

