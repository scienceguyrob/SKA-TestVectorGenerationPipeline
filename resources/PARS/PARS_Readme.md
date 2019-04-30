# `PARS` Directory                        
-
### Author: Rob Lyon
### Email : robert.lyon@manchester.ac.uk
### web   : www.scienceguyrob.com
-

This directory contains one sub-directories, `Pulsar`. This contains `Tempo2` `.par` parameter files. There is one file for each valid source in the ATNF catalog (version 1.54). The par files were created by the `CandidateParGenerator.py` script.

To create these files, the script had to read a valid ATNF pulsar catalog database file. The `CandidateParGenerator.py` script then extracts the RA, DEC, period, and DM values for each catalog source, and stores them in a valid par file.