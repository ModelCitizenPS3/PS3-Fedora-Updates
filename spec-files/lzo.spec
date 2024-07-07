%define platform .PS3

ExclusiveArch:  ppc ppc64
Name:           lzo
Version:        2.10
Release:        2%{?dist}%{platform}
Summary:        Data compression library with very fast (de)compression
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.oberhumer.com/opensource/%{name}/
Source0:        http://www.oberhumer.com/opensource/%{name}/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel
Provides:       %{name} < %{version}

%description
LZO is a portable lossless data compression library written in ANSI C. It
offers pretty fast compression and very fast decompression. Decompression
requires no memory. In addition there are slower compression levels achieving
a quite competitive compression ratio while still decompressing at this very
high speed.

%package minilzo
Summary:    Mini version of lzo for apps which don't need the full version
Group:      System Environment/Libraries

%description minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.

%package devel
Summary:    Development files for the lzo library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-minilzo = %{version}-%{release}
Requires:   zlib-devel pkgconfig

%description devel
LZO is a portable lossless data compression library written in ANSI C. It
offers pretty fast compression and very fast decompression. This package
contains development files needed for lzo.


%prep
%setup -q


%build
%configure --enable-static=no --enable-shared=yes
make %{?_smp_mflags}
%ifarch ppc
export BITS=-m32
%else
export BITS=-m64
%endif
gcc $BITS %{optflags} -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc $BITS %{optflags} -g -shared -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
cp -f libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}/
rm $RPM_BUILD_ROOT%{_libdir}/liblzo2.la
mkdir $RPM_BUILD_ROOT%{_datadir}/minilzo
cp -f minilzo/README.LZO $RPM_BUILD_ROOT%{_datadir}/minilzo/README.LZO


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}/AUTHORS
%doc %{_datadir}/doc/%{name}/COPYING
%doc %{_datadir}/doc/%{name}/NEWS
%doc %{_datadir}/doc/%{name}/THANKS
%{_libdir}/liblzo2.so.*

%files minilzo
%defattr(-,root,root,-)
%doc %{_datadir}/minilzo/README.LZO
%{_libdir}/libminilzo.so.0

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}/LZOAPI.TXT
%doc %{_datadir}/doc/%{name}/LZO.FAQ
%doc %{_datadir}/doc/%{name}/LZO.TXT
%{_includedir}/lzo
%{_libdir}/lib*lzo*.so
%{_libdir}/pkgconfig/lzo2.pc


%changelog
* Fri Jul 5 2024 The Model Citizen <model.citizen@ps3linux.net> - 2.10-2
- Enabled checks

* Fri Jul 5 2024 The Model Citizen <model.citizen@ps3linux.net> - 2.10-1
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

