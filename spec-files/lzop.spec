%define platform .PS3

ExclusiveArch:  ppc
Name:           lzop
Version:        1.04
Release:        1%{?dist}%{platform}
Summary:        Real-time fire compressor
Group:          Applications/Archiving
License:        GPL+
URL:            http://www.%{name}.org/
Source0:        http://www.%{name}.org/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  lzo-devel

%description
lzop is a compression utility which is designed to be a companion to gzip. It
is based on the LZO library and its main advantages over gzip are much higher
compression and decompression speed at the cost of compression ratio.
lzop was designed with reliability, speed, portibility and as a reasonable
drop-in compatiblity to gzip.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}/*
%{_bindir}/lzop
%{_mandir}/man1/lzop.1*


%changelog
* Tue Jul 23 2024 The Model Citizen <model.citizen@ps3linux.net> - 1.04-1
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

