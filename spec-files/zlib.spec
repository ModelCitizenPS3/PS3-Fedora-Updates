Name:           zlib
Version:        1.2.13
Release:        1%{?dist}%{?platform}
Summary:        The zlib compression and decompression library
Group:          System Environment/Libraries
License:        zlib
URL:            https://%{name}.net/
Source0:        http://www.%{name}.net/fossils/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  automake, autoconf, libtool
ExclusiveArch:  ppc ppc64

%description
Zlib is a general-purpose, patent-free, lossless data compression library which is used by many different programs.

%package devel
Summary:    Header files and libraries for Zlib development
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed to develop programs that use the zlib compression and decompression library.

%package static
Summary:    Static libraries for Zlib development
Group:      Development/Libraries
Requires:   %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed to develop programs that use the zlib compression and decompression library.

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
Requires:   zlib-devel = %{version}-%{release}
Requires:   pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for developing applications which use minizip.


%prep
%setup -q


%build
CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple"
CXXFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple"
FFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple -I/usr/lib/gfortran/modules"
export CFLAGS CXXFLAGS FFLAGS
%ifarch ppc64
./configure --const --64 --prefix=/usr --libdir=%{_libdir} --sharedlibdir=%{_libdir} --includedir=%{_includedir}
%else
./configure --const --prefix=/usr --libdir=%{_libdir} --sharedlibdir=%{_libdir} --includedir=%{_includedir}
%endif
make %{?_smp_mflags}
pushd $(pwd)
cd contrib/minizip
autoreconf --install
%configure
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd $(pwd)
cd contrib/minizip
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libminizip.la
mkdir $RPM_BUILD_ROOT/%{_lib}
ln -s ..%{_libdir}/libz.so.1.2.13 $RPM_BUILD_ROOT/%{_lib}/libz.so.1
ln -s ..%{_libdir}/libz.so.1.2.13 $RPM_BUILD_ROOT/%{_lib}/libz.so.1.2.3


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README ChangeLog FAQ
%{_libdir}/libz.so.1
%{_libdir}/libz.so.1.2.13
/%{_lib}/libz.so.1
/%{_lib}/libz.so.1.2.3

%files devel
%defattr(-,root,root,-)
%doc README doc/algorithm.txt doc/rfc1950.txt doc/rfc1951.txt doc/rfc1952.txt doc/txtvsbin.txt
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%{_mandir}/man3/zlib.3.*

%files static
%defattr(-,root,root,-)
%doc README
%{_libdir}/libz.a
%{_libdir}/libminizip.a

%files -n minizip
%defattr(-,root,root,-)
%doc contrib/minizip/MiniZip64_info.txt contrib/minizip/MiniZip64_Changes.txt
%{_libdir}/libminizip.so.1
%{_libdir}/libminizip.so.1.0.0

%files -n minizip-devel
%defattr(-,root,root,-)
%dir %{_includedir}/minizip
%{_includedir}/minizip/crypt.h
%{_includedir}/minizip/ioapi.h
%{_includedir}/minizip/mztools.h
%{_includedir}/minizip/unzip.h
%{_includedir}/minizip/zip.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc


%changelog
* Tue May 28 2024 Model Citizen <model.citizen@ps3linux.net> - 1.2.13-1
- Initial build for Sackboy Linux on Playstation 3 (Cell/B.E.)

