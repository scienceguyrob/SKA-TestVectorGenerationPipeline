##############################################################################################
# Purpose   : Dockerize Components of Pulsar software stack.
# Python    : 2.7
# Version   : 0.1
# Author    : Rob Lyon (robert.lyon@manchester.ac.uk)
##############################################################################################
#
# This docker file will setup an environment with only a basic pulsar stack. This
# is because the image is to be used for test vector generation, for tests of SKA
# SDP and CSP software. For a more complete pulsar image, look at the Dockerfile's
# written by Casey Law, or Maciej Serylak. I've documented this Dockerfile which I
# hope makes its content a lot easier to understand.
#
# SOFTWARE:
#
# tempo, tempo2
# sigproc
# inject_pulsar (Mike keith's build of sigproc)
# python 2.6 (scipy, numpy stacks).
# fftw 3
# dev tools (gfortran etc.)
# PRESTO is not compiled due to an error: https://github.com/scottransom/presto/issues/68
#
# Please see DockerImageReadme.txt for software version information.
##############################################################################################

# Use well supported distribution.
FROM centos:7

# Contact me for help!
MAINTAINER robert.lyon@manchester.ac.uk

# The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT,
# COPY and ADD instructions that follow it in the Dockerfile. If the WORKDIR doesn’t
# exist, it will be created even if it’s not used in any subsequent Dockerfile instruction.
WORKDIR /home

##############################################################################################
# Install 'OS' software.
##############################################################################################

