# BUILD COMMAND: rpmbuild -ba --target ppc/ppc64 --define "platform .PS3" --define "debug_package %{nil}" zlib.spec

Packager:       The Model Citizen <model.citizen@ps3linux.net>
Name:           zlib
Version:        1.2.13
Release:        1%{?dist}%{?platform}
Summary:        The zlib compression and decompression library
Group:          System Environment/Libraries
License:        zlib
URL:            http://www.gzip.org/%{name}/
Source0:        http://www.%{name}.net/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  automake, autoconf, libtool
Provides:       %{name} = 1.2.3-23%{?dist}
ExclusiveArch:  ppc ppc64

%description
Zlib is a general-purpose, patent-free, lossless data compression library which is used by many different programs.

%package devel
Summary:    Header files and libraries for Zlib development
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:   %{name}-devel = 1.2.3-23%{?dist}

%description devel
The zlib-devel package contains the header files and libraries needed to develop programs that use the zlib compression and decompression library.

%package static
Summary:    Static libraries for Zlib development
Group:      Development/Libraries
Requires:   %{name}-devel = %{version}-%{release}
Provides:   %{name}-static = 1.2.3-23%{?dist}

%description static
The zlib-static package includes static libraries needed to develop programs that use the zlib compression and decompression library.

%package -n minizip
Summary:    Minizip manipulates files from a .zip archive
Group:      System Environment/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:   minizip = 1.2.3-23%{?dist}

%description -n  minizip
Minizip manipulates files from a .zip archive.

%package -n minizip-devel
Summary:    Development files for the minizip library
Group:      Development/Libraries
Requires:   minizip = %{version}-%{release}
Requires:   zlib-devel = %{version}-%{release}
Provides:   minizip-devel = 1.2.3-23%{?dist}
Requires:   pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for developing applications which use minizip.


%prep
%setup -q


%build
export CFLAGS="%{optflags}"
%ifarch ppc
./configure --const --prefix=/usr --libdir=%{_libdir} --sharedlibdir=%{_libdir} --includedir=%{_includedir}
%else
./configure --const --64 --prefix=/usr --libdir=%{_libdir} --sharedlibdir=%{_libdir} --includedir=%{_includedir}
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
rm -f $RPM_BUILD_ROOT%{_libdir}/libminizip.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libminizip.la
# Replace original files in /lib or /lib64 with symlinks to new lib
mkdir $RPM_BUILD_ROOT/%{_lib}
pushd $(pwd)
cd $RPM_BUILD_ROOT/%{_lib}
ln -s ..%{_libdir}/libz.so.1.2.13 libz.so.1
ln -s ..%{_libdir}/libz.so.1.2.13 libz.so.1.2.3
ln -s ..%{_libdir}/libminizip.so.1.0.0 libminizip.so.1
ln -s ..%{_libdir}/libminizip.so.1.0.0 libminizip.so.1.0.0
popd


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/libz.so.1
%{_libdir}/libz.so.1.2.13
/%{_lib}/libz.so.1
/%{_lib}/libz.so.1.2.3

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libz.so
%{_libdir}/pkgconfig/minizip.pc
%{_libdir}/pkgconfig/zlib.pc
%{_mandir}/man3/zlib.3.gz

%files static
%defattr(-,root,root,-)
%{_libdir}/libz.a

%files -n minizip
%defattr(-,root,root,-)
%{_libdir}/libminizip.so.1
%{_libdir}/libminizip.so.1.0.0
/%{_lib}/libminizip.so.1
/%{_lib}/libminizip.so.1.0.0

%files -n minizip-devel
%defattr(-,root,root,-)
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so


%changelog
* Mon May 13 2024 Model Citizen <model.citizen@ps3linux.net> - 1.2.13-1
- Initial build for Sackboy Linux on Playstation 3 (Cell/B.E.)

