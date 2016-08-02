# How to measure timing differences in Python 2.7

## Setup

Install `taskset`

```
sudo apt-get install util-linux
```

Install tool requirements

```
pip install -r requirements.txt
```

Boot your linux kernel using these parameters:

```
isolcpus=0 idle=poll
```

`isolcpus=0` will isolate the CPU (no processes will be assigned to it by the
kernel process scheduler). Please note that using these instructions the
CPU core 0 will be isolated, this will most likely fail if your workstation
only has once core.

Without `idle=poll` the clock is stopped for a short period of time if
the CPU is idle. Consequently, CPU ticks have different time durations.

To temporarily add a boot parameter to a kernel start your system and
wait for the GRUB menu to show (if you don't see a GRUB menu, press and
hold the left `Shift` key right after starting the system).

Now highlight the kernel you want to use, and press the `e` key. You
should be able to see and edit the commands associated with the highlighted kernel.
Go down to the line starting with linux and add the `isolcpus=0` parameter
to its end. Now press `Ctrl + x` to boot.

Once your workstation has started, verify the new kernel parameter is present
using:

```
cat /proc/cmdline
```

Set other kernel settings:

```
sudo sh -c "echo "performance" > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
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

## Documentation

[Good documentation on how to use isolcpus](http://xmodulo.com/run-program-process-specific-cpu-cores-linux.html)

## Graph with Plotly

```ipython
In [1]: import plotly 
In [2]: plotly.tools.set_credentials_file(username='andres.riancho', api_key='...')
```

# Results

## Environment
 * Ubuntu 14.04
 * Linux 3.13.0-91-generic #138-Ubuntu SMP Fri Jun 24 17:00:34 UTC 2016 x86_64
 * Quad Core / 64-bit CPU / AMD Phenom(tm) II X4 945 Processor
 * 3.00 GHz
 * `ldd --version`: (Ubuntu EGLIBC 2.19-0ubuntu6.9) 2.19
 
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

