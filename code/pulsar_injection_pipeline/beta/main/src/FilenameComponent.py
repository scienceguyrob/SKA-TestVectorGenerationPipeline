"""
**************************************************************************
|                                                                        |
| FilenameComponent.py                                                   |
|                                                                        |
**************************************************************************
| Description:                                                           |
**************************************************************************
|                                                                        |
| Represents an individual component of some character delimited         |
| filename. For instance, if we have a file name a_b_c.txt then there    |
| are three components 'a', 'b', 'c' which are string/char types. This   |
| class represents components and stores information regarding their     |
| type.                                                                  |
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
##
# FilenameComponent.py
#
#
# Description:
#
# Represents an individual component of some character delimited filename. For
# instance, if we have a file name a_b_c.txt then there are three components
# 'a', 'b', 'c' which are string/char types. This class represents components
# and stores information regarding their type.
#
# The code is compatible with python version 3.6.
#
#
# Author: Rob Lyon
# Email : robert.lyon@manchester.ac.uk
# web   : www.scienceguyrob.com
#
# License:
#
# Code made available under the GPLv3 (GNU General Public License), that
# allows you to copy, modify and redistribute the code as you see fit
# (http://www.gnu.org/copyleft/gpl.html). Though a mention to the
# original author using the citation above in derivative works, would be
# very much appreciated.

# ******************************
#
# CLASS DEFINITION
#
# ******************************


class FilenameComponent:
    """
    Description:

    Represents a basic file name text component, assuming
    the file is delimited by some character.

    """


    def __init__(self, cmp=None):
        """
        Initialises the class variables.

        Parameters
        ----------

        :param cmp: the file name component.

        """
        self.component = cmp  # File name of the .asc file
        self.type = "unknown"

        # Causes the object to determine it's own type upon init.
        self.type = self.get_component_type(self.component)

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
