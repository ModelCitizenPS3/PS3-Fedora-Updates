Name:           zlib
Version:        1.2.13
Release:        1%{?dist}%{?platform}
Summary:        The zlib compression and decompression library
Group:          System Environment/Libraries
Source0:        %{name}-%{version}.tar.gz
URL:            https://www.%{name}.net/
License:        %{name}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  automake, autoconf, libtool
Provides:       %{name} < %{version}
ExclusiveArch:  ppc ppc64

%description
Zlib is a general-purpose, patent-free, lossless data compression library
which is used by many different programs.

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
Provides:   minizip < %{version}

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
CC=%{__cc} CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple" ./configure --const --prefix=%{_prefix} --libdir=/%{_lib} --sharedlibdir=/%{_lib} --includedir=%{_includedir}
%else
CC=%{__cc} CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple" ./configure --const --64 --prefix=%{_prefix} --libdir=/%{_lib} --sharedlibdir=/%{_lib} --includedir=%{_includedir}
%endif
make %{?_smp_mflags}
cd contrib/minizip
autoreconf --install
%configure CC=%{__cc} CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple"
make %{?_smp_mflags}
cd ../../


%check
make check


%install
rm -rf ${RPM_BUILD_ROOT}
cd contrib/minizip
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
cd ../../
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libminizip.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libminizip.la
mv -f $RPM_BUILD_ROOT/%{_lib}/pkgconfig/%{name}.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/%{name}.pc
rm -rf $RPM_BUILD_ROOT/%{_lib}/pkgconfig
mv -f $RPM_BUILD_ROOT/%{_lib}/libz.a $RPM_BUILD_ROOT%{_libdir}/libz.a
rm $RPM_BUILD_ROOT/%{_lib}/libz.so
ln -s ../../%{_lib}/libz.1.2.13 $RPM_BUILD_ROOT%{_libdir}/libz.so
ln -s ../../%{_lib}/libz.1.2.13 $RPM_BUILD_ROOT%{_libdir}/libz.so.1
ln -s ../../%{_lib}/libz.1.2.13 $RPM_BUILD_ROOT%{_libdir}/libz.so.1.2.13

    
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
/%{_lib}/libz.so.1.2.13
%{_libdir}/libz.so.1
%{_libdir}/libz.so.1.2.13

%files devel
%defattr(-,root,root,-)
%{_libdir}/libz.so
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/zlib.3*

%files static
%defattr(-,root,root,-)
%{_libdir}/libz.a

%files -n minizip
%defattr(-,root,root,-)
%{_libdir}/libminizip.so.1
%{_libdir}/libminizip.so.1.0.0

%files -n minizip-devel
%defattr(-,root,root,-)
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc


%changelog
* Fri Jun 07 2024 Model Citizen <model.citizen@ps3linux.net> - 1.2.13-1
- Initial build for PS3 Fedora on Cell/B.E (sackboy)

