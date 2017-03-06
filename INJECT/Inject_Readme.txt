**************************************************************************
|                                                                        |
|  Inject_Readme.txt                                                     |
|                                                                        |
**************************************************************************
| Author: Rob Lyon                                                       |
| Email : robert.lyon@manchester.ac.uk                                   |
| web   : www.scienceguyrob.com                                          |
**************************************************************************

This directory contains python files useful for automating the insertion
of fake pulsar signals into fast_fake generated filterbank files.

SUMMARY:

We would like to automate the generation of filterbank files containing
real pulsar signals. These filterbank files will then be used to test our
pulsar search pipelines and related software. However inserting a real
pulsar signal into a filterbank file, requires many files, and lots of
command line calls. It's relatively easy to get this wrong. So to make this
process easier, these scripts have been written to make the process entirely
reproducible.

There are two files summarised below. The first creates files containing
terminal commands, one per line. These terminal commands describe how to run
the inject_pulsar tool on a specified filterbank file. The inject_pulsar
application requires a few command line parameters to execute. These include:

    * A random seed.
    * The full path to the Tempo2 predictor file which describes the pulsar
        signal to be injected.
    * The full path to the '.asc' file, that describes the integrated profile
        of the pulsar to be injected.

If the InjectPulsarCommandCreator.py script is passed this information, it
will generate a valid command that will inject the pulsar when executed. The
InjectPulsarAutomator.py script then simply executes the inject_pulsar commands
stored in the 'command' file.


InjectPulsarCommandCreator.py   -   Creates files containing inject_pulsar
                                    command. These 'command' files are used
                                    by the InjectPulsarAutomator.py script
                                    to execute inject_pulsar.

InjectPulsarAutomator.py        -   Executes inject_pulsar, by reading in
                                    a file containing inject_pulsar commands.

ExecuteInjectPulsar.sh          -   An example script that shows how to execute
                                    InjectPulsarAutomator.py.
