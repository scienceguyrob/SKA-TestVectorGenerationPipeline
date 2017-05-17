**************************************************************************
|                                                                        |
|  Test vector machine Docker Image (version 1.1)                        |
|                                                                        |
**************************************************************************
| Author: Rob Lyon                                                       |
| Email : robert.lyon@manchester.ac.uk                                   |
| web   : www.scienceguyrob.com                                          |
**************************************************************************

This image sets up an environment with only a basic pulsar stack. This
is because the image is to be used for test vector generation, for tests
of SKA SDP and CSP software. For a more complete pulsar image, look at the
Dockerfile's written by Casey Law, or Maciej Serylak.

Image update based on feedback from Sally Cooper (thanks Sal!). Sally
found issues with how Mike's version of Sigproc produces file headers
(filterbank file headers), and with how the software created fake files.
Both issues should be fixed in this build.

Please note that it takes around 1 hour to build the entire image on the
dockerhub. Also note that the image size is approximately 2.5 GB on disk.

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
15. glibc           2.17
16. glibc-devel     2.17

PYTHON MODULES (Python 2.7):

1. numpy
2. scipy
3. fitsio
4. astropy
5. astroplan
6. pyfits
7. matplotlib
8. pyephem

PULSAR SOFTWARE:

Latest versions of the pulsar software were obtained on December 8th 2016.

The software can be found in: /home/psr/soft

Software Package                Version                             Link
1. Tempo2                       2016.11.3 (SNAPSHOT 08 12 2016)     https://bitbucket.org/psrsoft/tempo2/downloads/tempo2-2016.11.3.tar.gz
                                Uploaded on 2016-12-05 by MKeith.

2. Sigproc (Mike Keith's build) Latest commit 55e94fa on 6th May    https://github.com/SixByNine/sigproc
                                2017 (Master branch)

3. Test vector generation code. Commit 91d8472                      https://github.com/scienceguyrob/Docker/blob/master/Resources/Deploy/pulsar_injection_pipeline.zip

4. Elmarie van Heerden's code that
   inserts non-stationary noise and
   RFI into filterbank files.

5. PRESTO                       Commit bd3c0181                     https://github.com/scottransom/presto

6. Tempo                        (Master branch) SNAPSHOT 08 12      https://sourceforge.net/p/tempo/tempo/ci/master/tree/
                                2016

OTHER SOFTWARE:

1. CUDA version 8.0
