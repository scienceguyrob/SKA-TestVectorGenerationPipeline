"""
    **************************************************************************
    |                                                                        |
    |                 Test Parameter Handling Version 1.0                    |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Tests the parameter handling capabilities of the GaussianProfileGen    |
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

from code.pulsar_injection_pipeline.beta.main.src.GaussianProfileGen import GaussianProfileGen

# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestParameterHandling(unittest.TestCase):
    """
    The tests for the GaussianProfileGen class.
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
        # args[1] = number of bins
        # args[2] = min profile value
        # args[3] = max profile value
        # args[4] = duty cycle
        # args[5] = profile type
        # args[6] = mu
        # args[7] = sigma

        # Example invalid arguments
        args0 = ['a', 'a', 'a', 'a', 'a', 'a']  # all invalid

        args1a = ['a',128,0.0,1.0,0.5,0] # Verbose flag invalid (character)
        args1b = [-1, 128, 0.0, 1.0, 0.5, 0]   # Verbose flag invalid (negative number)
        args1c = [2.0, 128, 0.0, 1.0, 0.5, 0]  # Verbose flag invalid (float)

        args2a = [True, 'a', 0.0, 1.0, 0.5, 0] # Bins invalid (character)
        args2b = [True, 1.0, 0.0, 1.0, 0.5, 0] # Bins invalid (float)
        args2c = [True, True, 0.0, 1.0, 0.5, 0]# Bins invalid (boolean)

        args3a = [True, 128, 'a', 1.0, 0.5, 0] # min value invalid (character)
        args3b = [True, 128, 1, 1.0, 0.5, 0]   # min value invalid (int)
        args3c = [True, 128, True, 1.0, 0.5, 0]# min value invalid (boolean)

        args4a = [True, 128, 0.0, 'a', 0.5, 0] # max value invalid (character)
        args4b = [True, 128, 0.0, 1, 0.5, 0] # max value invalid (int)
        args4c = [True, 128, 0.0, True, 0.5, 0]# max value invalid (boolean)

        args5a = [True, 128, 0.0, 1.0, 'a', 0] # duty cycle invalid (character)
        args5b = [True, 128, 0.0, 1.0, 1, 0]   # duty cycle invalid (int)
        args5c = [True, 128, 0.0, 1.0, True, 0]# duty cycle invalid (boolean)

        args6a = [True, 128, 0.0, 1.0, 0.5, 'a']  # Profile type invalid (character)
        args6b = [True, 128, 0.0, 1.0, 0.5, 1.0]  # Profile type invalid (float)
        args6c = [True, 128, 0.0, 1.0, 0.5, True] # Profile type invalid (boolean)


        # Test with invalid arguments
        self.assertFalse(GaussianProfileGen.check_parameter_types(args0, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args1a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args1b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args1c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args2a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args2b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args2c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args3a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args3b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args3c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args4a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args4b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args4c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args5a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args5b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args5c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args6a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args6b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_types(args6c, testing=True))


        # Example valid arguments
        args0a = [True, 128, 0.0, 1.0, 0.5, 0]
        args0b = [False, 128, 0.0, 1.0, 0.5, 0]

        # Test with valid arguments
        self.assertTrue(GaussianProfileGen.check_parameter_types(args0a, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_types(args0b, testing=True))

    # ****************************************************************************************************

    def test_parameter_value_checks(self):
        """ Tests the method that checks if parameter values are correct."""

        # The arguments expected by the check function are stored in an array with
        # the following structure:
        #
        # args[0] = verbose flag
        # args[1] = number of bins - must be greater than 0
        # args[2] = min profile value - must be less than args[3]
        # args[3] = max profile value - must be greater than args[2]
        # args[4] = duty cycle - must be greater than 0 and less than or equal to 1.
        # args[5] = profile type - must be either 0 or 1 at present.
        # args[6] = mu
        # args[7] = sigma

        # Example invalid arguments

        args1a = [True, -1, 0.0, 1.0, 0.5, 0] # Bins invalid
        args1b = [True, 0, 1.0, 1.0, 0.5, 0]  # Bins invalid
        args1c = [True, 2, 1.0, 1.0, 0.5, 0]  # Bins invalid

        args2a = [True, 128, 1.1, 1.0, 0.5, 0] # min value invalid
        args2b = [True, 128, 1.2, 1.0, 0.5, 0] # min value invalid
        args2c = [True, 128, 9.0, 1.0, 0.5, 0] # min value invalid

        args3a = [True, 128, 0.0, -1, 0.5, 0]   # max value invalid
        args3b = [True, 128, 0.0, -1.1, 0.5, 0] # max value invalid
        args3c = [True, 128, 0.0, -9.0, 0.5, 0] # max value invalid

        args4a = [True, 128, 0.0, 1.0, 0.0, 0] # duty cycle invalid
        args4b = [True, 128, 0.0, 1.0, 1.1, 0] # duty cycle invalid
        args4c = [True, 128, 0.0, 1.0, 1.2, 0] # duty cycle invalid

        args5a = [True, 128, 0.0, 1.0, 0.5, -1]  # Profile type invalid
        args5b = [True, 128, 0.0, 1.0, 0.5, 2]   # Profile type invalid


        # Test with invalid arguments
        self.assertFalse(GaussianProfileGen.check_parameter_values(args1a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args1b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args1c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args2a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args2b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args2c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args3a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args3b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args3c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args4a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args4b, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args4c, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args5a, testing=True))
        self.assertFalse(GaussianProfileGen.check_parameter_values(args5b, testing=True))


        # Example valid arguments
        args1a = [True, 3, 0.0, 1.0, 0.5, 0]    # Bins valid
        args1b = [True, 100, 0.0, 1.0, 0.5, 0]  # Bins valid
        args1c = [True, 1000, 0.0, 1.0, 0.5, 0] # Bins valid

        args2a = [True, 128, 0.0, 1.0, 0.5, 0]  # min value valid
        args2b = [True, 128, 0.9, 1.0, 0.5, 0]  # min value valid
        args2c = [True, 128, 0.99, 1.0, 0.5, 0] # min value valid

        args3a = [True, 128, 0.0, 0.1, 0.5, 0]  # max value valid
        args3b = [True, 128, 0.0, 0.2, 0.5, 0]  # max value valid
        args3c = [True, 128, 0.0, 0.3, 0.5, 0]  # max value valid

        args4a = [True, 128, 0.0, 1.0, 0.1, 0]  # duty cycle valid
        args4b = [True, 128, 0.0, 1.0, 0.4, 0]  # duty cycle valid
        args4c = [True, 128, 0.0, 1.0, 0.5, 0]  # duty cycle valid

        args5a = [True, 128, 0.0, 1.0, 0.5, 0]  # Profile type valid
        args5b = [True, 128, 0.0, 1.0, 0.5, 1]  # Profile type valid

        # Test with valid arguments
        self.assertTrue(GaussianProfileGen.check_parameter_values(args1a, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args1b, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args1c, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args2a, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args2b, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args2c, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args3a, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args3b, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args3c, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args4a, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args4b, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args4c, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args5a, testing=True))
        self.assertTrue(GaussianProfileGen.check_parameter_values(args5b, testing=True))

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
