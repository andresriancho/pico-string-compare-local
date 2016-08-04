# How to measure timing differences in Java 1.8.0_101

## Setup

Follow the `Common steps for all languages` from the main README.md file,
and then install `java`.

The results shown in this page are for:

``` console
$ java -version
java version "1.8.0_101"
Java(TM) SE Runtime Environment (build 1.8.0_101-b13)
Java HotSpot(TM) 64-Bit Server VM (build 25.101-b13, mixed mode)

$ javac -version 
javac 1.8.0_101
```

## Capture samples

With optimized code (default):

```
rm -rf strcmp.class
javac strcmp.java
sudo taskset 0x1 java strcmp | tee java-strcmp.csv
```

Without optimized code:

```
rm -rf strcmp.class
javac strcmp.java
sudo taskset 0x1 java -Djava.compiler=NONE strcmp | tee java-strcmp.csv
```

## Context switches

You can measure the context switches in the java process using:

```
watch -n1 grep ctxt /proc/`pgrep -f 'java strcmp' -n`/status
```

(less is better)

## Graph

```
python ../utils/graph.py java-strcmp.csv java-1.8.0_101-b13 String.equals
```

# Analysis

## Default settings

The results I'm getting from the Java program are confusing:

  * There are outliers in almost every measurement I make. And in each
  measurement the outlier is different:
  
   * https://plot.ly/~andres.riancho/79.embed
   * https://plot.ly/~andres.riancho/81.embed
   * https://plot.ly/~andres.riancho/83.embed
   * https://plot.ly/~andres.riancho/85.embed
   * https://plot.ly/~andres.riancho/87.embed
    
  * If the outliers are removed from the graph (just select the area that
  doesn't contain them) you'll see a pattern where the time to compare
  the test strings increases; but still with a lot of dispersion between
  each character.
  
Tried to increase the memory available to the Java VM to
(256M)[https://plot.ly/~andres.riancho/95.embed] but that didn't seem to
help.

Also tried debugging the garbage collector to try to identify it as the
noise source; but my Java skills are really bad.

## Running with `-Djava.compiler=NONE`

The `-Djava.compiler=NONE` flag disables JIT, which makes a **huge difference**.
The results of a simple run with this flag is almost the same as the
naive string comparison: [a straight line](https://plot.ly/~andres.riancho/75.embed).

Sadly (for an attacker trying to exploit a side channel) nobody is going
to run Java like this in production.

## Naive string comparison

The code also has a naive string compare function with a byte-per-byte
comparison and an artificial `Thread.sleep(1)`. When generating a graph
with this function the result is [a straight line](https://plot.ly/~andres.riancho/61.embed).

# Source code

When comparing two strings using `String.equals()` Java will run
[String.java#l974](http://hg.openjdk.java.net/jdk7u/jdk7u6/jdk/file/8c2c5d63a17e/src/share/classes/java/lang/String.java#l974)
which compares byte-per-byte:

```java
    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        if (anObject instanceof String) {
            String anotherString = (String) anObject;
            int n = value.length;
            if (n == anotherString.value.length) {
                char v1[] = value;
                char v2[] = anotherString.value;
                int i = 0;
                while (n-- != 0) {
                    if (v1[i] != v2[i])
                            return false;
                    i++;
                }
                return true;
            }
        }
        return false;
    }
```

But the JVM might decide that its faster to run [this optimized code](https://github.com/openjdk-mirror/jdk7u-hotspot/blob/master/src/cpu/x86/vm/x86_64.ad#L10609),
which calls [char_arrays_equals](https://github.com/openjdk-mirror/jdk7u-hotspot/blob/50bdefc3afe944ca74c3093e7448d6b889cd20d1/src/cpu/x86/vm/assembler_x86.cpp#L9946-L10057).
