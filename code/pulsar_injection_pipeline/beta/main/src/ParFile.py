"""
**************************************************************************
|                                                                        |
| ParFile.py                                                             |
|                                                                        |
**************************************************************************
| Description:                                                           |
**************************************************************************
|                                                                        |
| Represents a .par file object.                                         |
|                                                                        |
| Example par file content, where only values between '< >'              |
| will be changed.                                                       |
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
| BINARY		   DD                                                    |
| PB			   1.068160314236914                                     |
| A1			   7.196981485798689                                     |
| TO			   56000.266169418835                                    |
|                                                                        |
| Each par file is either saved using the name 'FakePulsar', and some    |
| additional parameters, followed by the .par suffix e.g.,               |
|                                                                        |
| FakePulsar<number>_DM=<DM>_P0=<Period >ms_Z=<Acceleration>.par         |
|                                                                        |
| Where <Number> is an integer that helps identify the par file, <DM>    |
| is a float representing the dispersion measure, <PO> is a float        |
| representing the period in milliseconds, and <Accel> is a float that   |
| describes the acceleration in m/s/s.                                   |
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
|                                                                        |
**************************************************************************
"""

from Common import Common
from BaseFile import BaseFile
from DelimitedFilename import DelimitedFilename

import math

# ******************************
#
# CLASS DEFINITION
#
# ******************************


