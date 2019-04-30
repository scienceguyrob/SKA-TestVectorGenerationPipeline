"""
    **************************************************************************
    |                                                                        |
    |            Profile Generator Test Suite Runner Version 1.0             |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Executes simple tests of functions/functionality in the python script  |
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

# Used for logging purposes, please don't delete.
import logging
import sys

# Unit testing modules
from unittest import TestLoader, TextTestRunner, TestSuite

# Modules to test.
from code.pulsar_injection_pipeline.beta.test.src.profile.TestProfileGeneration import TestProfileGeneration
from code.pulsar_injection_pipeline.beta.test.src.utils.TestParameterHandling import TestParameterHandling
from code.pulsar_injection_pipeline.beta.test.src.utils.TestFakeParParameterHandling import TestFakeParParameterHandling
from code.pulsar_injection_pipeline.beta.test.src.files.TestParFileObject import TestParFileObject
from code.pulsar_injection_pipeline.beta.test.src.files.TestPredFileObject import TestPredFileObject
from code.pulsar_injection_pipeline.beta.test.src.files.TestAscFileObject import TestAscFileObject
from code.pulsar_injection_pipeline.beta.test.src.files.TestFilenameComponent import TestFilenameComponent
from code.pulsar_injection_pipeline.beta.test.src.files.TestCompoundFilenameComponent import TestCompoundFilenameComponent
from code.pulsar_injection_pipeline.beta.test.src.files.TestDelimitedFilename import TestDelimitedFilename
from code.pulsar_injection_pipeline.beta.test.src.utils.TestCommon import TestCommon


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class ProfileGenTestSuiteRunner(TestSuite):
    """                
    Executes unit tests on all functions/functionality.
    """

    def __init__(self):
        """
        Default constructor for the base class.

        Parameters
        ----------

        Returns
        ----------

        Examples
        --------
        >>>

        :return: N/A
        """

        # Create a logger object.
        super(ProfileGenTestSuiteRunner, self).__init__()
        self.logger = logging.getLogger('TestVectorUtils')

        # create a file handler
        handler = logging.FileHandler('TestVectorUtils.log')

        # Set the logging level.
        self.logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)

        # Create the logging format
        formatter = logging.Formatter('%(levelname)s,%(asctime)s,%(message)s', datefmt='%H:%M:%S')

        # Configure the logging handler with the desired output format
        handler.setFormatter(formatter)

        # Setup the log file writer
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(handler)
        self.logger.addHandler(ch)

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    def main(self):
        """
        Main entry point for the Application.

        Parameters
        ----------

        Returns
        ----------

        Examples
        --------
        >>>
        """

        self.run_tests()

    # ****************************************************************************************************

    def run_tests(self):
        """
        Runs the tests in the test suite.

        Parameters
        ----------

        Returns
        ----------

        Examples
        --------
        >>>

        :return: N/A
        """

        self.logger.info('Running Unit Tests')

        loader = TestLoader()
        suite = TestSuite((
            loader.loadTestsFromTestCase(TestParameterHandling),
            loader.loadTestsFromTestCase(TestProfileGeneration),
            loader.loadTestsFromTestCase(TestFakeParParameterHandling),
            loader.loadTestsFromTestCase(TestParFileObject),
            loader.loadTestsFromTestCase(TestPredFileObject),
            loader.loadTestsFromTestCase(TestAscFileObject),
            loader.loadTestsFromTestCase(TestFilenameComponent),
            loader.loadTestsFromTestCase(TestCompoundFilenameComponent),
            loader.loadTestsFromTestCase(TestDelimitedFilename),
            loader.loadTestsFromTestCase(TestCommon)
        ))

        runner = TextTestRunner(verbosity=3)
        runner.run(suite)

        # ****************************************************************************************************


if __name__ == '__main__':
    ProfileGenTestSuiteRunner().main()