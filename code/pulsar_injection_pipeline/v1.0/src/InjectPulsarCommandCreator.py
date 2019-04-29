## @package Inject
# A module used to automate the execution of inject_pulsar
#
# Author: Rob Lyon
# Email : robert.lyon@manchester.ac.uk
# web   : www.scienceguyrob.com

# Start normal non-doxygen docstring...
"""
    **************************************************************************
    |                                                                        |
    |              Inject Pulsar Command Creator Version 1.0                 |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Creates files containing run commands, useful for automating the use   |
    | of inject_pulsar.                                                      |
    |                                                                        |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@manchester.ac.uk                                   |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | Required Command Line Arguments:                                       |
    |                                                                        |
    | --asc (string)   full path to the directory containing files which     |
    |                  describe an individual pulsars pulse profile in plain |
    |                  ascii text (use the script EpnToAcs.py to get the     |
    |                  correctly formatted files).                           |
    |                                                                        |
    | --pred (string)  full path to the directory containing predictor files.|
    |                                                                        |
    | --out (string)   full path to the output directory where the command   |
    |                  files will be stored.                                 |
    |                                                                        |
    | --noise (string) full path to the noise filterbank file.               |
    |                                                                        |
    **************************************************************************
    | Optional Command Line Arguments:                                       |
    |                                                                        |
    | -v (boolean) verbose debugging flag.                                   |
    |                                                                        |
    | --seed (int) the random seed (1 by default).                           |
    |                                                                        |
    | --buffer (int)   frequency buffer in MHz (default 100 Mhz).            |
    |                                                                        |
    | --batch (int)    the number of commands to include in a single command |
    |                  file (default is all).                                |
    |                                                                        |
    | -f (int)    frequency in MHz of EPN data to use. EPN data describing   |
    |             total pulse intensities at a the specified frequency +/-   |
    |             b MHz will be used (see --buffer flag). The frequency      |
    |             supplied determines what sort of profiles will be injected |
    |             into the noise file - the default value is 1400 MHz.       |
    |                                                                        |
    **************************************************************************
    | License:                                                               |
    |                                                                        |
    | Code made available under the GPLv3 (GNU General Public License), that |
    | allows you to copy, modify and redistribute the code as you see fit    |
    | (http://www.gnu.org/copyleft/gpl.html). Though a mention to the        |
    | original author using the citation above in derivative works, would be |
    | very much appreciated.                                                 |
    **************************************************************************
"""

# Command Line processing Imports:
from optparse import OptionParser

import os, sys

# Numpy Imports:
from numpy import random

# ******************************
#
# CLASS DEFINITION
#
# ******************************

