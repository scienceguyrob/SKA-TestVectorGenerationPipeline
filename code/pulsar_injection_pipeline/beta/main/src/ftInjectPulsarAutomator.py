"""
    ***************************************************************************************
    |                                                                                     |
    |                      ft Inject Pulsar Automator Version 2.0                         |
    |                                                                                     |
    ***************************************************************************************
    | Description:                                                                        |
    ***************************************************************************************
    |                                                                                     |
    | Automates execution of the ft_inject_pulsar python module, found in Mike Keith's    |
    | version of filtools (https://bitbucket.org/mkeith/filtools/src/master/). This script|
    | uses the Python subprocess library to execute ft_inject_pulsar. The input parameters|
    | required by ft_inject_pulsar are obtained from a "Command File" that must be given  |
    | to this script. A command file is a simple ascii file that contains ft_inject_pulsar|
    | commands followed by a destination path. The destination path tells this script     |
    | where to move ft_inject_pulsar's outputs to. The format of the command file is      |
    | as follows:                                                                         |
    |                                                                                     |
    | <ft_inject_pulsar command 1>                                                        |
    | <Destination file name 1>                                                           |
    | <ft_inject_pulsar command 2>                                                        |
    | <Destination file name 2>                                                           |
    | <ft_inject_pulsar command 3>                                                        |
    | <Destination file name 3>                                                           |
    | ...                                                                                 |
    | <ft_inject_pulsar command n>                                                        |
    | <Destination file name n>                                                           |
    |                                                                                     |
    |                                                                                     |
    | .fil File Output:                                                                   |
    |                                                                                     |
    | Successful execution of the script should produce .fil files with the following     |
    | file name format:                                                                   |
    |                                                                                     |
    | <label>_<batch>_<P0>_<dc>_<DM>_<Accel>_<Pulse>_<Targ SNR>_<FD>.fil                  |
    |                                                                                     |
    | or                                                                                  |
    |                                                                                     |
    | <label>_<batch>_<P0>_<dc>_<DM>_<Accel>_<Pulse>_<Pulse Freq.>_<Targ SNR>_<FD>.fil    |
    |                                                                                     |
    |                                                                                     |
    | where                                                                               |
    |                                                                                     |
    | <Label> = a unique string identifier for the batch of test vectors that will        |
    |           emerge when the commands in the command file are executed. This helps us  |
    |           achieve a primitive type of version control. When possible you should     |
    |           choose short but informative names for your vectors. This value is set    |
    |           when running the InjectPulsarCommandCreator.py script.                    |
    |                                                                                     |
    | <batch> = an identifier that is used to version control test vector creation in a   |
    |           primitive way. Users should supply a batch number when possible. This     |
    |           value is set when running the InjectPulsarCommandCreator.py script.       |
    |                                                                                     |
    | <P0>    = period  in milliseconds.                                                  |
    |                                                                                     |
    | <DC>    = duty cycle.                                                               |
    |                                                                                     |
    | <DM>    = the Dispersion Measure (DM)                                               |
    |                                                                                     |
    | <Accel> =  the acceleration in m/s/s.                                               |
    |                                                                                     |
    | <Pulse> =  A unique identifier for the pulse inserted in to the test vector, e.g.   |
    |            "Gaussian", or some pulsar JName.                                        |
    |                                                                                     |
    | <Pulse Freq.> = If the pulse shape corresponds to a real known pulsar, the freq. in |
    |                 MHz that the pulse was observed at, e.g. 1400 MHz.                  |
    |                                                                                     |
    | <Targ SNR> = the target Signal-to-noise ratio (SNR) given to ft_inject_pulsar.      |
    |                                                                                     |
    | <FD> = the flux density given to ft_inject_pulsar.                                  |
    |                                                                                     |
    ***************************************************************************************
    | Required Arguments:                                                                 |
    ***************************************************************************************
    |                                                                                     |
    | --cmd (string)  full path to the file containing the inject pulsar commands to      |
    |                 execute.                                                            |
    |                                                                                     |
    | --out (string)   full path to the output directory where the output files will be   |
    |                  stored.                                                            |
    |                                                                                     |
    ***************************************************************************************
    | Optional Arguments:                                                                 |
    ***************************************************************************************
    |                                                                                     |
    | -v (boolean) verbose output flag.                                                   |
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

# Other imports...
import os
import datetime
import subprocess
from shutil import copyfile
from Common import Common


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class InjectPulsarAutomator:
    """
    Automates the use of ft_inject_pulsar using preprocessed "Command Files".
    These contain "Command" and "Destination" pairs. The text comprising a
    command allows inject_pulsar to be executed using the python subprocess
    library. Whilst the destination tells this script where to copy the outputs
    of inject_pulsar to, on disk. At a basic level this script reads the command
    file, executes the inject_pulsar command using the subprocess library, and
    copies the outputs to the desired destination.

    The format of the command file is as follows:
    <ft_inject_pulsar command 1>
    <Destination file name 1>
    <ft_inject_pulsar command 2>
    <Destination file name 2>
    <ft_inject_pulsar command 3>
    <Destination file name 3>
    ...
    <ft_inject_pulsar command n>
    <Destination file name n>

    """

    def __init__(self):
        """
        Initialises the class and class variables.
        """
        self.verbose       = False  # Logging flag.
        self.cmd_file_path = ""     # The full path to the command file.
        self.output_dir    = ""     # The output directory where inject_pulsar outputs should be stored.
        self.arguments     = []     # Used to store command line arguments supplied by the user.

        # Stores the commands used to inject data into a noise fil file.
        self.inject_commands = []

        # Stores the output destination file names.
        self.inject_command_destinations = []

    # ******************************************************************************************

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    def main(self, argv=None):
        """Main method.

        Main entry point for the Application. Processes command line
        input and begins automating the execution of ft_inject_pulsar.

        Parameters
        ----------
        argv : str
            The command line arguments.

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
        parser.add_option("--cmd", action="store", dest="c",
                          help='Path to a file containing execution commands (REQUIRED).', default="")

        parser.add_option("--out", action="store", dest="o",
                          help='Path to an output directory (REQUIRED).', default="")

        # OPTIONAL ARGUMENTS
        parser.add_option("-v", action="store_true", dest="v",
                          help='Verbose output flag (optional).', default=False)

        (args, options) = parser.parse_args()

        # Update variables with command line parameter values provided.
        self.verbose       = args.v
        self.cmd_file_path = args.c
        self.output_dir    = args.o

        # Store the arguments obtained for easier processing later on.
        self.arguments     = [self.verbose, self.cmd_file_path, self.output_dir]

        # Stores the commands used to inject data into a noise fil file.
        self.inject_commands = []
        self.inject_command_destinations = []

        # ****************************************
        #      Print command line arguments
        # ****************************************

        print("\n\t**************************")
        print("\t| Command Line Arguments |")
        print("\t**************************")
        print("\tDebug: "             + str(self.verbose))
        print("\tCommand file path: " + str(self.cmd_file_path))
        print("\tOutput directory: "  + str(self.output_dir))

        # Check the command line parameters are valid.
        if self.check_parameters(self.arguments):

            # Now try to obtain inject_pulsar commands from the
            # command file supplied by the user....
            print("\n\t**************************")
            print("\t|    Read command file   |")
            print("\t**************************")
            print("\n\tReading: " + str(self.cmd_file_path) + "\n")

            # Get the file contents. Reads the contents into a List of strings.
            command_file_contents = Common.read_file(self.cmd_file_path)

            # The file contents should not be none...
            if command_file_contents is not None:

                # The file should contain *some* data...
                if len(command_file_contents) > 0:

                    # Let user know what we've found out about the command file.
                    print("\tLines in command file:\t" + str(len(command_file_contents)))
                    print("\tCommands in file:\t\t"    + str(len(command_file_contents) / 2))

                    # The command file should contain an even number of entries.
                    # This is because it's comprised of command:destination pairs
                    # as described earlier on.
                    if len(command_file_contents) % 2 == 0:

                        # Now we iterate over the file contents to obtain the commands,
                        # and the destinations. We store the values found in separate
                        # lists.
                        command_file_valid = True # A flag useful for error checking...
                        for line in command_file_contents:

                            # If line has a command, it should start with...
                            if line.startswith("ft_inject_pulsar"):
                                self.inject_commands.append(line)
                            elif ".fil" in line:
                                # The line should contain a destination path
                                self.inject_command_destinations.append(line)
                            else:
                                # Not too sure what the line contains, worrying... we
                                # should bother trying to read the file, get the user
                                # to check the file is valid - they can always re-run.
                                # This is probably the best approach, as executing
                                # inject_pulsar can take hours if a lot of commands are
                                # provided.
                                command_file_valid = False
                                print("\tWARNING: Command file contains lines with unexpected formatting!")
                                print("\tWARNING: Remove empty lines from command file, ensure all lines are valid.")

                        if command_file_valid:

                            print("\tCommands found:\t\t\t"   + str(len(self.inject_commands)))
                            print("\tOutput paths found:\t\t" + str(len(self.inject_command_destinations)))

                            # We should have some commands, and more importantly, each command
                            # should be accompanied by an output path. First we check that is
                            # the case
                            if len(self.inject_commands) > 0 and \
                                            len(self.inject_commands) == len(self.inject_command_destinations):

                                # Good news, we can proceed to execution...
                                print("\n\tExecuting ft_inject_pulsar commands...")

                                # Maintain some useful stats for the user.
                                execution_count  = 0
                                execution_errors = 0
                                copy_errors      = 0
                                copy_successes   = 0

                                # Lets measure the process runtime - might help the user make better
                                # generation decisions, if they know how long it takes.
                                start = datetime.datetime.now()

                                # For each command, destination pair...
                                for cmd, dest_filename in zip(self.inject_commands, self.inject_command_destinations):

                                    # Execute the command
                                    process = subprocess.Popen(cmd, shell=True)
                                    process.wait()

                                    # Only used when debugging without running inject_pulsar directly -  we do this
                                    # as this command can take a VERY long time to execute if there are lots of
                                    # execute commands.
                                    #Common.create_file("output.fil")

                                    # This should only increment once the process terminates.
                                    execution_count += 1

                                    # If the command executed successfully, the output file
                                    # produced by inject_pulsar must exists. Lets check for this.
                                    if os.path.exists("output.fil"):

                                        # The output file must exist. This can only be the case IF inject_pulsar
                                        # executed successfully. Now we move the output file to the output directory.
                                        full_destination_path = self.output_dir + "/" + dest_filename

                                        # Added a string replace "?" as some weird behaviour was being seen
                                        # I don't think this is really needed though.
                                        copyfile("output.fil", full_destination_path.replace("?", ""))

                                        # Check the command file has been copied correctly.
                                        if os.path.exists(full_destination_path):
                                            if self.verbose:
                                                print("\t"  + str(dest_filename) + " \tcopied successfully.")
                                            copy_successes += 1
                                        else:
                                            print("\n\tExecution " + str(execution_count) +
                                                  " failed to copy output file!")
                                            copy_errors += 1
                                    else:
                                        print("\n\tExecution " + str(execution_count) +
                                              " failed to create output file!")

                                        execution_errors += 1

                                # Finally get the time the procedure finished.
                                end = datetime.datetime.now()

                                # We're done. Compute some stats for the user.
                                execution_successes = execution_count - execution_errors
                                duration = end - start
                                print("\n\tinject_pulsar runs:\t\t" + str(execution_count))
                                print("\tExecution errors:\t\t"     + str(execution_errors))
                                print("\tExecution successes: \t"   + str(execution_successes))
                                print("\tFile copy errors:\t\t"     + str(copy_errors))
                                print("\tFile copy successes:\t"    + str(copy_successes))
                                print("\n\tExecution time: \t\t"    + str(end - start) + " (hh:mm:ss)")

                                # Average execution time per test vector...
                                avg_execution_time_secs = (duration.total_seconds()) / float(execution_successes)
                                print("\tAvg. per vector:\t\t" + str(avg_execution_time_secs) + " seconds")

                            else:
                                print("\tCommand file does not contain even number of entries - " +
                                      "destinations must be missing, exiting.")
                        else:
                            print("\tCommand file contains unexpected line format - " +
                                  "check the file before proceeding, exiting.")
                    else:
                        print("\tCommand file does not contain even number of entries - " +
                              "destinations must be missing, exiting.")
                else:
                    print("\tCommand file empty, exiting.")
            else:
                print("\tCommand file does not contain any entries, exiting.")
        else:
            print("\n\t**************************")
            print("\t|   Parameters Invalid  |")
            print("\t**************************")
            print("\tCannot execute inject_pulsar commands, exiting.")

        print("\n\tDone.")
        print("\n**************************************************************************\n")

    # ******************************************************************************************

    def check_parameters(self, args):
        """
        Checks the parameters provided by the user.

        Parameters
        ----------

        args : []
            The arguments. These are ordered as follows:
            args[0]  = verbose flag
            args[1]  = Path to the command file.
            args[2]  = output directory.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        print("\n\t**************************")
        print("\t|  Checking Parameters   |")
        print("\t**************************")

        # There are 3 command line parameters - these must be checked
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
            args[0]  = verbose flag
            args[1]  = Path to the command file.
            args[2]  = output directory.

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
                print("\tVerbose parameter not the correct type (" + str(type(args[0])) + ") .")
            outcome = False

        # Command file path...
        if type(args[1]) != str:
            if not testing:
                print("\tCommand file path parameter not a string (" + str(type(args[1])) + ") .")
            outcome = False

        # Output directory...
        if type(args[2]) != str:
            if not testing:
                print("\tOutput directory parameter not a string (" + str(type(args[2])) + ") .")
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
            args[0]  = verbose flag
            args[1]  = Path to the command file.
            args[2]  = output directory.

        testing : boolean
                A flag that when true, suppresses output during testing.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        outcome = True

        # Lets check the directory paths provided by the user...
        if len(args[1]) > 0:
            if Common.file_exists(args[1]):
                outcome = True
            else:
                if not testing:
                    print("\tCommand file does not exist/could not be accessed.")
                return False

        # Check the predictor output directory is valid.
        if len(args[2]) > 0:
            outcome = InjectPulsarAutomator.check_dir_exists_or_create(args[2])

            if not outcome:
                if not testing:
                    print("\tOutput directory does not exist/could not be created.")
                return False

        return outcome

    # ******************************************************************************************

    @staticmethod
    def check_dir_exists_or_create(out_dir):
        """
        Checks if a directory exists. If it doesn't, we try to create it.
        If this method returns false, this operation failed. Otherwise
        True is returned.

        Parameters
        ----------
        :param out_dir: the directory to check for/create as appropriate.

        Returns
        -------
        True if the directory exists/was created, else false.
        """

        # The user should have supplied an output directory path. But, it may
        # not be valid. to check we first, try to create the directory. If the
        # create call fails, the directory path is invalid.
        if not os.path.exists(out_dir):
            print("\n\tOutput directory does not exist, trying to create...")
            try:
                os.makedirs(out_dir)
            except OSError:
                print("\n\tException encountered trying to create output directory.")
                return False
        else:
            return True  # Directory must exist.

        # If the directory creation call above did not fail, the output directory
        # should now exist. Check that this is the case...
        if not os.path.isdir(out_dir):
            print("\n\tOutput directory could not be created.")
            return False
        else:
            print("\n\tOutput directory exists.")
            return True

    # ******************************
    #
    # FILE HANDLING CODE
    #
    # ******************************

    @staticmethod
    def append_to_file(path, text):
        """
        Appends the provided text to the file at the specified path.

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
    InjectPulsarAutomator().main()
