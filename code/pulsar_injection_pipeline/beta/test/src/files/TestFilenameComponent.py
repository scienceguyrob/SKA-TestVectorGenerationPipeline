"""
**************************************************************************

 TestFilenameComponent.py

**************************************************************************
 Description:

 Tests the object that represents the components of a character
 delimited filename.

**************************************************************************
 Author: Rob Lyon
 Email : robert.lyon@manchester.ac.uk
 web   : www.scienceguyrob.com

**************************************************************************
 Required Command Line Arguments:

 N/A

**************************************************************************
 Optional Command Line Arguments:

 N/A

**************************************************************************
 License:

 Code made available under the GPLv3 (GNU General Public License), that
 allows you to copy, modify and redistribute the code as you see fit
 (http://www.gnu.org/copyleft/gpl.html). Though a mention to the
 original author using the citation above in derivative works, would be
 very much appreciated.

**************************************************************************
"""
import os
import unittest

from code.pulsar_injection_pipeline.beta.main.src.FilenameComponent import FilenameComponent


# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestFilenameComponent(unittest.TestCase):
    """
    The tests for the class.
    """

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_get_component_type(self):
        """Tests the method that determines the filename component type."""

        fnc = FilenameComponent(None)

        self.assertEqual(fnc.get_component_type(None)      , "none")
        self.assertEqual(fnc.get_component_type("")        , "none")
        self.assertEqual(fnc.get_component_type("a")       , "string")
        self.assertEqual(fnc.get_component_type("1")       , "int")
        self.assertEqual(fnc.get_component_type("1.0")     , "float")
        self.assertEqual(fnc.get_component_type("1a")      , "string")
        self.assertEqual(fnc.get_component_type("1.0a")    , "string")
        self.assertEqual(fnc.get_component_type("1True")   , "string")
        self.assertEqual(fnc.get_component_type("1.0False"), "string")


    # ****************************************************************************************************


    # ****************************************************************************************************

    # ******************************
    #
    # Test Setup & Teardown
    #
    # ******************************

    # preparing to test
    def setUp(self):
        """ Setting up for the test """

    # ****************************************************************************************************

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    # ****************************************************************************************************

    if __name__ == "__main__":
        unittest.main()
