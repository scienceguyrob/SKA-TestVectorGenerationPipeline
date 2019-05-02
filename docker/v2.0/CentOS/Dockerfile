##############################################################################################
# Purpose   : Dockerize Components of Pulsar test vector generation software stack.
# Python    : 3.6
# Version   : 2.0
# Author    : Rob Lyon (robert.lyon@manchester.ac.uk), Rob Lyon, Yan Grange, Wietze Albers .
##############################################################################################
#
# This docker file sets up a basic test vector generation pipeline environment. It inlcudes
# only a minimal subset of pulsar community software. For a more complete pulsar image, please
# look at the excellent Dockerfile's written by,
#
# Casey Law: https://github.com/caseyjlaw/docker-psr
# Ewan Barr: https://github.com/ewanbarr?tab=repositories (multiple images here)
# Maciej Serylak: https://github.com/mserylak/pulsar_docker
#
# There is also:
#
# The docker images produced by the nanograv consortia: https://github.com/nanograv
# The kernsuite repository docker images: https://github.com/kernsuite-docker/base
#
# Perhaps these resources will prove useful.
#
# Note the size of this image is ~2.25 GB.
#
#
# SOFTWARE IN THIS IMAGE:
#
# 1. dev tools (gcc, gfortran etc.)
# 2. python 3.6
# 3. fftw 3
# 4. tempo
# 5. tempo2
# 6. sigproc (Mike keith's build of sigproc with inject_pulsar and fast_fake)
#
# SOFTWARE WE HOPE TO HAVE EVENTUALLY
# 7. psrchive
# 8. dspsr
# 9. presto
#
# Please see DockerImageReadme.md for software version information.
##############################################################################################

# Use well supported distribution. v1.0 used: FROM centos:7
FROM centos/python-36-centos7

# Contact me for help!
MAINTAINER robert.lyon@manchester.ac.uk

# The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT,
# COPY and ADD instructions that follow it in the Dockerfile. If the WORKDIR doesn’t
# exist, it will be created even if it’s not used in any subsequent Dockerfile instruction.
WORKDIR /home

# Required as user in base image set to something other than root.
USER root

##############################################################################################
# Install 'OS' software.
##############################################################################################
RUN yum -y install epel-release  && \
    yum -y update && yum -y install \

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
    fftw-devel \

    # VERSION: 5.2.2
    # LINK: https://centos.pkgs.org/7/rpmfusion-nonfree-updates-x86_64/pgplot-5.2.2-35.el7.x86_64.rpm.html
    #
    # DESCRIPTION:
    # The PGPLOT Graphics Subroutine Library is a Fortran- or C-callable,
    # device-independent graphics package for making simple scientific graphs.
    pgplot \

    git

##############################################################################################
# Setup python environment
##############################################################################################

RUN yum -y install \
    python-pip \
    python-devel  && \

    # Install python modules
    pip install --no-cache-dir --upgrade pip  && \
    pip install --no-cache-dir pip -U  && \
    pip install --no-cache-dir setuptools -U  && \
    pip install --no-cache-dir numpy -U && \
    pip install --no-cache-dir scipy -U  && \
    pip install --no-cache-dir matplotlib -U && \
    pip install --no-cache-dir pyephem -U

#RUN yum -y install tkinter

##############################################################################################
# Setup environment variables
##############################################################################################

# Make the directory where software will be installed. Note the -p flag tells mkdir to
# also create parent directories as required.
RUN mkdir -p /home/psr/soft

# Define home, psrhome, OSTYPE
ENV HOME=/home
ENV PSRHOME=/home/psr/soft
ENV TEST_VECTOR_PIPELINE=$PSRHOME/tvp
ENV PIPELINE_V1=$TEST_VECTOR_PIPELINE/v1.0
ENV PIPELINE_BETA=$TEST_VECTOR_PIPELINE/beta
ENV OSTYPE=linux

