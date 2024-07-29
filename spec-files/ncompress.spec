%define platform .PS3

ExclusiveArch:  ppc
Name:           ncompress
Version:        4.2.4.6
Release:        1%{?dist}%{platform}
Summary:        Fast compression and decompression utilities
Group:          Applications/File
License:        Public Domain
URL:            https://%{name}.sourceforge.io/
Source0:        https://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gcc glibc-devel fileutils

%description
The ncompress package contains the compress and uncompress file compression and
decompression utilities, which are compatible with the original UNIX compress
utility (.Z file extensions).  These utilities can't handle gzipped
(.gz file extensions) files, but gzip can handle compressed files.
Install ncompress if you need compression/decompression utilities which are
compatible with the original UNIX compress utility.


%prep
%setup -q


%build
CC="gcc -m32" CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" ENDIAN=1234 make


%check
make check


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m755 compress $RPM_BUILD_ROOT%{_bindir}
ln -sf compress $RPM_BUILD_ROOT%{_bindir}/uncompress
install -p -m644 compress.1 $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf compress.1 $RPM_BUILD_ROOT%{_mandir}/man1/uncompress.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LZW.INFO README.md
%{_bindir}/compress
%{_bindir}/uncompress
%{_mandir}/man1/compress.1*
%{_mandir}/man1/uncompress.1*


%changelog
* Sat Jul 27 2024 The Model Citizen <model.citizen@ps3linux.net> - 4.2.4.6-1
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