class ParFile(BaseFile):
    """
    Description:

    Represents a Tempo2 '.par' parameter file.
    """

    def __init__(self):
        """
        Initialises the class and class variables.
        """
        self.name    = "J0000-0000"
        self.ra      = "00:00:00.0"
        self.dec     = "00:00:00.0"
        self.pepoch  = 56000.0
        self.tzrmjd  = 56000.0
        self.tzrfreq = 1000.0
        self.units   = "TBD"
        self.dm      = 1.0
        self.period  = 1000.0 # in milliseconds

        self.freq    = 1.0
        self.valid_file_name = False

        self.accel   = 0.0
        self.pb      = 0.0
        self.a1      = 0.0
        self.t0      = 0.0
        self.delimfnme = None
        self.binary = False

    # ******************************************************************************************

    def read(self, pth, verbose):
        """
        Reads a par file and loads the data into this object.

        Parameters
        ----------

        :param pth: the path to a valid Tempo2 '.par' file.
        :param verbose: verbose logging flag.

        Returns
        --------

        :return: true if the file was read correctly, else false.
        """
        self.fpth = pth

        if self.is_filename_valid(pth):
            self.valid_file_name = True
            self.fname = Common.get_file_name(self.fpth)

            self.delimfnme = DelimitedFilename()
            self.delimfnme.read(self.fname, "_")

            try:
                self.accel = float(self.delimfnme.get_component_value("Z"))

            except ValueError:
                self.accel = 0.0

        contents = Common.read_file(self.fpth)

        delimiter = "\t"

        if contents is None:
            return False
        else:
            if len(contents) > 0:

                updates = 0
                line_count = 0

                for line in contents:

                    # Update line count
                    line_count += 1

                    line_contents = self.tokenise_par_file_line(line.replace("\n", ""), delimiter)

                    if line_contents is not None:

                        updates += self.parse_par_line_tokens(line_contents)
                    else:
                        if verbose:
                            print("\tCould not read par file line:\n", line, "\n")

                if updates > 0:

                    if verbose:
                        lines_not_processed = line_count - updates
                        print("\tIn total", lines_not_processed, " line not used from the .par file.\n")

                    return True
                else:
                    return False
            else:
                return False

    # ******************************************************************************************

    def tokenise_par_file_line(self, line, delimiter):
        """
        Reads a line of text from a '.par' file, and returns a list
        of important string components.

        Parameters
        ----------

        :param line: the line of text
        :param delimiter: a string delimiter used to split the text

        Returns
        --------

        :return: the main components of the line of text.
        """

        if delimiter is None:
            return None  # What else can we do?

        tokens = self.tokenise(line, delimiter)

        if tokens is None:
            return None   # What else can we do?

        filtered_tokens = self.remove_empty_strings(tokens)

        if filtered_tokens is None:
            return None   # What else can we do?

        return filtered_tokens

    # ******************************************************************************************

    def parse_par_line_tokens(self, line):
        """
        Reads a line of components from a par file.

        Parameters
        ----------

        :param line: the line of text reduced to a list of tokens.

        Returns
        --------

        :return: 1 if the line contains usable information which is stored
                    in the object, otherwise 0.
        """

        if len(line) < 2:
            return 0
        else:

            if line[0] == "PSRJ":
                self.name = line[1]
            elif line[0] == "RAJ":
                self.ra = line[1]
            elif line[0] == "DECJ":
                self.dec = line[1]
            elif line[0] == "DM":
                try:
                    self.dm = float(line[1])
                except ValueError:
                    return 0
            elif line[0] == "PEPOCH":
                try:
                    self.pepoch = float(line[1])
                except ValueError:
                    self.pepoch = 56000.0  # Set to default.
                    return 0
            elif line[0] == "F0":
                try:
                    self.freq = float(line[1])
                    period_seconds = 1.0 / self.freq
                    self.period = period_seconds * 1000.0
                except ValueError:
                    return 0
            elif line[0] == "TZRMJD":
                try:
                    self.tzrmjd = float(line[1])
                except ValueError:
                    self.tzrmjd = 56000.0  # Set to default.
                    return 0
            elif line[0] == "TZRFREQ":
                try:
                    self.tzrfreq = float(line[1])
                except ValueError:
                    self.tzrfreq = 1000.0  # Set to default.
                    return 0
            elif line[0] == "UNITS":
                try:
                    self.units = line[1]
                except ValueError:
                    return 0
            elif line[0] == "P0":
                period_seconds = float(line[1])
                self.period = period_seconds * 1000.0
                self.freq = 1.0 / period_seconds
            elif line[0] == "BINARY":
                self.binary = True
            elif line[0] == "PB":
                self.pb = float(line[1])
            elif line[0] == "A1":
                self.a1 = float(line[1])
            elif line[0] == "T0":
                self.t0 = float(line[1])
            else:
                return 0

            return 1

    # ******************************************************************************************

    def is_filename_valid(self, pth):
        """
        Returns true if a par file filename is valid.

        Parameters
        ----------
        :param pth: the full path to the file.

        Returns
        ----------
        :return:  true if the filename is valid, else false.
        """
        if pth is None:
            return False
        elif len(pth) <= 4:  # Must at least be something'.par'
            return False
        else:
            file_name = Common.get_file_name(pth)

            if file_name is None:
                return False
            else:

                # File name should be in this format:
                #
                # <PULSAR NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms_Z=<Acceleration>.par
                #
                # Any file names adhering to this format should have the following
                # properties:
                #
                # 1. End in ".par"
                # 2. Have 3 underscore characters '_'
                # 3. Contain "DM=", "P0=" and "Z="
                # 4. Supplied DM, Period, and acceleration values must be floats.
                #
                # We check we meet this requirements here.

                if file_name.endswith(".par"):
                    if "DM=" in file_name and "P0=" in file_name and "Z=" in file_name:

                        components = self.tokenise(file_name, "_")

                        if len(components) == 4:

                            # Now check parameters are floats
                            try:
                                float(components[1].replace("DM=", ""))
                            except ValueError:
                                return False

                            try:
                                float(components[2].replace("P0=", "").replace("ms", ""))
                            except ValueError:
                                return False

                            try:
                                float(components[3].replace("Z=", "").replace(".par", ""))
                            except ValueError:
                                return False

                            return True

                        else:
                            return False
                    else:
                        return False
                else:
                    return False

    # ******************************************************************************************

    def create_valid_file_name(self, nme, dm, period_ms, accel):
        """
        Creates a valid file name using a pre-defined format.

        Parameters
        ----------
        :param nme: the name for the pulsar/fake pulsar described by the par file.
        :param dm: the DM for the par file.
        :param period_ms: the period of for the par file in milliseconds.
        :param accel: the acceleration.

        Returns
        ----------
        :return:  a string file name in the correct format.
        """

        # File name should be in this format (order matters):
        #
        # <PULSAR NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms_Z=<Acceleration>.par
        #
        # Thus the variable nme should not contain any underscores,
        # dm should be a float, and period_ms should also be a float
        # We check for these requirements here:

        if nme is None or dm is None or period_ms is None:
            return None

        if "_" in nme:
            return None

        if len(nme) < 1:
            return None

        dm_float  = 0.0
        period_float_ms = 0.0
        accel_float = 0.0

        try:
            dm_float = float(dm)
        except ValueError:
            return None

        try:
            period_float_ms = float(period_ms)
        except ValueError:
            return None

        try:
            accel_float = float(accel)
        except ValueError:
            return None

        return nme + "_DM=" + str(dm_float) + "_P0=" + str(period_float_ms) + "ms_Z=" + str(accel_float) + ".par"

    # ******************************************************************************************

    @staticmethod
    def compute_binary_params(accel, period_in_seconds, pepoch):
        """
        Computes the binary parameters that must be put into a par file,
        if adding acceleration into the test vectors.

        Parameters
        ----------
        :param accel: the acceleration value in m/s/s.
        :param period_in_seconds: the period in seconds.
        :param pepoch: the period epoch.

        Returns
        --------
        :return: a list of 3 elements, (pb,a1,t0), else None
        """

        # Code presented here based on an AWK script written by
        # Lina Levin - thanks Lina!

        if accel is None or period_in_seconds is None or pepoch is None:
            return None


        Mc = 1.4  # Mass of companion.
        Mp = 1.4
        Tsun = 4.92549e-6

        # Mass function
        f = math.pow(Mc, 3) / (math.pow((Mp + Mc), 2))

        pb_s = 2.0 * math.pi * math.pow((Tsun *f), 0.25) * math.pow(accel, -0.75) * math.pow((3.0 * math.pow(10, 8)), 0.75)
        pb_d = pb_s / 3600.0 / 24.0
        x = math.pow(pb_s, 0.6667) * math.pow(2 * math.pi, -0.6667) * math.pow(Tsun*f, 0.3333)

        # Period modulation
        t0Mod = 0.25 * (pb_s-300.9)/3600.0/24.0
        t0 = pepoch + t0Mod

        return pb_d, x, t0

    # ******************************************************************************************

    def __str__(self):
        """
        Overriden to string method.

        Parameters
        ----------
        N/A

        Returns
        -------

        The object as a string.
        """
        text = "PSRJ\t\t\t" + self.name + "\n"
        text += "RAJ\t\t\t\t" + self.ra + "\t\t\t2.000e-05\n"
        text += "DECJ\t\t\t" + self.dec + "\t\t\t2.000e-04\n"
        text += "DM\t\t\t\t" + self.dm + "\t\t\t\t\t1.000e-02\n"
        text += "PEPOCH\t\t\t" + self.pepoch + "\n"
        text += "F0\t\t\t\t" + str(1.0/self.period) + "\t\t\t\t\t5.000e-10\n"
        text += "TZRMJD\t\t\t" + self.tzrmjd + "\n"
        text += "TZRFREQ\t\t\t" + self.tzrfreq + "\n"
        text += "UNITS\t\t\t" + self.units

        # If acceleration included...
        if self.accel != 0.0:
            text += "\nBINARY\t\t\t" + "DD" + "\n"
            text += "PB\t\t\t" + self.pb + "\n"
            text += "A1\t\t\t" + self.a1 + "\n"
            text += "TO\t\t\t" + self.t0


        return text

    # ******************************************************************************************
