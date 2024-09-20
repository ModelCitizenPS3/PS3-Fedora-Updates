%define platform .PS3

ExclusiveArch:  ppc ppc64
Name:           lzma
Version:        4.32.7
Release:        4%{?dist}%{platform}
Summary:        LZMA utils
Group:          Applications/File
License:        GPLv2,GPLv3,LGPLv2.1
URL:            https://tukaani.org/%{name}/
Source0:        https://tukaani.org/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  compat-gcc-34-g77
Requires:       %{name}-libs = %{version}-%{release}

%description
LZMA provides very high compression ratio and fast decompression. The core of
the LZMA utils is Igor Pavlov's LZMA SDK containing the actual LZMA
encoder/decoder. LZMA utils add a few scripts which provide gzip-like command
line interface and a couple of other LZMA related tools.

%package libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+

%description libs
Libraries for decoding LZMA compression.

%package devel
Summary:	Development libraries & headers for liblzmadec
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Devel libraries & headers for liblzmadec.


%prep
%setup -q


%build
%ifarch ppc
CC="gcc -m32"
CXX="g++ -m32"
F77="f77 -m32"
%else
CC="gcc -m64"
CXX="g++ -m64"
F77="f77 -m64"
%endif
export CC CXX F77
%configure --enable-static=no
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/liblzmadec.la
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-libs-%{version}
cp -f COPYING.GPLv2 $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-libs-%{version}/COPYING.GPLv2
cp -f COPYING.GPLv3 $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-libs-%{version}/COPYING.GPLv3
cp -f COPYING.LGPLv2.1 $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-libs-%{version}/COPYING.LGPLv2.1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp -f README $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/README
cp -f THANKS $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/THANKS
cp -f COPYING.GPLv2 $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/COPYING.GPLv2
cp -f COPYING.GPLv3 $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/COPYING.GPLv3
cp -f COPYING.LGPLv2.1 $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/COPYING.LGPLv2.1
cp -f ChangeLog $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/ChangeLog
cp -f AUTHORS $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/AUTHORS


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/*lz*
%{_mandir}/man1/*lz*.1*
%dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/README
%doc %{_datadir}/doc/%{name}-%{version}/THANKS
%doc %{_datadir}/doc/%{name}-%{version}/COPYING.*
%doc %{_datadir}/doc/%{name}-%{version}/ChangeLog
%doc %{_datadir}/doc/%{name}-%{version}/AUTHORS
#%doc README THANKS COPYING.* ChangeLog AUTHORS

%files libs
%defattr(-,root,root,-)
%{_libdir}/liblzmadec.so.0
%{_libdir}/liblzmadec.so.0.0.0
%dir %{_datadir}/doc/%{name}-libs-%{version}
%doc %{_datadir}/doc/%{name}-libs-%{version}/COPYING.GPLv2
%doc %{_datadir}/doc/%{name}-libs-%{version}/COPYING.GPLv3
%doc %{_datadir}/doc/%{name}-libs-%{version}/COPYING.LGPLv2.1

%files devel
%defattr(-,root,root,-)
%{_includedir}/lzmadec.h
%{_libdir}/liblzmadec.so


%changelog
* Wed Jul 31 2024 The Model Citizen <model.citizen@ps3linux.net> - 4.32.7-4
- Initial build for Playstation 3 Fedora (Sackboy) on Cell/B.E.

