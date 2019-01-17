#!/bin/bash

CVMFS=pwd

build_cvmfs () {
  if [ $# -eq 1" ]
    CVMFS=$1
  fi
  cd $CVMFS
  git clone https://github.com/cvmfs/cvmfs.git
  cd cvmfs
  mkdir build
  cd build
  cmake -DBUILD_SHRINKWRAP=on ../cvmfs
  make
}

create_trace () {
  bash $CVMFS/cvmfs/cvmfs/shrinkwrap/scripts/trace.sh --trace_dir=$1 --spec_dir=$2 run_benchmark
}

create_image () {
  local REPO=$1
  cvmfs_shrinkwrap -r $REPO.cern.ch -f $REPO.cern.ch.config -t $REPO.cern.ch.spec --dest-base $2 -j $3
}

create_sqfs () {
  mksquashfs $1 $2
}

#native_cvmfs

#shrinkwrap_tmp

#shrinkwrap_sqfs

#docker_native_cvmfs

#docker_shrinkwrap_tmp

#docker_shrinkwrap_mnt

#docker_shrinkwrap_sqfs

#parrot_cvmfs?

create_id_map () {
  echo "* $2" > $1\.map
}

create_config () {
    local REPO=$1
    local CONFIG=$REPO\.cern.ch.config
    local DIR=$2
    local KEYS=$3
    echo "CVMFS_REPOSITORIES=$REPO.cern.ch" > $CONFIG
    echo "CVMFS_REPOSITORY_NAME=$REPO.cern.ch" >> $CONFIG
    echo "CVMFS_CONFIG_REPOSITORY=cvmfs-config.cern.ch" >> $CONFIG
    echo "CVMFS_DEFAULT_DOMAIN=cern.ch" >> $CONFIG
    echo "CVMFS_SERVER_URL='http://cvmfs-stratum-zero-hpc.cern.ch/cvmfs/$REPO.cern.ch;http://cvmfs-stratum-one.cern.ch/cvmfs/$REPO.cern.ch'" >> $CONFIG
    echo "CVMFS_HTTP_PROXY=DIRECT" >> $CONFIG
    echo "CVMFS_MOUNT_DIR=/cvmfs" >> $CONFIG
    echo "CVMFS_CACHE_BASE=$DIR/cache/cvmfs/shrinkwrap" >> $CONFIG
    echo "CVMFS_SHARED_CACHE=no # Important as libcvmfs does not support shared caches" >> $CONFIG
    echo "CVMFS_USER=$USER" >> $CONFIG
    echo "CVMFS_DEBUGLOG=$DIR/cvmfs.log" >> $CONFIG
    echo "CVMFS_SYSLOG_LEVEL=LOG_DEBUG" >> $CONFIG
    echo "CVMFS_KEYS_DIR=$KEYS" >> $CONFIG
    echo "CVMFS_UID_MAP=$DIR/uid.map" >> $CONFIG
    echo "CVMFS_GID_MAP=$DIR/gid.map" >> $CONFIG

    create_id_map uid $(id -u)
    create_id_map gid $(id -g)
}

configure_environment () {
    yum install -y http://linuxsoft.cern.ch/wlcg/centos7/x86_64/wlcg-repo-1.0.0-1.el7.noarch.rpm \
      HEP_OSlibs \
      git cmake gcc-c++ gcc binutils \
      libX11-devel libXpm-devel libXft-devel libXext-devel which \
      gcc-gfortran openssl-devel pcre-devel \
      mesa-libGL-devel mesa-libGLU-devel glew-devel ftgl-devel mysql-devel \
      fftw-devel cfitsio-devel graphviz-devel \
      avahi-compat-libdns_sd-devel libldap-dev python-devel \
      libxml2-devel gsl-static make
}

build_benchmark () {
    git clone https://gitlab.cern.ch/cloud-infrastructure/cloud-benchmark-suite.git
    cd cloud-benchmark-suite
    make all
}

run_benchmark () {
    time cern-benchmark --benchmarks="kv;DB12;whetstone" -o
    time cern-benchmark --benchmarks="kv;DB12;whetstone" -o --mp_num=1
}

configure_root () {
    . /cvmfs/sft.cern.ch/lcg/views/LCG_94a/x86_64-centos7-gcc7-opt/setup.sh
}

run_root () {
    root -q -b TMVA_Higgs_Classification.C
}

create_config sft $(pwd) $(pwd)/keys
