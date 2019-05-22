# SKA-TestVectorGenerationPipeline (version 2.0)
A software pipeline used to generate SKA like pulsar observations, aka 'test vectors'. These are used to test CSP.PSS modules.

[![DOI](https://zenodo.org/badge/84049113.svg)](https://zenodo.org/badge/latestdoi/84049113) [![Build Status](https://travis-ci.org/scienceguyrob/SKA-TestVectorGenerationPipeline.svg?branch=master)](https://travis-ci.org/scienceguyrob/SKA-TestVectorGenerationPipeline)

## Author: Rob Lyon
## Email : robert.lyon@manchester.ac.uk
## web   : www.scienceguyrob.com

### Overview
This repository consists of, 

* a Dockerfile that creates the software environment used for test vector generation.
* Data used to support the generation of test vectors.
* Python scripts which automate the generation of test vectors.

Note that during the recent [Astron Hackathon](http://astron.nl/hackathon/#), improvements were made to the pipeline and it's containerisation. Big thanks to Yan Grange, Sophie Ashcroft, Liam Conner, Wietze Albers, Anne Archibald, and Amruta Jaodand for contributing! These changes will be fully implemented and the repository updated soon.

Big thanks to Sally Cooper and Lars Kunkel for providing some [bug fixes e.g.](https://github.com/larskuenkel/SKA-TestVectorGenerationPipeline), and testing out the pipeline in the wild. 
### Docker File
The docker file sets up a software environment with a basic pulsar stack. This image is designed to be used for test vector generation, i.e., the generation of gold standard test vectors used to test software written for the SKA (SDP and CSP software). The image is not intended to provide a useful pulsar software stack. For a more complete pulsar image, please look at the Dockerfile's written by Casey Law, or Maciej Serylak. These can be found on the docker hub.

Please note that it takes around 1 hour to build this image on the dockerhub. Also note that the image size is approximately 1 GB on disk. It is probably best to build locally on your own machine. The image can lso be found on the docker hub:

https://hub.docker.com/r/scienceguyrob/ska-test-vectors/

This image sets up an environment with a basic pulsar stack. This
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
|6. PSRCHIVE*                       |(Master branch) SNAPSHOT 30/04/2019      | [Link](http://psrchive.sourceforge.net/download.shtml)|

* Indicates this software cannot currently be provided due to build issues (as of 02/05/2019).

### `fast_fake` Modification
The version of `fast_fake` provided in Mke Meith's build of `sigproc`, has been modified to prevent an incompatibility issue between `fast_fake` outputs, and `PRESTO`. The only difference between the modified version, and the code in `Sigproc_MJK_SNAPSHOT_08_12_2016.zip`, is as follows.

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

###  Python Scripts

There are 4 scripts that can be directly executed. These are described in detail in their respective python files. We summarise here.

#### Gaussian Profile Generator Version 1.0 (GaussianProfileGen.py)

Generates simple Gaussian or double Gaussian pulse profiles, and writes them out to `.asc` files compatible with the `inject_pulsar` tool. Pulse profile length can be varied, as can the numerical range for pulse intensity values.                                              
                                                                     
The `.asc` files produced by this script will:                         
                                                                     
1. contain pulse intensity values in ascii format. Each line in the file corresponds to a phase bin value. For example,               
                                                                     
   1.0                                                               
   2.0                                                               
   3.0                                                               
   2.0                                                               
   1.0                                                               
                                                                     
   Contains 5 bins, with a max value of 3.0, and min of 1.0.         
                                                                     
2. Have a file name that adheres to the format,                      
                                                                     
  `<ID>_DC=<Duty Cycle>_BINS=<Bins>_FWHM=<FWHM>.asc`                   
                                                                     
  where `<ID>` is a string that uniquely identifies the `.asc` file,     
  `<Duty Cycle>` is a float describing the fraction of the period that the pulse is "on" for, `<Bins>` is an integer describing the number of phase bins in the profile, and `<FWHM>` is a float corresponding to the full-width at half maximum (FWHM). A valid filename could be as follows:                                                           
                                                                     
      `Gaussian_DC=0.5_BINS=128_FWHM=64.asc`

--
      
#### Generate Tempo 2 predictor Files Version 2.0 (GeneratePredictorFiles.py)    

Generates Tempo2 predictor files, for all `.par` files in a user specified directory. The predictor files are stored in a user defined output directory. This script will ONLY run on the `.par` files output by the `CreateFakeParFiles.py` python script. These
have a specific file name format which this script expects. You are free to create your own `.par` files manually for use with this script, though these must adhere to the file name format described in the pre-requisites section below.                
                                                                                   
Note: this script will overwrite existing predictor files during the generation   
process.                                                                           
                                                                                   
                                                                                   
Predictor files generated by this script will adhere to the file name format:      
                                                                                   
`<ID>_DM=<DM>_P0=<P0>ms_OBS=<Obs>s_F1=<F1>_F2=<F2>_T=<TC>_F=<FC>_Z=<Accel>.dat`      
                                                                                   
where `<ID>` is a string that uniquely identifies the `.dat` file, `<DM>` is a float representing the dispersion measure, `<PO>` is a float representing the period in milliseconds, `<Obs>` is an integer representing the observation length in seconds, `<F1>` and `<F2>` are floats representing the frequency in MHz of the first and the last channel respectively, `<TC>` is an integer corresponding to the number of time coefficients used in `Tempo2`, whilst `<FC>` is similarly defined but for the frequency coefficients, and finally `<Accel>` is a float that describes the          
acceleration in m/s/s.                                                             
                                                                                   

##### Pre-requisites                                                                    
                                                                                   
1. The user has must have generated `Tempo2` compatible `.par` files using the script `CreateFakeParFiles.py` to create valid `.par` files. The `.par` files should adhere to the following filename format:                                               
                                                                                   
   `FakePulsar<Number>_DM=<DM>_P0=<P0>ms_Z=<Accel>.par`                              
                                                                                   
   Where `<Number>` is an integer that helps identify the par file, `<DM>` is a float representing the dispersion measure, `<PO>` is a float representing the period in milliseconds, and `<Accel>` is a float that describes the acceleration in m/s/s.  
                                                                                   
2. Valid `.par` files that adhere to the naming standards mentioned above, are stored in a directory whose path is provided by the user at runtime.
                    
--

#### Inject Pulsar Automator Version 2.0 (InjectPulsarAutomator.py)

Automates execution of the `inject_pulsar` C++ software module, found in Mike Keith's version of [`sigproc`](https://github.com/SixByNine/sigproc). This script uses the Python subprocess library to execute `inject_pulsar`. The input parameters required 
by `inject_pulsar` are obtained from a "Command File" that must be given to this script. A command file is a simple ascii file that contains `inject_pulsar` commands followed by a destination path. The destination path tells this script where to move `inject_pulsar's` outputs to. The format of the command file is as follows:  
  
```                                                                                  
<inject_pulsar command 1>                                                         
<Destination file name 1>                                                         
<inject_pulsar command 2>                                                         
<Destination file name 2>                                                         
<inject_pulsar command 3>                                                         
<Destination file name 3>                                                         
...                                                                               
<inject_pulsar command n>                                                         
<Destination file name n>                                                         
```                                                                              
For example,

```                                                                      
inject_pulsar --snr 35.0 --pred Fake1.dat --prof Fake1.asc Noise.fil > out.fil    
Desired_output1.fil                                                               
inject_pulsar --snr 35.0 --pred Fake2.dat --prof Fake2.asc Noise.fil > out.fil    
Desired_output2.fil                                                               
inject_pulsar --snr 35.0 --pred Fake3.dat --prof Fake3.asc Noise.fil > out.fil    
Desired_output3.fil                                                               
...
```                                                                               
                                                                                  
Here the destinations are not full paths, but file names only.                    
                                                                                  
Please note the file names used in this example are not valid according to our file name standards developed elsewhere.

--

#### Inject Pulsar Command Creator Version 2.0 (InjectPulsarCommandCreator.py)

Creates a "command" file that can be used to automate use of the `inject_pulsar` tool. `inject_pulsar` is a C++ software module found in Mike Keith's version of [`sigproc`](https://github.com/SixByNine/sigproc). The command file made here is eventually used by the script InjectPulsarAutomator.py. NOTE: this script will overwrite an existing command file if given the same parameters.                            
                                                                               
Command files produced by this script have a simple file name:                 
                                                                               
`InjectPulsarCommandFile_<Batch>.txt`                                            
                                                                               
Where `<Batch>` is a user supplied parameter (with a default value of 1).        
                                                                               
A command file is a simple ascii file that contains `inject_pulsar` commands followed by a destination path. The command can be directly executed by the script `InjectPulsarAutomator.py` using the Python subprocess library. While the destination path tells `InjectPulsarAutomator.py` where to move `inject_pulsar`'s outputs to. The format of the command file is as follows:                                      

```                                                                               
<inject_pulsar command 1>                                                      
<Destination file name 1>                                                      
<inject_pulsar command 2>                                                      
<Destination file name 2>                                                      
<inject_pulsar command 3>                                                      
<Destination file name 3>                                                      
...                                                                            
<inject_pulsar command n>                                                      
<Destination file name n> 
```                                                     
                                                                               
For example,  
```                                                                 
inject_pulsar --snr 35.0 --pred Fake1.dat --prof Fake1.asc Noise.fil > out.fil 
Desired_output1.fil                                                            
inject_pulsar --snr 35.0 --pred Fake2.dat --prof Fake2.asc Noise.fil > out.fil 
Desired_output2.fil                                                            
inject_pulsar --snr 35.0 --pred Fake3.dat --prof Fake3.asc Noise.fil > out.fil 
Desired_output3.fil                                                            
...
```                                                                        
                                                                               
Here the destinations are not full paths, but file names only.                 
                                                                               
Please note the file names used in this example are not valid according to our file name standards developed as part of this work - more details on those standards below in the "Pre-requisites" section.                               
                                                                               
To generate a command, we need to know the full paths to the files that `inject_pulsar` requires to execute correctly. These pre-requisite files include a `.asc` file that describes the shape of the pulse to be injected, a `.dat` file that describes pulse arrival times, and a `.fil` (filterbank) file into which the signal will be injected.                                                              
                                                                               
Rather than pass these files in one by one, this script generates commands when given the full path to directories containing all the pre-requisite files. This means the user must provide two directory paths ( `.asc` and `.dat` directories respectively), plus a `.fil` file path.                                          
                                                                               
##### Pre-requisites                                                               
                                                                               
`inject_pulsar` is a C++ software module compiled as part of Mike Keith's version of `Sigproc`. It is used to inject pulsar signals into valid filterbank files, however to do this, it needs multiple prerequisites. These include a `.asc file` that describes the pulse to inject, a `Tempo2` predictor file (`.dat` extension) that describes pulse arrival times, and a valid noise filterbank (`.fil`) file.       
                                                                               
To proceed, this script makes a number of assumptions regarding the prerequisites:
                                                                               
1. The user has generated pulse profile files (`.asc`) using the script `GaussianProfileGen.py`, or some other tool that produces output files which, 
   * contain pulse intensity values in ascii format, i.e. each line in the file corresponds to a phase bin value.                                        
   * Have a file name that adheres to the format,                             
                                                                               
      `<ID>_DC=<Duty Cycle>_BINS=<Bins>_FWHM=<FWHM>.asc`                         
                                                                               
      where `<ID>` is a string that uniquely identifies the `.asc` file, `<Duty Cycle>` is a float describing the fraction of the period that the pulse is "on" for, `<Bins>` is an integer describing the number of phase bins in the profile, and `<FWHM>` is a float corresponding to the full-width at half maximum (FWHM). A valid filename could be as follows:                                      
                                                                               
      `Gaussian_DC=0.5_BINS=128_FWHM=64.asc`                                     
                                                                               
2. The user has generated `Tempo2` predictor files by firstly using the script `CreateFakeParFiles.py` to create valid `.par` files, and then passing these files as inputs to `GeneratePredictorFiles.py`, to create the valid `.dat` `Tempo2` predictor files. The `.par` files should adhere to the following filename format:
                                                                               
   `FakePulsar<Number>_DM=<DM>_P0=<P0>ms_Z=<Accel>.par`                          
                                                                               
   Where `<Number>` is an integer that helps identify the par file, `<DM>` is a float representing the dispersion measure, `<PO>` is a float representing the period in milliseconds, and `<Accel>` is a float that describes the acceleration in m/s/s.
                                                                               
   while the `.dat` files should adhere to the format:                           
                                                                               
   `<ID>_DM=<DM>_P0=<P0>ms_OBS=<Obs>s_F1=<F1>_F2=<F2>_T=<TC>_F=<FC>_Z=<Accel>.dat`
                                                                               
   where `<ID>` is a string that uniquely identifies the `.dat` file, `<DM>` is a float representing the dispersion measure, `<PO>` is a float representing the period in milliseconds, `<Obs>` is an integer representing the observation length in seconds, `<F1>` and `<F2>` are floats representing the frequency in MHz of the first and the last channel respectively, `<TC>` is an integer corresponding to the number of time coefficients used in Tempo2, whilst `<FC>` is similarly defined but for the frequency coefficients, and finally `<Accel>` is a float that describes the acceleration in m/s/s.                                                      
                                                                               
                                                                               
3. Valid `.asc` and `.dat` files that adhere to the naming standards mentioned above, are stored in directories whose paths are provided by the user at runtime. 
                                                                               
4. The user provides the full path to a valid `.fil`, filterbank file.  
      
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

The intensity values stored in the files are scaled to a [0,255] range.

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


### Pipeline Use

**Step 1.** The first step involves the creation of a filter bank file output by `fast_fake`, which we call `‘noise.fil’`. This file contains only Gaussian white noise. This single noise file serves as the basis for all the steps that follow in test vector creation. To create the noise file using `fast_fake`, we use the following parameters:

|Parameter         | Value             |
|------------------|-------------------|
|Observation length| 536.870912 seconds|
|Sampling interval| 64 microseconds|
|Frequency of channel 1| 1350 MHz|
|Channel bandwidth| 78.12500 KHz (0.078125 MHz which gives 320 MHz bandwidth overall)|
|Number of channels| 4096|
|Output number of bits| 8|
|Random seed| 1|
|Total samples| 2^23 (8,388,608)|
|Header size (approx) | 1kb|
|File size| 34,359,738,368 bytes (~34 GB)|

We can pass these parameter in as follows:

```fast_fake --tobs 600 --tsamp 64 --fch1 1350 --foff -0.078125 --nbits 8 --nchans 4096 --seed 1 > output.fil```

**Step 2.** To insert a signal into the noise filterbank file, the `inject_pulsar`tool is used. The `inject_pulsar` tool requires two prerequisite files which describe the pulsar signal to be injected into the noise file. The first is a `tempo2` predictor file (a Par file which uses the `.dat`extension). The second an ascii file that describes the shape of the signal to be injected (`.asc file`). These files have already been created to assist with test vector creation. Par files have been generated for all pulsars in the ATNF catalog. These can be found in the `'PARS'` folder. Files describing pulse shapes have also been extracted for all pulsar entries in the EPN database. These can be found in the `'ASC'` folder. Thus with these two sets of files, many pulsar test vectors can be created.

**Step 3.** To inject a specific pulsar signal, the following command is used:

```inject_pulsar --snr <SNR> --seed 1 --pred <Par file> --prof <profile file> noise.fil > output.fil```

This will create a noise file with the pulsar signal described in the Par and profile files, at the user specified S/N. There are other options available:

```
    --snr,-s            Target signal-to-noise ratio (phase average S/N). (def=15)
    --subprof,-b        Profile for sub-profile structure. Same format as prof.asc
    --nsub,-n           Number of sub-pulses per profile, over full pulse phase (def=5).
    --sidx,-i           Spectral index of pulsar. (def=-1.5)
    --scatter-time,-c   Scattering timescale at ref freq, s. (def=no scattering).
    --scint-bw,-C       Scintilation bandwidth, MHz. Cannot use in conjunction with -c
    --scatter-index,-X  Index of scattering. (def=4.0).
    --freq,-f           Reference frequency for scattering/spectral index, MHz. (def=1500)
    --pulse-sigma,-E    'sigma' for log-normal pulse intensity distribution. (def=0.2)
    --seed,-S           Random seed for simulation. (def=time())

```
   For the creation of test vectors for real pulsars, we use only the `inject_pulsar` defaults. The exception is the seed value, which we set to 1. If these steps are copied, then the same real pulsar test vectors can be independently generated, assuming the same `.par` and `.asc` files are used.