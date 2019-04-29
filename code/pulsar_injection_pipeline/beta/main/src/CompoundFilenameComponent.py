"""
**************************************************************************
|                                                                        |
| CompoundFilenameComponent.py                                           |
|                                                                        |
**************************************************************************
| Description:                                                           |
**************************************************************************
|                                                                        |
| Represents an individual component of some character delimited         |
| filename. For instance, if we have a file name a_b_c.txt then there    |
| are three components 'a', 'b', 'c' which are string/char types. This   |
| class represents components and stores information regarding their     |
| type. This class is also able to process compound components, which    |
| are themselves sub-divided according to some delimiter, for example,   |
|                                                                        |
| a_b=1.0_c.txt                                                          |
|                                                                        |
| where "b=1.0" is compound, and separable by the equals character.      |
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

from FilenameComponent import FilenameComponent


# ******************************
#
# CLASS DEFINITION
#
# ******************************


class CompoundFilenameComponent(FilenameComponent):
    """
    Description:

    Represents a basic file name text component, assuming
    the file is delimited by some character. Capable of
    processing compound filename components, sub-dividable
    by some delimiter.

    """


    def __init__(self, cmp=None, delim="="):
        """
        Initialises the class variables.

        Parameters
        ----------

        :param cmp: the file name component.
        :param delim: the delimiter used to sub-divide the component.

        """
        self.component = cmp  # File name of the .asc file
        self.delimiter = delim
        self.type = "unknown"

        # Variables used if component can be sub-divided.
        self.compound = False
        self.compound_prefix = ""

        # First check if this is the case.
        self.compound = self.is_compound(self.component, self.delimiter)

        if self.compound:
            # Split according to the delimiter

            tokens = self.tokenise(self.component, self.delimiter)

            if tokens is not None or len(tokens) == 2:

                self.compound_prefix = tokens[0]
                self.component = tokens[1]

                # Get component type.
                self.type = self.get_component_type(self.component)

            else:
                self.type = "Unknown"
        else:

            # Causes the object to determine it's own type upon init.
            self.type = self.get_component_type(self.component)

    # ******************************************************************************************

    def is_compound(self, cmp, delim):
        """
        Determines the data type of the component.

        Parameters
        ----------
        :param cmp: the file name component.
        :param delim: the delimiter used to sub-divide the component.

        Returns
        ----------
        :return:  the type as a string, either 'float', 'int', 'string', 'unknown', 'None'
        """

        if delim is None or cmp is None:
            return False

        if len(delim) < 1 or len(cmp) < 3:
            return False

        if len(cmp.split(delim)) == 2:
            return True
        else:
            return False

    # ******************************************************************************************

    def get_component_type(self, cmp):
        """
        Determines the data type of the component.

        Parameters
        ----------
        :param cmp: the file name component.

        Returns
        ----------
        :return:  the type as a string, either 'float', 'int', 'string', 'unknown', 'None'
        """

        # Some basic error checking first...
        if cmp is None:
            return "none"
        elif len(cmp) <= 0:
            return "none"

        try:
            int(cmp)
            return "int"
        except ValueError:
            pass

        try:
            float(cmp)
            return "float"
        except ValueError:
            pass

        try:
            str(cmp)
            return "string"
        except ValueError:
            pass

        return "unknown"

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
