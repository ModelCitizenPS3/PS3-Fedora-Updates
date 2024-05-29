Name:           lzo
Version:        2.10
Release:        1%{?dist}%{?platform}
Summary:        Data compression library with very fast (de)compression
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.oberhumer.com/opensource/%{name}/
Source0:        http://www.oberhumer.com/opensource/%{name}/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel
ExclusiveArch:  ppc ppc64

%description
LZO is a portable lossless data compression library written in ANSI C. It offers pretty fast compression and very fast decompression. Decompression requires no memory. In addition there are slower compression levels achieving a quite competitive compression ratio while still decompressing at this very high speed.

%package minilzo
Summary:    Mini version of lzo for apps that do not need the full version
Group:      System Environment/Libraries

%description minilzo
A small (mini) version of lzo for embedding into applications which do not need full blown lzo compression support.

%package devel
Summary:    Development files for the lzo library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-minilzo = %{version}-%{release}
Requires:   zlib-devel, pkgconfig

%description devel
LZO is a portable lossless data compression library written in ANSI C. It offers pretty fast compression and very fast decompression. This package contains development files needed for lzo.


%prep
%setup -q


%build
%configure --disable-silent-rules --enable-shared=yes --enable-static=no
make %{?_smp_mflags}
gcc %{optflags} -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc %{optflags} -shared -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/liblzo2.la
install -m 755 libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}/libminilzo.so
install -p -m 644 minilzo/minilzo.h $RPM_BUILD_ROOT%{_includedir}/%{name}


%check
make %{?_smp_mflags} check test


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post minilzo -p /sbin/ldconfig

%postun minilzo -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/liblzo2.so.2
%{_libdir}/liblzo2.so.2.0.0
%dir %{_datadir}/doc/%{name}
%doc %{_datadir}/doc/%{name}/AUTHORS
%doc %{_datadir}/doc/%{name}/COPYING
%doc %{_datadir}/doc/%{name}/THANKS
%doc %{_datadir}/doc/%{name}/NEWS

%files minilzo
%defattr(-,root,root,-)
%{_libdir}/libminilzo.so.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/liblzo2.so
%{_libdir}/libminilzo.so
%{_libdir}/pkgconfig/lzo2.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/lzo1.h
%{_includedir}/%{name}/lzo1a.h
%{_includedir}/%{name}/lzo1b.h
%{_includedir}/%{name}/lzo1c.h
%{_includedir}/%{name}/lzo1f.h
%{_includedir}/%{name}/lzo1x.h
%{_includedir}/%{name}/lzo1y.h
%{_includedir}/%{name}/lzo1z.h
%{_includedir}/%{name}/lzo2a.h
%{_includedir}/%{name}/lzo_asm.h
%{_includedir}/%{name}/lzoconf.h
%{_includedir}/%{name}/lzodefs.h
%{_includedir}/%{name}/lzoutil.h
%{_includedir}/%{name}/minilzo.h
%doc %{_datadir}/doc/%{name}/LZO.FAQ
%doc %{_datadir}/doc/%{name}/LZO.TXT
%doc %{_datadir}/doc/%{name}/LZOAPI.TXT


%changelog
* Tue May 28 2024 Model Citizen <model.citizen@ps3linux.net> - 2.10-1
- Initial build for Sackboy Linux on Playstation 3 (Cell/B.E.)

