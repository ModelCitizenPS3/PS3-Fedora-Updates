Name:           ncompress
Version:        5.0
Release:        1%{?dist}%{?platform}
Summary:        Fast compression and decompression utilities
License:        Public Domain
Group:          Applications/File
URL:            https://vapier.github.io/%{name}/
Source:         https://fossies.org/linux/privat/%{name}-%{version}.tar.gz
BuildRequires:  gcc glibc-devel fileutils
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  ppc

%description
The ncompress package contains the compress and uncompress file compression
and decompression utilities, which are compatible with the original UNIX
compress utility (.Z file extensions). These utilities can't handle gzipped
(.gz file extensions) files, but gzip can handle compressed files. Install
ncompress if you need compression/decompression utilities which are compatible
with the original UNIX compress utility.


%prep
%setup -q


%build
make %{?_smp_mflags} CC="%{__cc} -m32" CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" ENDIAN=1234


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -p -m755 compress $RPM_BUILD_ROOT/%{_bindir}
ln -sf compress $RPM_BUILD_ROOT/%{_bindir}/uncompress
install -p -m644 compress.1 $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf compress.1 $RPM_BUILD_ROOT%{_mandir}/man1/uncompress.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LZW.INFO README.md
%{_bindir}/compress
%{_bindir}/uncompress
%{_mandir}/man1/*


%changelog
* Fri May 31 2024 Model Citizen <model.citizen@ps3linux.net> - 5.0-1
- Initial build for Playstation 3 Fedora on Cell/B.E. (sackboy)

