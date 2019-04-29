"""
    **************************************************************************
    |                                                                        |
    |                  Create Fake Par Files Version 1.0                     |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    **************************************************************************
    |                                                                        |
    | Generates simple '.par' files for use with Tempo2. Multiple files      |
    | are created when a comma delimited set of periods is given. This tool  |
    | creates files that vary in terms of period, DM, acceleration only -    |
    | other fields are frozen (at least in this initial version of the code).|
    | Example file where only values between '< >' will be changed.          |
    |                                                                        |
    |                                                                        |
    | PSRJ             J0000-0000                                            |
    | RAJ              00:00:00.0             2.000e-05                      |
    | DECJ             00:00:00.0             3.000e-04                      |
    | DM               <CHANGE>               1.000e-02                      |
    | PEPOCH           56000.0                                               |
    | F0               <CHANGE>               5.000e-10                      |
    | TZRMJD           56000.0                                               |
    | TZRFREQ          1000.0                                                |
    | UNITS            TDB                                                   |
    | BINARY           DD                                                    |
    | PB               1.068160314236914                                     |
    | A1               7.196981485798689                                     |
    | TO               56000.266169418835                                    |
    |                                                                        |
    | The script stores the par files in a user specified directory.         |
    | Each par file is either saved using the name 'FakePulsar', and some    |
    | additional parameters, followed by the .par suffix e.g.,               |
    |                                                                        |
    | FakePulsar<number>_DM=<DM>_P0=<Period >ms_Z=<Acceleration>.par         |
    |                                                                        |
    | Running this code will overwrite existing par files for both pulsar    |
    | and non-pulsar examples if automatically generated file names match    |
    | the names of existing files.                                           |
    |                                                                        |
    | The code is compatible with python version 3.6.                        |
    |                                                                        |
    **************************************************************************
    | Required Arguments:                                                    |
    **************************************************************************
    |                                                                        |
    | -d (string) full path to the dir to store par files in (def=local dir).|
    | -m (float) the dispersion measure for the Par file (def=1.0).          |
    | -p (string) the periods in seconds to insert as a comma delimited      |
    |             string, e.g.                                               |
    |                         -p "1.0,2.0,10.0,30.0"                         |
    |                                                                        |
    **************************************************************************
    | Optional Arguments:                                                    |
    **************************************************************************
    |                                                                        |
    | -v (boolean) plots the pulse profile shape for viewing (def = FALSE).  |
    | -a (float) the acceleration in m/s/s. (default=0.0)                    |
    |                                                                        |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@manchester.ac.uk                                   |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | License:                                                               |
    **************************************************************************
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

import os
from ParFile import ParFile


# ******************************
#
# CLASS DEFINITION
#
# ******************************


class CreateFakeParFiles:
    """
    Description:

    This script generates '.par' files for use with the Tempo2 tool.
    The files themselves are somewhat contrived, with mostly fixed
    parameters. However using this tool you can vary the DM, period,
    and acceleration values written in to the .par files.
    """

    def __init__(self):
        """
        Initialises the class and class variables.
        """
        self.output_dir         = ""     # The directory to store created .par files in.
        self.dm                 = 1.0    # The default DM value.
        self.period_str         = ""     # String containing periods as provided by the user, e.g. "1.0,2.0,10.0,30.0".
        self.verbose            = False  # Verbose logging flag.
        self.arguments          = None
        self.store_in_local_dir = False  # When true tells the script to write .par files to the local directory.
        self.periods            = []     # The periods the user wants to generate .par files for.
        self.accel              = 0.0    # The acceleration value to use.

    # ******************************************************************************************

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    def main(self, argv=None):
        """Main method.

        Main entry point for the Application. Processes command line
        input and begins automating the the creation of .par files.

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
        parser.add_option("-d", action="store", dest="d", type=str,
                          help='Path to a valid output directory.', default="")

        parser.add_option("-m", action="store", dest="m", type=float,
                          help='Dispersion measure to insert into the file.', default=1.0)

        parser.add_option("-p", action="store", dest="p", type=str,
                          help='Comma delimited period string', default="")

        # OPTIONAL ARGUMENTS
        parser.add_option("-v", action="store_true", dest="v",
                          help='Verbose debugging flag (optional).', default=False)

        parser.add_option("-a", dest="a", type=float,
                          help='The acceleration to apply (optional).', default=0.0)


        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        self.output_dir = args.d
        self.dm         = args.m
        self.period_str = args.p
        self.verbose    = args.v
        self.accel      = args.a

        # Pre-process arguments to make unit testing easier.
        self.arguments = [args.v, args.d, args.m, args.p, args.a]

        # ****************************************
        #     Print command line arguments
        # ****************************************

        print("\n\t**************************")
        print("\t| Command Line Arguments |")
        print("\t**************************")
        print("\tDebug: " + str(self.verbose))
        print("\tOutput directory: " + str(self.output_dir))
        print("\tDM: "               + str(self.dm))
        print("\tPeriod string: "    + str(self.period_str))
        print("\tAcceleration: "      + str(self.accel))

        # Check the command line parameters are valid.
        if self.check_parameters(self.arguments):

            print("\n\t**************************")
            print("\t| Par Creation Underway  |")
            print("\t**************************")

            # If we get here, then the period string is valid. So parse and store for use:
            self.periods = CreateFakeParFiles.process_period_string(self.period_str)

            # for each period, we should create a par file.
            fake_pulsar_count = 1
            files_created = 0

            for period_in_seconds in self.periods:

                # Create a file name to write to! File name format:
                #
                # FakePulsar_<number>_DM=<DM>_P0=<Period (ms)>ms_Z=<Acceleration>.par

                period_ms = str(period_in_seconds * 1000.0)

                par = ParFile()
                par_nme = "FakePulsar" + str(fake_pulsar_count)

                # Use par file object to create valid output file name.
                file_name = par.create_valid_file_name(par_nme, self.dm, period_ms, self.accel)

                if file_name is not None:

                    files_created += self.create_par_file(file_name, self.output_dir, period_in_seconds,
                                                          self.dm, self.store_in_local_dir, self.accel)

                    fake_pulsar_count += 1
                else:
                    print("\tCould not construct par file name for period " + str(period_ms) + " ms.")

            print("\tFiles written: " + str(files_created))
            print("\tPar file creation completed.")

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
    # PAR CREATION
    #
    # ******************************

    def create_par_file(self, fname, output_dir, period, dm, local_dir, accel):
        """
        Creates the par files given some basic parameters.

        Parameters
        ----------
        :param fname: the name of the par file to create.
        :param output_dir: the output directory where the par file should be written to.
        :param period: the period in milliseconds to insert into the par file.
        :param dm: the DM to insert into the par file.
        :param local_dir: a flag that when set to true, indicates that par files should be stored
                          in the local directory.
        :param accel: the acceleration in m/s/s.

        Returns
        -------

        True if the file was created, else false.
        """

        output_path = ""
        if local_dir:
            output_path = fname
        else:
            output_path = output_dir + "/" + fname

        CreateFakeParFiles.clear_file(output_path)

        name    = "J0000-0000"
        ra      = "00:00:00.0"
        dec     = "00:00:00.0"
        pepoch  = "56000.0"
        tzrmjd  = "56000.0"
        tzrfreq = "1000.0"
        units   = "TBD"

        text = "PSRJ\t\t\t" + name + "\n"
        text += "RAJ\t\t\t\t" + ra + "\t\t\t2.000e-05\n"
        text += "DECJ\t\t\t" + dec + "\t\t\t3.000e-04\n"
        text += "DM\t\t\t\t" + str(dm) + "\t\t\t\t\t1.000e-02\n"
        text += "PEPOCH\t\t\t" + pepoch + "\n"
        text += "F0\t\t\t\t" + str(1.0 / period) + "\t\t\t\t\t5.000e-10\n"
        text += "TZRMJD\t\t\t" + tzrmjd + "\n"
        text += "TZRFREQ\t\t\t" + tzrfreq + "\n"
        text += "UNITS\t\t\t" + units

        # If acceleration included...
        if self.accel != 0.0:

            # Use the par file obejct to compute the binary parameters.
            pb, a1, t0 = ParFile.compute_binary_params(self.accel, period, float(pepoch))

            if pb is None and a1 is None and t0 is None:
                print("\tWARNING: Could not compute binary parameters for par file (PB, A1, T0).")
            else:
                text += "\nBINARY\t\t\t" + "DD" + "\n"
                text += "PB\t\t\t" + str(pb) + "\n"
                text += "A1\t\t\t" + str(a1) + "\n"
                text += "TO\t\t\t" + str(t0)

        CreateFakeParFiles.append_to_file(output_path, text)

        if os.path.isfile(output_path):
            return 1
        else:
            return 0

    # ******************************************************************************************

    # ******************************
    #
    # COMMAND LINE PROCESSING CODE
    #
    # ******************************

    @staticmethod
    def process_period_string(prd_str):
        """
        Splits a period string containing comma delimited numerical values.

        Parameters
        ----------

        :param prd_str: a comma delimited string of period values.

        Returns
        -------

         A float array if the string is correctly formatted, else None.
        """

        # The delimiter for string splitting...
        delim = ","
        output = []

        # The components of the string after splitting
        components = prd_str.split(delim)

        if len(components) <= 0:
            return []
        else:
            for c in components:
                try:
                    output.append(float(c))
                except ValueError:
                    print("\tPeriod string contains non-numeric characters!")
                    return []

        return output

    # ******************************************************************************************

    @staticmethod
    def check_period_string(prd_str):
        """
        Checks the period string parameter provided by the user.
        This should be a comma delimited string of floating-point values.

        Parameters
        ----------

        prd_str : []
            The period string which should be comma delimited.

        Returns
        -------
        True if the parameters are valid, else False.

        """
        output = CreateFakeParFiles.process_period_string(prd_str)

        if output == []:
            return False
        else:
            return True

    # ******************************************************************************************

    def check_parameters(self, args):
        """
        Checks the parameters provided by the user.

        Parameters
        ----------
        self : object
            The object pointer.

        args : []
            The arguments. These are ordered as follows:
            args[0] = verbose flag
            args[1] = output directory path
            args[2] = the DM
            args[3] = the period values to use.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        print("\n\t**************************")
        print("\t|  Checking Parameters   |")
        print("\t**************************")

        # There are eight command line parameters - these must be checked
        # to ensure the user doesn't do anything crazy. We check each parameter
        # in turn, in different ways including,
        #
        # 1. Type checking
        # 2. Formatting checks
        # 3. Boundary condition checks
        #
        # This means there are a lot of checks to do...

        outcome = True

        # Check the types are as expected.
        outcome = CreateFakeParFiles.check_parameter_types(args)

        if not outcome:
            print("\tOne or more parameters are not of the expected type.")
            return False

        outcome = CreateFakeParFiles.check_parameter_values(args)

        if not outcome:
            print("\tOne or more parameters values are not correctly formatted/have values outside of expected ranges.")
            return False

        # Check the output directory is valid.
        if len(args[1]) > 0:
            outcome = CreateFakeParFiles.check_dir_exists_or_create(args[1])

            if not outcome:
                return False
        else:
            self.store_in_local_dir = True
            print("\tUser wants to output files in the local directory.")


        if not outcome:
            print("\tOne or more parameter values do not adhere to boundary/range conditions.")
            return outcome

        print("\n\tParameter check complete.")

        return True

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
            args[1] = output directory path
            args[2] = the DM
            args[3] = the period values to use.
            args[4] = the acceleration to use.

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

        # Output directory
        if type(args[1]) != str:
            if not testing:
                print("\tOutput directory parameter not a string (" + str(type(args[1])) + ").")
            outcome = False

        # DM
        if type(args[2]) != float:
            if not testing:
                print("\tDM parameter not a float (" + str(type(args[2])) + ").")
            outcome = False

        # Periods
        if type(args[3]) != str:
            if not testing:
                print("\tPeriod parameter not a string (" + str(type(args[3])) + ").")
            outcome = False

        # Acceleration
        if type(args[4]) != float:
            if not testing:
                print("\tAcceleration parameter not a float (" + str(type(args[4])) + ").")
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
            args[1] = output directory path
            args[2] = the DM
            args[3] = the period values to use.
            args[4] = the acceleration to use.

        testing : boolean
                A flag that when true, suppresses output during testing.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        outcome = True

        # DM value
        if args[2] < 0.0:
            if not testing:
                print("\tThe DM value must be greater than or equal to zero.")
            outcome = False

        # Period string - we expect a comma delimited string of the format "<p1>,<p2>,...,<pn>"
        if len(args[3]) < 0:
            outcome = False
            if not testing:
                print("\tPeriod string parameter is empty.")
            outcome = False

        elif len(args[3]) > 0:

            result = CreateFakeParFiles.check_period_string(args[3])

            if not result:
                if not testing:
                    print("\tPeriod string formatting invalid.")
                outcome = False

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
            return True # Directory must exist.

        # If the directory creation call above did not fail, the output directory
        # should now exist. Check that this is the case...
        if not os.path.isdir(out_dir):
            print("\n\tOutput directory could not be created.")
            return False
        else:
            print("\n\tOutput directory exists.")
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
    CreateFakeParFiles().main()
