import unittest

from code.pulsar_injection_pipeline.beta.main.src.PredFile import PredFile


# ******************************
#
# CLASS DEFINITION
#
# ******************************



class TestPredFileObject(unittest.TestCase):
    """
    The tests for the class.
    """

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_read(self):
        """Tests the highest level method that reads the predictor files."""

        # Pred File name should be in this format (order matters):
        #
        # <NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms_OBS=<Obs Length (s)>_F1=<F1>_F2=<F2>_T=<TCOEFF>_F=<FCOEEF>_Z=<Accel>.dat

        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"

        pred = PredFile()
        verbose_flag = True

        # Read a valid file
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))

        # Increased period
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))
        self.assertEqual(pred.dm, 1000.0)
        self.assertEqual(pred.p0, 1.0)
        self.assertEqual(pred.obs_length, 100)
        self.assertEqual(pred.f1, 1350.0)
        self.assertEqual(pred.f2, 1650.0)
        self.assertEqual(pred.tcoeff, 12)
        self.assertEqual(pred.fcoeff, 12)
        self.assertEqual(pred.accel, 0.0)

        # Increased period
        example_file_1_pth = "A_DM=1000.0_P0=10000.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))

        # Increased obs
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100000s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))

        # Increased F1
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=135000.0_F2=165000.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))

        # Increased F2
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=16500.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))

        # Increased T
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=120_F=12_Z=0.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))

        # Increased F
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=120_Z=0.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))

        # Positive accel
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=120_Z=1.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))

        # Negative accel
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=120_Z=-1.0.dat"
        self.assertTrue(pred.read(example_file_1_pth, verbose_flag))
        self.assertEqual(pred.dm, 1000.0)
        self.assertEqual(pred.p0, 1.0)
        self.assertEqual(pred.obs_length, 100)
        self.assertEqual(pred.f1, 1350.0)
        self.assertEqual(pred.f2, 1650.0)
        self.assertEqual(pred.tcoeff, 12)
        self.assertEqual(pred.fcoeff, 120)
        self.assertEqual(pred.accel, -1.0)

        # Lets induce some errors.....


        # Break DM prefix.
        example_file_1_pth = "A_M=1.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break period prefix.
        example_file_1_pth = "A_DM=1.0_0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break obs prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_BS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break f1 prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break f2 prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break T prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_j=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break F prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_j=12_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Remove suffix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=12_Z=0.0.da"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break accel prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=12_C=0.0.da"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Value errors

        # Break DM
        example_file_1_pth = "A_DM=a_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break period
        example_file_1_pth = "A_DM=1.0_P0=ams_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break obs.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=s_F1=1350.0_F2=1650.0_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break f1
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=A_F2=1650.0_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break f2
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=A_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break T
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=A_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Break F
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=A.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))


        # Invalid DM
        example_file_1_pth = "A_DM=-0.0001_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Invalid period
        example_file_1_pth = "A_DM=1.0_P0=-0.0001ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Invalid obs.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=-0.0001_F1=1350.0_F2=1650.0_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Invalid f1
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=-0.0001_F2=1650.0_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Invalid f2
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=-0.0001_T=12_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Invalid T
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=-0.0001_F=12.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Invalid F
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=-0.0001.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # F2 less than F1
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1250.0_T=12_F=-2.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # F2 equal to F1
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1350.0_T=12_F=-2.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))


    # ****************************************************************************************************

    def test_is_filename_valid(self):
        """Tests the method that checks if a '.dat' file's filename is valid."""

        # Pred File name should be in this format (order matters):
        #
        # <NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms_OBS=<Obs Length (s)>_F1=<F1>_F2=<F2>_T=<TCOEFF>_F=<FCOEEF>_Z=<Accel>.dat

        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"

        pred = PredFile()
        verbose_flag = True

        # Read a valid file
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Increased period
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Increased period
        example_file_1_pth = "A_DM=1000.0_P0=10000.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Increased obs
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100000s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Increased F1
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=135000.0_F2=165000.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Increased F2
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=16500.0_T=12_F=12_Z=0.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Increased T
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=120_F=12_Z=0.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Increased F
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=120_Z=1.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Positive accel
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=120_F=12_Z=1.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # negative accel
        example_file_1_pth = "A_DM=1000.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=120_Z=-1.0.dat"
        self.assertTrue(pred.is_filename_valid(example_file_1_pth))

        # Lets induce some errors.....


        # Break DM prefix.
        example_file_1_pth = "A_M=1.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break period prefix.
        example_file_1_pth = "A_DM=1.0_0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break obs prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_BS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break f1 prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break f2 prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break T prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_j=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break F prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_j=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break accel prefix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_j=12_Y=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Remove suffix.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=12_Z=0.0.da"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Value errors

        # Break DM
        example_file_1_pth = "A_DM=a_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break period
        example_file_1_pth = "A_DM=1.0_P0=ams_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break obs.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break f1
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=A_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break f2
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=A_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break T
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=A_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Break F
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=A_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Invalid DM
        example_file_1_pth = "A_DM=-0.0001_P0=1.0ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Invalid period
        example_file_1_pth = "A_DM=1.0_P0=-0.0001ms_OBS=100s_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Invalid obs.
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=-0.0001_F1=1350.0_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Invalid f1
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=-0.0001_F2=1650.0_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Invalid f2
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_F2=-0.0001_T=12_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Invalid T
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=-0.0001_F=12_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # Invalid F
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=-0.0001_Z=0.0.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

        # F2 less than F1
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1250.0_T=12_F=-2_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # F2 equal to F1
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1350.0_T=12_F=-2_Z=0.0.dat"
        self.assertFalse(pred.read(example_file_1_pth, verbose_flag))

        # Invalid accel
        example_file_1_pth = "A_DM=1.0_P0=1.0ms_OBS=100s_F1=1350.0_2=1650.0_T=12_F=12_Z=a.dat"
        self.assertFalse(pred.is_filename_valid(example_file_1_pth))

    # ****************************************************************************************************

    def test_create_valid_file_name(self):
        """Tests the method that creates a par file, file name."""

        # Pred File name should be in this format (order matters):
        #
        # <NAME>_DM=<DM VALUE>_P0=<PERIOD VALUE>ms_OBS=<Obs Length (s)>_F1=<F1>_F2=<F2>_T=<TCOEFF>_F=<FCOEEF>_Z=<Accel>.dat

        input_1 = ["A", 1.0, 1.0, 1, 1.0, 2.0, 1, 2, 0.0]
        out_1   = "A_DM=1.0_P0=1.0ms_OBS=1s_F1=1.0_F2=2.0_T=1_F=2_Z=0.0.dat"

        pred = PredFile()

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         out_1)

        # Now some test cases that should fail...
        input_1 = [None, 1.0, 1.0, 1, 1.0, 2.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", 1.0, 1.0, 1, 1.0, 2.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["_", 1.0, 1.0, 1, 1.0, 2.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", -1.0, 1.0, 1, 1.0, 2.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", 1.0, -1.0, 1, 1.0, 2.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", 1.0, 1.0, -1, 1.0, 2.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", 1.0, 1.0, 1, -1.0, 2.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", 1.0, 1.0, 1, 1.0, -2.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", 1.0, 1.0, 1, 1.0, 2.0, -1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", 1.0, 1.0, 1, 1.0, 2.0, 1, -2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)

        input_1 = ["", 1.0, 1.0, 1, 2.0, 1.0, 1, 2, 0.0]

        self.assertEqual(pred.create_valid_file_name(input_1[0], input_1[1], input_1[2], input_1[3],
                                                     input_1[4], input_1[5], input_1[6], input_1[7],
                                                     input_1[8]),
                         None)



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
