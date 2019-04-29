"""
    **************************************************************************
    |                                                                        |
    |               Gaussian Profile Generator Version 1.0                   |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    **************************************************************************
    |                                                                        |
    | Generates simple Gaussian or double Gaussian pulse profiles, and       |
    | writes them out to .asc files compatible with the inject_pulsar tool.  |
    | Pulse profile length can be varied, as can the numerical range for     |
    | pulse intensity values.                                                |
    |                                                                        |
    | The .asc files produced by this script will:                           |
    |                                                                        |
    | 1. contain pulse intensity values in ascii format. Each line in the    |
    |    file corresponds to a phase bin value. For example,                 |
    |                                                                        |
    |    1.0                                                                 |
    |    2.0                                                                 |
    |    3.0                                                                 |
    |    2.0                                                                 |
    |    1.0                                                                 |
    |                                                                        |
    |    Contains 5 bins, with a max value of 3.0, and min of 1.0.           |
    |                                                                        |
    | 2. Have a file name that adheres to the format,                        |
    |                                                                        |
    |   <ID>_DC=<Duty Cycle>_BINS=<Bins>_FWHM=<FWHM>.asc                     |
    |                                                                        |
    |   where <ID> is a string that uniquely identifies the .asc file,       |
    |   <Duty Cycle> is a float describing the fraction of the period that   |
    |   the pulse is "on" for, <Bins> is an integer describing the number of |
    |   phase bins in the profile, and <FWHM> is a float corresponding to    |
    |   the full-width at half maximum (FWHM). A valid filename could be as  |
    |   follows:                                                             |
    |                                                                        |
    |       Gaussian_DC=0.5_BINS=128_FWHM=64.asc                             |
    |                                                                        |
    | The code is compatible with python version 3.6. It requires Scipy,     |
    | Numpy and matplotlib libraries.                                        |
    |                                                                        |
    **************************************************************************
    | Required Arguments:                                                    |
    **************************************************************************
    |                                                                        |
    | -n (integer) number of profile bins (def = 256).                       |
    | -a (float)  min profile value when normalising to [a,b] (def = 0).     |
    | -b (float)  max profile value when normalising to [a,b] (def = 255).   |
    | -d (integer) duty cycle (def = 10%) computed using the FWHM (max 50%). |
    | -t (integer) type of signal to generate (def = 1). Valid values:       |
    |              0 = Gaussian                                              |
    |              1 = Double Gaussian                                       |
    |                                                                        |
    **************************************************************************
    | Optional Arguments:                                                    |
    **************************************************************************
    |                                                                        |
    | -v (boolean) plots the pulse profile shape for viewing (def = FALSE).  |
    |                                                                        |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@manchester.ac.uk                                   |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | License:                                                               |
    **************************************************************************
    |                                                                        |
    | Code made available under the GPLv3 (GNU General Public License), that |
    | allows you to copy, modify and redistribute the code as you see fit    |
    | (http://www.gnu.org/copyleft/gpl.html). Though a mention to the        |
    | original author using the citation above in derivative works, would be |
    | very much appreciated.                                                 |
    **************************************************************************
"""

# Command line processing imports:
from optparse import OptionParser

