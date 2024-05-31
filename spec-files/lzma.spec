Name:           lzma
Version:        4.32.7
Release:        4%{?dist}%{?platform}
Summary:        LZMA Utils
Group:          Applications/File
License:        GPLv2+
URL:            https://tukaani.org/%{name}/
Source0:        https://tukaani.org/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       %{name}-libs = %{version}-%{release}
ExclusiveArch:  ppc ppc64

%description
LZMA provides very high compression ratio and fast decompression. The core of the LZMA utils is Igor Pavlov's LZMA SDK containing the actual LZMA encoder/decoder. LZMA utils add a few scripts which provide gzip-like command line interface and a couple of other LZMA related tools. 

%package libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+
Obsoletes:  %{name}-libs < %{version}

%description libs
Libraries for decoding LZMA compression.

%package devel
Summary:	Devel libraries & headers for liblzmadec
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}

%description  devel
Devel libraries & headers for liblzmadec.


%prep
%setup -q


%build
%configure --disable-static CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
rm -f %{buildroot}/%{_libdir}/liblzmadec.la


%check
make %{?_smp_mflags} check


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README THANKS COPYING.* ChangeLog AUTHORS
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%%doc COPYING.*
%{_libdir}/liblzmadec.so.0
%{_libdir}/liblzmadec.so.0.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/lzmadec.h
%{_libdir}/liblzmadec.so


%changelog
* Fri May 31 2024 Model Citizen <model.citizen@ps3linux.net> - 4.32.7-4
- Initial build for Sackboy Linux on Playstation 3 (Cell/B.E.)

