# SKA-TestVectorGenerationPipeline (version 1.1)
A software pipeline used to generate SKA like pulsar observations, aka 'test vectors'. These are used to test CSP.PSS modules.

## Author: Rob Lyon
## Email : robert.lyon@manchester.ac.uk
## web   : www.scienceguyrob.com

### Overview
This repository consists of, 

* a Dockerfile that creates the software environment used for test vector generation.
* Data used to support the generation of test vectors.
* Python scripts which automate the generation of test vectors.

### Docker File
The docker file sets up a software environment with a basic pulsar stack. This image is designed to be used for test vector generation, i.e., the generation of gold standard test vectors used to test software written for the SKA (SDP and CSP software). The image is not intended to provide a useful pulsar software stack. For a more complete pulsar image, please look at the Dockerfile's written by Casey Law, or Maciej Serylak. These can be found on the docker hub.

Please note that it takes around 1 hour to build this image on the dockerhub. Also note that the image size is approximately 2.5 GB on disk. It is probably best to build locally on your own machine. The image can lso be found on the docker hub:

https://hub.docker.com/r/scienceguyrob/docker/

#### Docker Image Software

Image OS: CentOS 7
Image OS PACKAGES INSTALLED:

| Number |   Package | Version |
|--- | --- | ---|
|1. | tcsh | 6.18.01 |
|2. |  unzip | 6.0 |
|3. |  wget | 1.14 |
|4. |  make | 2.8.11 |
|5. |  autoconf | 2.69 |
|6. |  automake | 1.13.4 |
|7. |  gcc | 4.8.5 |
|8. |  gcc-gfortran | 4.8.5 |
|9. |  libtool | 2.4.2 |
|10.| gcc-c++ | 4.8.5 |
|12.| cfitsio | 3.370 |
|13.| cfitsio-devel | 3.370 |
|14.| fftw-devel | 3.3.3 |
|15.| glibc | 2.17 |
|16.| glibc-devel | 2.17 |

##### PYTHON MODULES (Python 2.7):

| Number | Package |
|--- | --- |
|1. | numpy |
|2. | scipy |
|3. | fitsio |
|4. | astropy |
|5. | astroplan |
|6. | pyfits |
|7. | matplotlib |
|8. | pyephem |

##### PULSAR SOFTWARE

Latest versions of the pulsar software were obtained on December 8th 2016.

The software can be found in: /home/psr/soft

