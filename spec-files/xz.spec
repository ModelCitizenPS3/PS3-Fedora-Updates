%define git_date 20091007

Summary:	    LZMA compression utilities
Name:		    xz
Version:	    4.999.9
Release:	    0.3.beta.%{git_date}git%{?dist}%{?platform}
License:	    LGPLv2+
Group:		    Applications/File
Source0:	    http://tukaani.org/%{name}/%{name}-%{version}beta.%{git_date}git.tar.xz
URL:		    http://tukaani.org/%{name}/
BuildRoot:	    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	    %{name}-libs = %{version}-%{release}
ExclusiveArch:  ppc ppc64

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.
LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.

%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package 	devel
Summary:	Devel libraries & headers for liblzma
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig

%description  devel
Devel libraries and headers for liblzma.

%package 	lzma-compat
Summary:	Older LZMA format compatibility binaries
Group:		Development/Libraries
License:	GPLv2+ and LGPLv2+
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lzma < 5
Provides:	lzma = 5

%description  lzma-compat
The lzma-compat package contains compatibility links for older commands that
deal with the older LZMA format.


%prep
%setup -q -n %{name}-%{version}beta


%build
./autogen.sh
%ifarch ppc
export BITS=-m32
%else
export BITS=-m64
%endif
%configure --enable-shared=yes --enable-static=no --disable-nls --enable-unaligned-access CC="gcc $BITS" CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple -D_FILE_OFFSET_BITS=64"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make %{?_smp_mflags} check


%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_docdir}/%{name}


%clean
rm -rf %{buildroot}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS README THANKS COPYING.* ChangeLog 
%{_bindir}/*xz*
%{_mandir}/man1/*xz*

%files libs
%defattr(-,root,root,-)
%doc COPYING.*
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblzma.pc

%files lzma-compat
%defattr(-,root,root,-)
%{_bindir}/*lz*
%{_mandir}/man1/*lz*


%changelog
* Thu Jun 06 2024 Model Citizen <model.citizen@ps3linux.net> - 4.999.9-0.3.beta.20091007
- Recompiled for Playstation 3 Fedora on Cell/B.E. (sackboy)

