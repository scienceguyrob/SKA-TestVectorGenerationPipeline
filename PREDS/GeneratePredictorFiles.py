## @package PREDS
# A module used to create Tempo2 predictor files.
#
# Author: Rob Lyon
# Email : robert.lyon@manchester.ac.uk
# web   : www.scienceguyrob.com

# Start normal non-doxygen docstring...
"""
    **************************************************************************
    |                                                                        |
    |             Generate Tempo 2 predictor Files Version 1.0               |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Generates TEMPO2 predictor files for all PAR files in a user specified |
    | Directory. The predictor files are stored in a user defined output     |
    | directory. This script is design to run on the par files output by the |
    | CandidateParGenerator.py python script.                                |
    |                                                                        |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@manchester.ac.uk                                   |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | Required Command Line Arguments:                                       |
    |                                                                        |
    | -p (string) full path to the directory containing par files.           |
    |                                                                        |
    | -d (string) full path to store predictor files in.                     |
    |                                                                        |
    **************************************************************************
    | Optional Command Line Arguments:                                       |
    |                                                                        |
    | -v (boolean) verbose debugging flag.                                   |
    |                                                                        |
    | -s (int) the length of the observation in seconds to be passed in      |
    |             to tempo2 for predictor file creation (default=600).       |
    |                                                                        |
    | -b (int) the maximum number of par files to process. This is useful if |
    |          processing directories containing many par files. By using    |
    |          this flag, the pars can be processed in batches. This is      |
    |          possible as the script will not overwrite a predictor file if |
    |          it already exists. Thus predictor files generated for par     |
    |          files for the first batch, will simply be skipped over on the |
    |          second run. The pars missing out on predictor file generation |
    |          on the first run may be processed in the second run, depending|
    |          on the batch size used (default = 1000).                      |
    |                                                                        |
    | --f1 (int) the frequency of the first channel which is passed in to    |
    |              tempo2 for predictor file creation (default=1350).        |
    |                                                                        |
    | --f2 (int) the frequency of the last channel which is passed in to     |
    |              tempo2 for predictor file creation (default=1670).        |
    |                                                                        |
    | --tcoeff (int) the number of time coefficients to be computed by       |
    |                tempo2 during predictor file creation (default=12).     |
    |                                                                        |
    | --fcoeff (int) the number of frequency coefficients to be computed by  |
    |                tempo2 during predictor file creation (default=2).      |
    |                                                                        |
    | --mjd1 (string) the start time mjd used by tempo2 during predictor     |
    |                file creation (default=56000).                          |
    |                                                                        |
    | --mjd2 (string) the start time mjd used by tempo2 during predictor     |
    |                file creation (default=56001).                          |
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

import os, sys,datetime

import subprocess

# Other imports
from shutil import copyfile

# ******************************
#
# CLASS DEFINITION
#
# ******************************

## Generate Tempo 2 predictor Files Version 1.0
#
# Description:
#
# Generates TEMPO2 predictor files for all PAR files in a user specified
# Directory. The predictor files are stored in a user defined output
# directory. This script is design to run on the par files output by the
# CandidateParGenerator.py python script.
#
#
# Author: Rob Lyon
# Email : robert.lyon@manchester.ac.uk
# web   : www.scienceguyrob.com
#
# Required Command Line Arguments:
#
# -p (string) full path to the directory containing par files.
#
# -d (string) full path to store predictor files in.
#
#
# Optional Command Line Arguments:
#
# -v (boolean) verbose debugging flag.
#
# -s (int) the length of the observation in seconds to be passed in
#             to tempo2 for predictor file creation (default=600).
#
# -b (int) the maximum number of par files to process. This is useful if
#          processing directories containing many par files. By using
#          this flag, the pars can be processed in batches. This is
#          possible as the script will not overwrite a predictor file if
#          it already exists. Thus predictor files generated for par
#          files for the first batch, will simply be skipped over on the
#          second run. The pars missing out on predictor file generation
#          on the first run may be processed in the second run, depending
#          on the batch size used (default = 1000).
#
# --f1 (int) the frequency of the first channel which is passed in to
#              tempo2 for predictor file creation (default=1350).
#
# --f2 (int) the frequency of the last channel which is passed in to
#              tempo2 for predictor file creation (default=1670).
#
# --tcoeff (int) the number of time coefficients to be computed by
#                tempo2 during predictor file creation (default=12).
#
# --fcoeff (int) the number of frequency coefficients to be computed by
#                tempo2 during predictor file creation (default=2).
#
# --mjd1 (string) the start time mjd used by tempo2 during predictor
#                file creation (default=56000).
#
# --mjd2 (string) the start time mjd used by tempo2 during predictor
#                file creation (default=56001).
#
#
# License:
#
# Code made available under the GPLv3 (GNU General Public License), that
# allows you to copy, modify and redistribute the code as you see fit
# (http://www.gnu.org/copyleft/gpl.html). Though a mention to the
# original author using the citation above in derivative works, would be
# very much appreciated.
class GeneratePredictorFiles:
    """
    Description:

    Generates TEMPO2 predictor files for all PAR files in a user specified
    Directory. The predictor files are stored in a user defined output
    directory. This script is design to run on the par files output by the
    CandidateParGenerator.py python script.

    """

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    ## The main method for the class.
    # Main entry point for the Application. Processes command line
    # input and begins automating the creation of Tempo2 predictor
    # files.
    #
    #  @param self The object pointer.
    #  @param argv The unused arguments.
    def main(self,argv=None):
        """Main method.

        Main entry point for the Application. Processes command line
        input and begins automating the the creation of Tempo2 predictor
        files.

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
        parser.add_option("-p", action="store", dest="parDir",help='Path to a directory containing par files.',default="")
        parser.add_option("-d", action="store", dest="outputDir",help='Path to the directory to store the predictor files in.',default="")

        # OPTIONAL ARGUMENTS
        parser.add_option("-v", action="store_true", dest="verbose",help='Verbose debugging flag (optional).',default=False)
        parser.add_option("-s", type="int", dest="secs",help='The total of seconds to pass in to tempo2 (optional).',default=600)
        parser.add_option("-b", type="int", dest="batch",help='The number of files to process in a batch (optional).',default=1000)
        parser.add_option("--f1", type="int", dest="f1",help='The frequency of the first channel passed in to tempo2 (optional).',default=1350)
        parser.add_option("--f2", type="int", dest="f2",help='The frequency of the last channel passed in to tempo2 (optional).',default=1670)
        parser.add_option("--tcoeff", type="int", dest="tcoeff",help='The number of time coefficients to be computed by tempo2 (optional).',default=12)
        parser.add_option("--fcoeff", type="int", dest="fcoeff",help='The number of frequency coefficients to be computed by tempo2 (optional).',default=2)
        parser.add_option("--mjd1", action="store", dest="mjd1",help='Start time MJD.',default="56000")
        parser.add_option("--mjd2", action="store", dest="mjd2",help='Start time MJD.',default="56001")
        (args,options) = parser.parse_args()# @UnusedVariable : Tells Eclipse IDE to ignore warning.

        # Update variables with command line parameters.
        self.verbose    = args.verbose
        self.parDir     = args.parDir
        self.outputDir  = args.outputDir
        self.extensions = [".par"]
        self.obsLength  = args.secs
        self.f1         = args.f1
        self.f2         = args.f2
        self.tcoeff     = args.tcoeff
        self.fcoeff     = args.fcoeff
        self.batch      = args.batch
        self.mjd1       = args.mjd1
        self.mjd2       = args.mjd2

        # ****************************************
        #   Print command line arguments & Run
        # ****************************************

        print "\n\t**************************"
        print "\t| Command Line Arguments |"
        print "\t**************************"
        print "\tDebug:",self.verbose
        print "\tPar directory path:",self.parDir
        print "\tOutput directory path:",self.outputDir
        print "\tSegment length:",self.obsLength
        print "\tF1 value:",self.f1
        print "\tF2 value:",self.f2
        print "\tNumber of time coeffs:",self.tcoeff
        print "\tNumber of freq. coeffs:",self.fcoeff
        print "\tMJD 1:",self.mjd1
        print "\tMJD 2:",self.mjd2
        print "\tBatch size:",self.batch

        # Check the buffer value supplied by the user...
        if(self.obsLength <= 0):
            print "\n\tSupplied observation length invalid - Exiting!"
            sys.exit()

        if(self.f1 <= 0):
            print "\n\tSupplied f1 value invalid - Exiting!"
            sys.exit()

        if(self.f2 <= 0):
            print "\n\tSupplied f2 value invalid - Exiting!"
            sys.exit()

        if(self.tcoeff <= 0):
            print "\n\tSupplied number of time coefficicents invalid - Exiting!"
            sys.exit()

        if(self.fcoeff <= 0):
            print "\n\tSupplied number of time coefficicents invalid - Exiting!"
            print "\tExiting..."
            sys.exit()

        # First check user has supplied a par directory path ...
        if(not self.parDir):
            print "\n\tYou must supply a valid par directory file via the -p flag."
            print "\tExiting..."
            sys.exit()

        # Now check user has supplied a predictor file output directory path ...
        if(not self.outputDir):
            print "\n\tYou must supply a valid output directory file via the -d flag."
            print "\tExiting..."
            sys.exit()

        # Now the user may have supplied an output directory path, but it may
        # not be valid. So first, try to create the directory, if it doesn't
        # already exist. If the create fails, the directory path must be invalid,
        # so exit the application.
        if(os.path.exists(self.outputDir) == False):
            try:
                os.makedirs(self.outputDir)
            except OSError as exception:
                print "\n\tException encountered trying to create par file output directory - Exiting!"
                sys.exit()

        self.pulsarPredictorFileDir = self.outputDir + "/Pulsar"
        self.fakePulsarPredictorFileDir  = self.outputDir + "/FakePulsar"

        # If the directory creation call above did not fail, the output directory
        # should now exist. Check that this is the case...
        if(os.path.isdir(self.outputDir) == False):
            print "\n\tPredictor file output directory invalid - Exiting!"
            sys.exit()
        else:
            # Create new output directories
            if(os.path.exists(self.pulsarPredictorFileDir) == False):
                os.makedirs(self.pulsarPredictorFileDir)

            if(os.path.exists(self.fakePulsarPredictorFileDir) == False):
                os.makedirs(self.fakePulsarPredictorFileDir)

        # ****************************************
        #
        #
        #
        #         File parsing section
        #
        #
        #
        # ****************************************

        # ****************************************
        #          Parse Par files
        # ****************************************

        # This part of the code tries to find par files in the directory
        # specified by the use, then attempts to use those file paths to create
        # a TEMPO2 predictor file...
        #
        print "\n\tLooking for PAR files...\n\n"
        parCount = 0
        fakePulsarErrors = 0
        pulsarParErrors = 0
        fakePulsarSuccesses = 0
        pulsarParSuccesses = 0

        batchEntryCount = 0

        start = datetime.datetime.now() # Used to measure feature generation time.

        # Loop through the specified directory
        for root, subFolders, filenames in os.walk(self.parDir):
            # for each file
            for filename in filenames:
                path = os.path.join(root, filename) # Gets full path to the par.

                # Break if we have reached the batch limit
                if(batchEntryCount == self.batch):
                    break

                for ext in self.extensions:

                    if(ext in path):

                        name = filename.replace(ext,"")
                        print "\tPath: ", path , " Filename: ",name


                        fakePulsarDestPath = self.fakePulsarPredictorFileDir + "/" + name + ".dat"
                        pulsarDestPath = self.pulsarPredictorFileDir + "/" + name + ".dat"

                        # If the file already exists, don't over write it...
                        if(os.path.exists(fakePulsarDestPath) or os.path.exists(pulsarDestPath)):
                            continue

                        if(batchEntryCount < self.batch):

                            # update count
                            batchEntryCount+=1

                            #                                                  MJD 1  MJD2 FCH1 FCHN
                            tempo2Command = "tempo2 -f " + path + " -pred \"meerkat "+self.mjd1+" "+self.mjd2+" "+ str(self.f1) + " " +\
                                            str(self.f2) + " " + str(self.tcoeff) + " " + str(self.fcoeff) + " " + str(self.obsLength)+"\""

                            # Now try to execute the tempo2 command...
                            #
                            process = subprocess.Popen(tempo2Command, shell=True)
                            process.wait()

                            # If the expected output file exists...
                            if(os.path.exists("t2pred.dat") == True):

                                # If we are dealing with a noise file, move predictor file to
                                # the correct noise output folder.
                                if("FakePulsar_" in name):

                                    # Physically copy the file
                                    self.clearFile(fakePulsarDestPath)
                                    copyfile("t2pred.dat", fakePulsarDestPath)

                                    # Check the file exists.
                                    if(os.path.exists(fakePulsarDestPath) == True):
                                        # The file was copied successfully.
                                        fakePulsarSuccesses +=1
                                    else:
                                        fakePulsarErrors +=1
                                else:

                                    # Physically copy the file
                                    self.clearFile(pulsarDestPath)
                                    copyfile("t2pred.dat", pulsarDestPath)

                                    # Check the file exists.
                                    if(os.path.exists(pulsarDestPath) == True):
                                        # The file was copied successfully.
                                        pulsarParSuccesses +=1
                                    else:
                                        pulsarParErrors +=1

                            else:
                                # The expected t2pred.dat file does not exist - tempo2 must have
                                # encountered some problem. Tell the user...
                                print "\tError generating predictor file for par: ", path

                                # Update error counting stats.
                                if("FakePulsar_" in name):
                                    fakePulsarErrors +=1
                                else:
                                    pulsarParErrors +=1

        # Finally get the time that the procedure finished.
        end = datetime.datetime.now()

        noisePars = fakePulsarErrors + fakePulsarSuccesses
        pulsarPars = pulsarParErrors + pulsarParSuccesses
        print "\n\tFake Pulsar Par files found: " + str(noisePars)
        print "\tPulsar Par files found: " + str(pulsarPars)
        print "\tFake pulsar Par errors (predictor file creation) : " + str(fakePulsarErrors)
        print "\tPulsar Par errors (predictor file creation): " + str(pulsarParErrors)
        print "\tFake pulsar Par successes (predictor file creation) : " + str(fakePulsarSuccesses)
        print "\tPulsar Par successes (predictor file creation): " + str(pulsarParSuccesses), "\n\n"
        print "\tExecution time: ", str(end - start)
        print "\n\tDone."
        print "\t**************************************************************************" # Used only for formatting purposes.

    # ****************************************************************************************************

    ## Appends the provided text to the file at the specified path.
    #
    #  @param self The object pointer.
    #  @param path The full path to the file to write to.
    #  @param text The text to write to the output file.
    def appendToFile(self,path,text):
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

        destinationFile = open(path,'a')
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
    GeneratePredictorFiles().main()