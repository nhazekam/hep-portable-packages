#!/usr/bin/make -f

CVMFS=$(pwd)
STORAGE=/storage
THREADS=16
DIR=$(shell pwd)
KEYS=$(DIR)/keys

all : sft.cern.ch.config

cvmfs/cvmfs.git :
	if [ ! -d cvmfs ] ; then git clone https://github.com/cvmfs/cvmfs.git; fi

build/cvmfs/cvmfs_shrinkwrap  : cvmfs/cvmfs.git
	mkdir -p build; \
	cd build; \
	cmake -DBUILD_SHRINKWRAP=on ../cvmfs; \
	make

trace/% spec/% : build/cvmfs/cvmfs_shrinkwrap cvmfs/cvmfs/shrinkwrap/scripts/trace.sh run_benchmark
	bash cvmfs/cvmfs/shrinkwrap/scripts/trace.sh --trace_dir=$1 --spec_dir=$2 run_benchmark

${STORAGE}/cvmfs/% : %.config %.spec uid.map gid.map
	build/cvmfs/cvmfs_shrinkwrap -r $* -f $*.config -t $*.spec --dest-base ${STORAGE}/cvmfs -j ${THREADS}

${STORAGE}/%.sqfs : ${STORAGE}/%/atlas.cern.ch ${STORAGE}/%/sft.cern.ch ${STORAGE}/%/cvmfs-config.cern.ch
	mksquashfs $* $@

uid.map :
	echo "* $(shell id -u)" > $@

gid.map :
	echo "* $(shell id -g)" > $@

%.config : uid.map gid.map
	echo "CVMFS_REPOSITORIES=$*" > $@
	echo "CVMFS_REPOSITORY_NAME=$*" >> $@
	echo "CVMFS_CONFIG_REPOSITORY=cvmfs-config.cern.ch" >> $@
	echo "CVMFS_DEFAULT_DOMAIN=cern.ch" >> $@
	echo "CVMFS_SERVER_URL='http://cvmfs-stratum-zero-hpc.cern.ch/cvmfs/$*;http://cvmfs-stratum-one.cern.ch/cvmfs/$*'" >> $@
	echo "CVMFS_HTTP_PROXY=DIRECT" >> $@
	echo "CVMFS_MOUNT_DIR=/cvmfs" >> $@
	echo "CVMFS_CACHE_BASE=$(STORAGE)/cache/cvmfs/shrinkwrap" >> $@
	echo "CVMFS_SHARED_CACHE=no" >> $@
	echo "CVMFS_USER=$(USER)" >> $@
	echo "CVMFS_DEBUGLOG=$(DIR)/cvmfs.log" >> $@
	echo "CVMFS_SYSLOG_LEVEL=LOG_DEBUG" >> $@
	echo "CVMFS_KEYS_DIR=$(KEYS)" >> $@
	echo "CVMFS_UID_MAP=$(DIR)/uid.map" >> $@
	echo "CVMFS_GID_MAP=$(DIR)/gid.map" >> $@

run_docker_benchmark : setup_benchmark
	echo "yum install -y http://linuxsoft.cern.ch/wlcg/centos7/x86_64/wlcg-repo-1.0.0-1.el7.noarch.rpm \\" > $@
	echo "HEP_OSlibs \\" >> $@
	echo "git cmake gcc-c++ gcc binutils \\" >> $@
	echo "libX11-devel libXpm-devel libXft-devel libXext-devel which \\" >> $@
	echo "gcc-gfortran openssl-devel pcre-devel \\" >> $@
	echo "mesa-libGL-devel mesa-libGLU-devel glew-devel ftgl-devel mysql-devel \\" >> $@
	echo "fftw-devel cfitsio-devel graphviz-devel \\" >> $@
	echo "avahi-compat-libdns_sd-devel libldap-dev python-devel \\" >> $@
	echo "libxml2-devel gsl-static make" >> $@
	echo >> $@
	cat $< >> $@

setup_benchmark : run_benchmark
	echo "git clone https://gitlab.cern.ch/cloud-infrastructure/cloud-benchmark-suite.git" > $@
	echo "cd cloud-benchmark-suite" >> $@
	echo "make all" >> $@
	echo >> $@
	cat $< >> $@

run_benchmark :
	echo "time cern-benchmark --benchmarks=\"kv;DB12;whetstone\" -o;" >> $@
	echo "time cern-benchmark --benchmarks=\"kv;DB12;whetstone\" -o --mp_num=1;" >> $@


run_root :
	echo ". /cvmfs/sft.cern.ch/lcg/views/LCG_94a/x86_64-centos7-gcc7-opt/setup.sh" > $@
	echo "root -q -b TMVA_Higgs_Classification.C" >> $@


#native_cvmfs

native_shrinkwrap_bind : run_benchmark ${STORAGE}/cvmfs
	mount --bind ${STORAGE}/cvmfs /cvmfs ; \
	{ time sh run_benchmark ; } |& tee $@ ; \
	umount /cvmfs

native_shrinkwrap_sqfs : run_benchmark ${STORAGE}/cvmfs.sqfs
	mount -t squashfs ${STORAGE}/cvmfs.sqfs /cvmfs ; \
	{ time sh run_benchmark ; } |& tee $@ ; \
	umount /cvmfs

#docker_native_cvmfs

docker_shrinkwrap_bind :  run_docker_benchmark ${STORAGE}/cvmfs
	mount --bind ${STORAGE}/cvmfs /cvmfs
	{ time docker run --name centest -v ${STORAGE}/cvmfs:/cvmfs --rm -t centos run_docker_benchmark  ; } &> $@
	umount /cvmfs

#docker_shrinkwrap_mnt

#docker_shrinkwrap_sqfs

#parrot_cvmfs?

clean :
	rm *.map *.config

