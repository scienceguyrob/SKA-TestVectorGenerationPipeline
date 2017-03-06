**************************************************************************
|                                                                        |
|  ATNF_Readme.txt                                                       |
|                                                                        |
**************************************************************************
| Author: Rob Lyon                                                       |
| Email : robert.lyon@manchester.ac.uk                                   |
| web   : www.scienceguyrob.com                                          |
**************************************************************************

This directory contains a copy of the ATNF pulsar catalog database file,
a parsed version of this file, and a script that does the parsing. The
files are:

psrcat.db           -   the pulsar catalog database file, version 1.54.

parsed_psrcat.txt   -   a parsed version of the pulsar catalog file, which
                        contains data in comma separated value (CSV) format.
                        Each line of the file describes an individual known
                        pulsar source. The format of the file is as follows
                        (two example entries shown, header included):

                        Name,RA,DEC,GL,GB,Period (s),Frequency (Hz),DM,W10 (ms),W50 (ms)
                        J0033+57,00:33,+57,120.41,-5.78145,0.315,3.1746031746,76,0,0
                        J0033+61,00:33,+61,120.698,-1.79175,0.912,1.09649122807,37,0,0
                        ...

                        This file can be used by the CandidateParGenerator.py script
                        to generate valid par files for known pulsar sources.

ATNFDataExtractor   -   A python file that extracts data from the psrcat.db
                        file, and outputs this data to a file in csv format.
                        The script only extracts the values of the variables
                        shown above.
