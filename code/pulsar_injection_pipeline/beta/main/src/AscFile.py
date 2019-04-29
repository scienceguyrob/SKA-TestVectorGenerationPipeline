"""
**************************************************************************
|                                                                        |
| AscFile.py                                                             |
|                                                                        |
| These files will:                                                      |
|                                                                        |
| 1. contain pulse intensity values in ascii format. Each line in the    |
|    file corresponds to a phase bin value. For example,                 |
|                                                                        |
|    1.0                                                                 |
|    2.0                                                                 |
|    3.0                                                                 |
|    2.0                                                                 |
|    1.0                                                                 |
|                                                                        |
|    Contains 5 bins, with a max value of 3.0, and min of 1.0.           |
|                                                                        |
| 2. Have a file name that adheres to the format,                        |
|                                                                        |
|   <ID>_DC=<Duty Cycle>_BINS=<Bins>_FWHM=<FWHM>.asc                     |
|                                                                        |
|   where <ID> is a string that uniquely identifies the .asc file,       |
|   <Duty Cycle> is a float describing the fraction of the period that   |
|   the pulse is "on" for, <Bins> is an integer describing the number of |
|   phase bins in the profile, and <FWHM> is a float corresponding to    |
|   the full-width at half maximum (FWHM). A valid filename could be as  |
|   follows:                                                             |
|                                                                        |
|       Gaussian_DC=0.5_BINS=128_FWHM=64.asc                             |
**************************************************************************
| Description:                                                           |
**************************************************************************
|                                                                        |
| Represents a .asc file object.                                         |
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
#from DelimitedFilename import DelimitedFilename

# ******************************
#
# CLASS DEFINITION
#
# ******************************


class AscFile(BaseFile):
    """
    Description:

    Represents a '.asc' pulse profile file. This is a simple ascii file
    containing pulse profile files, with 1 value stored per line (a column
    file) i.e.

    1.0
    2.0
    3.0
    2.0
    1.0

    """

    def __init__(self):
        """
        Initialises the class variables.
        """
        self.name  = ""   # Name of the pulse
        self.freq  = ""   # The frequency the pulse was observed at, if applicable.
        self.dc    = 0.0  # The pulse duty cycle, in % in [0,1] i.e. 0.5 = 50%.
        self.bins  = 0    # The number of bins in the pulse profile.
        self.fwhm  = 0.0  # The FWHM of the pulse profile, in bins.
        self.valid_file_name = False
        self.data = []    # The profile data.
        #self.delimited_filename = None

    # ******************************************************************************************

    def read(self, pth, verbose):
        """
        Reads a .asc file and loads the data into this object. This
        also extracts metadata information from the .asc file's file
        name.

        Parameters
        ----------

        :param pth: the path to a valid '.asc' file.
        :param verbose: verbose logging flag.

        Returns
        --------

        :return: true if the file was read correctly, else false.
        """

        # Get the full path.
        self.fpth = pth

        if verbose:
            print("\n\tAttempt to read .asc file at: ", self.fpth)

        # First check the file name provided is valid.
        if self.is_filename_valid(pth):
            self.valid_file_name = True

            # If the filename is valid, get the filename from the full path.
            self.fname = Common.get_file_name(self.fpth)

            #self.delimited_filename = DelimitedFilename()
            #self.delimited_filename.read(self.fname, "_")

            # Attempt to parse the file name, extracting meta information. This
            # step will only return true if the file name is in the expected format.
            success = self.parse_asc_file_name_tokens(self.tokenise(self.fname, "_"))

            if not success:
                if verbose:
                    print("\tInvalid .asc file name, could not be parsed.")
                return False

            if verbose:
                print("\tValid .asc file name, proceeding to read.")
        else:
            # File name is invalid...
            if verbose:
                print("\tInvalid .asc file name, cannot read.")
            return False

        if verbose:
            print("\tAttempting to read .asc file: ", self.fname)

        # Try to read the file...
        contents = Common.read_file(self.fpth)

        if contents is None:
            if verbose:
                print("\tThe .asc file is empty!")
            return False
        else:
            if len(contents) > 0:

                line_count = 0

                if verbose:
                    print("\tParsing lines extracted from .asc file.")

                for line in contents:

                    # Update line count
                    line_count += 1

                    try:
                        self.data.append(float(line.replace("\r", "").replace("\n", "")))
                    except ValueError:
                        if verbose:
                            print("\tError parsing data in file, not all values are numerical.")
                        return False

                if len(contents) < 1:
                    if verbose:
                        print("\tThe .asc file is empty!")
                    return False
                else:

                    if self.bins == len(self.data):
                        return True
                    else:
                        if verbose:
                            print("\tBins specified in the file name not equal to the number of bins in the file!")
                            print("\tBins expected: ", self.bins, " Bins in data: ", len(self.data))
                        return False
            else:
                if verbose:
                    print("\tThe .asc file is empty!")
                return False

    # ******************************************************************************************

    def parse_asc_file_name_tokens(self, tokens):
        """
        Reads a the text components from a .asc file's file name.

        Parameters
        ----------

        :param tokens: the tokens comprising the file name.

        Returns
        --------

        :return: True if the tokens contain usable information which is stored
                    in the object, otherwise False.
        """

        # File name should be in this format (order matters):
        #
        # <IDENTIFIER>_<Freq., OPTIONAL>_<Duty Cycle, OPTIONAL>_<BINS, OPTIONAL>_<FWHM, OPTIONAL>.asc
        #
        # where,
        #
        # <Freq., OPTIONAL> has two components: <frequency>Mhz
        # <Duty cycle> has two components: DC=<Duty cycle>
        # <Bins> has two components: BINS=<Bins>
        # <FWHM> has two components: FWHM=<Duty cycle>
        #
        # File names adhering to this format should have the following properties:
        #
        # 1. End in ".asc".
        # 2. Have at least 1 underscore, and at most 4 underscore characters.
        # 3. Supplied duty cycle, and FWHM values must be floats, the bins value must be an integer.
        if tokens is not None:

            tokens_length = len(tokens)

            # Should be at least 1 token, at most 5
            if 0 < tokens_length < 6:

                # Here we use a dictionary to store key:value pairs found in the filename.
                # This makes it easier to parse irrespective of pair ordering in the filename.
                component_dic = {}

                # The first component should always be the identifier.
                component_dic["nme"] = tokens[0]
                self.name = tokens[0]

                # Return if the tokens only contain an identifier...
                if tokens_length == 1:
                    return True

                # Populate the dictionary... only need to start from index 1, as
                # index 0 should be the identifier.
                for c in tokens[1:]:

                    t = c.replace(".asc", "")
                    if "MHz" in c:
                        component_dic["freq"] = t.replace("MHz", "")  # Remove prefixes/suffixes to get values.
                    elif c.startswith("DC="):
                        component_dic["dc"] = t.replace("DC=", "")  # Remove prefixes/suffixes to get values.
                    elif c.startswith("BINS="):
                        component_dic["bins"] = t.replace("BINS=", "")  # Remove prefixes/suffixes to get values.
                    elif c.startswith("FWHM="):
                        component_dic["fwhm"] = t.replace("FWHM=", "")  # Remove prefixes/suffixes to get values.
                    else:
                        return False  # Unknown token

                # Now simply parse the values to ensure they are of the correct type.
                if "freq" in component_dic:
                    try:
                        self.freq = float(component_dic["freq"])
                    except ValueError:
                        return False

                if "dc" in component_dic:
                    try:
                        self.dc = float(component_dic["dc"])
                    except ValueError:
                        return False

                if "bins" in component_dic:
                    try:
                        self.bins = int(component_dic["bins"])
                    except ValueError:
                        return False

                if "fwhm" in component_dic:
                    try:
                        self. fwhm = float(component_dic["fwhm"])
                    except ValueError:
                        return False
                return True
            else:
                return False
        else:
            return False

    # ******************************************************************************************

    def is_filename_valid(self, pth):
        """
        Returns true if the .asc filename is valid.

        Parameters
        ----------
        :param pth: the full path to the file.

        Returns
        ----------
        :return:  true if the filename is valid, else false.
        """

        if pth is None:
            return False
        elif len(pth) <= 4:  # Must at least be something'.asc'
            return False
        else:

            file_name = Common.get_file_name(pth)

            if file_name is None:
                return False
            else:

                # File name should be in this format (order matters as far as the user is concerned):
                #
                # <IDENTIFIER>_<Freq., OPTIONAL>_<Duty Cycle, OPTIONAL>_<BINS, OPTIONAL>_<FWHM, OPTIONAL>.asc
                #
                # where,
                #
                # <Freq., OPTIONAL> has two components: <frequency>Mhz
                # <Duty cycle> has two components: DC=<Duty cycle>
                # <Bins> has two components: BINS=<Bins>
                # <FWHM> has two components: FWHM=<Duty cycle>
                #
                #
                #
                # Thus there is only 1 mandatory component to the name format, which is the identifier.
                #
                # Any file names adhering to this format should have the following
                # properties:
                #
                # 1. End in ".asc".
                # 2. Have at least 1 underscore, and at most 4 underscore characters.
                # 3. Supplied duty cycle, and FWHM values must be floats, the bins value must be an integer.
                #
                # We check we meet these requirements here.

                if file_name.endswith(".asc"):

                    if "_" in file_name:
                        # Could be <IDENTIFIER>_....asc

                        components = self.tokenise(file_name.replace(".asc", ""), "_")

                        # If there is an underscore in the filename, yet we have
                        # empty components, then the filename format is invalid. It must
                        # be something like example_.asc which is incorrect.
                        if "" in components:
                            return False

                        # Here we use a dictionary to store key:value pairs found in the filename.
                        # This makes it easier to parse irrespective of pair ordering in the filename.
                        component_dic = {}

                        # The first component should always be the identifier.
                        component_dic["nme"] = components[0]

                        # Populate the dictionary...
                        for c in components:
                            if "MHz" in c:
                                component_dic["freq"] = c.replace("MHz", "")  # Remove prefixes/suffixes to get values.
                            elif c.startswith("DC="):
                                component_dic["dc"] = c.replace("DC=", "")  # Remove prefixes/suffixes to get values.
                            elif c.startswith("BINS="):
                                component_dic["bins"] = c.replace("BINS=", "") # Remove prefixes/suffixes to get values.
                            elif c.startswith("FWHM="):
                                component_dic["fwhm"] = c.replace("FWHM=", "") # Remove prefixes/suffixes to get values.

                        # The first part of the filename should be the asc file
                        # name (identifier), and if we reach this part of the code,
                        # there should also be optional details provided. If not, we
                        # return false right away...
                        if len(component_dic) < 2:
                            return False

                        # Now we check the number of values in the dictionary, against what we
                        # expect to see according to the number of underscores in the filename.
                        # If there are 4 underscores, we should have 5 values, if there are 3
                        # underscores we should have 4 values and so on....
                        if len(component_dic)-1 != file_name.count('_'):
                            return False

                        # Now simply parse the values to ensure they are of the correct type.
                        if "freq" in component_dic:
                            try:
                                float(component_dic["freq"])
                            except ValueError:
                                return False

                        if "dc" in component_dic:
                            try:
                                float(component_dic["dc"])
                            except ValueError:
                                return False

                        if "bins" in component_dic:
                            try:
                                int(component_dic["bins"])
                            except ValueError:
                                return False

                        if "fwhm" in component_dic:
                            try:
                                float(component_dic["fwhm"])
                            except ValueError:
                                return False

                        return True

                    else:
                        # Should just be <IDENTIFIER>.asc. There are no requirements on exactly
                        # what <IDENTIFIER> should contain, so just accept whatever user supplies.
                        return True
                else:
                    return False

    # ******************************************************************************************

    def create_valid_file_name(self, nme, freq=None, dc=None, bins=None, fwhm=None):
        """
        Creates a valid file name using a pre-defined format.

        Parameters
        ----------
        :param nme: the name/identifier for the .asc file.
        :param freq: the frequency the profile was observed at, if applicable.
        :param dc: the duty cycle of the pulse, if applicable.
        :param bins: the number of bins in the profile, if applicable.
        :param fwhm: the FWHM for the pulse, if applicable.

        Returns
        ----------
        :return:  a string file name in the correct format.
        """

        # File name should be in this format (order matters):
        #
        # <IDENTIFIER>_<Freq., OPTIONAL>_<Duty Cycle, OPTIONAL>_<BINS, OPTIONAL>_<FWHM, OPTIONAL>.asc
        #
        # where,
        #
        # <Freq., OPTIONAL> has two components: <frequency>Mhz
        # <Duty cycle> has two components: DC=<Duty cycle>
        # <Bins> has two components: BINS=<Bins>
        # <FWHM> has two components: FWHM=<Duty cycle>

        if nme is None:
            return None

        if len(nme) < 1:
            return None

        # Most simple valid file name e.g. "example.asc"
        if freq is None and dc is None \
                and bins is None and fwhm is None:
            return nme + ".asc"

        # Now we test that user supplied values are valid.

        freq_float = 0
        dc_float   = 0.0
        bins_int   = 0.0
        fwhm_float = 0.0

        if freq is not None and dc is None \
                and bins is None and fwhm is None:
            try:
                freq_float = float(freq)
            except ValueError:
                return None

            return nme + "_" + str(freq_float) + "MHz" + ".asc"

        elif freq is not None and dc is not None \
                and bins is None and fwhm is None:
            try:
                freq_float = float(freq)
                dc_float = float(dc)
            except ValueError:
                return None

            return nme + "_" + str(freq_float) + "MHz" + "_DC=" + str(dc_float) + ".asc"

        elif freq is not None and dc is not None \
                and bins is not None and fwhm is None:
            try:
                freq_float = float(freq)
                dc_float = float(dc)
                bins_int = int(bins)
            except ValueError:
                return None

            return nme + "_" + str(freq_float) + "MHz" + "_DC=" + str(dc_float) +\
                   "_BINS=" + str(bins_int) + ".asc"

        elif freq is not None and dc is not None \
                and bins is not None and fwhm is not None:
            try:
                freq_float = float(freq)
                dc_float = float(dc)
                bins_int = int(bins)
                fwhm_float = float(fwhm)
            except ValueError:
                return None

            return nme + "_" + str(freq_float) + "MHz" + "_DC=" + str(dc_float) +\
                   "_BINS=" + str(bins_int) + "_FWHM=" + str(fwhm_float) + ".asc"
        else:
            return None

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

        text = ""
        for d in self.data:
            text += str(d) + "\n"

        return text

    # ******************************************************************************************
