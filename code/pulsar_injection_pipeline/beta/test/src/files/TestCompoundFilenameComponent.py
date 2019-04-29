"""
**************************************************************************

 TestCompoundFilenameComponent.py

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

from code.pulsar_injection_pipeline.beta.main.src.CompoundFilenameComponent import CompoundFilenameComponent


# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestCompoundFilenameComponent(unittest.TestCase):
    """
    The tests for theclass.
    """

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_get_component_type(self):
        """Tests the method that determines the filename component type."""

        fnc = CompoundFilenameComponent(None, None)

        self.assertEqual(fnc.get_component_type(None), "none")
        self.assertEqual(fnc.get_component_type(""), "none")
        self.assertEqual(fnc.get_component_type("a"), "string")
        self.assertEqual(fnc.get_component_type("1"), "int")
        self.assertEqual(fnc.get_component_type("1.0"), "float")
        self.assertEqual(fnc.get_component_type("1a"), "string")
        self.assertEqual(fnc.get_component_type("1.0a"), "string")
        self.assertEqual(fnc.get_component_type("1True"), "string")
        self.assertEqual(fnc.get_component_type("1.0False"), "string")

    # ****************************************************************************************************

    def test_is_compound(self):
        """Tests the method that determines if the component is compound or not."""

        fnc = CompoundFilenameComponent(None, None)

        self.assertFalse(fnc.is_compound(None, None))
        self.assertFalse(fnc.is_compound("", None))
        self.assertFalse(fnc.is_compound("a", None))
        self.assertFalse(fnc.is_compound(None, ""))
        self.assertFalse(fnc.is_compound(None, "a"))

        self.assertFalse(fnc.is_compound("a", "a"))
        self.assertFalse(fnc.is_compound("aa", "a"))
        self.assertFalse(fnc.is_compound("aaa", "a"))
        self.assertFalse(fnc.is_compound("aaaa", "a"))

        self.assertFalse(fnc.is_compound("a", "="))
        self.assertFalse(fnc.is_compound("aa", "="))
        self.assertFalse(fnc.is_compound("aaa", "="))

        self.assertTrue(fnc.is_compound("aa=a", "="))
        self.assertTrue(fnc.is_compound("a=1", "="))
        self.assertTrue(fnc.is_compound("a=True", "="))
        self.assertTrue(fnc.is_compound("a=1.0", "="))
        self.assertTrue(fnc.is_compound("a=1000000", "="))
        self.assertTrue(fnc.is_compound("a=1.00000", "="))
        self.assertTrue(fnc.is_compound("a=-1000000", "="))
        self.assertTrue(fnc.is_compound("a=-1.00000", "="))

        self.assertTrue(fnc.is_compound("ABC=1000000", "="))
        self.assertTrue(fnc.is_compound("DEF=1.00000", "="))


    # ****************************************************************************************************

    def test_init(self):
        """Tests the method that builds a component on init."""

        fnc = CompoundFilenameComponent(None, None)
        self.assertFalse(fnc.compound)

        fnc = CompoundFilenameComponent("", None)
        self.assertFalse(fnc.compound)

        fnc = CompoundFilenameComponent("A", None)
        self.assertFalse(fnc.compound)
        self.assertEqual(fnc.component, "A")

        fnc = CompoundFilenameComponent("A", "")
        self.assertFalse(fnc.compound)
        self.assertEqual(fnc.component, "A")

        fnc = CompoundFilenameComponent("A", "A")
        self.assertFalse(fnc.compound)
        self.assertEqual(fnc.component, "A")

        fnc = CompoundFilenameComponent("AA", "A")
        self.assertFalse(fnc.compound)
        self.assertEqual(fnc.component, "AA")

        fnc = CompoundFilenameComponent("AAA", "A")
        self.assertFalse(fnc.compound)
        self.assertEqual(fnc.component, "AAA")

        fnc = CompoundFilenameComponent("AAA", "=")
        self.assertFalse(fnc.compound)
        self.assertEqual(fnc.component, "AAA")

        fnc = CompoundFilenameComponent("ABC=A", "=")
        self.assertTrue(fnc.compound)
        self.assertEqual(fnc.component, "A")
        self.assertEqual(fnc.compound_prefix, "ABC")
        self.assertEqual(fnc.type, "string")

        fnc = CompoundFilenameComponent("ABC=1", "=")
        self.assertTrue(fnc.compound)
        self.assertEqual(fnc.component, "1")
        self.assertEqual(fnc.compound_prefix, "ABC")
        self.assertEqual(fnc.type, "int")

        fnc = CompoundFilenameComponent("ABC=-1", "=")
        self.assertTrue(fnc.compound)
        self.assertEqual(fnc.component, "-1")
        self.assertEqual(fnc.compound_prefix, "ABC")
        self.assertEqual(fnc.type, "int")

        fnc = CompoundFilenameComponent("ABC=1.0", "=")
        self.assertTrue(fnc.compound)
        self.assertEqual(fnc.component, "1.0")
        self.assertEqual(fnc.compound_prefix, "ABC")
        self.assertEqual(fnc.type, "float")

        fnc = CompoundFilenameComponent("ABC=-1.0", "=")
        self.assertTrue(fnc.compound)
        self.assertEqual(fnc.component, "-1.0")
        self.assertEqual(fnc.compound_prefix, "ABC")
        self.assertEqual(fnc.type, "float")


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