# Python packages
ENV PYTHONPATH=$HOME/ve/lib/python3.6/site-packages

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
# them out, Sigproc will not build correctly.
ENV SIGPROC=$PSRHOME/sigproc
ENV PATH=$PATH:$SIGPROC/install/bin
ENV FC=gfortran
ENV F77=gfortran
ENV CC=gcc
ENV CXX=g++

# Commented out until PSRCHIVE build error can be fixed.
# EPSIC (required for PSRCHIVE)
#ENV EPSIC=$PSRCHIVE/packages/epsic
#ENV PATH=$PATH:$EPSIC/src
#ENV C_INCLUDE_PATH=$C_INCLUDE_PATH:$EPSIC/src

# Commented out until PSRCHIVE build error can be fixed.
# PSRCHIVE
#ENV PSRCHIVE=$PSRHOME/psrchive
#ENV PATH=$PATH:$PSRCHIVE/install/bin
#ENV C_INCLUDE_PATH=$C_INCLUDE_PATH:$PSRCHIVE/install/include
#ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PSRCHIVE/install/lib
#ENV PYTHONPATH=$PSRCHIVE/install/lib/python2.7/site-packages

# Commented out until PSRCHIVE build error can be fixed.
# DSPSR
#ENV DSPSR=$PSRHOME/dspsr
#ENV PATH=$PATH:$DSPSR/install/bin
#ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DSPSR/install/lib
#ENV C_INCLUDE_PATH=$C_INCLUDE_PATH:$DSPSR/install/include

# PGPLOT
ENV PGPLOT_DIR /usr/lib/pgplot5
ENV PGPLOT_FONT /usr/lib/pgplot5/grfont.dat
ENV PGPLOT_INCLUDES /usr/include

# Commented out until we integrate PRESTO.
# PRESTO
#ENV PRESTO=$PSRHOME/presto
#ENV PATH=$PATH:$PRESTO/bin
#ENV LD_LIBRARY_PATH=$PRESTO/lib
#ENV PYTHONPATH=$PYTHONPATH:$PRESTO/lib/python

##############################################################################################
# TEST VECTOR PIPELINE v1.0 + README Setup
##############################################################################################
# Download test vector files
RUN mkdir $TEST_VECTOR_PIPELINE
RUN mkdir $PIPELINE_V1
WORKDIR $PIPELINE_V1

RUN wget https://raw.githubusercontent.com/scienceguyrob/SKA-TestVectorGenerationPipeline/v2.0/code/pulsar_injection_pipeline/v1.0/inject_pulsar_pipeline_readme.txt
RUN wget https://raw.githubusercontent.com/scienceguyrob/SKA-TestVectorGenerationPipeline/v2.0/docker/v1.0/CentOS/DockerImageReadme.txt && \
    wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v2.0/lib/30_04_2019/pulsar_injection_pipeline_v1.0.zip && \
    unzip pulsar_injection_pipeline_v1.0.zip -d $PIPELINE_V1 && \
    rm __MACOSX -R && \
    rm pulsar_injection_pipeline_v1.0.zip

##############################################################################################
# Beta TEST VECTOR PIPELINE v2.0 + README Setup
##############################################################################################
# Download test vector files
RUN mkdir $PIPELINE_BETA
WORKDIR $PIPELINE_BETA

RUN wget https://raw.githubusercontent.com/scienceguyrob/SKA-TestVectorGenerationPipeline/v2.0/code/pulsar_injection_pipeline/beta/TestVectorPipelineReadme_v2.0.md
RUN wget https://raw.githubusercontent.com/scienceguyrob/SKA-TestVectorGenerationPipeline/v2.0/docker/v2.0/CentOS/DockerImageReadme.md && \
    wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v2.0/lib/30_04_2019/beta_pipeline_v2.0.zip && \
    unzip beta_pipeline_v2.0.zip -d beta_pipeline_v2.0 && \
    rm beta_pipeline_v2.0/__MACOSX -R && \
    rm beta_pipeline_v2.0.zip

