# `PREDS` Directory                        
-
### Author: Rob Lyon
### Email : robert.lyon@manchester.ac.uk
### web   : www.scienceguyrob.com
-

This directory contains `Tempo2 predictor files, one for each valid source in the ATNF pulsar catalog (version 1.54)

To create the predictor files, the following tempo2 command was used:

`tempo2 -f <path to pulsar par> -pred "@ 56000 56001 1350 1670 12 2 600"`

Note it is probably advisable to replace the "@" symbol with a real telescope name, e.g. PKS, MEERKAT, SKA etc if building predictors for yourself. Also note these predictor files will likely be unsuitbale for binary pulsars - you're best generating these by yourself - either via manually running `Tempo2` or by running the `GeneratePredictorFiles.p` script, providing it with an acceleration value/parameters.