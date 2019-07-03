"""
***************************************************************************************
|                                                                                     |
| PredFile.py                                                                         |
|                                                                                     |
***************************************************************************************
| Description:                                                                        |
***************************************************************************************
|                                                                                     |
| Represents a .dat file (Tempo2 predictor file) object.                              |
|                                                                                     |
| .dat files should adhere to the following filename format:                          |
|                                                                                     |
| <ID>_DM=<DM>_P0=<P0>ms_OBS=<Obs>s_F1=<F1>_F2=<F2>_T=<TC>_F=<FC>_Z=<Accel>.dat       |
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
***************************************************************************************
| Author: Rob Lyon                                                                    |
| Email : robert.lyon@manchester.ac.uk                                                |
| web   : www.scienceguyrob.com                                                       |
***************************************************************************************
| License:                                                                            |
***************************************************************************************
|                                                                                     |
| Code made available under the GPLv3 (GNU General Public License), that              |
| allows you to copy, modify and redistribute the code as you see fit                 |
| (http://www.gnu.org/copyleft/gpl.html). Though a mention to the                     |
| original author using the citation above in derivative works, would be              |
| very much appreciated.                                                              |
|                                                                                     |
***************************************************************************************
"""

from Common import Common
from BaseFile import BaseFile

# ******************************
#
# CLASS DEFINITION
#
# ******************************


