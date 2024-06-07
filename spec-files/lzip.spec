Name:               lzip
Version:            1.24
Release:            1%{?dist}%{?platform}
Summary:            LZMA compressor with integrity checking
Group:              Applications/File
License:            GPLv3+
URL:                https://www.nongnu.org/%{name}/
Source0:            http://download-mirror.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post):     info
Requires(preun):    info
ExclusiveArch:      ppc

%description
Lzip compresses data using LZMA (Lempel-Ziv-Markov chain-Algorithm). It
supports integrity checking using CRC (Cyclic Redundancy Check). To archive
multiple files, tar can be used with lzip. Please note, that the lzip file
format (.lz) is not compatible with the lzma file format (.lzma).


%prep
%setup -q


%build
%configure CXX="g++ -m32" CXXFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple"
make %{?_smp_mflags}


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -Rf $RPM_BUILD_ROOT%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/lzip
%{_infodir}/lzip.info*
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Jun 07 2024 Model Citizen <model.citizen@ps3linux.net> - 1.24-1
- Initial build for Playstation 3 Fedora on Cell/B.E. (sackboy)

