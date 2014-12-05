#
# spec file for package boost
#
# Library build that is dependent on compiler
# toolchain and MPI

%{!?compiler_family: %define compiler_family gnu}
#%define compiler_family gnu
%define _unpackaged_files_terminate_build 0

%define build_mpi 1

%if %build_mpi
%{!?mpi_family: %define mpi_family openmpi}
#%define mpi_family      openmpi
%define mpi 		1
%endif

#-fsp-header-comp-begin-----------------------------


# Compiler dependencies
BuildRequires: lmod coreutils
%if %{compiler_family} == gnu
BuildRequires: FSP-gnu-compilers
Requires:      FSP-gnu-compilers
## Toolsets supported by boost script are:
##     acc, como, darwin, gcc, intel-darwin, intel-linux, kcc, kylix,
##     mipspro, mingw(msys), pathscale, pgi, qcc, sun, sunpro, tru64cxx, vacpp
%define toolset gcc 
%endif

%if %{compiler_family} == intel
BuildRequires: gcc-c++ FSP-intel-compilers
Requires:      gcc-c++ FSP-intel-compilers
## Toolsets supported by boost script are:
##     acc, como, darwin, gcc, intel-darwin, intel-linux, kcc, kylix,
##     mipspro, mingw(msys), pathscale, pgi, qcc, sun, sunpro, tru64cxx, vacpp
%define toolset intel-linux  
%if 0%{?FSP_BUILD}
BuildRequires: intel_licenses
%endif
%endif

# MPI dependencies
%if %{mpi_family} == impi
BuildRequires: FSP-intel-mpi
Requires:      FSP-intel-mpi
%endif
%if %{mpi_family} == mvapich2
BuildRequires: FSP-mvapich2-%{compiler_family}
Requires:      FSP-mvapich2-%{compiler_family}
%endif
%if %{mpi_family} == openmpi
BuildRequires: FSP-openmpi-%{compiler_family}
Requires:      FSP-openmpi-%{compiler_family}
%endif

#-fsp-header-comp-end-------------------------------


#Added FSP build convention
%define debug_package %{nil}
%define openmp        1

%define ver 1.57.0
%define bversion 1_57_0
%define short_version 1_57


# Base package name
%define pname boost
%define PNAME %(echo %{pname} | tr [a-z] [A-Z])

Summary:	Boost free peer-reviewed portable C++ source libraries
Name:		%{pname}-%{compiler_family}-%{mpi_family}
Version:        1.57.0
Release:        0
License:        BSL-1.0
Group:		System Environment/Libraries
Url:            http://www.boost.org
Source0:	%{pname}_%{bversion}.tar.gz 
Source1:        boost-rpmlintrc
Source100:      baselibs.conf
Source101:	FSP_macros
Source102:	FSP_setup_compiler
Source103:	FSP_setup_mpi

#__BuildRequires:  chrpath
#__BuildRequires:  dos2unix
#__BuildRequires:  fdupes
#BuildRequires:  gcc-c++
BuildRequires:  libbz2-devel
BuildRequires:  libexpat-devel
BuildRequires:  libicu-devel >= 4.4
BuildRequires:  python-devel
BuildRequires:  xorg-x11-devel
#!BuildIgnore:  python
BuildRequires:  zlib-devel
BuildRequires:  openmpi-devel

#!BuildIgnore: post-build-checks rpmlint-Factory

#FSP build root
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include %{_sourcedir}/FSP_macros


# Default library install path
%define install_path %{FSP_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%version


%description
Boost provides free peer-reviewed portable C++ source libraries. The
emphasis is on libraries that work well with the C++ Standard Library.
One goal is to establish "existing practice" and provide reference
implementations so that the Boost libraries are suitable for eventual
standardization. Some of the libraries have already been proposed for
inclusion in the C++ Standards Committee's upcoming C++ Standard
Library Technical Report.

Although Boost was begun by members of the C++ Standards Committee
Library Working Group, membership has expanded to include nearly two
thousand members of the C++ community at large.

This package is mainly needed for updating from a prior version, the
dynamic libraries are found in their respective package. For development
using Boost, you also need the boost-devel package. For documentation,
see the boost-doc package.


%prep
%setup -q -n %{pname}_%{bversion} 

%build
# FSP compiler/mpi designation
export FSP_COMPILER_FAMILY=%{compiler_family}
. %{_sourcedir}/FSP_setup_compiler


%if %build_mpi
export FSP_MPI_FAMILY=%{mpi_family}
. %{_sourcedir}/FSP_setup_mpi
export CC=mpicc
export CXX=mpicxx
export F77=mpif77
export FC=mpif90
export MPICC=mpicc
export MPIFC=mpifc
export MPICXX=mpicxx
%endif
# End FSP #####################


LIBRARIES_FLAGS=--with-libraries=all
./bootstrap.sh $LIBRARIES_FLAGS --prefix=%{install_path} --with-toolset=%{toolset} || cat config.log

%if %build_mpi
cat << EOF >>user-config.jam
using mpi ;
EOF
%endif

# perform the compilation
./b2 --a %{?_smp_mflags} --prefix=%{install_path} --user-config=./user-config.jam --threading=multi || config.log


%install

# FSP compiler/mpi designation
export FSP_COMPILER_FAMILY=%{compiler_family}
. %{_sourcedir}/FSP_setup_compiler


%if %build_mpi
export FSP_MPI_FAMILY=%{mpi_family}
. %{_sourcedir}/FSP_setup_mpi
export CC=mpicc
export CXX=mpicxx
export F77=mpif77
export FC=mpif90
export MPICC=mpicc
export MPIFC=mpifc
export MPICXX=mpicxx
%endif

./b2 %{?_smp_mflags} install --prefix=%{buildroot}/%{install_path} --threading=multi --user-config=./user-config.jam


# FSP module file
%if %build_mpi
%{__mkdir} -p %{buildroot}%{FSP_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
%else
%{__mkdir} -p %{buildroot}%{FSP_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
%endif
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{PNAME} library built with the %{compiler_family} compiler toolchain"
puts stderr "and the %{mpi_family} MPI stack."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{PNAME} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "%{url}"

set             version             %{version}
 
prepend-path    PATH                %{install_path}/bin
prepend-path    MANPATH             %{install_path}/share/man
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_LIB        %{install_path}/lib
setenv          %{PNAME}_INC        %{install_path}/include

family "boost"
EOF

%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{FSP_HOME}


%changelog