class PredFile(BaseFile):
    """
    Description:

    Represents a '.dat' Tempo2 predictor file.

    """

    def __init__(self):
        """
        Initialises the class variables.
        """

        # Parameters of the .par file used to generate the predictor file.
        self.dm = 0.0
        self.p0 = 0.0  # in milliseconds.
        self.name = ""

        # Tempo2 parameters
        self.obs_length = 0.0  # The length of the observation, passed to Tempo2.
        self.f1 = 0.0  # Frequency of first channel.
        self.f2 = 0.0  # Frequency of last channel.
        self.tcoeff = 0  # The number of time coefficients to be computed by Tempo2.
        self.fcoeff = 0  # The number of frequency coefficients to be computed by Tempo2.
        self.batch = 1000  # The maximum number of par files to process in a processing batch.
        self.mjd1 = 0.0  # The start time mjd used by Tempo2.
        self.mjd2 = 0.0  # The end time mjd used by Tempo2.
        self.telescope = ""  # The telescope name given to Tempo2.
        self.accel     = 0.0

    # ******************************************************************************************

    def read(self, pth, verbose):
        """
        Reads a .dat predictor file and loads metadata from the file name.
        name.

        Parameters
        ----------

        :param pth: the path to a valid '.dat' file.
        :param verbose: verbose logging flag.

        Returns
        --------

        :return: true if the file was read correctly, else false.
        """

        self.fpth = pth

        if pth is None:
            return False
        elif len(pth) <= 4:  # Must at least be something'.par'
            return False
        else:
            file_name = Common.get_file_name(pth)

            if file_name is None:
                return False
            else:

                # File name should be in this format (order matters):
                #
                # <NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms_OBS=<Obs Length (s)>_F1=<F1>_F2=<F2>_T=<TCOEFF>_F=<FCOEEF>_Z=<Accel>.dat
                #
                # The variable nme should not contain any underscores,
                # dm should be a float, and period_ms should also be a float
                # We check for these requirements here:

                if file_name.endswith(".dat"):
                    if "DM=" in file_name and "P0=" in file_name and "OBS=" in file_name and \
                                    "F1=" in file_name and "F2=" in file_name and "T=" in file_name and \
                                    "F=" in file_name and "Z=" in file_name:

                        components = self.tokenise(file_name, "_")

                        if len(components) == 9:

                            # Now check parameters are floats
                            try:
                                self.name = components[0]
                                self.dm = float(components[1].replace("DM=", ""))
                                self.p0 = float(components[2].replace("P0=", "").replace("ms", ""))
                                self.obs_length = int(components[3].replace("OBS=", "").replace("s", ""))
                                self.f1 = float(components[4].replace("F1=", ""))
                                self.f2 = float(components[5].replace("F2=", ""))
                                self.tcoeff = int(components[6].replace("T=", ""))
                                self.fcoeff = int(components[7].replace("F=", ""))
                                self.accel = float(components[8].replace("Z=", "").replace(".dat", ""))

                                # Now check values:

                                if self.dm <= 0:
                                    return False
                                if self.p0 <= 0:
                                    return False
                                if self.obs_length <= 0:
                                    return False
                                if self.f1 <= 0:
                                    return False
                                if self.f2 <= 0:
                                    return False
                                if self.tcoeff <= 0:
                                    return False
                                if self.fcoeff <= 0:
                                    return False
                                if self.f2 <= self.f1:
                                    return False

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

    def is_filename_valid(self, pth):
        """
        Returns true if a predictor filename is valid.

        Parameters
        ----------
        :param pth: the full path to the file.

        Returns
        ----------
        :return:  true if the filename is valid, else false.
        """
        if pth is None:
            return False
        elif len(pth) <= 4:  # Must at least be something'.dat'
            return False
        else:
            file_name = Common.get_file_name(pth)

            if file_name is None:
                return False
            else:

                # File name should be in this format (order matters):
                #
                # <NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms_OBS=<Obs Length (s)>_F1=<F1>_F2=<F2>_T=<TCOEFF>_F=<FCOEEF>_Z=<Accel>.dat
                #
                # The variable nme should not contain any underscores,
                # dm should be a float, and period_ms should also be a float
                # We check for these requirements here:

                if file_name.endswith(".dat"):
                    if "DM=" in file_name and "P0=" in file_name and "OBS=" in file_name and \
                                    "F1=" in file_name and "F2=" in file_name and "T=" in file_name and \
                                    "F=" in file_name and "Z=" in file_name:

                        components = self.tokenise(file_name, "_")

                        if len(components) == 9:

                            # Now check parameters are floats
                            try:
                                if float(components[1].replace("DM=", "")) <= 0:
                                    return False
                                elif float(components[2].replace("P0=", "").replace("ms", "")) <= 0:
                                    return False
                                elif int(components[3].replace("OBS=", "").replace("s", "")) <= 0:
                                    return False
                                elif float(components[4].replace("F1=", "")) <= 0:
                                    return False
                                elif float(components[5].replace("F2=", "")) <= 0:
                                    return False
                                elif int(components[6].replace("T=", "")) <= 0:
                                    return False
                                elif int(components[7].replace("F=", "")) <= 0:
                                    return False
                                elif float(components[5].replace("F2=", "")) <= float(components[4].replace("F1=", "")):
                                    return False

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

    def create_valid_file_name(self, nme, dm, period_ms, obslen, f1, f2, tc, fc, accel):
        """
        Creates a valid file name using a pre-defined format.

        Parameters
        ----------
        :param nme: the name for the pulsar/fake pulsar described by the par file.
        :param dm: the DM for the par file.
        :param period_ms: the period of for the par file in milliseconds.

        Returns
        ----------
        :return:  a string file name in the correct format.
        """

        # File name should be in this format (order matters):
        #
        # <NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms_OBS=<Obs Length (s)>s_F1=<F1>_F2=<F2>_T=<TCOEFF>_F=<FCOEEF>_Z=<Accel>.dat
        #
        # The variable nme should not contain any underscores,
        # dm should be a float, and period_ms should also be a float
        # We check for these requirements here:

        if nme is None or dm is None or period_ms is None:
            return None

        if "_" in nme:
            return None

        if len(nme) < 1:
            return None

        dm_float = 0.0
        period_float_ms = 0.0
        obslen_int = 0
        f1_float = 0.0
        f2_float = 0.0
        tc_int = 0
        fc_int = 0
        accel_float = 0.0

        try:
            dm_float = float(dm)
            period_float_ms = float(period_ms)
            obslen_int = int(obslen)
            f1_float = float(f1)
            f2_float = float(f2)
            tc_int = int(tc)
            fc_int = int(fc)
            accel_float = float(accel)
        except ValueError:
            print("Error parsing numerical values passed to create_valid_file_name() in PredFile.py - unable to cast"+\
                  "1 or more parameters to float types. Current values and data types for the variables to be cast to"+\
                  " floats:")
            print
            print("\tVariable: dm            value=" + str(dm)        + " type=" + str(type(dm)))
            print("\tVariable: period_ms     value=" + str(period_ms) + " type=" + str(type(period_ms)))
            print("\tVariable: obslen        value=" + str(obslen)    + " type=" + str(type(obslen)))
            print("\tVariable: f1            value=" + str(f1)        + " type=" + str(type(f1)))
            print("\tVariable: f2            value=" + str(f2)        + " type=" + str(type(f2)))
            print("\tVariable: tc            value=" + str(tc)        + " type=" + str(type(tc)))
            print("\tVariable: fc            value=" + str(fc)        + " type=" + str(type(fc)))
            print("\tVariable: accel         value=" + str(accel)     + " type=" + str(type(accel)))


            return None

        if dm_float <= 0:
            return None
        if period_float_ms <= 0:
            return None
        if obslen_int <= 0:
            return None
        if f1_float <= 0:
            return None
        if f2_float <= 0:
            return None
        if tc_int <= 0:
            return None
        if fc_int <= 0:
            return None
        if f2_float <= f1_float:
            return None

        return nme + "_DM=" + str(dm_float) + "_P0=" + str(period_float_ms) + "ms_OBS=" + str(obslen_int) + "s_F1=" + \
               str(f1_float) + "_F2=" + str(f2_float) + "_T=" + str(tc_int) + "_F=" + str(fc_int) + \
               "_Z=" + str(accel_float) + ".dat"

    # ******************************************************************************************
