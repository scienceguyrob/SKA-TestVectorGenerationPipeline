"""
    **************************************************************************
    |                                                                        |
    |               Test Fake Par Parameter Handling Version 1.0             |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Tests the parameter handling capabilities of the CreateFakeParFiles    |
    | application.                                                           |
    |                                                                        |
    | The code is compatible with python version 3.6.                        |
    |                                                                        |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@manchester.ac.uk                                   |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | Required Command Line Arguments:                                       |
    |                                                                        |
    | N/A                                                                    |
    |                                                                        |
    **************************************************************************
    | Optional Command Line Arguments:                                       |
    |                                                                        |
    | N/A                                                                    |
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

import os
import unittest

from code.pulsar_injection_pipeline.beta.main.src.CreateFakeParFiles import CreateFakeParFiles

# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestFakeParParameterHandling(unittest.TestCase):
    """
    The tests for the CreateFakeParFiles class.
    """

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_parameter_type_checks(self):
        """ Tests the method that checks if parameter types are correctly checked."""

        # The arguments expected by the check function are stored in an array with
        # the following structure:
        #
        # args[0] = verbose flag
        # args[1] = output directory path
        # args[2] = the DM
        # args[3] = the period values to use.

        # Example invalid arguments
        args0 = [None, None, None, None, None]  # all invalid

        args1a = ['a', "a", 1.0, "", "0.0"] # Verbose flag invalid (character)
        args1b = [-1 , "a", 1.0, "", "0.0"] # Verbose flag invalid (negative number)
        args1c = [2.0, "a", 1.0, "", "0.0"] # Verbose flag invalid (float)

        args2a = [True, None, 1.0, "", "0.0"] # Output directory invalid
        args2b = [True,   -1, 1.0, "", "0.0"] # Output directory invalid
        args2c = [True, True, 1.0, "", "0.0"] # Output directory invalid

        args3a = [True, "a", 'c' , "", "0.0"] # DM invalid (character)
        args3b = [True, "a", 1   , "", "0.0"] # DM invalid (int)
        args3c = [True, "a", True, "", "0.0"] # DM invalid (boolean)

        args4a = [True, "a", 1.0, None, "0.0"] # Period string invalid (None)
        args4b = [True, "a", 1.0, 1   , "0.0"] # Period string invalid (int)
        args4c = [True, "a", 1.0, True, "0.0"] # Period string invalid (boolean)



        # Test with invalid arguments
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args0 , testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args1a, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args1b, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args1c, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args2a, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args2b, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args2c, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args3a, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args3b, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args3c, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args4a, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args4b, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_types(args4c, testing=True))


        # Example valid arguments
        args0a = [True, "a/b/c", 0.0, "1.0,2.0", 1.0]
        args0b = [False, "aaaa", 1.0, "1,2,3,4", 1.0]

        # Test with valid arguments
        self.assertTrue(CreateFakeParFiles.check_parameter_types(args0a, testing=True))
        self.assertTrue(CreateFakeParFiles.check_parameter_types(args0b, testing=True))

    # ****************************************************************************************************

    def test_parameter_value_checks(self):
        """ Tests the method that checks if parameter values are correct."""

        # Create some directories for testing.
        tempDir = "temp"
        tempDirNested = "temp/nested"

        #try:
        #    os.mkdir(tempDir)
        #    os.mkdir(tempDirNested)
        #except OSError:
        #    print("Creation of the directory %s failed" % tempDir)
        #    print("Creation of the directory %s failed" % tempDirNested)

        # Now define the test cases...

        # The arguments expected by the check function are stored in an array with
        # the following structure:
        #
        # args[0] = verbose flag
        # args[1] = output directory path
        # args[2] = the DM
        # args[3] = the period values to use.

        # Example invalid arguments

        args1a = [True, tempDir, -0.01, "1.0,2.0,3.0"] # DM value invalid
        args1b = [True, tempDir, -1.0, "1.0,2.0,3.0"]  # DM value invalid
        args1c = [True, tempDir, -100, "1.0,2.0,3.0"]  # DM value invalid

        args2a = [True, tempDir, 1.0, "1.a,2.0,3.0"]  # Period string value invalid (has char in it)
        args2b = [True, tempDir, 1.0, "1.0,True,3.0"] # Period string value invalid (has bool in it)
        args2c = [True, tempDir, 1.0, "1.0,2.0,"]     # Period string value invalid (missing value)



        # Test with invalid arguments
        self.assertFalse(CreateFakeParFiles.check_parameter_values(args1a, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_values(args1b, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_values(args1c, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_values(args2a, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_values(args2b, testing=True))
        self.assertFalse(CreateFakeParFiles.check_parameter_values(args2c, testing=True))


        # Example valid arguments
        args1a = [True, tempDir, 0.0, "1.0,2.0,3.0"]       #
        args1b = [True, tempDir, 1.0, "1.0,2.0,3.0"]       #

        args2a = [True, tempDir, 1.0, "1.0"]               #
        args2b = [True, tempDir, 1.0, "1.0,2.0,3.0"]       #
        args2c = [True, tempDir, 1.0, "1.0,2.0,3"]         #


        # Test with valid arguments
        self.assertTrue(CreateFakeParFiles.check_parameter_values(args1a, testing=True))
        self.assertTrue(CreateFakeParFiles.check_parameter_values(args1b, testing=True))
        self.assertTrue(CreateFakeParFiles.check_parameter_values(args2a, testing=True))
        self.assertTrue(CreateFakeParFiles.check_parameter_values(args2b, testing=True))
        self.assertTrue(CreateFakeParFiles.check_parameter_values(args2c, testing=True))

        # Now clean up.
        #try:
        #    os.rmdir(tempDirNested)
        #    os.rmdir(tempDir)
        #except OSError:
        #    print("Deletion of the directory %s failed" % tempDir)
        #    print("Deletion of the directory %s failed" % tempDirNested)


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