| Number | Software Package | Version | Link |
| --- | --- | --- | --- |
|1. | Tempo2 | 2016.11.3 (SNAPSHOT 08 12 2016) Uploaded on 2016-12-05 by MKeith | [Link](https://bitbucket.org/psrsoft/tempo2/downloads/tempo2-2016.11.3.tar.gz) |
| 2. | Sigproc | (Mike Keith's build) Latest commit 668de78  on 25 Oct 2016 (Master branch) | [Link](https://github.com/SixByNine/sigproc)|
| 3. | Test vector generation code. | Commit 91d8472 | [Link](https://github.com/scienceguyrob/Docker/blob/master/Resources/Deploy/pulsar_injection_pipeline.zip) |
| 4. | Elmarie van Heerden's code that inserts non-stationary noise and RFI into filterbank files. |N/A |N/A |
| 5. | PRESTO | Commit bd3c0181 | [Link](https://github.com/scottransom/presto) |
| 6. | Tempo | (Master branch) SNAPSHOT 08 12 2016 | [Link](https://sourceforge.net/p/tempo/tempo/ci/master/tree/) |

### Data

The repository contains many files useful for test vector creation. These are summarised by directory.

**ASC** - This directory contains files which describe pulse profiles extracted from the EPN database. Each file in the directory is named as follows:

&lt;Pulsar name>_&lt;Frequency>.asc

Where &lt;Pulsar name> is the pulsar 'J' name, and &lt;Frequency> the observation frequency of the EPN data.

There is a single file per each unique entry in the EPN database, representing observations covering a wide range of frequencies. The files themselves are in comma separated value (CSV) format. They contain the total pulse intensity observed (the I stokes parameter) written to a single line of ascii text.

For example:

0,1,2,3,11,29,67,180,71,39,9,2,1,1,1,0

has 16 bins, each describing total pulse intensity.

Note:

The intensity values stored in the files are scaled a [0,255] range.

This directory also contains a python script, EpnToAsc.py, which converts EPN files saved from the EPN database, to .asc files which describe pulsar pulse profiles. In total there are 3698 asc files (~30 MB unzipped).

**EPN_Raw** - This directory contains 3000+ files extracted from the EPN database, that describe pulsar profiles in plain text files. The files are named as follows:

&lt;Pulsar name>_&lt;Freq.>.acn

or

&lt;Pulsar name>_&lt;Freq.>_&lt;Number>.acn

if there is more than one EPN file representing a pulsar observed at the specified frequency. These files are space delimited. More details about the files can be found at:

http://www.epta.eu.org/epndb/

The data in this directory were obtained from the EPN database under the Creative Commons Attribution 4.0 International licence. We gratefully acknowledge the authors of the EPN database (past and present), and those who have contributed data to it over the years.

Data was extracted from the EPN database on March 15th 2016. In total there are 3698 EPN files (~65 MB unzipped).

**PARS** - This directory contains par files for real pulsars. These par files were generated by the CandidateParGenerator.py script v1.0. To create these files, the script had to read a valid ATNF pulsar catalog database file. It extracts the RA, DEC, period, and DM values from this file per source, and then stores them in a valid par file. The pars were generated using pulsar catalog version 1.54. In total there are 2536 par files in the zip (~11 MB unzipped).

**PREDS** - This directory contains Tempo2 predictor (.dat) files. The files it contains correspond to real pulsars. These files were generated by Tempo2 version 2014.11.1, using the par files in the PARS.zip file. In total there are 2536 predictor files in the zip (~425 MB unzipped).

### Python Scripts

Scripts have been written to automate the creation of test vectors. These include:

- *CandidateParGenerator.py* (version 1.0) - this generates par files for ATNF catalog sources, and par files for fake pulsars created via sampling user specified distributions over pulse period, S/N, and DM. The script is compatible with python version 2.7. It requires scipy version 0.15 or later to function. Numpy 1.0 or later, and matplotlib version 1.5 or later are also required.
    
- *GeneratePredictorFiles.py* (version 1.0) - this automatically generates tempo2 (Tempo2 version 2014.11.1) predictor files for any par files found in a user supplied directory. The script is compatible with python version 2.7.  It requires Tempo2 version 2014.11.1, scipy version 0.15 or later to function. Numpy 1.0 or later, and matplotlib version 1.5 or later are also required.
    
- *InjectPulsarCommandCreator.py*  (version 1.0) - this generates a file containing inject_pulsar commands, useful for batching the creation of modified noise filterbank files. The script locates the correct .asc files for legitimate pulsars when creating the inject_pulsar commands. For fake pulsar par files (generated by CandidateParGenerator.py), the script will randomly choose an available .asc file, thereby creating a fake pulsar example using realistic profile data. It is possible to audit which .asc files were allocated to fake pulsars. The script is compatible with python version 2.7.  It requires scipy version 0.15 or later to function. Numpy 1.0 or later, and matplotlib version 1.5 or later are also required.
    
- *InjectPulsarAutomator.py* (version 1.0) - this script reads the files output by InjectPulsarCommandCreator.py (version 1.0), and executes the commands. The script is compatible with python version 2.7.  It requires scipy version 0.15 or later to function. Numpy 1.0 or later, and matplotlib version 1.5 or later are also required.

Versions of pulsar software assumed by these scripts:
    - *Tempo2* version 2014.11.1
    - *fast_fake* version updated on 6th May 2017, Latest commit 55e94fa (Master branch) (see https://github.com/SixByNine/sigproc/blob/master/src/fast_fake.c).
    - *inject_pulsar* version updated on 6th May 2017, Latest commit 55e94fa (Master branch) (see https://github.com/SixByNine/sigproc/blob/master/src/inject_pulsar.c)

### Change log

**Changes since version 1.0** - Image update based on feedback from Sally Cooper (thanks Sal!). Sally found issues with how Mike's version of Sigproc produces file headers (filterbank file headers), and with how the software created fake files. Both issues should be fixed in this build. This build contains a new build of fast_fake and inject_pulsar. No other differences with respect to version 1.0.