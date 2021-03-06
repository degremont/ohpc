#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%include %{_sourcedir}/OHPC_macros
%{!?PROJ_DELIM: %define PROJ_DELIM -ohpc}

%define pname advisor

Summary:   Intel(R) Advisor XE
Name:      intel-%{pname}%{PROJ_DELIM}
Version:   16.1.0.423501
Source0:   intel-%{pname}%{PROJ_DELIM}-%{version}.tar.gz
Source1:   OHPC_macros
Source2:   modfile-ohpc.input
Release:   1
License:   Copyright (C) 2015 Intel Corporation. All rights reserved.
Vendor:    Intel Corporation
URL:       https://software.intel.com/en-us/intel-parallel-studio-xe
Group:     ohpc/perf-tools
BuildArch: x86_64
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
AutoReq:   no

%define __spec_install_post /usr/lib/rpm/brp-strip-comment-note /bin/true
%define __spec_install_post /usr/lib/rpm/brp-compress /bin/true
%define __spec_install_post /usr/lib/rpm/brp-strip /bin/true

#!BuildIgnore: post-build-checks rpmlint-Factory
%define debug_package %{nil}

%define package_target %{OHPC_PUB}/%{pname}/%{version}

%description

OpenHPC collection of the Intel(R) Adviser XE toolset for treading design and prototyping.

%prep

%build

%install

%{__mkdir} -p %{buildroot}/
cd %{buildroot}
%{__tar} xfz %{SOURCE0}
cd -

# OpenHPC module file
%{__mkdir} -p %{buildroot}/%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################
proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the Intel(R) Advisor XE:"
puts stderr " "
puts stderr "Version %{version}"
puts stderr " "

}

module-whatis "Name: Intel(R) Advisor XE"
module-whatis "Version: %{version}"
module-whatis "Category: performance tools"
module-whatis "Description: Intel(R) Advisor XE for threading desing and prototyping"
module-whatis "URL: https://software.intel.com/en-us/intel-advisor-xe"

set             version             %{version}
setenv          ADVISOR_DIR         %{package_target}
setenv          ADVISOR_BIN         %{package_target}/bin64
setenv          ADVISOR_LIB         %{package_target}/lib64
prepend-path    MANPATH             %{package_target}/man
EOF

# Append with machine-generated contribution for modulefile settings

%{__cat} %{SOURCE2} >> %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
set     ModulesVersion      "%{version}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{OHPC_HOME}

%changelog

