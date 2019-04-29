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
    |                 Inject Pulsar Automator Version 1.0                    |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Automates the use of inject_pulsar using preprocessed command files.   |
    | These contain the text command to execute using the python subprocess  |
    | library. Each command in the file calls inject_pulsar with three       |
    | parameters: an ascii .asc file describing the a pulse profile, a       |
    | tempo2 predictor file (.dat), and the noise filterbank file to inject  |
    | the signal into.                                                       |
    |                                                                        |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@manchester.ac.uk                                   |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | Required Command Line Arguments:                                       |
    |                                                                        |
    | --cmd (string)  full path to the file containing the inject pulsar     |
    |                 commands to execute.                                   |
    |                                                                        |
    | --out (string)   full path to the output directory where the output    |
    |                  files will be stored.                                 |
    |                                                                        |
    **************************************************************************
    | Optional Command Line Arguments:                                       |
    |                                                                        |
    | -v (boolean) verbose debugging flag.                                   |
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

import os, sys, datetime, ntpath, subprocess

# Other imports
from shutil import copyfile

# ******************************
#
# CLASS DEFINITION
#
# ******************************

## Inject Pulsar Automator Version 1.0
#
# Description:
#
# Automates the use of inject_pulsar using preprocessed command files.
# These contain the text command to execute using the python subprocess
# library. Each command in the file calls inject_pulsar with three
# parameters: an ascii .asc file describing the a pulse profile, a
# tempo2 predictor file (.dat), and the noise filterbank file to inject
# the signal into.
#
# Author: Rob Lyon
# Email : robert.lyon@manchester.ac.uk
# web   : www.scienceguyrob.com
# Required Command Line Arguments:
#
# --cmd (string)  full path to the file containing the inject pulsar
#                 commands to execute.
#
# --out (string)   full path to the output directory where the output
#                  files will be stored.
#
# Optional Command Line Arguments:
#
# -v (boolean) verbose debugging flag.
#
# License:
#
# Code made available under the GPLv3 (GNU General Public License), that
# allows you to copy, modify and redistribute the code as you see fit
# (http://www.gnu.org/copyleft/gpl.html). Though a mention to the
# original author using the citation above in derivative works, would be
# very much appreciated.


