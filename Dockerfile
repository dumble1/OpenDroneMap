FROM phusion/baseimage

# Env variables
ENV DEBIAN_FRONTEND noninteractive

#Install dependencies
RUN apt-get update -y
RUN apt-get install software-properties-common -y
#Required Requisites
RUN add-apt-repository -y ppa:ubuntugis/ppa
RUN add-apt-repository -y ppa:george-edison55/cmake-3.x
RUN apt-get update -y


###openMVS
RUN apt-get update -y
RUN apt-get install --fix-missing -y \
mercurial libglu1-mesa-dev \
libboost-program-options-dev libboost-system-dev libboost-serialization-dev \
libcgal-dev libcgal-qt5-dev \
freeglut3-dev libglew-dev libglfw3-dev 
#libopencv-dev


# All packages (Will install much faster)
RUN apt-get install --no-install-recommends -y  git cmake python-pip build-essential software-properties-common python-software-properties libgdal-dev gdal-bin libgeotiff-dev \
libgtk2.0-dev libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libflann-dev \
libproj-dev libxext-dev liblapack-dev libeigen3-dev libvtk6-dev python-networkx libgoogle-glog-dev libsuitesparse-dev libboost-filesystem-dev libboost-iostreams-dev \
libboost-regex-dev libboost-python-dev libboost-date-time-dev libboost-thread-dev python-pyproj python-empy python-nose python-pyside python-pyexiv2 python-scipy \
libexiv2-dev liblas-bin python-matplotlib libatlas-base-dev swig2.0 python-wheel libboost-log-dev libjsoncpp-dev python-gdal

RUN apt-get remove libdc1394-22-dev
RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install -U --ignore-installed PyYAML exifread gpxpy xmltodict catkin-pkg appsettings https://github.com/OpenDroneMap/gippy/archive/v0.3.9.tar.gz loky scipy shapely numpy pyproj psutil


#RUN pip install pillow


ENV PYTHONPATH="$PYTHONPATH:/code/SuperBuild/install/lib/python2.7/dist-packages"
ENV PYTHONPATH="$PYTHONPATH:/code/SuperBuild/src/opensfm"
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/code/SuperBuild/install/lib"

# Prepare directories

RUN mkdir /code
WORKDIR /code

##VCG for openMVS
RUN git clone https://github.com/cdcseacave/VCG.git /code/vcglib
##openMVS
RUN apt-get install -y cmake libopencv-dev  \
libatlas-base-dev libsuitesparse-dev
RUN apt-get install -y qt-sdk libxmu-dev libxi-dev
RUN  hg clone https://bitbucket.org/eigen/eigen/Source#3.2.9 Source && mkdir eigen_build && cd eigen_build && cmake . ../Source && make && make install
RUN git clone https://ceres-solver.googlesource.com/ceres-solver ceres-solver && mkdir ceres_build && cd ceres_build \
&& cmake . ../ceres-solver/ -DMINIGLOG=ON -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF \
&& make -j$(nproc) && make install 

#RUN mkdir /code/test

# Copy repository files
COPY ccd_defs_check.py /code/ccd_defs_check.py
COPY CMakeLists.txt /code/CMakeLists.txt
COPY configure.sh /code/configure.sh
COPY /modules/ /code/modules/
COPY /opendm/ /code/opendm/
COPY /patched_files/ /code/patched_files/
COPY run.py /code/run.py
COPY run.sh /code/run.sh
COPY /scripts/ /code/scripts/
COPY /SuperBuild/cmake/ /code/SuperBuild/cmake/
COPY /SuperBuild/CMakeLists.txt /code/SuperBuild/CMakeLists.txt
COPY docker.settings.yaml /code/settings.yaml
COPY VERSION /code/VERSION

###my code
#COPY /my_code/ /code/my_code/

#Compile code in SuperBuild and root directories

RUN cd /code/SuperBuild && mkdir build && cd build && cmake .. && make -j$(nproc) && cd ../.. && mkdir build && cd build && cmake .. && make -j$(nproc)
RUN git clone https://github.com/cdcseacave/openMVS.git /code/openMVS \
    && mkdir openMVS_build && cd openMVS_build && cmake . ../openMVS -DCMAKE_BUILD_TYPE=Release -DOpenMVS_USE_CUDA=OFF  -DVCG_DIR="/code/vcglib" \
    && make  && make install


RUN apt-get -y remove libgl1-mesa-dri git cmake python-pip build-essential
RUN apt-get install -y libvtk6-dev
######my code
#RUN cd my_code && make all && ls
# Cleanup APT
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

# Clean Superbuild

RUN rm -rf /code/SuperBuild/download /code/SuperBuild/src/vtk7 /code/SuperBuild/src/opencv /code/SuperBuild/src/pcl /code/SuperBuild/src/pdal /code/SuperBuild/src/opengv /code/SuperBuild/src/mvstexturing /code/SuperBuild/src/ceres /code/SuperBuild/build/vtk7 /code/SuperBuild/build/opencv

#????
#RUN ls my_code


# Entry point

ENTRYPOINT ["python", "/code/run.py", "code"]
#ENTRYPOINT ["/code/scripts/metadataset/run_all.sh", "/code/test"]
