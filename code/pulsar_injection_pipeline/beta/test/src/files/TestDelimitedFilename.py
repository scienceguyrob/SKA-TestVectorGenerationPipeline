"""
**************************************************************************

 TestDelimitedFilename.py

**************************************************************************
 Description:

 Tests the object that represents a delimited filename.

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

from code.pulsar_injection_pipeline.beta.main.src.DelimitedFilename import DelimitedFilename


# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestDelimitedFilename(unittest.TestCase):
    """
    The tests for the class.
    """

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_read(self):
        """Tests the method that reads the filename."""

        dfn = DelimitedFilename(None, None)

        self.assertFalse(dfn.read(None, None))
        self.assertFalse(dfn.read("", None))
        self.assertFalse(dfn.read(None, ""))
        self.assertFalse(dfn.read("", ""))
        self.assertFalse(dfn.read("", "_"))
        self.assertFalse(dfn.read("a", "_"))
        self.assertFalse(dfn.read("aa", "_"))
        self.assertFalse(dfn.read("aaa_.dat", "_"))


        self.assertTrue(dfn.read("aaa", "_"))  # Fname length at least plausibly contains enough info
        self.assertTrue(dfn.read("aaa.txt", "_"))
        self.assertTrue(dfn.read("aaa.dat", "_"))

        self.assertTrue(dfn.read("aa_a.dat", "_"))
        self.assertEqual(dfn.components[0].component, "aa")
        self.assertEqual(dfn.components[0].type, "string")
        self.assertEqual(dfn.components[1].component, "a")
        self.assertEqual(dfn.components[1].type, "string")

        self.assertTrue(dfn.read("100_1.0.dat", "_"))
        self.assertEqual(dfn.components[0].component, "100")
        self.assertEqual(dfn.components[0].type, "int")
        self.assertEqual(dfn.components[1].component, "1.0")
        self.assertEqual(dfn.components[1].type, "float")

        self.assertTrue(dfn.read("100_1.0_DC=0.1.dat", "_"))
        self.assertEqual(dfn.components[0].component, "100")
        self.assertEqual(dfn.components[0].type, "int")
        self.assertEqual(dfn.components[1].component, "1.0")
        self.assertEqual(dfn.components[1].type, "float")
        self.assertEqual(dfn.components[2].component, "0.1")
        self.assertEqual(dfn.components[2].type, "float")
        self.assertEqual(dfn.components[2].compound, True)
        self.assertEqual(dfn.components[2].compound_prefix, "DC")





    # ****************************************************************************************************

    def test_remove_extension(self):
        """Tests the method that reads the filename."""

        dfn = DelimitedFilename(None, None)
        self.assertEqual(dfn.remove_extension(None), None)
        self.assertEqual(dfn.remove_extension(""), None)
        self.assertEqual(dfn.remove_extension("a"), None)
        self.assertEqual(dfn.remove_extension("aa"), None)
        self.assertEqual(dfn.remove_extension("aaa"), "aaa")
        self.assertEqual(dfn.remove_extension("aaa.txt"), "aaa")
        self.assertEqual(dfn.remove_extension("aaa.dat"), "aaa")
        self.assertEqual(dfn.remove_extension("aaa.asc"), "aaa")
        self.assertEqual(dfn.remove_extension("aaa.par"), "aaa")

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
