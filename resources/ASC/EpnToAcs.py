## @package ASC
# A module used to convert pulsar EPN database entries, into plain
# text ascii files describing pulse profile intensity scaled to within
# the range [0,255]. These plain text files will then be used as inputs
# in to the inject_pulsar application.
#
# Author: Rob Lyon
# Email : robert.lyon@manchester.ac.uk
# web   : www.scienceguyrob.com

# Start normal non-doxygen docstring...
"""
    **************************************************************************
    |                                                                        |
    |                        EPN to ASC Version 1.0                          |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Extracts pulse profile data from EPN database files, and writes the    |
    | profile data out to a new .asc file. The profiles are written out as   |
    | a single line of comma delimited ascii text. Pulse profiles are        |
    | normalised to the range [0,255] before being written out.              |
    |                                                                        |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@manchester.ac.uk                                   |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | Required Command Line Arguments:                                       |
    |                                                                        |
    | -e (string) full path to the directory containing EPN files.           |
    |                                                                        |
    | -a (string) full path to the directory to store ACN files in.          |
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

import os
import sys

# ******************************
#
# CLASS DEFINITION
#
# ******************************

## EPN to ASC Version 1.0
#
# Description:
#
# Extracts pulse profile data from EPN database files, and writes the
# profile data out to a new .asc file. The profiles are written out as
# a single line of comma delimited ascii text. Pulse profiles are
# normalised to the range [0,255] before being written out.
#
# EPN files consist of space delimited columns of data, for example:
#
#     0 0 0 -0.0136168
#     0 0 1 0.000744573
#     0 0 2 0.00829874
#     0 0 3 -0.00871086
#
#     The 4th 'column' is the I stokes parameter, or pulse intensity. This is the
#     data that this script extracts, and normalises. The data is written out to
#     a new file as a single line of text. For example the data above would be written
#     out as:
#
#     -0.0136168,0.000744573,0.00829874,-0.00871086
#
#     which is comma delimited.
#
# Author: Rob Lyon
# Email : robert.lyon@manchester.ac.uk
# web : www.scienceguyrob.com
#
# Required Command Line Arguments:
#
# -e (string) full path to the directory containing EPN files.
#
# -a (string) full path to the directory to store ACN files in.
#
# Optional Command Line Arguments:
#
# -v (boolean) verbose debugging flag.
#
#
# License:
#
# Code made available under the GPLv3 (GNU General Public License), that
# allows you to copy, modify and redistribute the code as you see fit
# (http://www.gnu.org/copyleft/gpl.html). Though a mention to the
# original author using the citation above in derivative works, would be
# very much appreciated.
class EpnToAsc:
    """
    Converts EPN database entries into plain text ascii files describing
    pulse profile intensity scaled to within the range [0,255]. These plain
    text files will then be used as inputs in to the inject_pulsar application.

    EPN files consist of space delimited columns of data, for example:

    0 0 0 -0.0136168
    0 0 1 0.000744573
    0 0 2 0.00829874
    0 0 3 -0.00871086

    The 4th 'column' is the I stokes parameter, or pulse intensity. This is the
    data that this script extracts, and normalises. The data is written out to
    a new file as a single line of text. For example the data above would be written
    out as:

    -0.0136168,0.000744573,0.00829874,-0.00871086

    which is comma delimited.
    """

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    ## The main method for the class.
    # Main entry point for the Application. Processes command line
    # input and begins extracting data from EPN files.
    #
    #  @param self The object pointer.
    #  @param argv The unused arguments.
    def main(self, argv=None):
        """Main method.

        Main entry point for the Application. Processes command line
        input and begins extracting data from EPN files.

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
        parser.add_option("-e", action="store", dest="epnPath",
                          help='Path to a directory containing EPN files.', default="")

        parser.add_option("-a", action="store", dest="outputPath",
                          help='Path to a directory to write asc files to.', default="")


        # OPTIONAL ARGUMENTS
        parser.add_option("-v", action="store_true", dest="verbose",
                          help='Verbose debugging flag (optional).', default=False)

        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        self.verbose    = args.verbose
        self.epnPath    = args.epnPath
        self.outputDir  = args.outputPath

        # ****************************************
        #   Print command line arguments & Run
        # ****************************************

        print("\n\t**************************")
        print("\t| Command Line Arguments |")
        print("\t**************************")
        print("\tDebug:" + str(self.verbose))
        print("\tEPN file input directory:" + str(self.epnPath))
        print("\tASC file output directory:" + str(self.outputDir))

        # First check user has supplied an EPN input director path ...
        if not self.outputDir:
            print("\n\tYou must supply a valid EPN input directory file via the -e flag.")
            print("\tExiting...")
            sys.exit()
        else:
            # User has passed in an input directory, now we need to check that
            # it is valid.
            if os.path.exists(self.epnPath) is False:
                print("\n\tSupplied EPN input directory invalid!")
                print("\tExiting...")
                sys.exit()

        # Now the user may have supplied an output directory path, but it may
        # not be valid. So first try to create the directory, if it doesn't
        # already exist. If the create fails, the directory path must be invalid,
        # so exit the application.
        if os.path.exists(self.outputDir) is False:
            try:
                os.makedirs(self.outputDir)
            except OSError as exception:
                print("\n\tException encountered trying to create ACN file output directory - Exiting!")
                sys.exit()

        # If the directory creation call above did not fail, the output directory
        # should now exist. Check that this is the case...
        if os.path.isdir(self.outputDir) is False:
            print("\n\tACN file output directory invalid - Exiting!")
            sys.exit()

        # Now we know the input files exist...

        # ****************************************
        #        File parsing section
        # ****************************************

        # Read parsed pulsar catalog file, extract useful variables:
        # Period, Frequency, DM, pulse width
        print("\tParsing files...")

        # Loop through the specified directory
        for root, subFolders, filenames in os.walk(self.epnPath):
            # for each file
            for filename in filenames:
                path = os.path.join(root, filename)  # Gets full path to the candidate.

                if ".acn" in path:

                    if self.verbose:
                        print("Processing:" + str(path))

                    self.readEPNFile(path, filename, self.outputDir)


        print("\n\tDone.\n")
        print("\n**************************************************************************\n")

    # ****************************************************************************************************

    ## Reads an EPN file, extracts pulse profile data.
    # This method reads an EPN database file, and isolates the data
    # within it describing the I stokes parameter (total pulse intensity).
    # The data is then scaled from [0,255], and finally written out as a
    # single line of text to a single .asc file.
    #
    #  @param self The object pointer.
    #  @param path The full string path to the EPN file.
    #  @param filename The full string filename of the EPN file including its file extension.
    #  @param outputDir The full string path to the output directory to store extracted data in.
    def readEPNFile(self, path, filename, outputDir):
        """Reads an EPN file, extracts pulse profile data.

        This method reads an EPN database file, and isolates the data
        within it describing the I stokes parameter (total pulse intensity).
        The data is then scaled from [0,255], and finally written out as a
        single line of text to a single .asc file.

        Parameters
        ----------
        self : object
            The object pointer.
        path : str
            The full path to the EPN file.
        filename : str
            The filename of the EPN file including its file extension.
        outputDir : str
            The full path to an output directory where extracted EPN data
            can be written to.

        Examples
        --------
        >>> readEPNFile("/Users/rob/EPN/J0014+4746_408.acn","file_1.acn","/Users/rob/ASC")

        which will create a new file J0014+4746_408.asc, in /Users/rob/ASC.
        """

        print("\tProcessing: " + str(path))
        data = []
        self.epnFile = open(path, 'r') # Read only access

        # For each line in the file, split on whitespace...
        for line in self.epnFile.readlines():

            components = line.rstrip('\r').split()

            # If line non empty
            if len(line) > 0:
                # If there are more than 0 components after splitting on whitespace...
                if len(components) > 0:
                    #print components

                    intensityValue = components[3]  # Column 4
                    data.append(float(intensityValue))

        self.epnFile.close()

        # Scale the data
        newData = self.scale(data)

        # Extract first element of new data, and store in output string.
        # I do this, as its then easier to append more data items to the
        # output string in CSV format.
        newDataStr = str(newData[0])

        for d in newData[1:len(data)]:

            # Now easier to append data, just have to prefix with a comma...
            newDataStr += "\n" + str(d)

        # Where to write new data to...
        outputPath = outputDir + "/" + filename

        # Save profile.
        self.appendToFile(outputPath.replace(".acn", ".asc"), newDataStr)

    # ******************************************************************************************

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

    # ****************************************************************************************************

    ## Scales data to within the range [0,255].
    #
    #  @param self The object pointer.
    #  @param data A list of numerical data items.
    #  @returns a scaled list of numbers.
    def scale(self, data):
        """Scales data to within the range [0,255].

        Parameters
        ----------
        self : object
            The object pointer.
        data : list
            A list of numerical data items.

        Returns
        -------
        list
            a list of scaled numerical values.

        Examples
        --------
        >>> a=[1,2,3]
        >>> newData = scale(a)

        """
        min_ = min(data)
        max_ = max(data)

        newMin = 0;
        newMax = 255

        newData = []

        for n in range(len(data)):

            value = data[n]
            x = (newMin * (1-((value-min_) / (max_-min_)))) + (newMax * ((value-min_) / (max_-min_)))
            newData.append(x)

        return newData

    # ****************************************************************************************************

if __name__ == '__main__':
    EpnToAsc().main()
