%define platform .PS3

ExclusiveArch:  ppc ppc64
Name:           lzma
Version:        4.32.7
Release:        4%{?dist}%{platform}
Summary:        LZMA utils
Group:          Applications/File
License:        GPLv2+
URL:            https://tukaani.org/%{name}/
Source0:        https://tukaani.org/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README THANKS COPYING.* ChangeLog AUTHORS
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%doc COPYING.*
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so


%changelog
* Wed Jul 3 2024 The Model Citizen <model.citizen@ps3linux.net> - 4.32.7-4
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

