
# Test Vector Filename, Metadata & Directory Standards


Dr. Rob Lyon (robert.lyon@manchester.ac.uk) 

University of Manchester

01/04/2019

Version 1.0

# 1. Test Vector File Format

### Overview
Test vectors are **filterbank** files used to analyse pulsar search software pipelines. These files are essentially n-dimensional matrices containing numerical values representing n-bit samples in time, frequency, phase, and even polarisation space. 

There are a number of parameters used to create test vectors. These include,

* The number of frequency channels.
* The time resolution in microseconds.
* The test vector length in seconds.
* The number of bits per sample.
* The number of polarisations.

We often inject various types of signals into our test vectors, to test the recovery capabilities of our data processing pipelines. Injected signals are described via another set of parameters that include,

* The type of signal injected (noise, RFI, pulsar, single-pulse burst etc).
* The width of the pulse injected, as a percentage of the pulse phase.
* The period of the injected pulse/pulses in milliseconds.
* The signal-to-noise ratio (SNR) of the signal injected.
* The Dispersion Measure (DM) of the pulse/pulses injected.
* The acceleration applied to the signal.
* The shape of the pulse, perhaps corresponding to a known pulsar/single-pulse burst.
* If injecting a known pulsar signal, it is useful to know at what frequency the injected pulse shape was originally observed at. This is useful to know given that pulse shape varies with frequency.

There are many more parameters, and therefore an effectively infinite number of configuration possibilities. However as a starting point, we need to be able to differentiate between test vectors generated via combinations of just these 12 parameters. 

