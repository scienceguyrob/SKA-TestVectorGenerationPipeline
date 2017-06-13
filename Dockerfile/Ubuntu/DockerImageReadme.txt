**************************************************************************
|                                                                        |
|  Test vector machine Docker Image (version 1.0)                        |
|                                                                        |
**************************************************************************
| Author: Rob Lyon                                                       |
| Email : robert.lyon@manchester.ac.uk                                   |
| web   : www.scienceguyrob.com                                          |
**************************************************************************

Based upon original script written by Casey Law (caseyjlaw@gmail.com) and
Maciej Serylak (mserylak@ska.ac.za).

This image sets up an environment with only a basic pulsar stack. This
is because the image is to be used for test vector generation, for tests
of SKA SDP and CSP software. For a more complete pulsar image, look at the
Dockerfile's written by Casey Law, or Maciej Serylak. 

Please note that it takes around 1 hour to build the entire image on the
dockerhub. Also note that the image size is approximately 1.5 GB on disk.

**************************************************************************

OS: Ubuntu 14.04.4

OS PACKAGES INSTALLED:

1. autoconf 
2. automake
3. autotools-dev
4. bison
5. build-essential
6. cmake
7. cmake-data
8. cmake-curses-gui
9. cpp
10. csh
11. cvs
12. cython
13. dkms
14. f2c
15. fftw2
16. fftw-dev
17. flex
18. fort77
19. gcc
20. g++
21. gfortran
22. ghostscript
23. ghostscript-x
24. git
25. git-core
26. gnuplot
27. gnuplot-x11
28. gsl-bin
29. gv
30. h5utils
31. hdf5-tools
32. htop
33. hdfview
34. hwloc
35. ipython
36. ipython-notebook
37. libbison-dev
38. libboost1.55-all-dev
39. libboost1.55-dev
40. libboost1.55-tools-dev
41. libc6-dev
42. libc-dev-bin
43. libcfitsio3
44. libcfitsio3-dev
45. libcloog-isl4
46. libcppunit-dev
47. libcppunit-subunit0
48. libcppunit-subunit-dev
49. libfftw3-bin
50. libfftw3-dbg
51. libfftw3-dev
52. libfftw3-double3
53. libfftw3-long3
54. libfftw3-quad3
55. libfftw3-single3
56. libgd2-xpm-dev
57. libgd3
58. libglib2.0-dev
59. libgmp3-dev
60. libgsl0-dev
61. libgsl0ldbl
62. libhdf5-7
63. libhdf5-dev
64. libhdf5-serial-dev
65. libhwloc-dev
66. liblapack3
67. liblapack3gf
68. liblapack-dev
69. liblapacke
70. liblapacke-dev
71. liblapack-pic
72. liblapack-test
73. libblas3
74. libblas3gf
75. libblas-dev
76. liblua5.1-0
77. liblua5.2-0
78. libltdl7
79. libltdl-dev
80. libncurses5-dev
81. libpng12-dev
82. libpng3
83. libpng++-dev
84. libpth-dev
85. libreadline6
86. libreadline6-dev
87. libsocket++1
88. libsocket++-dev
89. libtool
90. libx11-dev
91. locate
92. lsof
93. m4
94. make
95. man
96. mc
97. nano
98. nfs-common
99. numactl
100. openssh-server
101. pbzip2
102. pgplot5
103. pkgconf
104. pkg-config
105. python-qt4-dev
106. pyqt4-dev-tools
107. vim
108. wget
109. screen
110. subversion
111. swig
112. swig2.0
113. tcsh
114. tk
115. tk-dev
116. tmux
117. python-pip
118. bc
119. ca-certificates
120. curl

PYTHON MODULES:

1. numpy
2. scipy
3. fitsio
4. astropy
5. astroplan
6. pyfits
7. matplotlib
8. pyephem

PULSAR SOFTWARE:

The software can be found in: /home/psr/soft


1. Tempo2
2. Sigproc (Mike Keith's build)
3. Test vector generation scripts.
4. Elmarie van Heerden's code that inserts non-stationary noise and RFI into filterbank files.
5. PRESTO
6. Tempo

OTHER SOFTWARE:

1. CUDA version 8.0
