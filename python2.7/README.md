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