# Other imports
import os
import operator
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize
from scipy.interpolate import UnivariateSpline


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class GaussianProfileGen:
    """
    Description:

    Generates simple Gaussian or double Gaussian pulse profiles, and
    writes them out to .asc files compatible with the inject_pulsar tool.
    Pulse profile length can be varied, as can the numerical range for
    pulse intensity values.
    """

    def __init__(self):
        """
        Initialises the class and class variables.
        """
        # Set some initial values - will be overwritten when processing
        # command line parameters.
        self.verbose      = False     # Verbose logging flag.
        self.bins         = 250       # Number of bins in the profile.
        self.min_a        = 0.0       # Min value desired in the profile.
        self.max_b        = 255.0     # Max value desired in the profile.
        self.duty_cycle   = 0.1       # The pulse duty cycle.
        self.signal_type  = 0         # The signal type desired by the user.
        self.profile      = []        # Pulse profile data.
        self.signal_types = ['Gaussian', 'Double Gaussian']

        # Pre-process arguments to make unit testing easier.
        self.arguments = None

        # Values found during optimisation.
        self.opt_y = []
        self.opt_x = []
        self.optimised_sigma = 0.0
        self.actual_fwhm = 0.0

    # ******************************************************************************************

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    def main(self, argv=None):
        """Main method.

        Main entry point for the Application. Processes command line
        input and begins automating the the creation of par files.

        Parameters
        ----------
        argv : str
            The unused arguments.

        """

        # ****************************************
        #         Execution information
        # ****************************************

        print(__doc__)

        # ****************************************
        #    Command line argument processing
        # ****************************************

        # Argument processing.
        parser = OptionParser()


        # REQUIRED ARGUMENTS
        parser.add_option("-n", action="store", dest="n", type=int,
                          help='number of profile bins (def = 256)', default=256)

        parser.add_option("-a", action="store", dest="a", type=float,
                          help='min profile value when normalising to [a,b] (def = 0)', default=0.0)

        parser.add_option("-b", action="store", dest="b", type=float,
                          help='max profile value when normalising to [a,b] (def = 255)', default=255.0)

        parser.add_option("-d", action="store", dest="d", type=float,
                          help='duty cycle (def = 10%) computed using the FWHM', default=0.1)

        parser.add_option("-t", action="store", dest="t", type=int,
                          help='type of signal to generate (see help)', default=0)

        # OPTIONAL ARGUMENTS
        parser.add_option("-v", action="store_true", dest="v",
                          help='Verbose plotting flag (optional)', default=False)

        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        self.verbose        = args.v
        self.bins           = args.n
        self.min_a          = args.a
        self.max_b          = args.b
        self.duty_cycle     = args.d
        self.signal_type    = args.t
        self.profile        = []
        self.signal_types   = ['Gaussian', 'Double Gaussian']

        # Pre-process arguments to make unit testing easier.
        self.arguments = [args.v, args.n, args.a, args.b, args.d, args.t]

        # Values found during optimisation.
        self.opt_y = []
        self.opt_x = []
        self.optimised_sigma = 0.0
        self.actual_fwhm = 0.0

        # ****************************************
        #      Print command line arguments
        # ****************************************

        print("\n\t**************************")
        print("\t| Command Line Arguments |")
        print("\t**************************")
        print("\tDebug: "       + str(self.verbose))
        print("\tBins: "        + str(self.bins))
        print("\tDuty cycle: "  + str(self.duty_cycle))
        print("\tSignal type: " + str(self.signal_types[self.signal_type]))
        print("\tMin and max profile values [a,b]: [" + str(self.min_a) + "," + str(self.max_b) + "]")

        # Check the command line parameters are valid.
        if self.check_parameters(self.arguments):

            # Continue to build profile
            print("\n\t**************************")
            print("\t|   Generation Underway  |")
            print("\t**************************")
            print("\n\tBuilding profile...")
            print("\tGenerating a " + str(self.signal_types[self.signal_type]) + " profile.")

            no_profile_generated = True

            if self.signal_type == 0:

                self.profile = self.create_gaussian(self.min_a, self.max_b, self.bins, self.duty_cycle)

                if self.profile is not None:
                    no_profile_generated = False

            elif self.signal_type == 1:

                self.profile = GaussianProfileGen.create_double_gaussian()

                if self.profile is not None:
                    no_profile_generated = False

            #
            # Now we check the results of generation...
            #
            if no_profile_generated is True:
                print("\tUnable to build profile, unknown error, exiting")
            else:

                print("\n\t**************************")
                print("\t|     Profile Details    |")
                print("\t**************************")

                # Note the values for these variables are actually obtained in
                # the call to create_gaussian() which was made earlier.
                print("\tProfile length: " + str(len(self.profile)))
                print("\tOptimal Sigma value found:" + str(self.optimised_sigma))

                # Compute the FWHM for the data produced.
                spline = UnivariateSpline(self.opt_x, self.profile - np.max(self.profile) / 2.0, s=0)
                r1, r2 = spline.roots()  # find the roots
                self.actual_fwhm = (r2 - r1)

                print("\tActual FWHM = " + str(self.actual_fwhm))

                # Difference in actual and required FWHM to meet duty cycle requirements.
                diff_in_bins = (self.bins * self.duty_cycle) - self.actual_fwhm
                print("\tError margin in FWHM width: " + str(np.abs(((diff_in_bins / self.actual_fwhm) * 100))) + "%.")

                if self.verbose:
                    print("\n\tShowing profile plot (please close the plot to continue program).")
                    plt.plot(self.opt_x, self.profile)
                    plt.axvspan(r1, r2, facecolor='g', alpha=0.5)
                    plt.show()

                print("\n\t**************************")
                print("\t|  Building output Path  |")
                print("\t**************************")

                # Save profile to file.
                file_path = self.get_profile_file_name(self.signal_type, self.bins, self.actual_fwhm, self.duty_cycle)
                print("\n\tPath: " + str(file_path))

                file_ready = False

                # Check if file path exists.
                if os.path.exists(file_path):
                    # It exists, but is it a file?
                    if os.path.isfile(file_path):
                        # If it is a file, clear the file.
                        GaussianProfileGen.clear_file(file_path)

                        # Update the flag
                        file_ready = True
                else:
                    # Path doesn't exist, so we can just create the file.
                    GaussianProfileGen.append_to_file(file_path, '')

                    file_ready = True

                print("\n\t**************************")
                print("\t|       Writing File     |")
                print("\t**************************")

                if file_ready:
                    line_counter = 0
                    for sample in self.profile:
                        text = str(sample) + "\n"
                        GaussianProfileGen.append_to_file(file_path, text)
                        line_counter += 1

                    print("\tLines written: " + str(line_counter))
                    print("\tWritten to: " + str(file_path))
                    print("\tFile write complete.")
                else:
                    print("\tCould not write file to:"+ str(file_path))
                    print("\tCannot save profile, exiting.")

        else:
            print("\n\t**************************")
            print("\t|   Parameters Invalid  |")
            print("\t**************************")
            print("\tCannot build profile, exiting.")


        print("\n\tDone.")
        print("\t**************************************************************************")

    # ******************************************************************************************

    @staticmethod
    def gaussian(x, mu, sig):
        """
        The Gaussian function used to create a Gaussian pulse profile.

        Parameters
        ----------
        :param x: an array of data points on the x-axis.
        :param mu: distribution mean.
        :param sig: distribution standard deviation.

        Returns
        ----------
        :return: an array describing the y values.
        """
        # Compute Gaussian in parts for clarity
        p1 = 1.0 / (np.sqrt(2.0 * np.pi * (sig**2.0)))
        p2 = np.power((x-mu), 2.0) / (2.0 * (sig**2.0))
        return p1 * np.exp(-p2)

    # ****************************************************************************************************

    def optimise_sigma(self, params):
        """
        Optimises the value of sigma used to build a Gaussian with a FWHM
        exactly equal to the required duty cycle.

        Parameters
        ----------
        :param params: the parameters to be optimised (sigma)

        Returns
        ----------
        :return: the difference between the FWHM bins required, and the FWHM
                 achieved with sigma, squared.
        """
        # So what's all this code for? Well, simply put, creating a Gaussian with
        # an exact FWHM for a fixed number of bins and duty cycle, was proving
        # be more difficult than it should be! Using the formula for converting
        # between FWHM and Sigma, gave misleading results - the FWHM was always
        # out by more than you would expect. I assumed my implementation of the
        # FWHM or sigma calculation must be wrong. But after triple checking, I
        # Know I was getting misleading results. To overcome this problem, I
        # turned this into an optimisation task. The goal is to find a sigma value
        # for the standard Gaussian model, that gives rise to a FWHM closest to that
        # which the user asked for, for an arbitrary duty cycle.


        # General approach:
        # # use the Scipy.optimise.UnivariateSpline function to quickly calculate the
        # FWHM of Gaussian data. We compute the difference between the actual FWHM found
        # using an arbitrary value of sigma, and the desired FWHM determined by the duty
        # cycle, to calculate an error rate. Where the error rate is,
        #
        # (FWHM when using sigma - FWHM needed)**2
        #
        # We square this value so the error 'landscape becomes a parabola. The value of
        # sigma that minimises the difference, should give us a Gaussian with the exact
        # FWHM we need.

        # Get parameter - should just be sigma, so assign to variable directly.
        sig = params

        # Fix the mean and location parameter irrelevant.
        mu = 0.0

        # How many bins wide the FWHM should be.
        fwhm_bins = float(self.bins) * self.duty_cycle

        # The next bit is a hack to fix a problem I don't have the time
        # to fully understand. The choice of bin values effects the
        # Scipy.optimise.UnivariateSpline function, causing it to find
        # sub-optimal values of sigma. I have used empirical experience to
        # hard-code values that overcome this problem.
        if self.duty_cycle < 0.5:
            bin_start = (-(self.bins / 2.0)) - self.bins * self.duty_cycle
            bin_end = (self.bins / 2.0)      + self.bins * self.duty_cycle
        else:
            bin_start = -(self.bins / 2.0)-1
            bin_end = (self.bins / 2.0)+1

        # I assign the x-values and Gaussian data computed to class variables
        # for convenience.
        self.opt_x = np.linspace(bin_start, bin_end, self.bins)
        self.opt_y = GaussianProfileGen.gaussian(self.opt_x, mu, sig)

        spline = UnivariateSpline(self.opt_x, self.opt_y - np.max(self.opt_y) / 2.0, s=0)
        r1, r2 = spline.roots()  # find the roots
        actual_fwhm = (r2 - r1)
        needed = fwhm_bins

        # Compute error rate
        error_rate = (float(actual_fwhm) - float(needed)) ** 2.0

        return error_rate

    # ******************************************************************************************

    # ******************************
    #
    # PROFILE GENERATION CODE
    #
    # ******************************

    def create_gaussian(self, pMin, pMax, bins, dc):
        """
        Calls functions that create the Gaussian pulse profile,
        returns the profile as an array.

        Parameters
        ----------
        :param pMin: the min value in the pulse profile.
        :param pMax: the max value in the pulse profile.
        :param bins: the number of bins in the profile.
        :param dc: the duty cycle of the profile.

        Returns
        ----------
        :return: an array of profile values, scaled to the appropriate range.
        """
        # The number of bins that should be covered by the FWHM
        fwhm_bins = float(bins) * dc

        print("\tRequires" + str(dc * 100)+ "% duty cycle across " + str(bins) + " bins.")
        print("\tAssuming pulse width makes up " + str(dc * 100) + "% of profile (" + str(fwhm_bins) + " bins).")
        print("\tWhere pulse width is computed as the Full Width at Half Maximum (FWHM).")

        # Here we estimate what value of sigma gives us a pulse with a FWHM that matches the
        # duty cycle requirements. This isn't straightforward, as the formula that estimates
        # sigma doesn't appear to give exact answers.
        sigma = float(GaussianProfileGen.gamma_to_sigma(fwhm_bins))
        print("\tSigma = " + str(sigma) + " required to produce pulse with FWHM = " + str(fwhm_bins) + " bins")

        # We use scipy optimise the find the perfect sigma value that gives
        # us the desired FWHM in bins. The optimisation function I've used
        # doesn't play nice - so we have to restrict the parameter range it uses,
        # otherwise it finds sub-optimum local minima.
        #
        # This is because, for reasons I don't truly understand, the error rate
        # in the solutions found differs, according to the duty cycle used. This
        # is weird, but I don't have time to troubleshoot this. I imagine it is
        # simply odd behaviour caused by the optimisation algorithm used in Scipy.
        # To compensate, I've found some empirically useful bounds that allow us to
        # converge on a good result, such that the error rate is at worst, 0.36 ,
        # when using a profile of 4096 bins, with a 50% duty cycle.
        if self.duty_cycle >= 0.5:
            bnds = ((sigma*0.75, sigma*1.25),)
        else:
            bnds = ((sigma * 0.5, sigma * 1.5),)  # Bounds over sigma (don't need to search all sigma values.

        # Assign the initial guess made using the FWHM estimation formula,
        # see: https://en.wikipedia.org/wiki/Full_width_at_half_maximum
        initial_guess = [sigma]

        # Run the optimisation step.
        result = optimize.minimize(self.optimise_sigma, initial_guess, method='SLSQP', bounds=bnds)

        if result.success:

            # Obtain the sigma value found
            self.optimised_sigma = result.x[0]

            # Now scale the profile to the desired range.
            scaled_y = GaussianProfileGen.scale(self.opt_y, pMin, pMax)

            return scaled_y
        else:
            return None

    # ******************************************************************************************

    @staticmethod
    def create_double_gaussian():
        """
        Not implemented yet...
        :return:
        """

        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # ******************************************************************************************

    @staticmethod
    def gamma_to_sigma(Gamma):
        """
        Function to convert FWHM (Gamma) to standard deviation (sigma)
        """
        return Gamma * np.sqrt(2.0) / (np.sqrt(2.0 * np.log(2)) * 2.0)

    @staticmethod
    def sigma_to_gamma(sigma):
        """
        Function to convert standard deviation (sigma) to FWHM (Gamma)
        """
        return sigma * np.sqrt(2.0 * np.log(2.0)) * 2.0 / np.sqrt(2.0)

    # ******************************************************************************************

    @staticmethod
    def scale(data, new_min, new_max):
        """
        Scales the profile data for pfd files so that it is in the range [new_min,new_max].

        Parameters
        ----------
        :param data: the data to scale.
        :param new_min: the new minimum value for the data range.
        :param new_max: the new maximum value for the data range.

        Returns
        ----------
        :return: A new array with the data scaled to within the range [new_min,new_max].
        """
        min_ = min(data)
        max_ = max(data)

        new_data = []

        for n in range(len(data)):
            value = data[n]
            x = (new_min * (1 - ((value - min_) / (max_ - min_)))) + (new_max * ((value - min_) / (max_ - min_)))
            new_data.append(x)

        return new_data

    # ******************************************************************************************

    @staticmethod
    def centre_on_peak(data):
        """
        Centre the data such that the maximum value is at
        the centre of the data.

        Parameters
        ----------
        :param data: the data to centre.

        Returns
        ----------
        :return: a centred version of the data.
        """

        # Stores the centred data.
        centred_data = []

        # Get the index of the maximum value.
        index, value = max(enumerate(data), key=operator.itemgetter(1))

        # Find midpoint of the data.
        midpoint = int(len(data) / 2)

        # Figure out the shift required to centre the data (put max value in centre bin).
        n = midpoint - index  # N gives the number of bins the data should be shifted.
        a = n % len(data)

        # Actually do the centre
        centred_data = data[-a:] + data[:-a]

        return centred_data

    # ******************************************************************************************

    # ******************************
    #
    # COMMAND LINE PROCESSING CODE
    #
    # ******************************

    def check_parameters(self, args):
        """
        Checks the parameters provided by the user.

        Parameters
        ----------
        self : object
            The object pointer.

        args : []
            The arguments.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        print("\n\t**************************")
        print("\t|  Checking Parameters   |")
        print("\t**************************")

        # There are 6 command line parameters - these must be checked
        # to ensure the user doesn't do anything crazy. We check each parameter
        # in turn, in different ways including,
        #
        # 1. Type checking
        # 2. Formatting checks
        # 3. Boundary condition checks

        outcome = True

        # Check the types are as expected.
        outcome = GaussianProfileGen.check_parameter_types(args)

        if not outcome:
            print("\tOne or more parameters are not of the expected type.")
            return False

        outcome = GaussianProfileGen.check_parameter_values(args)

        if not outcome:
            print("\tOne or more parameter values do not adhere to boundary/range conditions.")
            return False

        print("\n\tParameter check complete.")

        return True

    # ******************************************************************************************

    @staticmethod
    def check_parameter_types(args, testing=False):
        """
        Checks the parameters provided by the user are of the correct type.

        Parameters
        ----------

        args : []
            The arguments. These are ordered as follows:
            args[0] = verbose flag
            args[1] = number of bins
            args[2] = min profile value
            args[3] = max profile value
            args[4] = duty cycle
            args[5] = profile type

        testing : boolean
                A flag that when true, suppresses output during testing.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        outcome = True

        # Verbose flag
        if type(args[0]) != bool:
            if not testing:
                print("\tVerbose parameter not the correct type", "(", type(args[0]), ")", ".")
            outcome = False

        # Number of bins
        if type(args[1]) != int:
            if not testing:
                print("\tBins parameter not an integer ", "(", type(args[1]), ")", ".")
            outcome = False

        # Min profile value
        if type(args[2]) != float:
            if not testing:
                print("\tMin parameter not a float ", "(", type(args[2]), ")", ".")
            outcome = False

        # Max profile value value
        if type(args[3]) != float:
            if not testing:
                print("\tMax parameter not a float ", "(", type(args[3]), ")", ".")
            outcome = False

        # Duty cycle
        if type(args[4]) != float:
            if not testing:
                print("\tDuty cycle parameter not a float ", "(", type(args[4]), ")", ".")
            outcome = False

        # Profile type
        if type(args[5]) != int:
            if not testing:
                print("\tType parameter not an integer ", "(", type(args[5]), ")", ".")
            outcome = False

        return outcome

    # ******************************************************************************************

    @staticmethod
    def check_parameter_values(args, testing=False):
        """
        Checks the parameter values provided by the user do not violate boundary
        or range conditions.

        Parameters
        ----------

        args : []
            The arguments. These are ordered as follows:
            args[0] = verbose flag
            args[1] = number of bins
            args[2] = min profile value
            args[3] = max profile value
            args[4] = duty cycle
            args[5] = profile type

        testing : boolean
                A flag that when true, suppresses output during testing.

        Returns
        -------
        True if the parameters are valid, else False.

        """

        outcome = True

        # Number of bins
        if args[1] <= 2:
            if not testing:
                print("\tNot enough bins specified (must be more than 0) .")
            outcome = False

        # Min and max parameters
        if args[2] >= args[3]:
            if not testing:
                print("\tMin parameter must be strictly less than Max parameter.")
            outcome = False

        # Duty cycle
        if args[4] <= 0.0 or args[4] > 0.5:
            if not testing:
                print("\tDuty cycle must have a value greater than zero and less than or equal to 0.5.")
            outcome = False

        # Type
        if args[5] < 0 or args[5] > 1:
            if not testing:
                print("\tType parameter must be either 0 (Gaussian) or 1 (Double Gaussian).")
            outcome = False

        return outcome

    # ******************************************************************************************

    # ******************************
    #
    # FILE HANDLING CODE
    #
    # ******************************

    def get_profile_file_name(self, typ, bins, fwhm, dc):
        """
        Builds a valid profile file name.

        Parameters
        ----------
        :param typ: the pulse type as an index corresponding to a value in the signal_types list.
        :param bins: the number of bins in the profile.
        :param fwhm: the FWHM of the pulse.
        :param dc: the duty cycle.

        Return
        --------
        A valid file name (string).
        """

        "{:.4f}".format(fwhm)

        extension = ".asc"

        return self.signal_types[typ] + "_DC=" + str(dc) + "_BINS=" + str(bins) + \
               "_FWHM=" + "{:.4f}".format(fwhm) + extension

    # ******************************************************************************************

    @staticmethod
    def append_to_file(path, text):
        """Appends the provided text to the file at the specified path.

        Parameters
        ----------
        path : str
            The full path to the file to write to.
        text : str
            The text to write to the output file.

        Returns
        ----------
        True if the operation completed successfully, else false.

        Examples
        --------
        >>> append_to_file("/Users/rob/test.txt","This is my text")

        which will append the text "This is my text" to the file.
        """

        try:
            destination_file = open(path, 'a')
            destination_file.write(str(text))
            destination_file.close()
            return True
        except IOError:
            return False

    # ******************************************************************************************

    @staticmethod
    def clear_file(path):
        """
        Clears the contents of the file at the specified path.

        Parameters
        ----------
        path : str
            The full path to the file to clear.

        Examples
        --------
        >>> clear_file("/Users/rob/test.txt")

        which will clear all text in the file.
        """
        open(path, 'w').close()

    # ******************************************************************************************

if __name__ == '__main__':
    GaussianProfileGen().main()
