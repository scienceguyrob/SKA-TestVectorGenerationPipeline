# `ASC` Directory                        
-
### Author: Rob Lyon
### Email : robert.lyon@manchester.ac.uk
### web   : www.scienceguyrob.com
-


This directory contains an archive `ASC.zip`. This contains files
that describe pulse profiles extracted from the EPN database. Each pulse profile file is named as follows:

`<Pulsar name>_<Frequency>.asc`

Where `<Pulsar name>` is the pulsar 'J' name, and `<Frequency>` the observation frequency of the EPN data.

There is a single file per each unique entry in the EPN database, representing observations covering a wide range of frequencies. The files themselves are in a simple column vector format. They contain the total pulse intensity observed (the I stokes parameter), where the value of each bin is written to a separate line in an individual file. For example:

```
0
1
2
3
11
29
67
180
71
39
9
2
1
1
1
0
```

has 16 bins, each describing total pulse intensity.

**Note:**

The intensity values stored in the files are usually scaled to a range such as `[0,255]`.

The data shown above was created by a python script, `EpnToAsc.py`,  which converts EPN files saved from the EPN database, to `.asc` files which describe pulsar pulse profiles. Data was extracted from the EPN database on March 15th 2016.