RUN yum -y install epel-release
RUN yum -y update && yum -y install \

    # **************************************************
    #
    # OS tools
    #
    # **************************************************

    # VERSION: 6.18.01
    # LINK: https://pkgs.org/centos-7/centos-x86_64/tcsh-6.18.01-8.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # Tcsh is an enhanced but completely compatible version of csh, the C shell.
    tcsh \

    # VERSION: 6.0
    # LINK: https://pkgs.org/centos-7/centos-x86_64/unzip-6.0-15.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # The unzip utility is used to list, test, or extract files from a zip archive.
    unzip \

    # VERSION: 1.14
    # LINK: https://pkgs.org/centos-7/centos-x86_64/wget-1.14-10.el7_0.1.x86_64.rpm.html
    #
    # DESCRIPTION:
    # GNU Wget is a file retrieval utility which can use either the HTTP or FTP protocols.
    wget \

    # **************************************************
    #
    # Compilation / Dev tools
    #
    # **************************************************

    # VERSION: 2.8.11
    # LINK: https://pkgs.org/centos-7/centos-x86_64/cmake-2.8.11-5.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # CMake is used to control the software compilation process using simple platform
    # and compiler independent configuration files.
    make \

    # VERSION: 2.69
    # LINK: https://pkgs.org/centos-7/centos-x86_64/autoconf-2.69-11.el7.noarch.rpm.html
    #
    # DESCRIPTION:
    # GNU's Autoconf is a tool for configuring source code and Makefiles.
    autoconf \

    # VERSION: 1.13.4
    # LINK: https://pkgs.org/centos-7/centos-x86_64/automake-1.13.4-3.el7.noarch.rpm.html
    #
    # DESCRIPTION:
    # Automake is a tool for automatically generating `Makefile.in' files compliant with
    # the GNU Coding Standards.
    automake \

    # VERSION: 4.8.5
    # LINK: https://pkgs.org/centos-7/centos-x86_64/gcc-4.8.5-4.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # The gcc package contains the GNU Compiler Collection version 4.8. You'll need this
    # package in order to compile C code.
    gcc \

    # VERSION: 4.8.5
    # LINK: https://pkgs.org/centos-7/centos-x86_64/gcc-gfortran-4.8.5-4.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # The gcc-gfortran package provides support for compiling Fortran programs with the GNU
    # Compiler Collection.
    gcc-gfortran \

    ##########################################################################################
    #
    # ALL THE SOFTWARE LISTED SO FAR IS REQUIRED TO BUILD TEMPO
    #
    ##########################################################################################

    # VERSION: 2.4.2
    # LINK: https://pkgs.org/centos-7/centos-x86_64/libtool-ltdl-2.4.2-20.el7.i686.rpm.html
    #
    # DESCRIPTION:
    # The libtool-ltdl package contains the GNU Libtool Dynamic Module Loader, a library that
    # provides a consistent, portable interface which simplifies the process of using dynamic
    # modules.
    libtool \

    # VERSION: 4.8.5
    # LINK: https://pkgs.org/centos-7/centos-x86_64/gcc-c++-4.8.5-4.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # This package adds C++ support to the GNU Compiler Collection. It includes support for
    # most of the current C++ specification, including templates and exception handling.
    gcc-c++ \

    ##########################################################################################
    #
    # ALL THE SOFTWARE LISTED SO FAR IS REQUIRED TO BUILD TEMPO 2
    #
    ##########################################################################################

    # VERSION: 3.370
    # LINK: https://pkgs.org/centos-7/epel-x86_64/cfitsio-3.370-1.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # CFITSIO is a library of C and FORTRAN subroutines for reading and writing data
    # files in FITS (Flexible Image Transport System) data format.
    cfitsio \
    cfitsio-devel \

    # VERSION: 3.3.3
    # LINK: https://pkgs.org/centos-7/centos-x86_64/fftw-devel-3.3.3-8.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # FFTW is a C subroutine library for computing the Discrete Fourier Transform (DFT) in
    # one or more dimensions, of both real and complex data, and of arbitrary input size.
    fftw-devel

    ##########################################################################################
    #
    # ALL THE SOFTWARE LISTED SO FAR IS REQUIRED TO BUILD SIGPROC
    #
    ##########################################################################################

    # X11 required by PRESTO
    RUN yum -y groupinstall "X11"


    RUN yum -y install \

    # X11 libraries
    libX11-devel \

    # VERSION: 1.5.13
    # LINK: https://pkgs.org/centos-7/centos-x86_64/libpng-1.5.13-7.el7_2.i686.rpm.html
    #
    # DESCRIPTION:
    # The libpng package contains a library of functions for creating and manipulating
    # PNG (Portable Network Graphics) image format files.
    libpng \
    libpng-devel \

    # VERSION: 2.17
    # LINK: https://pkgs.org/centos-7/centos-x86_64/glibc-2.17-105.el7.i686.rpm.html
    #
    # DESCRIPTION:
    # The glibc package contains standard libraries which are used by multiple programs
    # on the system.
    glibc \
    glibc-devel \

    # VERSION: 2.46.2
    # LINK: https://pkgs.org/centos-7/centos-x86_64/glib2-2.46.2-4.el7.i686.rpm.html
    #
    # DESCRIPTION:
    # GLib is the low-level core library that forms the basis for projects such as
    # GTK+ and GNOME.
    glib2 \
    glib2-devel \

    # VERSION: 7.1.0
    # LINK: https://pkgs.org/centos-7/epel-x86_64/python-pip-7.1.0-1.el7.noarch.rpm.html
    #
    # DESCRIPTION:
    # Pip is a replacement for 'easy_install'.
    python-pip \
    python-devel \

    # Install tkinter UI library.
    tkinter

    # Install python modules
    RUN pip install --upgrade pip
    RUN pip install pip -U
    RUN pip install setuptools -U
    RUN pip install numpy -U
    RUN pip install scipy -U
    RUN pip install fitsio -U
    RUN pip install astropy -U
    RUN pip install astroplan -U
    RUN pip install pyfits -U
    RUN pip install matplotlib -U
    RUN pip install pyephem -U

    # First use repo that has PGPLOT
    RUN yum -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/updates/6/i386/rpmfusion-free-release-6-1.noarch.rpm https://download1.rpmfusion.org/nonfree/el/updates/6/i386/rpmfusion-nonfree-release-6-1.noarch.rpm

    # Install PGPLOT.
    RUN yum -y install pgplot

    ##########################################################################################
    #
    # ALL THE SOFTWARE LISTED SO FAR IS REQUIRED TO BUILD PRESTO
    #
    ##########################################################################################

