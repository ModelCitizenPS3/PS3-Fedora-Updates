Name:           zlib
Version:        1.2.13
Release:        1%{?dist}%{?platform}
Summary:        The zlib compression and decompression library
Group:          System Environment/Libraries
Source0:        http://www.%{name}.net/fossils/%{name}-%{version}.tar.gz
URL:            http://www.%{name}.net/
License:        %{name}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:       %{name} = 1.2.3
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
Requires:   %{name}-devel = %{version}-%{release}
Requires:   pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for developing applications which use minizip.


%prep
%setup -q


%build
export CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple"
%ifarch ppc
CC="gcc -m32" ./configure --const --prefix=%{_prefix} --libdir=%{_libdir} --sharedlibdir=%{_libdir} --includedir=%{_includedir}
%else
CC="gcc -m64" ./configure --const --64 --prefix=%{_prefix} --libdir=%{_libdir} --sharedlibdir=%{_libdir} --includedir=%{_includedir}
%endif
make %{?_smp_mflags}
cd contrib/minizip
autoreconf --install
%ifarch ppc
%configure --enable-shared=yes --enable-static=no CC="gcc -m32"
%else
%configure --enable-shared=yes --enable-static=no CC="gcc -m64"
%endif
make %{?_smp_mflags}


%check
make check


%install
rm -rf ${RPM_BUILD_ROOT}
cd contrib/minizip
make install DESTDIR=$RPM_BUILD_ROOT
cd ../../
make install DESTDIR=$RPM_BUILD_ROOT
rm -f %{buildroot}%{_libdir}/libminizip.la
mkdir %{buildroot}/%{_lib}
ln -s ..%{_libdir}/libz.so.1.2.13 %{buildroot}/%{_lib}/libz.so.1
ln -s ..%{_libdir}/libz.so.1.2.13 %{buildroot}/%{_lib}/libz.so.1.2.3


%clean
rm -rf ${RPM_BUILD_ROOT}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README ChangeLog FAQ
/%{_lib}/libz.so.1
/%{_lib}/libz.so.1.2.3
%{_libdir}/libz.so.1
%{_libdir}/libz.so.1.2.13

%files devel
%defattr(-,root,root,-)
%doc README
%{_libdir}/libz.so
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/pkgconfig/zlib.pc
%{_mandir}/man3/zlib.3.*

%files static
%defattr(-,root,root,-)
%doc README
%{_libdir}/libz.a

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
%{_includedir}/minizip/unzip.h
%{_includedir}/minizip/zip.h
%{_libdir}/pkgconfig/minizip.pc
%{_libdir}/libminizip.so

%changelog
* Fri May 31 2024 Model Citizen <model.citizen@ps3linux.net> - 1.2.13-1
- Initial build for Sackboy Linux on Playstation 3 (Cell/B.E.)