RUN mv /home/psr/soft/tvp/beta/beta_pipeline_v2.0/beta/Filename_Standards.md /home/psr/soft/tvp/beta/Filename_Standards.md && \
    cp /home/psr/soft/tvp/beta/beta_pipeline_v2.0/beta/main/src /home/psr/soft/tvp/beta/src -R

##############################################################################################
# Elmarie van Heerden's Code
##############################################################################################

WORKDIR $PSRHOME

RUN mkdir /home/psr/soft/evh && \
    cd $PSRHOME/evh && \
    wget https://raw.githubusercontent.com/EllieVanH/PulsarDetectionLibrary/master/Readme_For_Ersartz.txt && \
    wget https://raw.githubusercontent.com/EllieVanH/PulsarDetectionLibrary/master/ersatz.py

##############################################################################################
# PULSAR SOFTWARE
##############################################################################################
WORKDIR /home

# Downloading pulsar software source codes. Here I've tried to version the software
# used, so we know all about our container environment. However some of the pulsar tools
# are not versioned explcitly. So to make sure we always have the same version of the
# pulsar tools in each image, versions of the software have been packaged and stored,
# in my github repository. It is these versions of the software that will be installed
# each time.

# Download the software

RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v2.0/lib/30_04_2019/Sigproc_MJK_SNAPSHOT_30_04_2019.zip
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v2.0/lib/08_12_2016/Tempo_SNAPSHOT_08_12_2016.zip
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v2.0/lib/08_12_2016/Tempo2_2016.11.3_SNAPSHOT_08_12_2016.zip
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v2.0/lib/30_04_2019/psrchive_SNAPSHOT_30_04_2019.zip
RUN wget https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline/raw/v2.0/lib/30_04_2019/dspsr_SNAPSHOT_30_04_2019.zip

# Unzip software
RUN unzip Tempo_SNAPSHOT_08_12_2016.zip -d /home/Tempo_SNAPSHOT_08_12_2016 && \
    unzip Tempo2_2016.11.3_SNAPSHOT_08_12_2016.zip -d /home/Tempo2_2016.11.3_SNAPSHOT_08_12_2016 && \
    unzip Sigproc_MJK_SNAPSHOT_30_04_2019.zip -d /home/Sigproc_MJK_SNAPSHOT_30_04_2019 && \
    unzip psrchive_SNAPSHOT_30_04_2019.zip -d /home/psrchive_SNAPSHOT_30_04_2019 && \
    unzip dspsr_SNAPSHOT_30_04_2019.zip -d /home/dspsr_SNAPSHOT_30_04_2019

# Move the software to the correct folder location
RUN mv /home/Tempo_SNAPSHOT_08_12_2016 /home/psr/soft/tempo && \
    mv /home/Tempo2_2016.11.3_SNAPSHOT_08_12_2016 /home/psr/soft/tempo2 && \
    mv /home/Sigproc_MJK_SNAPSHOT_30_04_2019/Sigproc_MJK_SNAPSHOT_30_04_2019 /home/psr/soft/sigproc && \
    mv /home/psrchive_SNAPSHOT_30_04_2019/psrchive_SNAPSHOT_30_04_2019 /home/psr/soft/psrchive && \
    mv /home/dspsr_SNAPSHOT_30_04_2019/dspsr_SNAPSHOT_30_04_2019 /home/psr/soft/dspsr

# Remove zip files / unecessary files and folders.
RUN rm Sigproc_MJK_SNAPSHOT_30_04_2019.zip && \
    rm Tempo_SNAPSHOT_08_12_2016.zip && \
    rm Tempo2_2016.11.3_SNAPSHOT_08_12_2016.zip && \
    rm psrchive_SNAPSHOT_30_04_2019.zip && \
    rm dspsr_SNAPSHOT_30_04_2019.zip && \
    rm /home/Sigproc_MJK_SNAPSHOT_30_04_2019 -R && \
    rm /home/psrchive_SNAPSHOT_30_04_2019 -R && \
    rm /home/dspsr_SNAPSHOT_30_04_2019 -R && \
    rm /home/psr/soft/tempo/__MACOSX -R && \
    rm /home/psr/soft/tempo2/__MACOSX -R