##############################################################################################
# Setup environment variables
##############################################################################################

# Make the directory where software will be installed. Note the -p flag tells mkdir to
# also create parent directories as required.
RUN mkdir -p /home/psr/soft

# Define home, psrhome, OSTYPE
ENV HOME=/home
ENV PSRHOME=/home/psr/soft
ENV OSTYPE=linux

# Python packages
ENV PYTHONPATH=$HOME/ve/lib/python2.7/site-packages

# psrcat
ENV PSRCAT_FILE=$PSRHOME/psrcat_tar/psrcat.db
ENV PATH=$PATH:$PSRHOME/psrcat_tar

# Tempo
ENV TEMPO=$PSRHOME/tempo
ENV PATH=$PATH:$PSRHOME/tempo/bin

# Tempo2
ENV TEMPO2=$PSRHOME/tempo2/T2runtime
ENV PATH=$PATH:$PSRHOME/tempo2/T2runtime/bin
ENV C_INCLUDE_PATH=$C_INCLUDE_PATH:$PSRHOME/tempo2/T2runtime/include
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PSRHOME/tempo2/T2runtime/lib

# SIGPROC
# These flags assist with the Sigproc compilation process, so do not remove them. If you take
# them out, then Sigproc will not build correctly.
ENV SIGPROC=$PSRHOME/sigproc
ENV PATH=$PATH:$SIGPROC/install/bin
ENV FC=gfortran
ENV F77=gfortran
ENV CC=gcc
ENV CXX=g++

# PRESTO
ENV PRESTO=$PSRHOME/presto
ENV PATH=$PATH:$PRESTO/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PRESTO/lib
ENV PYTHONPATH=$PYTHONPATH:$PRESTO/lib/python

##############################################################################################
# TEST VECTOR PIPELINE + README Setup
##############################################################################################
# Download test vector files
WORKDIR /home
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v1.1/Dockerfile/CentOS/DockerImageReadme.txt

WORKDIR $PSRHOME
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v1.1/Deploy/pulsar_injection_pipeline.zip
RUN unzip pulsar_injection_pipeline.zip -d $PSRHOME
RUN rm __MACOSX -R
RUN rm pulsar_injection_pipeline.zip

##############################################################################################
# Elmarie van Heerden's Code
##############################################################################################

RUN mkdir /home/psr/soft/evh
WORKDIR $PSRHOME/evh
RUN wget https://raw.githubusercontent.com/EllieVanH/PulsarDetectionLibrary/master/Readme_For_Ersartz.txt
RUN wget https://raw.githubusercontent.com/EllieVanH/PulsarDetectionLibrary/master/ersatz.py

##############################################################################################
# PULSAR SOFTWARE PIPELINE
##############################################################################################
WORKDIR /home

# Downloading pulsar software source codes. Here I've tried to version the software
# used, so we know all about our container environment. However some of the pulsar tools
# are not versioned explcitly. So to make sure we always have the same version of the
# pulsar tools in each image, versions of the software have been packaged and stored,
# in my github repository. It is these versions of the software that will be installed
# each time.

# Download the software
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v1.1/Deploy/Software/17_05_2017/Presto_SNAPSHOT_08_12_2016.zip
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v1.1/Deploy/Software/17_05_2017/Sigproc_MJK_SNAPSHOT_17_05_2017.zip
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v1.1/Deploy/Software/17_05_2017/Tempo_SNAPSHOT_08_12_2016.zip
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v1.1/Deploy/Software/17_05_2017/Tempo2_2016.11.3_SNAPSHOT_08_12_2016.zip

