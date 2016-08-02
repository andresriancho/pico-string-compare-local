# How to measure timing differences in Python 2.7

## Setup

Install `taskset`

```
sudo apt-get install util-linux
```

Boot your linux kernel using the `isolcpus=0`, this will isolate the
CPU (no processes will be assigned to it by the kernel process scheduler).
Please note that using these instructions the CPU core 0 will be isolated,
this will most likely fail if your workstation only has once core.

To temporarily add a boot parameter to a kernel:

Start your system and wait for the GRUB menu to show (if you don't see a
GRUB menu, press and hold the left `Shift` key right after starting the system).

Now highlight the kernel you want to use, and press the `e` key. You
should be able to see and edit the commands associated with the highlighted kernel.
Go down to the line starting with linux and add the `isolcpus=0` parameter
to its end. Now press `Ctrl + x` to boot.

Once your workstation has started, verify the new kernel parameter is present
using:

```
cat /proc/cmdline
```

## Capture samples

```
sudo taskset 0x1 python2.7 measure-str-cmp.py
```

## Documentation

[Good documentation on how to use isolcpus](http://xmodulo.com/run-program-process-specific-cpu-cores-linux.html)