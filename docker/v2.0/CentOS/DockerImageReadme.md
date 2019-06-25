# Test Vector Docker Image (version Experimental)                        
-
### Author: Rob Lyon
### Email : robert.lyon@manchester.ac.uk
### web   : www.scienceguyrob.com
-

This image sets up an environment with an experimental test vector generation pipeline. This
image is to be used for test vector generation, for tests of the SKA's SDP and CSP software. For a more complete pulsar image, look at the Dockerfile's written by Ewan Barr, Casey Law, the Nanograv consortia, or Maciej Serylak.

It takes around 1 hour to build the entire image.

## Operating System

**CentOS 7** is the operating system for the image.

### Packages installed

| ID | Name            | Version |
|----|-----------------|---------|
| 1. | `tcsh`          | 6.18.01 |
| 2. | `unzip`         | 6.0     |
| 3. | `wget`          | 1.14    |
| 4. | `make`          | 2.8.11  |
| 5. | `autoconf`      | 2.69    |
| 6. | `automake`      | 1.13.4  |
| 7. | `gcc`           | 4.8.5   |
| 8. | `gcc-gfortran`  | 4.8.5   |
| 9. | `libtool`       | 2.4.2   |
| 10.| `gcc-c++`       | 4.8.5   |
| 12.| `cfitsio`       | 3.370   | 
| 13.| `cfitsio-devel` | 3.370   | 
| 14.| `fftw-devel`    | 3.3.3   |

Python 3.6 is also configured.

## Pulsar Software

Latest versions of the pulsar software were obtained on April 30th 2019.

The software can be found in: /home/psr/soft

|Software Package               |Version                            |Link |
|-------------------------------|-----------------------------------|-----|
|1. Tempo2                      |2016.11.3 (SNAPSHOT 08/12/2016)    | [Uploaded on 2016-12-05 by MKeith.](https://bitbucket.org/psrsoft/tempo2/downloads/tempo2-2016.11.3.tar.gz)|
|2. Sigproc (Mike Keith's build)| Latest commit 668de78  on 25 Oct.  | [2016 (Master branch)](https://github.com/SixByNine/sigproc)|
|3. Test vector generation code.| Commit 91d8472                    | [Link](https://github.com/scienceguyrob/Docker/blob/master/Resources/Deploy/pulsar_injection_pipeline.zip)|
| 4. Elmarie van Heerden's code that inserts non-stationary noise and RFI into filterbank files.| 1.0|[Github link](https://github.com/EllieVanH/FilterbankFileGeneration)|
|5. Tempo                       |(Master branch) SNAPSHOT 08/12/2016      | [Link](https://sourceforge.net/p/tempo/tempo/ci/master/tree/)|
|6. Filtools                    |Latest      | [Link](https://bitbucket.org/mkeith/filtools/src/master/)|



### `fast_fake` Modification
This version of `fast_fake` in the `sigproc` build mentioned above, has been modified to prevent an incompatibility issue between `fast_fake` outputs, and `PRESTO`. The only difference between the modified version, and the code in `Sigproc_MJK_SNAPSHOT_08_12_2016.zip`, is as follows.

In the file `fast_fake.c`, lines 144-147 have been commented out, to prevent the "signedness" parameter being written to the `fast_fake` output file headers. 

Original code on lines 144-147:

```
if (nbits==8){
  send_char("signed",OSIGN);
}
```

New code:

```
/* Commented out, as apparently this causes problems for PRESTO (see Rob Lyon).*/
/*if (nbits==8){
	send_char("signed",OSIGN);
}*/
```

No other functionality is affected, no other changes have been made.


