%define platform .PS3

ExclusiveArch:  ppc ppc64
Name:           zstd
Version:        1.3.5
Release:        1%{?dist}%{platform}
Summary:        Zstd compression library
License:        BSD
URL:            https://github.com/facebook/%{name}
Source0:        http://sources.buildroot.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       zlib lzma-libs lz4-libs
Requires:       libzstd = %{version}-%{release}

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm, targeting
real-time compression scenarios at zlib-level compression ratio.

%package -n libzstd
Summary:    Zstd shared library

%description -n libzstd
Zstandard compression shared library.

%package -n libzstd-static
Summary:    Static variant of the Zstd library
Requires:   libzstd-devel = %{version}-%{release}

%description -n libzstd-static
Static variant of the Zstd library.

%package -n libzstd-devel
Summary:    Header files for Zstd library
Requires:   libzstd = %{version}-%{release}
Requires:   pkgconfig

%description -n libzstd-devel
Header files for Zstd library.


%prep
%setup -q


%build
%ifarch ppc
export BITS=-m32
%else
export BITS=-m64
%endif
CC="gcc $BITS" CXX="g++ $BITS" CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple" CXXFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple" make %{?_smp_mflags}


%check
make check


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install PREFIX=/usr DESTDIR=$RPM_BUILD_ROOT
%ifarch ppc64
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mv -f $RPM_BUILD_ROOT/usr/lib/libzstd.a $RPM_BUILD_ROOT%{_libdir}/libzstd.a
mv -f $RPM_BUILD_ROOT/usr/lib/libzstd.so.1.3.5 $RPM_BUILD_ROOT%{_libdir}/libzstd.so.1.3.5
mv -f $RPM_BUILD_ROOT/usr/lib/pkgconfig/libzstd.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libzstd.pc
rm -rf $RPM_BUILD_ROOT/usr/lib
pushd $(pwd)
cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libzstd.so.1.3.5 libzstd.so.1
ln -sf libzstd.so.1.3.5 libzstd.so
popd
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING LICENSE NEWS
%{_bindir}/unzstd
%{_bindir}/zstd
%{_bindir}/zstdcat
%{_bindir}/zstdgrep
%{_bindir}/zstdless
%{_bindir}/zstdmt
%{_mandir}/man1/unzstd.1*
%{_mandir}/man1/zstd.1*
%{_mandir}/man1/zstdcat.1*

%files -n libzstd
%defattr(-,root,root,-)
%{_libdir}/libzstd.so.1
%{_libdir}/libzstd.so.1.3.5

%files -n libzstd-static
%defattr(-,root,root,-)
%{_libdir}/libzstd.a

%files -n libzstd-devel
%defattr(-,root,root,-)
%{_includedir}/zbuff.h
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_includedir}/zstd_errors.h
%{_libdir}/libzstd.so
%{_libdir}/pkgconfig/libzstd.pc


%changelog
* Fri Jul 26 2024 The Model Citizen <model.citizen@ps3linux.net> - 1.3.5-1
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

