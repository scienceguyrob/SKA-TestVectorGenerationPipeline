"""
    **************************************************************************
    |                                                                        |
    |                 Test Profile Generation Version 1.0                    |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Tests the creation/generation of Gaussian profiles by the application  |
    | GaussianProfileGen.py.                                                 |
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

import unittest
from scipy.interpolate import UnivariateSpline
import numpy as np
from code.pulsar_injection_pipeline.beta.main.src.GaussianProfileGen import GaussianProfileGen



# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestProfileGeneration(unittest.TestCase):
    """
    The tests for the class.
    """

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_gaussian_generation(self):
        """Tests the method that creates the profiles."""

        # Some simple test cases which cover the duty cycle, bin lengths
        # etc that will be seen in practice.
        test_duty_cycles = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.499, 0.5]
        test_bin_lengths = [64, 128, 256, 512, 1024, 2048, 4096]
        test_min = 0.0
        test_max = 1.0

        # A variable to to track the error in FWHM
        total_error = 0.0

        # Max permissible error rate in FWHM. If the error is higher
        # than this, the test will be declared a failure.
        error_rate_limit = 0.6  # Percentage
        avg_error_rate_limit = 0.05  # Percentage

        # Iterate over all of the test cases...
        for bins in test_bin_lengths:
            for duty_cycle in test_duty_cycles:

                # Create the object used to generate profiles.
                gen = GaussianProfileGen()

                # Assign some class variables - these would usually be obtained
                # from the command line (or command line processing methods).
                gen.duty_cycle = duty_cycle
                gen.bins = bins

                # Actually create the profile.
                profile = gen.create_gaussian(test_min, test_max, bins, duty_cycle)

                # Now compute the FWHM
                spline = UnivariateSpline(gen.opt_x, profile - np.max(profile) / 2.0, s=0)
                r1, r2 = spline.roots()  # find the roots
                actual_fwhm = (r2 - r1)
                diff_in_bins = (bins * duty_cycle) - actual_fwhm

                # Check the error rate is below the desired level.
                error_margin_percent = np.abs(((diff_in_bins / actual_fwhm) * 100))
                total_error += error_margin_percent

                # This does the check...
                self.assertLess(error_margin_percent, error_rate_limit)

        # Finally check the average error rate is as expected.
        average_error = total_error / ((len(test_duty_cycles)) * (len(test_bin_lengths)))
        self.assertLess(average_error, avg_error_rate_limit)

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