We also need to consider how many test vectors are likely to be generated in practice. The analysis conducted for [AT4-7](https://jira.skatelescope.org/browse/AT4-7), suggests that 8,832 test vectors are needed just to test the Fourier Domain Acceleration Search (FDAS) software module. Many more will likely be needed in practice. Thus we require a naming convention that remains descriptive when test vectors are accumulated large quantities.

## 1.1. Naming Standard

We have decided upon the following naming standard:

`<LABEL>_<BATCH>_<PERIOD>_<WIDTH>_<DM>_<Z>_<S/N>_<PULSE>_<FREQ>.fil`

Where the 'tag' components comprising the filename are described in Table 1. below.

| Tag | Data Type | Max Length | Meaning  |
|:----------|:----------|:-----------|:---------|
|`<LABEL>`  | String    |30          | An alphanumeric tag describing the suite a test vector belongs to/or some other unique identifier.|
|`<BATCH>`  | String    |30          | An alphanumeric tag describing the processing batch that created the vector. Used along with `<LABEL>` to achieve primitive version control.|
|`<PERIOD>` | Float     |16          | Pulse period in milliseconds.  |
|`<WIDTH>`  | Float     |16          | The width of the injected signal (percentage of phase).|
|`<DM>`     | Float     |16          | The DM of the injected signal in pc cm<sup>-3</sup>.|   
|`<Z>`      | Float     |16          | The acceleration of the injected signal in m/s/s.|
|`<S/N>`    | Float     |16          | The SNR of the injected signal.|
|`<PULSE>`  | String    |20          | An alphanumeric tag describing the pulsar shape injected, e.g. the JName of a pulsar. Note that `+` and `-` characters are valid here too.|
|`<FREQ>`   | String    |10          | An alphanumeric tag describing the frequency of the injected pulse, e.g. '1400' corresponding to 1400 MHz.|
**Table 1. File name components.** 

Most operating systems restrict filenames to 255 characters or less. The max file size achievable if following the standard above, is 170 characters excluding the file extension (174 with the `.fil` extension). It is not necessary to pad components so that they meet the max length.

### Examples

Some valid file names presented below for clarity:

| Example  | Comment |
|:---------|:--------|
|`TEST_1_33.3_0.1_56.7_0.0_16.5_B0531+21_1408.fil`| An example test vector representing an observation of the crab pulsar.|
|`TEST_1_10.0_0.1_100_0.0_7.5_FAKE1_1408.fil`| An example test vector representing an observation of some artificial signal called `FAKE1`.|
**Table 2. Examples of valid file names.** 

### Tools

Here we have some code useful for managing and checking test vector file formats. TBD.

# 2. Metadata Standard

It is impractical to use test vector filenames to self-describe the parameters that generated them. It is recommended that metadata files with the `.tvm` extension be maintained to do this instead. Here `.tvm` stands for 'Test Vector Metadata'.

The `.tvm` file standard is simple. It is comprised of `<KEY>:<VALUE>` pairs, separated by `:`. 

Comments can be written in metadata files by starting a comment line, using the `#` symbol. Whitespace is ignored when reading metadata files (in code).

Due to the simple nature of the metadata format, the `:` symbol must not be included in either the `<KEY>` or `<VALUE>` components of a pair. A valid example metadata file is shown below.

```
# Author: Rob Lyon
# 01/04/2019
#
Description:
This is a fake batch. 

It contains some example information only.

Tobs: 600
Tsamp: 64
Fc: 1400
Fh: 1500
Fch1: 1300
deltav: 78
B: 200
Nchan: 1000
Nbit: 8
Seed: 1
```
**Listing 1. An example metadata file Example.tvm.**

You are free to define your own `<KEY>` values as you see fit.

## Metadata Management & Linking

Two sources of metadata should be maintained when creating test vectors.

* A Metadata file relating to the `<LABEL>` tag in a test vector's filename. This should be used to describe the test suite a vector belongs to, why it was created, which vectors it relates to, the owner of the test suite, which software the test suite is used to test, any caveats to using the vectors etc.
* A Metadata file describing the `<BATCH>` tag in a test vector's filename. This is crucial for enabling reproducibility. It should describe all additional parameters required to generate the test vectors, which software versions were used to generate them etc.

These files are not required for every test vector, but for every test suite (where a test suite consists of a group of individual tests).

To link individual test vectors to metadata files, ensure the `<LABEL>` and `<BATCH>` tags correspond to the filenames of existing metadata files. For example, if we have a test vector called:

`FOPTest_Batch1_33.3_0.1_56.7_0.0_16.5_B0531+21_1408.fil`

Then there should be two metadata files called `FOPTest.tvm` and `Batch1.tvm` respectively. These files can be located anywhere so long as they are accessible.



# 3. Test Vector Storage

Test vectors should be stored in the `/raid` directory on Dokimi. There is 55 TB of standard hard drive storage available here. To make finding test vectors straightforward, we adopt the following directory structure:

```
/raid
+-- atul
+-- llevin
+-- lyon
+-- TestVectors
    +-- Metadata
        +-- Batches
            +-- Batch1.tvm
        +-- TestSuites
            +-- TestSuite1.tvm
    +-- TestSuite1
        +-- TestCase1
            +-- TestSuite1_Batch1_33.0_0.1_10.0_0.0_4.0_B0531+21_1408.fil
            +-- TestSuite1_Batch1_33.0_0.1_20.0_0.0_8.0_B0531+21_1408.fil
            +-- TestSuite1_Batch1_33.0_0.1_30.0_0.0_9.0_B0531+21_1408.fil
            ...
        +-- TestCase2
        +-- TestCase3
    +-- TestSuite2
    +-- TestSuite3
    +-- TestSuiteN
``` 

It is up to the individual creating test vectors, to ensure test suites and test cases are appropriately named.

**Note:** We avoid using whitespace characters in file names and directory names.

# 4. Best Practices

Test vectors will proliferate over time. It is therefore important that we maintain metadata and the proposed directory structure to make them manageable. 

It is advised that the metadata shown in the following example, be provided at a minimum in metadata files (change the values as appropriate):

```
# Observation length.
Tobs: 600

# Sampling rate in microseconds.
Tsamp: 64

# Frequency information (first channel, last, and centre frequency).
Fc: 1400
Fh: 1500
Fch1: 1300

# Channel width.
deltav: 78

# Bandwidth in MHz.
B: 200

# Number of frequency channels.
Nchan: 1000

# Bits per sample.
Nbit: 8

# The random seed used for fast_fake.
Seed: 1
```
