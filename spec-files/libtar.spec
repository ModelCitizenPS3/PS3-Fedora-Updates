Name:           libtar
Version:        1.2.20
Release:        1%{?dist}%{?platform}
Summary:        Tar file manipulation API
License:        MIT
Group:          System Environment/Libraries
URL:            https://directory.fsf.org/wiki/Libtar/
Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib zlib-devel libtool make
Requires:       zlib
ExclusiveArch:  ppc ppc64

%description
libtar is a C library for manipulating tar archives. It supports both the
strict POSIX tar format and many of the commonly-used GNU extensions.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The libtar-devel package contains libraries and header files for developing
applications that use libtar.


%prep
%setup -q -n %{name}


%build
%ifarch ppc
export CC="%{__cc} -m32"
%else
export CC="%{__cc} -m64"
%endif
autoreconf --force --install
%configure --disable-encap --disable-maintainer-mode --enable-shared=yes --enable-static=no
make %{?_smp_mflags}
cd libtar
make %{?_smp_mflags}
cd ../doc
make %{?_smp_mflags}
cd ../


%install
rm -rf $RPM_BUILD_ROOT
cd libtar
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
cd ../doc
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
cd ../
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libtar.la
mv $RPM_BUILD_ROOT%{_libdir}/libtar.so $RPM_BUILD_ROOT%{_libdir}/libtar.so.1.2.20
chmod a+x $RPM_BUILD_ROOT%{_libdir}/libtar.so.1.2.20
ln -s libtar.so.1.2.20 $RPM_BUILD_ROOT%{_libdir}/libtar.so
ln -s libtar.so.1.2.20 $RPM_BUILD_ROOT%{_libdir}/libtar.so.1


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYRIGHT TODO README ChangeLog*
%{_bindir}/%{name}
%{_libdir}/libtar.so.1
%{_libdir}/libtar.so.1.2.20

%files devel
%defattr(-,root,root,-)
%{_includedir}/libtar.h
%{_includedir}/libtar_listhash.h
%{_libdir}/libtar.so
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 07 2024 Model Citizen <model.citizen@ps3linux.net> - 1.2.20-1
- Initial build for Playstation 3 Fedora on Cell/B.E. (sackboy)