class InjectPulsarAutomator:
    """
    Automates the use of inject_pulsar using preprocessed command files.
    These contain the text command to execute using the python subprocess
    library. Each command in the file calls inject_pulsar with three
    parameters: an ascii .asc file describing the a pulse profile, a
    tempo2 predictor file (.dat), and the noise filterbank file to inject
    the signal into.
    """

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    ## The main method for the class.
    # Main entry point for the Application. Processes command line
    # input and begins automating the execution of inject_pulsar.
    #
    #  @param self The object pointer.
    #  @param argv The unused arguments.
    def main(self,argv=None):
        """Main method.

        Main entry point for the Application. Processes command line
        input and begins automating the execution of inject_pulsar.

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
        parser.add_option("--cmd", action="store", dest="cmdFilePath",
                          help='Path to a file containing execution commands.', default="")

        parser.add_option("--out", action="store", dest="outputDir",
                          help='Path to an output directory.', default="")

        # OPTIONAL ARGUMENTS
        parser.add_option("-v", action="store_true", dest="verbose",
                          help='Verbose debugging flag (optional).', default=False)

        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        self.verbose     = args.verbose
        self.cmdFilePath = args.cmdFilePath
        self.outputDir   = args.outputDir

        # Stores the commands used to inject data into a noise fil file.
        self.injectCommands = []

        # ****************************************
        #   Print command line arguments & Run
        # ****************************************

        print("\n\t**************************")
        print("\t| Command Line Arguments |")
        print("\t**************************")
        print("\tDebug:"                  + str(self.verbose))
        print("\tCommand file path path:" + str(self.cmdFilePath))
        print("\tOutput directory:"       + str(self.outputDir))

        print("\n\tChecking user supplied parameters...")

        # Now check the user has supplied an output directory path
        if not self.outputDir:
            print("\n\tYou must supply a valid predictor file directory via the --out flag.")
            sys.exit()

        # Now the user may have supplied an output directory path, but it may
        # not be valid. So first, try to create the directory if it doesn't
        # already exist. If the create fails, the directory path must be invalid,
        # so exit the application.
        if os.path.exists(self.outputDir) is False:
            try:
                os.makedirs(self.outputDir)
            except OSError as exception:
                print("\n\tException encountered trying to create output directory - Exiting!")
                sys.exit()

        # If the directory creation call above did not fail, the output directory
        # should now exist. Check that this is the case...
        if os.path.isdir(self.outputDir) is False:
            print("\n\tOutput directory invalid - Exiting!")
            sys.exit()

        # Check the command file...
        if os.path.exists(self.cmdFilePath) is False:
            print("\n\tYou must supply a valid command file via the --cmd flag.")
            sys.exit()

        print("\n\tFinished checking supplied parameters...")

        # ****************************************
        #
        #
        #
        #            Execute commands
        #
        #
        #
        # ****************************************

        print("\n\tExecuting inject_pulsar commands...")
        executionCount  = 0
        executionErrors = 0
        copyErrors      = 0

        start = datetime.datetime.now()  # Used to measure feature generation time.

        # Open command file
        self.cmdFile = open(self.cmdFilePath, 'r')  # Read only access

        # For each line in the command file, which should be an inject_pulsar command
        for line in self.cmdFile.readlines():

            command = line.strip()

            commandComponents = line.split()

            # A command should start with inject_pulsar
            if command.startswith("inject_pulsar"):

                # Execute the command
                process = subprocess.Popen(command, shell=True)
                process.wait()

                executionCount += 1

                # Check the command file...
                if os.path.exists("output.fil") is False:
                    print("\n\tExecution " + str(executionCount) + " failed to create output file!")
                    executionErrors +=1
                else:
                    # The output file must exist. So here we move it to the output directory
                    # and give it a useful name. To give it a useful name, we need to extract 
                    # a useful name from the execution command.  Execution commands resemble
                    # the following:
                    #
                    # inject_pulsar --snr 15 --seed 1 --pred J1032-5911.dat --prof J1032-5911_1382_1.asc Noise.fil > output.fil
                    # inject_pulsar --snr 15 --seed 1 --pred J1428-5530.dat --prof J1428-5530_1382_1.asc Noise.fil > output.fil
                    # inject_pulsar --snr 15 --seed 1 --pred J0849-6322.dat --prof J0849-6322_1374.asc Noise.fil   > output.fil
                    #       ^         ^   ^      ^  ^     ^        ^          ^        ^                  ^
                    #       |         |   |      |  |     |        |          |        |                  |
                    #       |         |   |      |  |     |        |          |        |                  |
                    #       0         1   2      3  4     5        6          7        8                  9   INDEXES
                    #
                    #
                    # So as we can see the .dat and .asc files both contain useful descriptions of the output
                    # file produced. The asc file names have the most information, as these describe the source,
                    # and the frequency it was observed at (corresponding to the EPN profile that gave rise to
                    # the asc file). So we extract the source name and the frequency, to use for copying the
                    # output file.

                    # If there are twelve components to the command, we must have a valid command.
                    if len(commandComponents) == 12:

                        # From indexes shown in comments above, we know that...
                        fname = ntpath.basename(commandComponents[6].replace(".dat", ""))
                        ascFileName = ntpath.basename(commandComponents[8].replace(".asc", ""))

                        if "FakePulsar_" in fname:
                            # We want to retain knowledge of the ASC profile injected into the noise data.
                            destination = self.outputDir + "/" + fname + "_ASC_" + ascFileName + ".fil"
                        else:
                            destination = self.outputDir + "/" + fname + ".fil"

                        copyfile("output.fil", destination)

                        # Check the command file...
                        if os.path.exists(destination) is False:
                            print("\n\tExecution " + str(executionCount) + " failed to copy output file!")
                            copyErrors += 1

                    else:
                        # we just don't know where to move the file... best to delete it to ensure we
                        # don't use up all allocated disk space...
                        print("Not enough components!")
                        self.clearFile("output.fil")

        # Finally get the time that the procedure finished.
        end = datetime.datetime.now()

        print("\n\tExecutions of inject_pulsar: " + str(executionCount))
        print("\tExecution errors: " + str(executionErrors))
        print("\tExecution successes: " + str(executionCount-executionErrors))
        print("\tCopy errors: " + str(copyErrors))
        print("\tExecution time: " + str(end - start))
        print("\n\tDone.")
        print("\t**************************************************************************")

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
    InjectPulsarAutomator().main()
