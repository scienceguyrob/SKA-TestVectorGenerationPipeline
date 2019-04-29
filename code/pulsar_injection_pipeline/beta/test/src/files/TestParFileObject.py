import unittest

from code.pulsar_injection_pipeline.beta.main.src.ParFile import ParFile


# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestParFileObject(unittest.TestCase):
    """
    The tests for the class.
    """

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_read(self):
        """Tests the highest level method that reads the par files."""

        parent_dir = "/Users/rob/Documents/workspace/TestVectorUtilities/resources/test/par/"

        example_file_1_pth = parent_dir + "FakePulsar1_DM=1.0_P0=1.0ms_Z=1.0.par"
        example_file_2_pth = parent_dir + "FakePulsar2_DM=1.0_P0=2.0ms_Z=0.0.par"
        example_file_3_pth = parent_dir + "empty.par"
        example_file_4_pth = parent_dir + "wrong_delim.par"

        par = ParFile()
        verbose_flag = True

        # Read a valid file
        self.assertTrue(par.read(example_file_1_pth, verbose_flag))

        # Check values from the file are loaded
        self.assertEqual(par.name, "J0000-0001")
        self.assertEqual(par.ra, "00:00:00.0")
        self.assertEqual(par.dec, "00:00:00.0")
        self.assertEqual(par.dm, 1.0)
        self.assertEqual(par.pepoch, 56000.0)
        self.assertEqual(par.freq, 1000.0)
        self.assertEqual(par.period, 1.0)
        self.assertEqual(par.tzrmjd, 56000.0)
        self.assertEqual(par.tzrfreq, 1000.0)
        self.assertEqual(par.units, "TBD")
        self.assertEqual(par.accel, 1.0)
        self.assertEqual(par.pb, 1.06)
        self.assertEqual(par.a1, 7.19)
        self.assertEqual(par.t0, 56000.2)


        # Read a valid file
        self.assertTrue(par.read(example_file_2_pth, verbose_flag))

        # Check values from the file are loaded and overwrite previous values.
        self.assertEqual(par.name, "J0000-0002")
        self.assertEqual(par.ra, "00:00:00.1")
        self.assertEqual(par.dec, "00:00:00.1")
        self.assertEqual(par.dm, 2.0)
        self.assertEqual(par.pepoch, 56001.0)
        self.assertEqual(par.freq, 500.0)
        self.assertEqual(par.period, 2.0)
        self.assertEqual(par.tzrmjd, 56001.0)
        self.assertEqual(par.tzrfreq, 1001.0)
        self.assertEqual(par.units, "TBD1")
        self.assertEqual(par.accel, 0.0)

        self.assertFalse(par.read(example_file_3_pth, verbose_flag))  # Should fail.
        self.assertFalse(par.read(example_file_4_pth, verbose_flag))  # Should fail.

    # ****************************************************************************************************

    def test_tokenise_par_file_line(self):
        """ Tests the method that splits a par file line of text, into tokens."""

        delimiter = "\t"

        # Now some custom test cases....
        txt_1 = "RAJ\t\t\t00:00:00.0\t\t\t2.000e-05"
        out_1 = ["RAJ", "00:00:00.0", "2.000e-05"]

        txt_2 = "RAJ 00:00:00.0 2.000e-05"
        out_2 = ["RAJ 00:00:00.0 2.000e-05"]

        # Create object for testing.
        par = ParFile()

        # First test against invalid inputs:
        self.assertEqual(par.tokenise_par_file_line(None, None), None)
        self.assertEqual(par.tokenise_par_file_line(None, "\t"), None)
        self.assertEqual(par.tokenise_par_file_line("", "\t"), None)
        self.assertEqual(par.tokenise_par_file_line("\t", "\t"), [])
        self.assertEqual(par.tokenise_par_file_line("\t", None), None)


        self.assertEqual(par.tokenise_par_file_line(txt_1, delimiter), out_1)
        self.assertEqual(par.tokenise_par_file_line(txt_1, None), None)

        self.assertEqual(par.tokenise_par_file_line(txt_2, delimiter), out_2)

    # ****************************************************************************************************

    def test_parse_par_line_tokens(self):
        """Tests the method parses tokens extracted from a par file,
           updating the par file object as necessary."""

        parent_dir = "/Users/rob/Documents/workspace/TestVectorUtilities/resources/test/par/"

        example_file_1_pth = parent_dir + "FakePulsar_1_DM=1.0_P0=1.0ms_Z=0.0.par"
        example_file_2_pth = parent_dir + "FakePulsar_2_DM=1.0_P0=2.0ms_Z=0.0.par"
        example_file_3_pth = parent_dir + "empty.par"
        example_file_4_pth = parent_dir + "wrong_delim.par"

        # Now some custom test cases....
        txt_1 = "RAJ\t\t\t00:00:00.0\t\t\t2.000e-05"
        out_1 = "RAJ", "00:00:00.0", "2.000e-05"

        # Create object for testing.
        par = ParFile()

        # Should fail as inputs insufficient
        self.assertEqual(par.parse_par_line_tokens([""]), 0)
        self.assertEqual(par.parse_par_line_tokens(["1"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["a"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["RA"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["D"]), 0)
        self.assertEqual(par.parse_par_line_tokens([None]), 0)

        # Should fail as inputs insufficient
        self.assertEqual(par.parse_par_line_tokens(["PSRJ"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["RAJ"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["DECJ"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["DM"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["PEPOCH"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["FO"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["PO"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["TZRMJD"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["TZRFREQ"]), 0)
        self.assertEqual(par.parse_par_line_tokens(["UNITS"]), 0)

        # Should pass as inputs correct
        self.assertEqual(par.parse_par_line_tokens(["PSRJ", "PSR"]), 1)
        self.assertEqual(par.name, "PSR")

        self.assertEqual(par.parse_par_line_tokens(["RAJ", "ra"]), 1)
        self.assertEqual(par.ra, "ra")

        self.assertEqual(par.parse_par_line_tokens(["DECJ", "dec"]), 1)
        self.assertEqual(par.dec, "dec")

        self.assertEqual(par.parse_par_line_tokens(["DM", "1.0"]), 1)
        self.assertEqual(par.dm, 1.0)

        self.assertEqual(par.parse_par_line_tokens(["PEPOCH", "300.0"]), 1)
        self.assertEqual(par.pepoch, 300.0)

        self.assertEqual(par.parse_par_line_tokens(["F0", "1.0"]), 1)
        self.assertEqual(par.freq, 1.0)
        self.assertEqual(par.period, 1000.0)

        self.assertEqual(par.parse_par_line_tokens(["P0", "1.0"]), 1)
        self.assertEqual(par.period, 1000.0)

        self.assertEqual(par.parse_par_line_tokens(["TZRMJD", "100.0"]), 1)
        self.assertEqual(par.tzrmjd, 100.0)

        self.assertEqual(par.parse_par_line_tokens(["TZRFREQ", "200.0"]), 1)
        self.assertEqual(par.tzrfreq, 200.0)

        self.assertEqual(par.parse_par_line_tokens(["UNITS", "tbd"]), 1)
        self.assertEqual(par.units, "tbd")

    # ****************************************************************************************************

    def test_is_filename_valid(self):
        """Tests the method that checks if a '.par' file's filename is valid."""

        # File name should be in this format:
        #
        # <PULSAR NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms.par
        #
        # Any file names adhering to this format should have the following
        # properties:
        #
        # 1. End in "ms.par"
        # 2. Have 2 underscore characters '_'
        # 3. Contain "DM=" and "P0="
        # 4. Supplied DM and Period values must be floats.
        #
        # We check we meet this requirements here.

        # Create object for testing.
        par = ParFile()

        # Single file
        self.assertFalse(par.is_filename_valid("."))  # not a valid file name
        self.assertFalse(par.is_filename_valid(".par"))  # not a valid file name
        self.assertFalse(par.is_filename_valid("a.par"))  # file name valid, but not correct format.
        self.assertFalse(par.is_filename_valid("A_DM=_P0=ms.par"))  # DM missing
        self.assertFalse(par.is_filename_valid("A_DM=1.0_P0=ms.par"))  # Period missing
        self.assertFalse(par.is_filename_valid("A_DM=1.0_P0=ams.par"))  # Period not a float.
        self.assertFalse(par.is_filename_valid("A_DM=_P0=1.0ms.par"))  # DM missing
        self.assertFalse(par.is_filename_valid("A_DM=a_P0=1.0ms.par"))  # DM not a float

        # When given directory path
        self.assertFalse(par.is_filename_valid("/."))  # not a valid file name
        self.assertFalse(par.is_filename_valid("/.par"))  # not a valid file name
        self.assertFalse(par.is_filename_valid("/a.par"))  # file name valid, but not correct format.
        self.assertFalse(par.is_filename_valid("/A_DM=_P0=ms.par"))  # DM missing
        self.assertFalse(par.is_filename_valid("/A_DM=1.0_P0=ms.par"))  # Period missing
        self.assertFalse(par.is_filename_valid("/A_DM=1.0_P0=ams.par"))  # Period not a float.
        self.assertFalse(par.is_filename_valid("/A_DM=_P0=1.0ms.par"))  # DM missing
        self.assertFalse(par.is_filename_valid("/A_DM=a_P0=1.0ms.par"))  # DM not a

        self.assertFalse(par.is_filename_valid("/A_DM=1.0_P0=1.0ms_Z=a.par"))  # Acceleration not a float
        self.assertFalse(par.is_filename_valid("/A_DM=1.0_P0=1.0ms_Z=.par"))  # Acceleration not a float

        # All inputs are missing *something* so should fail.
        self.assertFalse(par.is_filename_valid("dir/."))  # not a valid file name
        self.assertFalse(par.is_filename_valid("dir/.par"))  # not a valid file name
        self.assertFalse(par.is_filename_valid("dir/a.par"))  # file name valid, but not correct format.
        self.assertFalse(par.is_filename_valid("dir/A_DM=_P0=ms.par"))  # not correct format (DM & P0 missing).
        self.assertFalse(par.is_filename_valid("dir/A_DM=1.0_P0=ms.par"))  # not correct format (P0 missing).
        self.assertFalse(par.is_filename_valid("dir/A_DM=1.0_P0=ams.par"))  # not correct format (P0 not a float).
        self.assertFalse(par.is_filename_valid("dir/A_DM=_P0=1.0ms.par"))   # not correct format (DM missing).
        self.assertFalse(par.is_filename_valid("dir/A_DM=a_P0=1.0ms.par"))  # not correct format (DM not a float).

        # Should pass as format is correct
        self.assertTrue(par.is_filename_valid("A_DM=1.0_P0=1.0ms_Z=0.0.par"))
        self.assertTrue(par.is_filename_valid("a/A_DM=1.0_P0=1.0ms_Z=0.0.par"))
        self.assertTrue(par.is_filename_valid("A_DM=1000.0_P0=1000.0ms_Z=-10.0.par"))
        self.assertTrue(par.is_filename_valid("a/A_DM=1000.0_P0=1000.0ms_Z=-10.0.par"))

    # ****************************************************************************************************

    def test_create_valid_file_name(self):
        """Tests the method that creates a par file, file name."""

        # File name should be in this format:
        #
        # <PULSAR NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms.par

        # Create object for testing.
        par = ParFile()

        # File name should be in this format:
        #
        # <PULSAR NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms.par
        #
        # Thus the name should not contain any underscores,
        # dm should be a float, and period_ms should also be a float
        # We check for these requirements here:

        # Name has incorrect format
        self.assertEqual(par.create_valid_file_name(None, 1.0, 1.0, 0.0), None)
        self.assertEqual(par.create_valid_file_name("", 1.0, 1.0, 0.0), None)
        self.assertEqual(par.create_valid_file_name("_", 1.0, 1.0, 0.0), None)

        # DM format incorrect
        self.assertEqual(par.create_valid_file_name("a", None, 1.0, 0.0), None)
        self.assertEqual(par.create_valid_file_name("a", "", 1.0, 0.0), None)
        self.assertEqual(par.create_valid_file_name("a", "a", 1.0, 0.0), None)

        # Period format incorrect
        self.assertEqual(par.create_valid_file_name("a", 1.0, None, 0.0), None)
        self.assertEqual(par.create_valid_file_name("a", 1.0, "", 0.0), None)
        self.assertEqual(par.create_valid_file_name("a", 1.0, "a", 0.0), None)

        self.assertEqual(par.create_valid_file_name("a", 1.0, 1.0, 0.0), "a_DM=1.0_P0=1.0ms_Z=0.0.par")

    # ****************************************************************************************************

    def test_compute_binary_parameters(self):
        """
        Tests the method that attempts to compute binary pulsar parameters, for a given acceleration,
        assuming some constants (1.4 mass host and the same for the companion.

        """

        # Create object for testing.
        par = ParFile()

        accel = 10.0
        period_seconds = 1.0
        pepoch = 56000.0
        pb, a1, t0 = par.compute_binary_params(accel, period_seconds, pepoch)

        self.assertAlmostEqual(pb, 1.06815941, 5)
        self.assertAlmostEqual(a1, 7.19698149, 5)
        self.assertAlmostEqual(t0, 56000.266171797, 5)

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
