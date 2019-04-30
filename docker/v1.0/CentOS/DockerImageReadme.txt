**************************************************************************
|                                                                        |
|  Test vector machine Docker Image (version 1.1)                        |
|                                                                        |
**************************************************************************
| Author: Rob Lyon, Yan Grange, Wietze Albers                            |
| Email : robert.lyon@manchester.ac.uk                                   |
| web   : www.scienceguyrob.com                                          |
**************************************************************************

This image sets up an environment with only a basic pulsar stack. This
is because the image is to be used for test vector generation, for tests
of the SKA's SDP and CSP software. For a more complete pulsar image, look
at the Dockerfile's written by Casey Law, or Maciej Serylak.

Please note that it takes around 1 hour to build the entire image on the
dockerhub.

**************************************************************************

OS: CentOS 7

OS PACKAGES INSTALLED:

#   Name            Version
1.  tcsh            6.18.01
2.  unzip           6.0
3.  wget            1.14
4.  make            2.8.11
5.  autoconf        2.69
6.  automake        1.13.4
7.  gcc             4.8.5
8.  gcc-gfortran    4.8.5
9.  libtool         2.4.2
10. gcc-c++         4.8.5
12. cfitsio         3.370
13. cfitsio-devel   3.370
14. fftw-devel      3.3.3


PULSAR SOFTWARE:

Latest versions of the pulsar software were obtained on December 8th 2016.

The software can be found in: /home/psr/soft

Software Package                Version                             Link
1. Tempo2                       2016.11.3 (SNAPSHOT 08 12 2016)     https://bitbucket.org/psrsoft/tempo2/downloads/tempo2-2016.11.3.tar.gz
                                Uploaded on 2016-12-05 by MKeith.

2. Sigproc (Mike Keith's build) Latest commit 668de78  on 25 Oct    https://github.com/SixByNine/sigproc
                                2016 (Master branch)

3. Test vector generation code. Commit 91d8472                      https://github.com/scienceguyrob/Docker/blob/master/Resources/Deploy/pulsar_injection_pipeline.zip

4. Elmarie van Heerden's code that
   inserts non-stationary noise and
   RFI into filterbank files.

5. Tempo                        (Master branch) SNAPSHOT 08 12      https://sourceforge.net/p/tempo/tempo/ci/master/tree/
                                2016

Changes since version 1.0

Removed:

1. CUDA version 8.0 as it wasn't being used. We can put Cuda back in if necessary.
2. Install of PRESTO (Commit bd3c0181) due to this issue: https://github.com/scottransom/presto/issues/68
3. Removed PRESTO dependencies to reduce the image size. This includes,

    3.1. numpy
    3.2. scipy
    3.3. fitsio
    3.4. astropy
    3.5. astroplan
    3.6. pyfits
    3.7. matplotlib
    3.8. pyephem
    3.9. PGPlot
    3.10 X11
    3.11 libX11-devel
    3.12 libpng
    3.13 libpng-devel
    3.14 glibc
    3.15 glibc-devel
    3.16 glib2
    3.17 glib2-devel
    3.18 python-pip
    3.19 python-devel