##############################################################################################
# TEMPO Installation
##############################################################################################
WORKDIR $PSRHOME/tempo
RUN ./prepare && \
    ./configure --prefix=$PSRHOME/tempo && \
    make && \
    make install &&\
    mv obsys.dat obsys.dat_ORIGINAL && \
    wget https://raw.githubusercontent.com/scienceguyrob/SKA-TestVectorGenerationPipeline/v2.0/lib/30_04_2019/obsys.dat

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

WORKDIR $PSRHOME/tempo2/T2runtime/observatory
RUN mv observatories.dat observatories.dat_ORIGINAL && \
    mv oldcodes.dat oldcodes.dat_ORIGINAL && \
    mv aliases aliases_ORIGINAL && \
    wget https://raw.githubusercontent.com/scienceguyrob/SKA-TestVectorGenerationPipeline/v2.0/lib/30_04_2019/observatories.dat && \
    wget https://raw.githubusercontent.com/scienceguyrob/SKA-TestVectorGenerationPipeline/v2.0/lib/30_04_2019/aliases

##############################################################################################
# Sigproc Installation
##############################################################################################
# Ok here we install sigproc - This is Mike Keith's version of Sigproc, which comes with the
# fast_fake utility. First we set the environment variables for the install, then execute the
# building steps.
WORKDIR $SIGPROC
RUN ./bootstrap && \
    ./configure

# Original configure command used - for some reason, this started to break. But repeating it helped.
RUN ./configure --prefix=$SIGPROC/install LDFLAGS="-L/home/psr/soft/tempo2/T2runtime/lib" LIBS="-ltempo2"

RUN make
RUN make install

##############################################################################################
# Psrchive Installation
#
# The latest version of PSRCHIVE will not compile.
#
# First we have to setup the EPSIC package: http://psrchive.sourceforge.net/third/epsic/
# PSRCHIVE will no longer build without it. There is a script provided in the PSRCHIVE
# distribution that allows you to build EPSIC, but this is broken... so we have to fix
# this script, and install EPSIC if we want PSRCHIVE at all....
##############################################################################################

#WORKDIR $PSRCHIVE/packages


# Now we can build...
#WORKDIR $PSRCHIVE
#RUN ./bootstrap

# We expect this next command to fail, so we continue when it does.
#RUN ./configure --prefix=$PSRCHIVE/install; exit 0
#WORKDIR $PSRCHIVE/packages

#RUN ./epsic.csh
#WORKDIR $PSRCHIVE
#RUN ./configure --prefix=$PSRCHIVE/install
#RUN make
#RUN make install

##############################################################################################
# DSPSR Installation
#
# The DSPSR installation cannot be completed as I can not build PSRCHIVE due to an error.
##############################################################################################
#WORKDIR $DSPSR
#RUN ./bootstrap && \
#    echo "bpsr dummy fits puma2 sigproc ska1" > backends.list
#RUN ./configure --prefix=$DSPSR/install
#RUN make
#RUN make install


##############################################################################################
# PRESETO INSTALL
#
# Note I have not built PRESTO due to this issue:
# https://github.com/scottransom/presto/issues/68
# I can workaround the issue by removing references to the code causing the problem, but I don't
# believe that to be a sensible solution. Especially as I'm unsure what consequence that would
# have. You can build this software from inside the docker container if absolutely necessary.
# However I have removed the PRESTO pre-requisites to make the pipeline image smaller.
#
# Presto will only be added at a later date, when I have time to correct these issues.
##############################################################################################
#RUN git clone https://github.com/scottransom/presto.git

##############################################################################################
# Finally...
##############################################################################################
# Define the command that will be exectuted when docker runs the container.
WORKDIR /home
ENTRYPOINT /bin/bash
