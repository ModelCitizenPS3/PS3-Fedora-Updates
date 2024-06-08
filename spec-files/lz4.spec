Name:           lz4
Version:        1.9.4
Release:        1%{?dist}%{?platform}
Summary:        Extremely fast compression algorithm
License:        BSD
URL:            https://%{name}.org/
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  ppc ppc64

%description
LZ4 is an extremely fast loss-less compression algorithm, providing compression
speed at 400 MB/s per core, scalable with multi-core CPU. It also features an
extremely fast decoder, with speed in multiple GB/s per core, typically
reaching RAM speed limits on multi-core systems.

%package libs
Summary:    Libaries for lz4

%description libs
This package contains the libaries for lz4.

%package devel
Summary:    Development files for lz4
Requires:   %{name}-libs = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains the header(.h) and library(.so) files required to build
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
export BITS=-m32
%else
export BITS=-m64
%endif
make %{?_smp_mflags} all CFLAGS="$BITS %{optflags}" CXXFLAGS="$BITS %{optflags}" V=2


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} LIBDIR=%{_libdir}


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc NEWS LICENSE
%{_bindir}/%{name}
%{_bindir}/lz4c
%{_bindir}/lz4cat
%{_bindir}/unlz4
%{_mandir}/man1/lz4.1*
%{_mandir}/man1/lz4c.1*
%{_mandir}/man1/lz4cat.1*
%{_mandir}/man1/unlz4.1*

%files libs
%defattr(-,root,root,-)
%{_libdir}/liblz4.so.1
%{_libdir}/liblz4.so.1.9.4

%files devel
%defattr(-,root,root,-)
%{_includedir}/lz4.h
%{_includedir}/lz4frame.h
%{_includedir}/lz4frame_static.h
%{_includedir}/lz4hc.h
%{_libdir}/liblz4.so
%{_libdir}/pkgconfig/liblz4.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/liblz4.a


%changelog
* Wed May 29 2024 Model Citizen <model.citizen@ps3linux.net> - 1.9.4-1
- Initial build for Playstation 3 Fedora on Cell/B.E. (sackboy)