## Inject Pulsar Command Creator Version 1.0
# Description:
#
# Creates files containing run commands, useful for automating the use
# of inject_pulsar.
#
# Author: Rob Lyon
# Email : robert.lyon@manchester.ac.uk
# web   : www.scienceguyrob.com
#
# Required Command Line Arguments:
#
# --asc (string)  full path to the directory containing files which
#                 describe an individual pulsars pulse profile in plain
#                 ascii text (use the script EpnToAcs.py to get the
#                 correctly formatted files).
#
# --pred (string)  full path to the directory containing predictor files.
#
# --out (string)   full path to the output directory where the command
#                 files will be stored.
#
# --noise (string) full path to the noise filterbank file.
#
#
# Optional Command Line Arguments:
#
# -v (boolean) verbose debugging flag.
#
# --seed (int) the random seed (1 by default).
#
# --buffer (int)   frequency buffer in MHz (default 100 Mhz).
#
# --batch (int)   the number of commands to include in a single command
#                 file (default is all).
#
# -f (int)   frequency in MHz of EPN data to use. EPN data describing
#            total pulse intensities at a the specified frequency +/-
#            b MHz will be used (see --buffer flag). The frequency
#            supplied determines what sort of profiles will be injected
#            into the noise file - the default value is 1400 MHz.
#
#
# License:
#
# Code made available under the GPLv3 (GNU General Public License), that
# allows you to copy, modify and redistribute the code as you see fit
# (http://www.gnu.org/copyleft/gpl.html). Though a mention to the
# original author using the citation above in derivative works, would be
# very much appreciated.
class InjectPulsarCommandCreator:
    """
    Creates files containing run commands, useful for automating the use
    of inject_pulsar.
    """

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    ## The main method for the class.
    # Main entry point for the Application. Processes command line
    # input and begins automating the creation of inject_pulsar command
    # files.
    #
    #  @param self The object pointer.
    #  @param argv The unused arguments.
    def main(self,argv=None):
        """Main method.

        Main entry point for the Application. Processes command line
        input and begins automating the the creation of inject_pulsar command
        files

        Parameters
        ----------
        self : object
            The object pointer.
        argv : str
            The unused arguments.

        """

        # ****************************************
        #         Execution information
        # ****************************************

        print(__doc__)

        # ****************************************
        #    Command line argument processing
        # ****************************************

        # Python 2.4 argument processing.
        parser = OptionParser()

        # REQUIRED ARGUMENTS
        parser.add_option("--asc", action="store", dest="ascDir",
                          help='Path to a directory containing asc files.', default="")

        parser.add_option("--out", action="store", dest="outputDir",
                          help='Path to an output directory.', default="")

        parser.add_option("--pred", action="store", dest="predDir",
                          help='Path to the directory to store the predictor files.', default="")

        parser.add_option("--noise", action="store", dest="filFilePath",
                          help='Path to a filterbank file.', default="")

        parser.add_option("-f", type="int", dest="frequency",
                          help='The target frequency of EPN files to use.', default=1400)

        # OPTIONAL ARGUMENTS
        parser.add_option("-v", action="store_true", dest="verbose",
                          help='Verbose debugging flag (optional).', default=False)

        parser.add_option("--seed", type="int", dest="seed",
                          help='The seed value for random number generation (optional).', default=1)

        parser.add_option("--buffer", type="int", dest="buffer",
                          help='The target frequency buffer.', default=100)

        parser.add_option("--batch", type="int", dest="batch",
                          help='The target frequency buffer.', default=100000000000)

        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        self.verbose     = args.verbose
        self.ascDir      = args.ascDir
        self.predDir     = args.predDir
        self.filFilePath = args.filFilePath
        self.frequency   = args.frequency
        self.buffer      = args.buffer
        self.outputDir   = args.outputDir
        self.batch       = args.batch
        predExt = ".dat"
        ascExt  = ".asc"
        self.extensions  = [predExt, ascExt]
        self.commandFilePrefix = "InjectPulsarCommands_"
        self.seed        = args.seed

        # Stores the commands used to inject data into a noise fil file.
        self.injectCommands = []

        # ****************************************
        #   Print command line arguments & Run
        # ****************************************

        print("\n\t**************************")
        print("\t| Command Line Arguments |")
        print("\t**************************")
        print("\tDebug: "                         + str(self.verbose))
        print("\tAsc directory path: "            + str(self.ascDir))
        print("\tPredictor file directory path: " + str(self.predDir))
        print("\tFilterbank file path: "          + str(self.filFilePath))
        print("\tFrequency range: "               + str(self.frequency) + " ( +/- " + str(self.buffer) + " )")
        print("\tOutput directory: "              + str(self.outputDir))
        print("\tCommand batch size: "            + str(self.batch))
        print("\tRandom seed: "                   + str(self.seed))
        print("\n\tChecking user supplied parameters...")

        # First check user has supplied a asc directory path ...
        if not self.ascDir:
            print("\n\tYou must supply a valid par file directory via the --par flag.")
            sys.exit()

        # Now check user has supplied a predictor file output directory path ...
        if not self.predDir:
            print("\n\tYou must supply a valid predictor file directory via the --pred flag.")
            sys.exit()

        # Check the filterbank file containing noise exists...
        if os.path.exists(self.filFilePath) is False:
            print("\n\tYou must supply a valid filterbank file via the --noise flag.")
            sys.exit()

        # Now the user may have supplied an output directory path, but it may
        # not be valid. So first, try to create the directory, if it doesn't
        # already exist. If the create fails, the directory path must be invalid,
        # so exit the application.
        if os.path.exists(self.outputDir) is False:
            try:
                os.makedirs(self.outputDir)
            except OSError as exception:
                print("\n\tException encountered trying to create output file directory - Exiting!")
                sys.exit()

        # If the directory creation call above did not fail, the output directory
        # should now exist. Check that this is the case...
        if os.path.isdir(self.outputDir) is False:
            print("\n\tOutput file directory invalid - Exiting!")
            sys.exit()

        # Check the buffer value supplied by the user...
        if self.seed < 0:
            print("\n\tSupplied seed value invalid - Exiting!")
            print("\tExiting...")
            sys.exit()

        # Check the frequency value supplied by the user...
        if self.frequency < 0:
            print("\n\tSupplied frequency value invalid - Exiting!")
            sys.exit()

        # Check the buffer value supplied by the user...
        if self.buffer < 0:
            print("\n\tSupplied buffer value invalid - Exiting!")
            sys.exit()

        if self.batch < 0:
            print("\n\tSupplied batch value invalid - Exiting!")
            sys.exit()

        # Now seed random number generator
        random.seed(seed=self.seed)

        print("\tFinished checking supplied parameters...")

        # ****************************************
        #
        #
        #
        #         File parsing section
        #
        #
        #
        # ****************************************

        print("\n\n\t*****************************")
        print("\t| Parsing input directories |")
        print("\t*****************************")

        # ****************************************
        #          Parse ASC files
        # ****************************************

        # This part of the code tries to find asc files in the directory
        # specified by the user, then attempts to use those file paths to create
        # an inject command.
        #
        print("\tLooking for asc files...")

        ascPaths       = {}
        ascFilesProcessed = 0

        frequencyLowerBound = self.frequency - self.buffer
        frequencyUpperBound = self.frequency + self.buffer

        # Loop through the specified directory
        for root, subFolders, filenames in os.walk(self.ascDir):
            # for each file
            for filename in filenames:
                path = os.path.join(root, filename)  # Gets full path to the candidate.
                # for each valid file extension
                for ext in self.extensions:
                    # If the file is a predictor file...
                    if ext in path and ascExt in ext:

                        ascFilesProcessed += 1
                        # Split file name to get useful information - this is possible
                        # as the file name should be <pulsar name>_<frequency>.pred
                        components = filename.replace(ext, "").split("_")

                        pulsarName = components[0]
                        freq       = float(components[1])

                        # Debugging
                        if self.verbose:
                            print("\t\tPulsar: " + str(pulsarName) + "\tFreq: "  + str(freq) +
                                  "\tFile: "  + str(filename))

                        if freq >= frequencyLowerBound and freq <= frequencyUpperBound:
                            if self.verbose:
                                print("\t\t\tPulsar: " + str(pulsarName) + " in the correct frequency range")
                            # Inject pulsar if in desired frequency range
                            ascPaths[pulsarName] = path

        print("\tASC files processed: " + str(ascFilesProcessed))
        print("\tASC files meeting frequency criteria: " + str(len(ascPaths)))

        # ****************************************
        #          Parse Predictor files
        # ****************************************

        # This part of the code tries to find predictor files in the directory
        # specified by the user, then attempts to use those file paths to create
        # an inject command.
        #
        print("\n\tLooking for Predictor files...")

        pulsarPredPaths = {}
        fakePulsarPredPaths = {}

        # Loop through the specified directory
        for root, subFolders, filenames in os.walk(self.predDir):
            # for each file
            for filename in filenames:
                path = os.path.join(root, filename)  # Gets full path to the candidate.
                # for each valid file extension
                for ext in self.extensions:
                    # If the file is a predictor file...
                    if ext in path and predExt in ext:

                        name = filename.replace(ext, "")

                        if "FakePulsar" in name:
                            fakePulsarPredPaths[name] = path
                        else:
                            pulsarPredPaths[name] = path

        print("\tPredictor files found: " + str(len(pulsarPredPaths) + len(fakePulsarPredPaths)))

        # ****************************************
        #
        #
        #
        #         Inject command creation
        #
        #
        #
        # ****************************************

        print("\n\n\t*****************************")
        print("\t|  Creating inject commands |")
        print("\t*****************************")

        print("\tCreating inject_pulsar commands...")
        commandCount = 0
        commandBatchCount = 1

        commandFilePath = self.outputDir + "/" + self.commandFilePrefix + str(commandBatchCount) + ".txt"

        # Clear file to make sure we are not adding to previous entries.
        self.clearFile(commandFilePath)

        # FIRST we process the predictor files belonging to real pulsars.
        # For each asc file...
        for key, value in ascPaths.iteritems():
            # Get the predictor file path if it exists...
            predictor = pulsarPredPaths.get(key)

            # If a key value pair does not exist, usually due to peculiarities of the
            # EPN data file names...
            if predictor is None:
                continue

            if self.verbose:
                print("\tkey: " + str(key) + " value: " + str(value) + " Predictor: " + str(predictor))

            # inject_pulsar inputs:
            #
            # INPUTS:
            #     t2pred.dat - A tempo2 predictor file (generate with tempo2 -f x.par -pred ...
            #     prof.asc   - Pulse profile in single-column text format. 2^n bins is best
            #     file.fil   - Input filterbank file. Can be a real file, or from fast_fake
            #
            # OPTIONS:
            #     --help, -h          This help text
            #     --snr,-s            Target signal-to-noise ratio (phase average S/N). (def=15)
            #     --subprof,-b        Profile for sub-profile structure. Same format as prof.asc
            #     --nsub,-n           Number of sub-pulses per profile, over full pulse phase (def=5).
            #     --sidx,-i           Spectral index of pulsar. (def=-1.5)
            #     --scatter-time,-c   Scattering timescale at ref freq, s. (def=no scattering).
            #     --scint-bw,-C       Scintilation bandwidth, MHz. Cannot use in conjunction with -c
            #     --scatter-index,-X  Index of scattering. (def=4.0).
            #     --freq,-f           Reference frequency for scattering/spectral index, MHz. (def=1500)
            #     --pulse-sigma,-E    'sigma' for log-normal pulse intensity distribution. (def=0.2)
            #     --seed,-S           Random seed for simulation. (def=time())
            #
            # Example of how inject_pulsar executes...
            # inject_pulsar --pred t2pred.dat --prof prof.asc file.fil > output.fil
            command = "inject_pulsar --snr 15 --seed " + str(self.seed) + " --pred " + predictor +\
                      " --prof " + value + " " + self.filFilePath + " > output.fil"

            if self.verbose:
                print("\tCommand " + str(command) + " : "  + str(command))

            # Write the command to the output file.
            commandCount += 1

            if commandCount % self.batch == 0:
                # Write last command to the current file
                self.appendToFile(commandFilePath, command+"\n")

                # Increment batch counter, since we are now creating a new command file
                commandBatchCount += 1

                # Create the new command file path
                commandFilePath = self.outputDir + "/" + self.commandFilePrefix + str(commandBatchCount) + ".txt"

                # Clear file to make sure we are not adding to previous entries.
                self.clearFile(commandFilePath)

            # Write the command to the current batch output file
            self.appendToFile(commandFilePath, command+"\n")

        # NEXT we process the fake pulsar predictor files, which must use the asc files
        # of existing pulsars. We just simply randomly choose profiles to do this.

        # Get the keys in the asc path dictionary
        ascKeys = list(ascPaths.keys())

        for key, value in fakePulsarPredPaths.iteritems():

            # choose a random asc file key
            random_index = random.randint(0, len(ascKeys))
            asc = ascPaths.get(ascKeys[random_index])

            # If a key value pair does not exist, usually due to peculiarities of the
            # EPN data file names...
            if asc is None:
                continue

            if self.verbose:
                print("\tkey: " + str(key) + " value: " + str(value) + " ASC: " + str(asc))

            # For fake pulsars, we have a pre-computed target SNR. Here we extract it
            # from the name of the fakse pulsar, which is in a pre-determined format:
            #
            # FakePulsar_<number>_<period>_<DM>_<SNR>
            #
            # For example...
            # FakePulsar_972_3.647749_8.3_9.0
            #
            # In both cases the SNR is the last component, so grab it.
            varComponents = key.split("_")
            SNR = varComponents[len(varComponents)-1]

            # inject_pulsar inputs:
            #
            # INPUTS:
            #     t2pred.dat - A tempo2 predictor file (generate with tempo2 -f x.par -pred ...
            #     prof.asc   - Pulse profile in single-column text format. 2^n bins is best
            #     file.fil   - Input filterbank file. Can be a real file, or from fast_fake
            #
            # OPTIONS:
            #     --help, -h          This help text
            #     --snr,-s            Target signal-to-noise ratio (phase average S/N). (def=15)
            #     --subprof,-b        Profile for sub-profile structure. Same format as prof.asc
            #     --nsub,-n           Number of sub-pulses per profile, over full pulse phase (def=5).
            #     --sidx,-i           Spectral index of pulsar. (def=-1.5)
            #     --scatter-time,-c   Scattering timescale at ref freq, s. (def=no scattering).
            #     --scint-bw,-C       Scintilation bandwidth, MHz. Cannot use in conjunction with -c
            #     --scatter-index,-X  Index of scattering. (def=4.0).
            #     --freq,-f           Reference frequency for scattering/spectral index, MHz. (def=1500)
            #     --pulse-sigma,-E    'sigma' for log-normal pulse intensity distribution. (def=0.2)
            #     --seed,-S           Random seed for simulation. (def=time())
            #
            # Example of how inject_pulsar executes...
            # inject_pulsar --pred t2pred.dat --prof prof.asc file.fil > output.fil
            command = "inject_pulsar --snr " + SNR + " --seed " + str(self.seed) + " --pred " + value +\
                      " --prof " + asc + " " + self.filFilePath + " > output.fil"

            if self.verbose:
                print("\tCommand " + str(command) + " : " + str(command))

            # Write the command to the output file.
            commandCount += 1

            if commandCount % self.batch == 0:
                # Write last command to the current file
                self.appendToFile(commandFilePath, command+"\n")

                # Increment batch counter, since we are now creating a new command file
                commandBatchCount += 1

                # Create the new command file path
                commandFilePath = self.outputDir + "/" + self.commandFilePrefix + str(commandBatchCount) + ".txt"

                # Clear file to make sure we are not adding to previous entries.
                self.clearFile(commandFilePath)

            # Write the command to the current batch output file
            self.appendToFile(commandFilePath, command+"\n")


        print("\n\tCommands created: " + str(commandCount))

        print("\n\tDone.\n")
        print("\n**************************************************************************\n")

    # ****************************************************************************************************

    ## Appends the provided text to the file at the specified path.
    #
    #  @param self The object pointer.
    #  @param path The full path to the file to write to.
    #  @param text The text to write to the output file.
    def appendToFile(self, path, text):
        """Appends the provided text to the file at the specified path.

        Parameters
        ----------
        self : object
            The object pointer.
        path : str
            The full path to the file to write to.
        text : str
            The text to write to the output file.

        Examples
        --------
        >>> appendToFile("/Users/rob/test.txt","This is my text")

        which will append the text "This is my text" to the file.
        """

        destinationFile = open(path, 'a')
        destinationFile.write(str(text))
        destinationFile.close()

    # ******************************************************************************************

    ## Clears the contents of the file at the specified path.
    #
    #  @param self The object pointer.
    #  @param path The full path to the file to clear.
    def clearFile(self, path):
        """Clears the contents of the file at the specified path.

        Parameters
        ----------
        self : object
            The object pointer.
        path : str
            The full path to the file to clear.

        Examples
        --------
        >>> clearFile("/Users/rob/test.txt")

        which will clear all text in the file.
        """
        open(path, 'w').close()

    # ******************************************************************************************

if __name__ == '__main__':
    InjectPulsarCommandCreator().main()
