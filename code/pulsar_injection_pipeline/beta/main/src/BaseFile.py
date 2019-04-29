"""
**************************************************************************
|                                                                        |
| AscFile.py                                                             |
|                                                                        |
**************************************************************************
| Description:                                                           |
**************************************************************************
|                                                                        |
| Represents a basic file type object - intended to be used as a base    |
| class in a simple class hierarchy.                                     |
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
import abc

# ******************************
#
# CLASS DEFINITION
#
# ******************************


class BaseFile:
    """
    Description:

    Represents a basic file type object - intended to be used as a base
    class in a simple class hierarchy.

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        Initialises the class variables.
        """
        self.fname = ""   # File name of the .asc file
        self.fpth  = ""   # Full path to the .asc file

    # ******************************************************************************************

    @abc.abstractmethod
    def read(self, pth, verbose):
        """
        Reads a file.

        Parameters
        ----------

        :param pth: the path to a valid file.
        :param verbose: verbose logging flag.

        Returns
        --------

        :return: true if the file was read correctly, else false.
        """

        return

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

    @staticmethod
    def tokenise(text, token):
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

    @staticmethod
    def remove_empty_strings(text_list):
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

    @abc.abstractmethod
    def is_filename_valid(self, pth):
        """
        Returns true if the filename is valid.

        Parameters
        ----------
        :param pth: the full path to the file.

        Returns
        ----------
        :return:  true if the filename is valid, else false.
        """

        return

    # ******************************************************************************************

    @abc.abstractmethod
    def create_valid_file_name(self, nme):
        """
        Creates a valid file name using a pre-defined format.

        Parameters
        ----------
        :param nme: the name/identifier for the .asc file.

        Returns
        ----------
        :return:  a string file name in the correct format.
        """
        return

    # ******************************************************************************************
