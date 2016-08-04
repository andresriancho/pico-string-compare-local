# How to measure timing differences in Ruby 2.3.0p0

## Setup

Follow the `Common steps for all languages` from the main README.md file,
and then install `ruby`. The results shown in this page are for this
ruby version:

``` console
$ ruby --version
ruby 2.3.0p0 (2015-12-25 revision 53290) [x86_64-linux]
```

## Capture samples

```
sudo taskset 0x1 ruby measure-str-cmp.rb  | tee ruby-strcmp.csv
```

## Graph

```
python ../utils/graph.py ruby-strcmp.csv ruby-2.3.0p0 strcmp
```

# Results
 
## Drunk Ruby

An initial version of the ruby script created graphs that indicated that
[ruby compared strings in less than zero nanoseconds](https://plot.ly/~andres.riancho/107.embed).

I'm not sure why this is, most likely a problem with the precision used
to store long numbers in Ruby. Fixed it by adding code that excludes
negative measurements:

```console
# taskset 0x1 ruby measure-str-cmp.rb  | tee ruby-strcmp-naive.csv
Go home Ruby, you're drunk. Negative time spent: -999965711
Go home Ruby, you're drunk. Negative time spent: -999945696
Go home Ruby, you're drunk. Negative time spent: -999974738
Go home Ruby, you're drunk. Negative time spent: -999961199
...
```

After filtering the negative measurements the graph for the naive string
comparison function looks as expected: [a straight line](https://plot.ly/~andres.riancho/111.embed).

## String compare

TBD

# Source code

TBD