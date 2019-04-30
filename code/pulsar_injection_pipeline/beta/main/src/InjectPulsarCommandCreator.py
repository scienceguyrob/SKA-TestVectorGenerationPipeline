"""
    ***************************************************************************************
    |                                                                                     |
    |                     Inject Pulsar Command Creator Version 2.0                       |
    |                                                                                     |
    ***************************************************************************************
    | Description:                                                                        |
    |                                                                                     |
    | Creates a "command" file that can be used to automate use of the inject_pulsar tool.|
    | inject_pulsar is a C++ software module found in Mike Keith's version of sigproc     |
    | (https://github.com/SixByNine/sigproc). The command file made here is eventually    |
    | used by the script InjectPulsarAutomator.py. NOTE: this script will overwrite an    |
    | existing command file if given the same parameters.                                 |
    |                                                                                     |
    | Command files produced by this script have a simple file name:                      |
    |                                                                                     |
    | InjectPulsarCommandFile_<Batch>.txt                                                 |
    |                                                                                     |
    | Where <Batch> is a user supplied parameter (with a default value of 1).             |
    |                                                                                     |
    | A command file is a simple ascii file that contains inject_pulsar commands followed |
    | by a destination path. The command can be directly executed by the script           |
    | InjectPulsarAutomator.py using the Python subprocess library. While the destination |
    | path tells InjectPulsarAutomator.py where to move inject_pulsar's outputs to. The   |
    | format of the command file is as follows:                                           |
    |                                                                                     |
    | <inject_pulsar command 1>                                                           |
    | <Destination file name 1>                                                           |
    | <inject_pulsar command 2>                                                           |
    | <Destination file name 2>                                                           |
    | <inject_pulsar command 3>                                                           |
    | <Destination file name 3>                                                           |
    | ...                                                                                 |
    | <inject_pulsar command n>                                                           |
    | <Destination file name n>                                                           |
    |                                                                                     |
    | For example,                                                                        |
    | inject_pulsar --snr 35.0 --pred Fake1.dat --prof Fake1.asc Noise.fil > out.fil      |
    | Desired_output1.fil                                                                 |
    | inject_pulsar --snr 35.0 --pred Fake2.dat --prof Fake2.asc Noise.fil > out.fil      |
    | Desired_output2.fil                                                                 |
    | inject_pulsar --snr 35.0 --pred Fake3.dat --prof Fake3.asc Noise.fil > out.fil      |
    | Desired_output3.fil                                                                 |
    | ...                                                                                 |
    |                                                                                     |
    | Here the destinations are not full paths, but file names only.                      |
    |                                                                                     |
    | Please note the file names used in this example are not valid according to our      |
    | file name standards developed as part of this work - more details on those          |
    | standards below in the "Pre-requisites" section.                                    |
    |                                                                                     |
    | To generate a command, we need to know the full paths to the files that             |
    | inject_pulsar requires to execute correctly. These pre-requisite files include a    |
    | .asc file that describes the shape of the pulse to be injected, a .dat file that    |
    | describes pulse arrival times, and a .fil (filterbank) file into which the signal   |
    | will be injected.                                                                   |
    |                                                                                     |
    | Rather than pass these files in one by one, this script generates commands when     |
    | given the full path to directories containing all the pre-requisite files. This     |
    | means the user must provide two directory paths ( .asc and .dat directories         |
    | respectively), plus a .fil file path.                                               |
    |                                                                                     |
    ***************************************************************************************
    | Pre-requisites:                                                                     |
    ***************************************************************************************
    |                                                                                     |
    | inject_pulsar is a C++ software module compiled as part of Mike Keith's version of  |
    | Sigproc. It is used to inject pulsar signals into valid filterbank files, however   |
    | to do this, it needs multiple prerequisites. These include a .asc file that         |
    | describes the pulse to inject, a Tempo2 predictor file (.dat extension) that        |
    | describes pulse arrival times, and a valid noise filterbank (.fil) file.            |
    |                                                                                     |
    | To proceed, this script makes a number of assumptions regarding the prerequisites:  |
    |                                                                                     |
    | 1. The user has generated pulse profile files (.asc) using the script               |
    |    GaussianProfileGen.py, or some other tool that produces output files which,      |
    |    a. contain pulse intensity values in ascii format, i.e. each line in the file    |
    |       corresponds to a phase bin value.                                             |
    |    b. Have a file name that adheres to the format,                                  |
    |                                                                                     |
    |       <ID>_DC=<Duty Cycle>_BINS=<Bins>_FWHM=<FWHM>.asc                              |
    |                                                                                     |
    |       where <ID> is a string that uniquely identifies the .asc file, <Duty Cycle>   |
    |       is a float describing the fraction of the period that the pulse is "on" for,  |
    |       <Bins> is an integer describing the number of phase bins in the profile, and  |
    |       <FWHM> is a float corresponding to the full-width at half maximum (FWHM). A   |
    |       valid filename could be as follows:                                           |
    |                                                                                     |
    |       Gaussian_DC=0.5_BINS=128_FWHM=64.asc                                          |
    |                                                                                     |
    | 2. The user has generated Tempo2 predictor files by firstly using the script        |
    |    CreateFakeParFiles.py to create valid .par files, and then passing these files   |
    |    as inputs to GeneratePredictorFiles.py, to create the valid .dat Tempo2          |
    |    predictor files. The .par files should adhere to the following filename format:  |
    |                                                                                     |
    |    FakePulsar<Number>_DM=<DM>_P0=<P0>ms_Z=<Accel>.par                               |
    |                                                                                     |
    |    Where <Number> is an integer that helps identify the par file, <DM> is a float   |
    |    representing the dispersion measure, <PO> is a float representing the period in  |
    |    milliseconds, and <Accel> is a float that describes the acceleration in m/s/s.   |
    |                                                                                     |
    |    while the .dat files should adhere to the format:                                |
    |                                                                                     |
    |    <ID>_DM=<DM>_P0=<P0>ms_OBS=<Obs>s_F1=<F1>_F2=<F2>_T=<TC>_F=<FC>_Z=<Accel>.dat    |
    |                                                                                     |
    |    where <ID> is a string that uniquely identifies the .dat file, <DM> is a float   |
    |    representing the dispersion measure, <PO> is a float representing the period in  |
    |    milliseconds, <Obs> is an integer representing the observation length in seconds,|
    |    <F1> and <F2> are floats representing the frequency in MHz of the first and the  |
    |    last channel respectively, <TC> is an integer corresponding to the number of     |
    |    time coefficients used in Tempo2, whilst <FC> is similarly defined but for the   |
    |    frequency coefficients, and finally <Accel> is a float that describes the        |
    |    acceleration in m/s/s.                                                           |
    |                                                                                     |
    |                                                                                     |
    | 3. Valid .asc and .dat files that adhere to the naming standards mentioned above,   |
    |    are stored in directories whose paths are provided by the user at runtime.       |
    |                                                                                     |
    | 4. The user provides the full path to a valid .fil, filterbank file.                |
    |                                                                                     |
    ***************************************************************************************
    | Required Arguments:                                                                 |
    ***************************************************************************************
    |                                                                                     |
    | --asc (string)   full path to a directory containing .asc files, which describe an  |
    |                  individual pulse profile in plain ascii text (use the script       |
    |                  GaussianProfileGen.py to get correctly formatted files).           |
    |                                                                                     |
    | --pred (string)  full path to a directory containing predictor (.dat) files.        |
    |                                                                                     |
    | --out (string)   full path to the output directory, where created command files     |
    |                  will be stored.                                                    |
    |                                                                                     |
    | --noise (string) full path to the noise filterbank (.fil) file.                     |
    |                                                                                     |
    ***************************************************************************************
    | Optional Arguments:                                                                 |
    ***************************************************************************************
    |                                                                                     |
    | -v (boolean) verbose output flag.                                                   |
    |                                                                                     |
    | --snr (float) the desired signal-to-noise ratio (SNR) for the signal injected. This |
    |               parameter is passed directly to the inject_pulsar tool.               |
    |                                                                                     |
    | --seed (int) the random seed used for inject_pulsar execution (1 by default). This  |
    |              is used by inject_pulsar to initialise internal random number          |
    |              generators, making the creation of test vectors deterministic (and     |
    |              therefore reproducible).                                               |
    |                                                                                     |
    | --batch (int) an identifier that is used to version control test vector creation in |
    |               a primitive way. Users should supply a batch number when possible.    |
    |                                                                                     |
    | --label (string) a unique string identifier for the batch of test vectors that will |
    |                  emerge when the commands in the command file are executed. This    |
    |                  helps us achieve a primitive type of version control. When possible|
    |                  you should choose short but informative names for your vectors.    |
    |                                                                                     |
    ***************************************************************************************
    | Author: Rob Lyon                                                                    |
    | Email : robert.lyon@manchester.ac.uk                                                |
    | web   : www.scienceguyrob.com                                                       |
    ***************************************************************************************
    | License:                                                                            |
    ***************************************************************************************
    |                                                                                     |
    | Code made available under the GPLv3 (GNU General Public License), that allows you   |
    | to copy, modify and redistribute the code as you see fit:                           |
    | (http://www.gnu.org/copyleft/gpl.html).                                             |
    | Though a mention to the original author using the citation above in derivative      |
    | works, would be very much appreciated.                                              |
    ***************************************************************************************
"""

