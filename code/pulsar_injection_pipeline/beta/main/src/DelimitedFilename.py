"""
**************************************************************************
|                                                                        |
| DelimitedFilename.py                                                   |
|                                                                        |
**************************************************************************
| Description:                                                           |
**************************************************************************
|                                                                        |
| Represents a basic file name type object - intended to be used to form |
| valid test vector pipeline file names, and check file names are valid. |
|                                                                        |
| The code is compatible with python version 3.6.                        |
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
from CompoundFilenameComponent import CompoundFilenameComponent

# ******************************
#
# CLASS DEFINITION
#
# ******************************


class DelimitedFilename:
    """
    Description:

    Represents a basic file name object - meant to represent the
    file name formats created for .asc, .dat, .pred, and .fil files.

    """

    def __init__(self, nme="", delim="_"):
        """
        Initialises the class variables.

        Parameters
        ----------

        :param nme: the file name.
        :param delim: the delimiter used to split the file name.
        """
        self.fname = nme        # File name of the .asc file
        self.delimiter = delim  # Default for ur use case.
        self.components = []    # A list of CompoundFilenameComponent objects

    # ******************************************************************************************

    def read(self, fname, delimiter):
        """
        Reads a file.

        Parameters
        ----------

        :param fname: the filename.
        :param delimiter: the delimiter used to split the file name.

        Returns
        --------

        :return: true if the file was read correctly, else false.
        """
        self.components = []

        if delimiter is None:
            return False  # What else can we do?

        delim_count = str(fname).count(delimiter)

        # remove file extension and tokenise
        tokens = self.tokenise(self.remove_extension(fname), delimiter)

        if tokens is None:
            return False   # What else can we do?

        filtered_tokens = self.remove_empty_strings(tokens)

        if filtered_tokens is None or len(filtered_tokens) <= delim_count:
            return False   # What else can we do?

        # Now we read the string tokens and build some new objects
        for ft in filtered_tokens:
            self.components.append(CompoundFilenameComponent(ft, "="))

        return True

    # ******************************************************************************************

    def get_component_value(self, prefix):

        for c in self.components:

            if c.compound_prefix == prefix:
                return c.component

        return None

    # ******************************************************************************************

    def remove_extension(self, fname):

        if fname is None:
            return None
        elif len(fname) < 3:
            return None
        else:
            return fname.rsplit('.', 1)[0]

    # ******************************************************************************************

    def tokenise_file_name(self, text, delimiter):
        """
        Reads the file name, returns it as string tokens,
        split according to the supplied delimiter.

        Parameters
        ----------

        :param text: the line of text
        :param delimiter: a string delimiter used to split the text

        Returns
        --------

        :return: the main components of the line of text, else None if
                 the text is invalid or if there is an error.
        """

        if delimiter is None:
            return None  # What else can we do?

        tokens = self.tokenise(text, delimiter)

        if tokens is None:
            return None   # What else can we do?

        filtered_tokens = self.remove_empty_strings(tokens)

        if filtered_tokens is None:
            return None   # What else can we do?

        return filtered_tokens

    # ******************************************************************************************

    def tokenise(self, text, token):
        """
        Splits a string using the supplied token, produces a
        list of strings.

        Parameters
        ----------
        :param text: the text string to split.
        :param token: the token to use to split the string.

        Returns
        ----------
        :return:  a list of strings.
        """
        if token is None or text is None:
            return None
        elif token is "" or text is "":
            return None
        else:

            tokens = text.split(token)

            if len(tokens) > 0:
                return tokens
            else:
                return None

    # ******************************************************************************************

    def remove_empty_strings(self, text_list):
        """
        Removes empty strings, from a list of strings.

        Parameters
        ----------
        :param text_list: a list of strings.

        Returns
        ----------
        :return:  a list of strings which does not contain empty strings.
        """
        return list(filter(None, text_list))

    # ******************************************************************************************
