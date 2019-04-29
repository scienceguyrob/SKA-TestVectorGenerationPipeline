**************************************************************************
|                                                                        |
|  Test Vector Inject Pulsar Pipeline (version 2.0)                      |
|                                                                        |
**************************************************************************
| Author: Rob Lyon                                                       |
| Email : robert.lyon@manchester.ac.uk                                   |
| web   : www.scienceguyrob.com                                          |
**************************************************************************

Note that all the source files described below can be found in the src folder.

1. The first step involves the creation of a filter bank file output by
   fast_fake, which we call ‘noise.fil’. This file contains only Gaussian
   white noise. This single noise file serves as the basis for all the
   steps that follow in test vector creation. To create the noise file
   using fast_fake, we use the following parameters:

    Observation length: 536.870912 seconds
    Sampling interval: 64 microseconds
    Frequency of channel 1: 1350 MHz
    Channel bandwidth: 78.12500 KHz (0.078125 MHz which gives 320 MHz bandwidth overall)
    Number of channels: 4096
    Output number of bits: 8
    Random seed: 1
    Total samples: 2^23 (8,388,608)
    Header size (approx) : 1kb
    File size: 34,359,738,368 bytes (~34 GB)

    fast_fake --tobs 600 --tsamp 64 --fch1 1350 --foff -0.078125 --nbits 8 --nchans 4096 --seed 1 > output.fil

2. To insert a signal into the noise filter bank file, the inject_pulsar
   tool is used. The inject_pulsar tool requires two prerequisite files
   which describe the pulsar signal to be injected into the noise file.
   The first is a tempo2 predictor file (a Par file which uses the .dat
   extension). The second an ascii file that describes the shape of the
   signal to be injected (.asc file). These files have already been created
   to assist with test vector creation. Par files have been generated for all
   pulsars in the ATNF catalog. These can be found in the 'PARS' folder.
   Files describing pulse shapes have also been extracted for all pulsar
   entries in the EPN database. These can be found in the 'ASC' folder.
   Thus with these two sets of files, many pulsar test vectors can be created.

3. To inject a specific pulsar signal, the following command is used:

    inject_pulsar --snr <SNR> --seed 1 --pred <Par file> --prof <profile file> noise.fil > output.fil

   This will create a noise file with the pulsar signal described in the Par
   and profile files, at the user specified S/N. There are other options
   available:

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

   For the creation of test vectors for real pulsars, we use only the inject_pulsar
   defaults. The exception is the seed value, which we set to 1. If these steps are
   copied, then the same real pulsar test vectors can be independently generated,
   assuming the same Par and Asc files are used.

4. Scripts have been written to automate the creation of test vectors following the
   recipe above.

5. Versions of pulsar software used:
    - Tempo2 version 2014.11.1
    - fast_fake version updated on 29th October 2014, commit 41d05788720577994848c8209b02c7bef02d7ece (see https://github.com/SixByNine/sigproc/blob/master/src/fast_fake.c).
    - inject_pulsar version updated on November 19th 2014, commit 94bb492ddea59ff1d8ef34f06e4f642afd06c4a9 (see https://github.com/SixByNine/sigproc/blob/master/src/inject_pulsar.c)

Format: Filterbank files generated using fast_fake.