**************************************************************************
|                                                                        |
|  PREDS_Readme.txt                                                      |
|                                                                        |
**************************************************************************
| Author: Rob Lyon                                                       |
| Email : robert.lyon@manchester.ac.uk                                   |
| web   : www.scienceguyrob.com                                          |
**************************************************************************

This directory contains tempo2 predictor files, and a python script used to
automate predictor file creation.

FakePulsar  -   This directory contains predictor files for fake pulsars.

Pulsar      -   This directory contains predictor files for real pulsars. The
                following tempo2 command was used:

                tempo2 -f <path to pulsar par> -pred "meerkat 56000 56001 1350 1670 12 2 600"

                Note it is probably advisable to replace the "@" symbol with a
                real telescope name.

                Note that Tempo2 version 2014.11.1 was used.

GeneratePredictorFiles.py   -   The python script used to auto generate predictor files.