# Command Line processing Imports:
from optparse import OptionParser

# Other imports
import os
from AscFile import AscFile
from PredFile import PredFile

# ******************************
#
# CLASS DEFINITION
#
# ******************************


class InjectPulsarCommandCreator:
    """
    Creates a "command file" containing inject_pulsar commands.

    A command file is a simple ascii file that contains inject_pulsar commands followed
    by a destination path. The command can be directly executed by the script
    InjectPulsarAutomator.py using the Python subprocess library. While the destination
    path tells the InjectPulsarAutomator.py where to move inject_pulsar's outputs to.
    The format of the command file is as follows:

    <inject_pulsar command 1>
    <Destination file name 1>
    <inject_pulsar command 2>
    <Destination file name 2>
    <inject_pulsar command 3>
    <Destination file name 3>
    ...
    <inject_pulsar command n>
    <Destination file name n>

    Command files have a filename such as,

    InjectPulsarCommandFile_<Batch>.txt

    Where <Batch> is a user supplied parameter (with a default value of 1).

    """

    def __init__(self):
        """
        Initialises the class and class variables.
        """
        # Set some initial values - will be overwritten when processing
        # command line parameters.

        # Update variables with command line parameters.
        self.verbose       = False      # Logging flag.
        self.asc_dir       = ""         # The directory containing .asc files
        self.pred_dir      = ""         # The directory containing .dat files
        self.fil_file_path = ""         # The full path to a valid .fil file
        self.output_dir    = ""         # The directory where command files will be created.
        self.batch         = 1          # The default batch ID
        self.snr           = 20.0       # The default signal-to-noise ratio to be used by inject pulsar.
        self.seed          = 0          # The default random seed to be used by inject pulsar.
        self.label         = "Default"  # The default label for new test vectors.

        # A prefix for the "command" file/s that will be created.
        self.command_file_prefix = "InjectPulsarCommands_"

        # Stores the commands used to inject data into a noise fil file.
        self.inject_commands = []
        self.asc_paths       = {}
        self.pred_paths      = {}
        self.arguments       = []  # Used to store command line arguments supplied by the user.

    # ******************************************************************************************

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    def main(self, argv=None):
        """
        Main method.

        Main entry point for the Application. Processes command line
        input and begins automating the the creation of inject_pulsar command
        files.

        Parameters
        ----------
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

        # Argument processing.
        parser = OptionParser()

        # REQUIRED ARGUMENTS
        parser.add_option("--asc", action="store", dest="a",
                          help='Path to a directory containing asc files.', default="")

        parser.add_option("--pred", action="store", dest="p",
                          help='Path to the directory to store the predictor files.', default="")

        parser.add_option("--out", action="store", dest="o",
                          help='Path to an output directory.', default="")

        parser.add_option("--noise", action="store", dest="f",
                          help='Path to a filterbank file.', default="")


        # OPTIONAL ARGUMENTS
        parser.add_option("-v", action="store_true", dest="v",
                          help='Verbose debugging flag (optional).', default=False)

        parser.add_option("--seed", type=int, dest="seed",
                          help='The seed value for random number generation (optional).', default=1)

        parser.add_option("--batch", type=int, dest="b",
                          help='The batch number for the vectors (for primitive version control).', default=1)

        parser.add_option("--label", type=str, dest="l",
                          help='A label useful for differentiating test vector batches.', default="Default")

        parser.add_option("--snr", action="store", dest="s",
                          help='SNR ratio.', type=float, default=20.0)


        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        self.verbose       = args.v
        self.asc_dir       = args.a
        self.pred_dir      = args.p
        self.fil_file_path = args.f
        self.output_dir    = args.o
        self.batch         = args.b
        self.snr           = args.s
        self.seed          = args.seed
        self.label         = args.l

        # Pre-process arguments to make unit testing easier.
        self.arguments = [args.v, args.a, args.p, args.f, args.o, args.b, args.s, args.seed, args.l]

        # ****************************************
        #   Print command line arguments
        # ****************************************

        print("\n\t**************************")
        print("\t| Command Line Arguments |")
        print("\t**************************")
        print("\tDebug: "                         + str(self.verbose))
        print("\tAsc directory path: "            + str(self.asc_dir))
        print("\tPredictor file directory path: " + str(self.pred_dir))
        print("\tFilterbank file path: "          + str(self.fil_file_path))
        print("\tOutput directory: "              + str(self.output_dir))
        print("\tCommand batch size: "            + str(self.batch))
        print("\tRandom seed: "                   + str(self.seed))
        print("\tSNR: "                           + str(self.snr))
        print("\tLabel: "                         + str(self.label))
        print("\n\tChecking user supplied parameters...")

        # Check the command line parameters are valid.
        if self.check_parameters(self.arguments):
            # Continue...

            print("\tFinished checking supplied parameters...")

            # Some flags which are only set to true, when we have the
            # directories (containing the files needed).
            have_asc_files = False
            have_pred_files = False

            # ****************************************
            #          Parse ASC Directory
            # ****************************************

            # This part of the code tries to find .asc files in the directory
            # specified by the user.
            print("\n\t*****************************")
            print("\t|    Parsing ASC directory  |")
            print("\t*****************************")
            print("\tLooking for asc files...")

            # Will return a dictionary of file paths (strings), which could
            # be empty...the dictionary uses file names as keys, and full file
            # paths as values.
            self.asc_paths = self.process_asc_dir(self.asc_dir)

            # We will create a list of paths know to lead to valid files.
            asc_file_objects = []

            if self.asc_paths is not None:

                # For key = file name, and value = full file path
                for key, value in self.asc_paths.items():

                    # Create an ASC file object.
                    asc_file = AscFile()

                    # If the object can successfully read the file and validate
                    # it internally... we want to keep the file and continue to
                    # work with it...
                    if asc_file.read(value, self.verbose):
                        asc_file_objects.append(asc_file)

                print("\n\tValid .asc files found: " + str(len(asc_file_objects)))
            else:
                # We found no .asc files to check...
                have_asc_files = False

            # Again, we found no .asc files...
            if asc_file_objects is not None and len(asc_file_objects) > 0:
                have_asc_files = True

            # ****************************************
            #        Parse Predictor Directory
            # ****************************************

            # This part of the code tries to find predictor files in the directory
            # specified by the user.

            print("\n\t*****************************")
            print("\t|   Parsing PRED directory  |")
            print("\t*****************************")
            print("\n\tLooking for .dat files...")

            # Will return a dictionary of file paths (strings), which could
            # be empty...the dictionary uses file names as keys, and full file
            # paths as values.
            self.pred_paths = self.process_pred_dir(self.pred_dir)

            # We will create a list of paths know to lead to valid files.
            pred_file_objects = []

            if self.pred_paths is not None:

                # For key = file name, and value = full file path
                for key, value in self.pred_paths.items():

                    # Create a PRED file object.
                    pred_file = PredFile()

                    # If the object can successfully read the file and validate
                    # it internally... we want to keep the file and continue to
                    # work with it...
                    if pred_file.read(value, self.verbose):
                        pred_file_objects.append(pred_file)

                print("\tValid .dat files found: " + str(len(pred_file_objects)))
            else:
                # We found no .dat files to check...
                have_pred_files = False

            if pred_file_objects is not None and len(pred_file_objects) > 0:
                have_pred_files = True

            # ****************************************
            #
            #         Inject command creation
            #
            # ****************************************

            # Both conditions must hold to proceed, otherwise how
            # can we created valid commands?
            if have_asc_files and have_pred_files:

                print("\n\t*****************************")
                print("\t|  Creating inject commands |")
                print("\t*****************************")
                print("\tCreating inject_pulsar commands...")

                # Maintain counters to track/report progress.
                commands_created     = 0
                commands_not_created = 0
                commands_written     = 0
                command_counter      = 1

                # Build path to the command file to write. it should have the format,
                #
                # InjectPulsarCommandFile_<Batch>.txt
                #
                # Where <Batch> is a user supplied parameter (with a default value of 1).
                command_file_path = self.output_dir + "/InjectPulsarCommandFile_" + str(self.batch) + ".txt"

                # Clear the file if it already exists. We do not check for an existing
                # file, it's up to the user to manage this. This is explained in the
                # docstring too.
                self.clear_file(command_file_path)

                # Now generate the commands.
                for asc in asc_file_objects:  # For each .asc file...
                    for pred in pred_file_objects:  # For each .dat file...

                        # Build the command string using user parameters where
                        # necessary.
                        cmd = self.generate_command(asc, pred, self.snr, self.seed, self.fil_file_path)

                        # Check the command was successfully created.
                        if cmd is None:
                            commands_not_created += 1
                        else:
                            commands_created = 0

                            # Now write the command out.
                            self.append_to_file(command_file_path, cmd + "\n")
                            commands_written += 1

                            # Write out desired destination following the command.
                            dest = self.generate_dest_path(asc, pred, self.snr, self.batch, self.seed, self.label)

                            self.append_to_file(command_file_path, dest + "\n")

                        command_counter += 1


                print("\tInject_pulsar commands created: "    + str(commands_created))
                print("\tInject_pulsar commands not created: "+ str(commands_not_created))
                print("\tInject_pulsar commands written out: "+ str(commands_written))
            else:
                print("\n\t**************************")
                print("\t|   Parameters Invalid  |")
                print("\t**************************")
                print("\tNo predictor '.dat' or '.asc' files, check they exist, exiting.")

        else:
            print("\n\t**************************")
            print("\t|   Parameters Invalid  |")
            print("\t**************************")
            print("\tCannot build profile, exiting.")

        print("\n\tDone.")
        print("\n**************************************************************************\n")

    # ******************************************************************************************

    # ******************************
    #
    # PROCESS ASC FILES
    #
    # ******************************

    @staticmethod
    def process_asc_dir(asc_dir):
        """
        Processes a directory containing '.asc' files, and stores them
        in a dictionary for later processing.

         Parameters
        ----------
        :param asc_dir: the directory to process.

        Returns
        -------

        :return: a dictionary of file paths.
        """
        asc_paths = {}

        # Loop through the specified directory
        for root, subFolders, filenames in os.walk(asc_dir):
            # for each file
            for filename in filenames:
                path = os.path.join(root, filename)  # Gets full path to the candidate.
                # If the file is a predictor file...
                if ".asc" in path:

                    asc_paths[filename] = path

        print("\tASC files meeting basic criteria: " + str(len(asc_paths)))

        return asc_paths

    # ******************************************************************************************

    # ******************************
    #
    # PROCESS PRED FILES
    #
    # ******************************

    @staticmethod
    def process_pred_dir(pred_dir):
        """
        Processes a directory containing '.dat' files, and stores them
        in a dictionary for later processing.

         Parameters
        ----------
        :param pred_dir: the directory to process.

        Returns
        -------

        :return: a dictionary of file paths.
        """

        pred_paths = {}

        # Loop through the specified directory
        for root, subFolders, filenames in os.walk(pred_dir):
            # for each file
            for filename in filenames:
                path = os.path.join(root, filename)  # Gets full path to the candidate.
                # If the file is a predictor file...
                if ".dat" in path:
                    name = filename.replace(".dat", "")
                    pred_paths[name] = path

        print("\tPRED files meeting basic criteria: " + str(len(pred_paths)))

        return pred_paths

    # ******************************************************************************************

    # ******************************
    #
    # GENERATE COMMANDS
    #
    # ******************************

    @staticmethod
    def generate_command(asc, pred, snr, seed, fil_file_path):
        """
        Processes a directory containing '.dat' files, and stores them
        in an array for later processing.

         Parameters
        ----------
        :param asc: A AscFile object.
        :param pred: A PredFile object.
        :param snr: the desired SNR.
        :param seed: the random seed.
        :param fil_file_path: the path to the noise filterbank file.

        Returns
        -------

        :return: a valid inject_pulsar command as a string, else None if there is an error.
        """

        # Some error checking first....

        if asc is None or pred is None:
            return None

        if snr is None or snr < 0:
            return None

        if seed is None or seed < 0:
            return None

        if fil_file_path is None:
            return None

        # Now build the command...
        #
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
        command = "inject_pulsar --snr " + str(snr) + " --seed " + str(seed) + \
                  " --pred " + pred.fpth + " --prof " + asc.fpth + " " + fil_file_path + " > output.fil"

        return command

    # ******************************************************************************************

    @staticmethod
    def generate_dest_path(asc, pred, snr, batch, seed, label):
        """
        Generates an output filename describing the new test vector.

         Parameters
        ----------
        :param asc: dictionary containing '.asc' file paths.
        :param pred: dictionary containing '.dat' predictor file paths.
        :param snr: the desired SNR.
        :param batch: the number of batches to create.
        :param seed: the random seed.
        :param label: the label for the group of test vectors to be generated.

        Returns
        -------

        :return: a string.
        """
        if asc is None or pred is None:
            return None

        if snr is None or snr < 0:
            return None

        if seed is None or seed < 0:
            return None

        if asc.freq is "":
            return label + "_" + str(batch) + "_" + str(pred.p0) + "_" + str(asc.dc) + "_" + str(pred.dm) +\
                   "_" + str(pred.accel) + "_" + asc.name + ".fil"
        else:
            return label + "_" + str(batch) + "_" + str(pred.p0) + "_" + str(asc.dc) + "_" + str(pred.dm) + \
                   "_" + str(pred.accel) + "_" + asc.name + "_" + str(asc.freq) + ".fil"

    # ******************************************************************************************

    # ******************************
    #
    # COMMAND LINE PROCESSING CODE
    #
    # ******************************

    def check_parameters(self, args):
        """
        Checks the parameters provided by the user.

        Parameters
        ----------

        args : []
            The arguments.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        print("\n\t**************************")
        print("\t|  Checking Parameters   |")
        print("\t**************************")

        # There are 9 command line parameters - these must be checked
        # to ensure the user doesn't do anything crazy. We check each parameter
        # in turn, in different ways including,
        #
        # 1. Type checking
        # 2. Formatting checks
        # 3. Boundary condition checks

        outcome = True

        # Check the types are as expected.
        outcome = self.check_parameter_types(args)

        if not outcome:
            print("\tOne or more parameters are not of the expected type.")
            return False

        outcome = self.check_parameter_values(args)

        if not outcome:
            print("\tOne or more parameter values do not adhere to boundary/range conditions.")
            return False

        print("\n\tParameter check complete.")

        return outcome

    # ******************************************************************************************

    @staticmethod
    def check_parameter_types(args, testing=False):
        """
        Checks the parameters provided by the user are of the correct type.

        Parameters
        ----------

        args : []
            The arguments. These are ordered as follows:

            args[0] = verbose flag
            args[1] = '.asc' file directory
            args[2] = predictor file directory
            args[3] = noise filterbank file path
            args[4] = output directory
            args[5] = batch ID
            args[6] = signal-to-noise ratio
            args[7] = random seed.
            args[8] = label.

        testing : boolean
                A flag that when true, suppresses output during testing.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        outcome = True

        # Verbose flag
        if type(args[0]) != bool:
            if not testing:
                print("\tVerbose parameter not the correct type (" + str(type(args[0])) + ").")
            outcome = False

        # '.asc' directory
        if type(args[1]) != str:
            if not testing:
                print("\t'.asc' directory parameter not a string (" + str(type(args[1])) + ").")
            outcome = False

        # Predictor directory
        if type(args[2]) != str:
            if not testing:
                print("\tPredictor directory not a string (" + str(type(args[2])) + ").")
            outcome = False

        # Noise file path
        if type(args[3]) != str:
            if not testing:
                print("\tNoise file path not a string (" + str(type(args[3])) + ").")
            outcome = False

        # Output directory
        if type(args[4]) != str:
            if not testing:
                print("\tOutput directory not a string (" + str(type(args[4])) + ").")
            outcome = False

        # Batch ID
        if type(args[5]) != int:
            if not testing:
                print("\tBatch ID not an integer (" + str(type(args[5])) + ").")
            outcome = False

        # SNR
        if type(args[6]) != float:
            if not testing:
                print("\tSNR parameter not a float (" + str(type(args[6])) + ").")
            outcome = False

        # Random seed
        if type(args[7]) != int:
            if not testing:
                print("\tRandom seed not an integer (" + str(type(args[7])) + ").")
            outcome = False

        # Label
        if type(args[8]) != str:
            if not testing:
                print("\tLabel parameter not a string (" + str(type(args[8])) + ").")
            outcome = False

        return outcome

    # ******************************************************************************************

    @staticmethod
    def check_parameter_values(args, testing=False):
        """
        Checks the parameter values provided by the user do not violate boundary
        or range conditions.

        Parameters
        ----------

        args : []
            The arguments. These are ordered as follows:
            args[0] = verbose flag
            args[1] = '.asc' file directory
            args[2] = predictor file directory
            args[3] = noise filterbank file path
            args[4] = output directory
            args[5] = batch ID
            args[6] = signal-to-noise ratio
            args[7] = random seed.
            args[8] = label.

        testing : boolean
                A flag that when true, suppresses output during testing.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        # First check user has supplied a asc directory path ...
        if os.path.isdir(args[1]):

            # Check the directory contains .asc files.
            files = [f for f in os.listdir(args[1]) if os.path.isfile(os.path.join(args[1], f))]

            contains_ascs = False
            for f in files:
                if ".asc" in f:
                    contains_ascs = True
                    break

            if not contains_ascs:
                if not testing:
                    print("\n\tNo '.asc' files in the ASC directory: " + str(args[1]))
                return False

        else:
            if not testing:
                print("\n\tYou must supply a path to a directory containing par files.")
            return False

        # First check user has supplied a predictor file directory path ...
        if os.path.isdir(args[2]):

            # Check the directory contains .asc files.
            files = [f for f in os.listdir(args[2]) if os.path.isfile(os.path.join(args[2], f))]

            contains_preds = False
            for f in files:
                if ".dat" in f:
                    contains_preds = True
                    break

            if not contains_preds:
                if not testing:
                    print("\n\tNo '.dat' files in the predictor directory: " + str(args[2]))
                return False

        else:
            if not testing:
                print("\n\tYou must supply a path to a directory containing predictor ('.dat') files.")
            return False


        # Check the filterbank file containing noise exists...
        if args[3].endswith(".fil"):
            if os.path.exists(args[3]) is False:
                if not testing:
                    print("\n\tSupplied filterbank file does not exist.")
                return False
        else:
            if not testing:
                print("\n\tSupplied noise file not a filterbank file.")
            return False

        if not os.path.isdir(args[4]):
            try:
                os.makedirs(args[4])
            except OSError:
                if not testing:
                    print("\n\tException encountered trying to create output file directory - Exiting!")
                return False

        # Check the batch
        if args[5] < 0:
            if not testing:
                print("\n\tSupplied batch value invalid.")
            return False

        # Check the SNR
        if args[6] <= 0.0:
            if not testing:
                print("\n\tSupplied SNR value invalid.")
            return False

        # Check the seed
        if args[7] < 0:
            if not testing:
                print("\tSeed parameter must be > 0.")
            return False

        return True

    # ******************************************************************************************

    # ******************************
    #
    # FILE HANDLING CODE
    #
    # ******************************

    @staticmethod
    def append_to_file(path, text):
        """Appends the provided text to the file at the specified path.

        Parameters
        ----------
        path : str
            The full path to the file to write to.
        text : str
            The text to write to the output file.

        Returns
        ----------
        True if the operation completed successfully, else false.

        Examples
        --------
        >>> append_to_file("/Users/rob/test.txt","This is my text")

        which will append the text "This is my text" to the file.
        """

        try:
            destination_file = open(path, 'a')
            destination_file.write(str(text))
            destination_file.close()
            return True
        except IOError:
            return False

    # ******************************************************************************************

    @staticmethod
    def clear_file(path):
        """
        Clears the contents of the file at the specified path.

        Parameters
        ----------
        path : str
            The full path to the file to clear.

        Examples
        --------
        >>> clear_file("/Users/rob/test.txt")

        which will clear all text in the file.
        """
        open(path, 'w').close()

    # ******************************************************************************************

if __name__ == '__main__':
    InjectPulsarCommandCreator().main()