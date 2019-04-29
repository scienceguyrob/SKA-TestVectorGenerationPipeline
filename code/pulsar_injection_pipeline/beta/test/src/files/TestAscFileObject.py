"""
**************************************************************************

 TestAscFileObject.py

**************************************************************************
 Description:

 Tests the object that represents a .asc file.

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

from code.pulsar_injection_pipeline.beta.main.src.AscFile import AscFile


# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestAscFileObject(unittest.TestCase):
    """
    The tests for the ".asc" file class.
    """

    # Points to the resource directory containing test files.
    data_root = os.path.abspath('../..') + '/resources'
    test_data_root = data_root + '/test/asc/'

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_read(self):
        """Tests the highest level method that reads the .asc files."""

        empty_file       = self.test_data_root + "Empty_DC=0.1_BINS=18_FWHM=0.5.asc"
        invalid_filename = self.test_data_root + "InvalidFilename_D=0.1_BIN=18_FWH=0.5.asc"
        invalid_data     = self.test_data_root + "InvalidData_DC=0.1_BINS=18_FWHM=0.5.asc"
        bin_error_file   = self.test_data_root + "BinsNotEqualToData_DC=0.1_BINS=18_FWHM=0.5.asc"
        valid_file       = self.test_data_root + "Gaussian_DC=0.1_BINS=18_FWHM=0.5.asc"

        data = [0.0, 0.1, 10.0, 25.0, 50.0, 100.0, 150.0, 200.0, 255.0,
                200.0, 150.0, 100.0, 50.0, 25.0, 10.0, 0.2, 0.1, 0.0]



        # Create object for testing.
        asc = AscFile()

        self.assertFalse(asc.read(empty_file, True))

        asc = AscFile()
        self.assertFalse(asc.read(invalid_filename, True))

        asc = AscFile()
        self.assertFalse(asc.read(invalid_data, True))

        sc = AscFile()
        self.assertFalse(asc.read(bin_error_file, True))

        asc = AscFile()
        self.assertTrue(asc.read(valid_file, True))

        self.assertEqual(asc.data, data)
        self.assertEqual(asc.fpth, valid_file)
        self.assertEqual(asc.fname, "Gaussian_DC=0.1_BINS=18_FWHM=0.5.asc")
        self.assertEqual(asc.valid_file_name, True)
        self.assertEqual(asc.name, "Gaussian")
        self.assertEqual(asc.dc, 0.1)
        self.assertEqual(asc.bins, 18)
        self.assertEqual(asc.fwhm, 0.5)


    # ****************************************************************************************************

    def test_create_valid_file_name(self):
        """Tests the method that creates a .asc file, file name."""

        # File name should be in this format (order matters):
        #
        # <IDENTIFIER>_<Freq., OPTIONAL>_<Duty Cycle, OPTIONAL>_<BINS, OPTIONAL>_<FWHM, OPTIONAL>.asc
        #
        # where,
        #
        # <Freq., OPTIONAL> has two components: <frequency>Mhz
        # <Duty cycle> has two components: DC=<Duty cycle>
        # <Bins> has two components: BINS=<Bins>
        # <FWHM> has two components: FWHM=<Duty cycle>

        # Create object for testing.
        asc = AscFile()

        # Name has incorrect format
        self.assertEqual(asc.create_valid_file_name(nme=None), None)
        self.assertEqual(asc.create_valid_file_name(nme=""), None)

        # All invalid parameter values
        self.assertEqual(asc.create_valid_file_name(nme="a", freq="a"), None)
        self.assertEqual(asc.create_valid_file_name(nme="a", dc="a"), None)
        self.assertEqual(asc.create_valid_file_name(nme="a", bins="a"), None)
        self.assertEqual(asc.create_valid_file_name(nme="a", fwhm="a"), None)

        # Valid but not very useful!
        self.assertEqual(asc.create_valid_file_name(nme="a", freq=None), "a.asc")
        self.assertEqual(asc.create_valid_file_name(nme="a", dc=None), "a.asc")
        self.assertEqual(asc.create_valid_file_name(nme="a", bins=None), "a.asc")
        self.assertEqual(asc.create_valid_file_name(nme="a", fwhm=None), "a.asc")

        # Valid
        self.assertEqual(asc.create_valid_file_name(nme="a", freq=None, dc=None, bins=None, fwhm=None), "a.asc")

        # Invalid
        self.assertEqual(asc.create_valid_file_name(nme="a", freq="a", dc="a", bins="a", fwhm="a"), None)
        self.assertEqual(asc.create_valid_file_name(nme="a", freq="1", dc="a", bins="a", fwhm="a"), None)
        self.assertEqual(asc.create_valid_file_name(nme="a", freq="a", dc="0.5", bins="a", fwhm="a"), None)
        self.assertEqual(asc.create_valid_file_name(nme="a", freq="a", dc="a", bins="128", fwhm="a"), None)
        self.assertEqual(asc.create_valid_file_name(nme="a", freq="a", dc="a", bins="a", fwhm="0.5"), None)

        # Valid
        self.assertEqual(asc.create_valid_file_name(nme="a", freq="1", dc="0.5", bins="128", fwhm="0.5"),
                         "a_1.0MHz_DC=0.5_BINS=128_FWHM=0.5.asc")

        self.assertEqual(asc.create_valid_file_name(nme="Gaussian", freq="1", dc="0.5", bins="128", fwhm="0.5"),
                         "Gaussian_1.0MHz_DC=0.5_BINS=128_FWHM=0.5.asc")


    # ****************************************************************************************************

    def test_is_filename_valid(self):
        """Tests the method that checks if a '.asc' file's filename is valid."""

        # File name should be in this format (order matters as far as the user is concerned):
        #
        # <IDENTIFIER>_<Freq., OPTIONAL>_<Duty Cycle, OPTIONAL>_<BINS, OPTIONAL>_<FWHM, OPTIONAL>.asc
        #
        # where,
        #
        # <Freq., OPTIONAL> has two components: <frequency>Mhz
        # <Duty cycle> has two components: DC=<Duty cycle>
        # <Bins> has two components: BINS=<Bins>
        # <FWHM> has two components: FWHM=<Duty cycle>
        #
        #
        #
        # Thus there is only 1 mandatory component to the name format, which is the identifier.
        #
        # File names adhering to this format should have the following
        # properties:
        #
        # 1. End in ".asc".
        # 2. Have at least 1 underscore, and at most 4 underscore characters.
        # 3. Supplied duty cycle, and FWHM values must be floats, the bins value must be an integer.
        #
        # We check we meet these requirements here.

        # Create object for testing.
        asc = AscFile()

        # Single file, just first name component.
        self.assertFalse(asc.is_filename_valid("."))  # not a valid file name
        self.assertFalse(asc.is_filename_valid(".asc"))  # not a valid file name
        self.assertTrue(asc.is_filename_valid("a.asc"))  # file name valid, just contains the identifier.

        # Single file, first two components.
        self.assertFalse(asc.is_filename_valid("a_.asc"))  # invalid, missing component.
        self.assertFalse(asc.is_filename_valid("a_a.asc"))  # invalid, second component should be an int, end in "MHz".

        # Single file, first three components.
        self.assertFalse(asc.is_filename_valid("a_1350.asc"))  # invalid, no "MHz" suffix after 1350
        self.assertFalse(asc.is_filename_valid("a_1350_.asc"))  # invalid, final component missing, no "MHz" suffix.
        self.assertFalse(asc.is_filename_valid("a_1350_a.asc"))  # invalid, third component should be a float.

        # Single file, first four components.
        self.assertFalse(asc.is_filename_valid("a_1350_0.5_.asc"))  # invalid missing component
        self.assertFalse(asc.is_filename_valid("a_1350MHz_0.5_.asc")) # missing component, duty cycle prefix missing.
        self.assertFalse(asc.is_filename_valid("a_1350MHz_DC=0.5_a.asc"))  # invalid, fourth component should be an int.

        # Single file, all five components.
        self.assertFalse(asc.is_filename_valid("a_1350_0.5_128_.asc"))  # invalid,
        self.assertFalse(asc.is_filename_valid("a_1350_0.5_128_a.asc"))  # invalid, fourth component should be an int.

        # Single file, all five components.
        self.assertFalse(asc.is_filename_valid("a_1350_0.5_128_64.0.asc"))  # invalid, prefixes missing.

        # Single file, all five components with meta information. Note that case matters here.
        self.assertFalse(asc.is_filename_valid("a_1350MHz_DC=0.5_128_64.0.asc"))    # BINS and FWHM prefixes missing.
        self.assertFalse(asc.is_filename_valid("a_1350MHz_0.5_BINS=128_64.0.asc"))  # DC and FWHM prefix missing.
        self.assertFalse(asc.is_filename_valid("a_1350MHz_0.5_128_FWHM=64.0.asc"))  # DC and BINS prefix missing.

        self.assertFalse(asc.is_filename_valid("a_1350MHz_D=0.5_BINS=128_FWHM=64.0.asc"))  # prefix invalid (duty cycle)
        self.assertFalse(asc.is_filename_valid("a_1350MH.asc"))  # prefix invalid
        self.assertFalse(asc.is_filename_valid("a_1350MHz_C=0.5.asc"))  # prefix invalid (duty cycle)
        self.assertFalse(asc.is_filename_valid("a_1350MHz_DC=0.5_BIN=128.asc"))  # prefix invalid (bins)
        self.assertFalse(asc.is_filename_valid("a_1350MHz_FWH=64.0.asc"))  # prefix invalid (FWHM)
        self.assertFalse(asc.is_filename_valid("a_FWH=64.0.asc"))  # prefix invalid (fwhm)
        self.assertFalse(asc.is_filename_valid("a_D=0.5.asc"))  # prefix invalid (duty cycle)
        self.assertFalse(asc.is_filename_valid("a_BIN=128.asc"))  # prefix invalid (bins)

        # This should fail - too many underscores
        self.assertFalse(asc.is_filename_valid("b_DC=0.5_BINS=128_FWHM=64.0_1350MHz_.asc"))  # invalid

        # Some valid examples.
        self.assertTrue(asc.is_filename_valid("a_1350MHz_DC=0.5_BINS=128_FWHM=64.0.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("a_1350MHz.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("a_1350MHz_DC=0.5.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("a_1350MHz_DC=0.5_BINS=128.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("a_1350MHz_FWHM=64.0.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("a_FWHM=64.0.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("a_DC=0.5.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("a_BINS=128.asc"))  # valid

        # Now test ordering

        # These should pass as ordering shouldn't matter, but user won't know that.
        self.assertTrue(asc.is_filename_valid("b_DC=0.5_BINS=128_FWHM=64.0_1350MHz.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("b_BINS=128_DC=0.5_FWHM=64.0_1350MHz.asc"))  # valid
        self.assertTrue(asc.is_filename_valid("b_FWHM=64.0_DC=0.5_BINS=128_1350MHz.asc"))  # valid

    # ****************************************************************************************************

    def test_file_name_create_against_validation_method(self):
        """
        Tests the method that creates a .asc file file name, using the custom function
        written to test file name validation. So we are testing two methods here (a
        simple integration test).
        """

        # Create object for testing.
        asc = AscFile()

        # Valid
        fnm1 = asc.create_valid_file_name(nme="a", freq="1", dc="0.5", bins="128", fwhm="0.5")
        fnm2 = asc.create_valid_file_name(nme="Gaussian", freq="1", dc="0.5", bins="128", fwhm="0.5")

        self.assertTrue(asc.is_filename_valid(fnm1))  # valid
        self.assertTrue(asc.is_filename_valid(fnm2))  # valid


    # ****************************************************************************************************

    def test_parse_asc_file_name_tokens(self):
        """Tests the method that parses a .asc file's file name."""

        # Create object for testing.
        asc = AscFile()

        # File name should be in this format (order matters):
        #
        # <IDENTIFIER>_<Freq., OPTIONAL>_<Duty Cycle, OPTIONAL>_<BINS, OPTIONAL>_<FWHM, OPTIONAL>.asc
        #
        # where,
        #
        # <Freq., OPTIONAL> has two components: <frequency>Mhz
        # <Duty cycle> has two components: DC=<Duty cycle>
        # <Bins> has two components: BINS=<Bins>
        # <FWHM> has two components: FWHM=<Duty cycle>

        # This will pass
        tokens = asc.tokenise_file_name("a.asc", "_")
        self.assertTrue(asc.parse_asc_file_name_tokens(tokens))

        tokens = asc.tokenise_file_name("a_1.asc", "_")
        self.assertFalse(asc.parse_asc_file_name_tokens(tokens))

        # Will pass
        tokens = asc.tokenise_file_name("a_1MHz.asc", "_")
        self.assertTrue(asc.parse_asc_file_name_tokens(tokens))

        # These will fail, extra underscore with no information following.
        tokens = asc.tokenise_file_name("a_1MHz_.asc", "_")
        self.assertFalse(asc.parse_asc_file_name_tokens(tokens))
        tokens = asc.tokenise_file_name("a_1MHz_DC=0.5_.asc", "_")
        self.assertFalse(asc.parse_asc_file_name_tokens(tokens))
        tokens = asc.tokenise_file_name("a_1MHz_DC=0.5_BINS=128_.asc", "_")
        self.assertFalse(asc.parse_asc_file_name_tokens(tokens))

        # Fail, string 'case' errors in metadata
        tokens = asc.tokenise_file_name("a_1Mhz.asc", "_")
        self.assertFalse(asc.parse_asc_file_name_tokens(tokens))
        tokens = asc.tokenise_file_name("a_1MHz_Dc=0.5_.asc", "_")
        self.assertFalse(asc.parse_asc_file_name_tokens(tokens))
        tokens = asc.tokenise_file_name("a_1MHz_DC=0.5_bINS=128_.asc", "_")
        self.assertFalse(asc.parse_asc_file_name_tokens(tokens))
        tokens = asc.tokenise_file_name("a_1MHz_DC=0.5_bINS=128_fwhm=1.0.asc", "_")
        self.assertFalse(asc.parse_asc_file_name_tokens(tokens))

        # These should pass, as the file names are valid.
        tokens = asc.tokenise_file_name("a_1MHz.asc", "_")
        self.assertTrue(asc.parse_asc_file_name_tokens(tokens))
        self.assertEqual(asc.freq, 1.0)

        tokens = asc.tokenise_file_name("a_1MHz_DC=0.5.asc", "_")
        self.assertTrue(asc.parse_asc_file_name_tokens(tokens))
        self.assertEqual(asc.dc, 0.5)

        tokens = asc.tokenise_file_name("a_1MHz_DC=0.5_BINS=128.asc", "_")
        self.assertTrue(asc.parse_asc_file_name_tokens(tokens))
        self.assertEqual(asc.bins, 128)

        tokens = asc.tokenise_file_name("a_1MHz_DC=0.5_BINS=128_FWHM=128.asc", "_")
        self.assertTrue(asc.parse_asc_file_name_tokens(tokens))
        self.assertEqual(asc.fwhm, 128.0)

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
