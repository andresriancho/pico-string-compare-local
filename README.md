## String comparison
This repository holds very simple code snippets that compare two strings 
in different languages .

The code is written in such a way that it is easy to measure if there is
a time side-channel in the string comparison implementation.

## Pico
The code in this repository is just a small part of a bigger research I'm
doing on timing attacks. More info and a tool can be found in
[pico's repository](https://github.com/andresriancho/pico).

## Output
An easy to read summary of the data can be found in
[pico's wiki](https://github.com/andresriancho/pico/wiki/String-comparison-analysis)
and in the README.md files inside each language name in this repository.

## Languages
 * Python 2.7.6
 * Python 3.4.3
 * Ruby
 * Java
 * C

## Common steps for all languages

Install `taskset`

```
sudo apt-get install util-linux
```

Boot your linux kernel using these parameters:

```
isolcpus=0 idle=poll noht
```

`isolcpus=0` will isolate the CPU (no processes will be assigned to it by the
kernel process scheduler). Please note that using these instructions the
CPU core 0 will be isolated, this will most likely fail if your workstation
only has once core.

Without `idle=poll` the clock is stopped for a short period of time if
the CPU is idle. Consequently, CPU ticks have different time durations.

`noht` will disable hyperthreading in all CPU cores.

To temporarily add a boot parameter to a kernel start your system and
wait for the GRUB menu to show (if you don't see a GRUB menu, press and
hold the left `Shift` key right after starting the system).

Now highlight the kernel you want to use, and press the `e` key. You
should be able to see and edit the commands associated with the highlighted kernel.
Go down to the line starting with linux and add the `isolcpus=0` parameter
to its end. Now press `Ctrl + x` to boot.

Once your workstation has started, verify the new kernel parameters are
present using:

```
cat /proc/cmdline
```

Set other operating system settings:

```
sudo sh -c "echo "performance" > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```

You can verify `hyperthreading` is disabled using `utils/ht-read.sh`.

## Documentation

[Good documentation on how to use isolcpus](http://xmodulo.com/run-program-process-specific-cpu-cores-linux.html)

## Graph with Plotly

In order to post the graph to plotly you'll have to configure the credentials:

```ipython
In [1]: import plotly 
In [2]: plotly.tools.set_credentials_file(username='andres.riancho', api_key='...')
```

## Environment

The results stored in this repository were generated using:
 
 * Ubuntu 14.04
 * Linux 3.13.0-91-generic #138-Ubuntu SMP Fri Jun 24 17:00:34 UTC 2016 x86_64
 * Quad Core / 64-bit CPU / AMD Phenom(tm) II X4 945 Processor
 * 3.00 GHz
 * `ldd --version`: (Ubuntu EGLIBC 2.19-0ubuntu6.9) 2.19

## References
More information about this repository can be found in
[this pico issue](https://github.com/andresriancho/pico/issues/47).
