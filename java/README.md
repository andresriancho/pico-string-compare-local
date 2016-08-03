# How to measure timing differences in Java 1.8.0_101

## Environment

``` console
$ java -version
java version "1.8.0_101"
Java(TM) SE Runtime Environment (build 1.8.0_101-b13)
Java HotSpot(TM) 64-Bit Server VM (build 25.101-b13, mixed mode)
```

## Capture samples

```
rm -rf strcmp.class
javac strcmp.java
sudo taskset 0x1 java strcmp | tee java-strcmp.csv
```

## Graph

```
python ../utils/graph.py java-strcmp.csv java-1.8.0_101-b13 strcmp
```

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