# Unzip the software
RUN unzip Presto_SNAPSHOT_08_12_2016.zip -d /home/Presto_SNAPSHOT_08_12_2016
RUN unzip Sigproc_MJK_SNAPSHOT_17_05_2017.zip -d /home/Sigproc_MJK_SNAPSHOT_17_05_2017
RUN unzip Tempo_SNAPSHOT_08_12_2016.zip -d /home/Tempo_SNAPSHOT_08_12_2016
RUN unzip Tempo2_2016.11.3_SNAPSHOT_08_12_2016.zip -d /home/Tempo2_2016.11.3_SNAPSHOT_08_12_2016

# Remove zip files
RUN rm Presto_SNAPSHOT_08_12_2016.zip
RUN rm Sigproc_MJK_SNAPSHOT_17_05_2017.zip
RUN rm Tempo_SNAPSHOT_08_12_2016.zip
RUN rm Tempo2_2016.11.3_SNAPSHOT_08_12_2016.zip

# Move the software to the correct folder location
RUN mv /home/Sigproc_MJK_SNAPSHOT_17_05_2017 /home/psr/soft/sigproc
RUN mv /home/Presto_SNAPSHOT_08_12_2016 /home/psr/soft/presto
RUN mv /home/Tempo_SNAPSHOT_08_12_2016 /home/psr/soft/tempo
RUN mv /home/Tempo2_2016.11.3_SNAPSHOT_08_12_2016 /home/psr/soft/tempo2

RUN rm /home/psr/soft/sigproc/__MACOSX -R
RUN rm /home/psr/soft/presto/__MACOSX -R
RUN rm /home/psr/soft/tempo/__MACOSX -R
RUN rm /home/psr/soft/tempo2/__MACOSX -R

##############################################################################################
# TEMPO Installation
##############################################################################################
WORKDIR $PSRHOME/tempo
RUN ./prepare && \
    ./configure --prefix=$PSRHOME/tempo && \
    make && \
    make install

##############################################################################################
# TEMPO2 Installation
##############################################################################################
# Ok here we install the latest version of TEMPO2.

WORKDIR $PSRHOME/tempo2
RUN ./bootstrap && \
    ./configure --x-libraries=/usr/lib/x86_64-linux-gnu --enable-shared --enable-static --with-pic F77=gfortran && \
    make && \
    make install && \
    make plugins-install


##############################################################################################
# Sigproc Installation
##############################################################################################
# Ok here we install sigproc - This is Mike Keith's version of Sigproc, which comes with the
# fast_fake utility. First we set the environment variables for the install, then execute the
# building steps.
WORKDIR $SIGPROC
RUN ./bootstrap && \
    ./configure --prefix=$SIGPROC/install LDFLAGS="-L/home/psr/soft/tempo2/T2runtime/lib" LIBS="-ltempo2" && \
    make && \
    make install

##############################################################################################
# PRESTO Installation
##############################################################################################
#WORKDIR $PRESTO/src
#RUN make makewisdom
# Note I have not built PRESTO due to this issue:
# https://github.com/scottransom/presto/issues/68
# I can workaround the issue by removing references to the code causing the problem, but I don't
# believe that to be a sensible solution. Especially as I'm unsure what consequence that would
# have. So for now I just inlcude the PRESTO prerequisites and the code. You can build this
# software from inside the docker container if absolutely necessary.
#RUN make prep && \
#    make
#WORKDIR $PRESTO/python/ppgplot_src
#RUN mv _ppgplot.c _ppgplot.c_ORIGINAL && \
    #wget https://raw.githubusercontent.com/mserylak/pulsar_docker/master/ppgplot/_ppgplot.c
#WORKDIR $PRESTO/python
#RUN make

##############################################################################################
# Finally...
##############################################################################################
# Define the command that will be exectuted when docker runs the container.
WORKDIR /home
ENTRYPOINT /bin/bash