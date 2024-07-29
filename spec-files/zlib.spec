%define  platform .PS3

ExclusiveArch:  ppc ppc64
Summary:        The zlib compression and decompression library
Name:           zlib
Version:        1.2.13
Release:        1%{?dist}%{platform}
Group:          System Environment/Libraries
License:        zlib
URL:            http://www.%{name}.net/
Source0:        http://www.%{name}.net/fossils/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  automake, autoconf, libtool
Provides:       %{name} < %{version}

%description
Zlib is a general-purpose, patent-free, lossless data compression library which
is used by many different programs.

%package devel
Summary:    Header files and libraries for Zlib development
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
The zlib-devel package contains the header files and libraries needed to
develop programs that use the zlib compression and decompression library.

%package static
Summary:    Static libraries for Zlib development
Group:      Development/Libraries
Requires:   %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed to develop programs
that use the zlib compression and decompression library.

%package -n minizip
Summary:    Minizip manipulates files from a .zip archive
Group:      System Environment/Libraries
Requires:   %{name} = %{version}-%{release}

%description -n  minizip
Minizip manipulates files from a .zip archive.

%package -n minizip-devel
Summary:    Development files for the minizip library
Group:      Development/Libraries
Requires:   minizip = %{version}-%{release}
Requires:   %{name}-devel = %{version}-%{release}
Requires:   pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for developing
applications which use minizip.


%prep
%setup -q


%build
%ifarch ppc
CC="gcc -m32" CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple" ./configure --const --prefix=%{_prefix} --libdir=%{_libdir} --sharedlibdir=%{_libdir} --includedir=%{_includedir}
%else
CC="gcc -m64" CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple" ./configure --const --prefix=%{_prefix} --64 --libdir=%{_libdir} --sharedlibdir=%{_libdir} --includedir=%{_includedir}
%endif
make %{?_smp_mflags}
pushd $PWD
cd contrib/minizip
autoreconf --install
%configure
make %{?_smp_mflags}
popd


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
pushd $PWD
cd contrib/minizip
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libminizip.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libminizip.la
mkdir -p $RPM_BUILD_ROOT/%{_lib}
ln -s ..%{_libdir}/libz.so.1.2.13 $RPM_BUILD_ROOT/%{_lib}/libz.so.1
ln -s ..%{_libdir}/libz.so.1.2.13 $RPM_BUILD_ROOT/%{_lib}/libz.so.1.2.3
ln -s ..%{_libdir}/libz.so.1.2.13 $RPM_BUILD_ROOT/%{_lib}/libz.so.1.2.13
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp -f ChangeLog $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/ChangeLog
cp -f FAQ $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/FAQ
cp -f README $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/README
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}
cp -f README $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}/README
cp -f doc/algorithm.txt $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}/algorithm.txt
cp -f test/example.c $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}/example.c
cp -f test/minigzip.c $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}/minigzip.c
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-static-%{version}
cp -f README $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-static-%{version}/README


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
/%{_lib}/libz.so.1
/%{_lib}/libz.so.1.2.3
/%{_lib}/libz.so.1.2.13
%{_libdir}/libz.so.1
%{_libdir}/libz.so.1.2.13
%dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/ChangeLog
%doc %{_datadir}/doc/%{name}-%{version}/FAQ
%doc %{_datadir}/doc/%{name}-%{version}/README

%files devel
%defattr(-,root,root,-)
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/libz.so
%dir %{_datadir}/doc/%{name}-devel-%{version}
%doc %{_datadir}/doc/%{name}-devel-%{version}/README
%doc %{_datadir}/doc/%{name}-devel-%{version}/algorithm.txt
%doc %{_datadir}/doc/%{name}-devel-%{version}/example.c
%doc %{_datadir}/doc/%{name}-devel-%{version}/minigzip.c
%{_mandir}/man3/%{name}.3.gz
%{_libdir}/pkgconfig/%{name}.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/libz.a
%dir %{_datadir}/doc/%{name}-static-%{version}
%doc %{_datadir}/doc/%{name}-static-%{version}/README

%files -n minizip
%defattr(-,root,root,-)
%{_libdir}/libminizip.so.1
%{_libdir}/libminizip.so.1.0.0

%files -n minizip-devel
%defattr(-,root,root,-)
%dir %{_includedir}/minizip
%{_includedir}/minizip/crypt.h
%{_includedir}/minizip/ioapi.h
%{_includedir}/minizip/mztools.h
%{_includedir}/minizip/zip.h
%{_includedir}/minizip/unzip.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc


%changelog
* Tue Jul 23 2024 The Model Citizen <model.citizen@ps3linux.net> - 1.2.13-1
- Initial build for PS3 Fedora (Sackboy) www.ps3linux.net on Cell/B.E.

