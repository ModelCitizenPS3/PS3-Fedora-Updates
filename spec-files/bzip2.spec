Name:           bzip2
Version:        1.0.8
Release:        1%{?dist}%{?platform}
Summary:        A file compression utility
License:        BSD
Group:          Applications/File
URL:            https://sourceware.org/%{name}/
Source0:        https://sourceware.org/pub/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  ppc ppc64

%description
Bzip2 is a freely available, patent-free, high quality data compressor. Bzip2
compresses files to within 10 to 15 percent of the capabilities of the best
techniques available. However, bzip2 has the added benefit of being
approximately two times faster at compression and six times faster at
decompression than those techniques. Bzip2 is not the fastest compression
utility, but it does strike a balance between speed and compression capability.
Install bzip2 if you need a compression utility.

%package devel
Summary:    Header files developing apps which will use bzip2
Group:      Development/Libraries
Requires:   %{name}-libs = %{version}-%{release}

%description devel
Header files and a library of bzip2 functions, for developing apps which will
use the library.

%package libs
Summary:    Libraries for applications using bzip2
Group:      System Environment/Libraries
Provides:   libbz2.so.1

%description libs
Libraries for applications using the bzip2 compression format.


%prep
%setup -q 


%build
%ifarch ppc
export BITS=-m32
%else
export BITS=-m64
%endif
make -f Makefile-libbz2_so CC="%{__cc} $BITS" AR="%{__ar}" RANLIB="%{__ranlib}" CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fpic -fPIC" %{?_smp_mflags} all
rm -f *.o
make CC="%{__cc} $BITS" AR="%{__ar}" RANLIB="%{__ranlib}" CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" %{?_smp_mflags} all


%install
rm -rf ${RPM_BUILD_ROOT}
make %{?_smp_mflags} install PREFIX=$RPM_BUILD_ROOT%{_prefix}
rm $RPM_BUILD_ROOT%{_prefix}/lib/libbz2.a
%ifarch ppc64
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib
mkdir -p $RPM_BUILD_ROOT%{_libdir}
%endif
install -m 755 libbz2.so.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -s libbz2.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libbz2.so.1.0
ln -s libbz2.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libbz2.so
mkdir -p $RPM_BUILD_ROOT/%{_lib}
ln -s ..%{_libdir}/libbz2.so.%{version} $RPM_BUILD_ROOT/%{_lib}/libbz2.so.1
ln -s ..%{_libdir}/libbz2.so.%{version} $RPM_BUILD_ROOT/%{_lib}/libbz2.so.1.0.6
rm $RPM_BUILD_ROOT%{_bindir}/bzcmp
rm $RPM_BUILD_ROOT%{_bindir}/bzegrep
rm $RPM_BUILD_ROOT%{_bindir}/bzfgrep
rm $RPM_BUILD_ROOT%{_bindir}/bzless
ln -s bzdiff $RPM_BUILD_ROOT%{_bindir}/bzcmp
ln -s bzgrep $RPM_BUILD_ROOT%{_bindir}/bzegrep
ln -s bzgrep $RPM_BUILD_ROOT%{_bindir}/bzfgrep
ln -s bzmore $RPM_BUILD_ROOT%{_bindir}/bzless
install -m 755 %{name}-shared  $RPM_BUILD_ROOT%{_bindir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mv $RPM_BUILD_ROOT%{_prefix}/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1/
rm -rf $RPM_BUILD_ROOT%{_prefix}/man


%post libs -p /sbin/ldconfig

%postun libs  -p /sbin/ldconfig


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES README 
%{_bindir}/*
%{_mandir}/man1/*.1*

%files libs
%defattr(-,root,root,-)
/%{_lib}/libbz2.so.1
/%{_lib}/libbz2.so.1.0.6
%{_libdir}/libbz2.so.1.0
%{_libdir}/libbz2.so.%{version}

%files devel
%defattr(-,root,root,-)
%doc manual.html manual.pdf
%{_includedir}/bzlib.h
%{_libdir}/libbz2.so


%changelog
* Fri May 31 2024 Model Citizen <model.citizen@ps3linux.net> - 1.0.8-1
- Initial build for Playstation 3 Fedora on Cell/B.E. (sackboy)

