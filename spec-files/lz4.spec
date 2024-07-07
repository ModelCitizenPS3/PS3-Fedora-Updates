%define platform .PS3

ExclusiveArch:  ppc ppc64
Name:           lz4
Version:        1.9.4
Release:        1%{?dist}%{platform}
Summary:        Extremely fast compression algorithm
License:        GPL-2.0-or-later AND BSD-2-Clause
URL:            https://%{name}.org/
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  make gcc

%description
LZ4 is an extremely fast loss-less compression algorithm, providing compression
speed at 400 MB/s per core, scalable with multi-core CPU. It also features an
extremely fast decoder, with speed in multiple GB/s per core, typically reaching
RAM speed limits on multi-core systems.

%package libs
Summary:    Libraries for lz4

%description libs
This package contains the libraries for lz4.

%package devel
Summary:    Development files for lz4
Requires:   %{name}-libs = %{version}-%{release}

%description devel
This package contains the header and library files required to build
applications using liblz4 library.

%package static
Summary:    Static library for lz4

%description static
LZ4 is an extremely fast loss-less compression algorithm. This package contains
static libraries for static linking of applications.


%prep
%setup -q


%build
%ifarch ppc
CC="gcc -m32"
CXX="g++ -m32"
%else
CC="gcc -m64"
CXX="g++ -m64"
%endif
export CC CXX
make %{?_smp_mflags} all


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install PREFIX=%{_usr} DESTDIR=$RPM_BUILD_ROOT
%ifarch ppc64
rm -rf $RPM_BUILD_ROOT/usr/lib/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{_libdir}
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc programs/COPYING NEWS
%{_bindir}/lz4
%{_bindir}/lz4c
%{_bindir}/lz4cat
%{_bindir}/unlz4
%{_mandir}/man1/lz4.1*
%{_mandir}/man1/lz4c.1*
%{_mandir}/man1/lz4cat.1*
%{_mandir}/man1/unlz4.1*

%files libs
%defattr(-,root,root,1)
%doc lib/LICENSE
%{_libdir}/liblz4.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lz4*.h
%{_libdir}/liblz4.so
%ifarch ppc
%{_libdir}/pkgconfig/liblz4.pc
%endif

%files static
%defattr(-,root,root,-)
%doc lib/LICENSE
%{_libdir}/liblz4.a


%changelog
* Thu Jul 4 2024 The Model Citizen <model.citizen@ps3linux.net> - 1.9.4-1
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

