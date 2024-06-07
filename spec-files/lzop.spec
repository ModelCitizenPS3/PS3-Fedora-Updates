Name:           lzop
Version:        1.04
Release:        1%{?dist}%{?platform}
Summary:        Real-time file compressor
Group:          Applications/Archiving
License:        GPL+
URL:            https://www.%{name}.org/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  lzo-devel
ExclusiveArch:  ppc

%description
lzop is a compression utility which is designed to be a companion to gzip. It
is based on the LZO library and its main advantages over gzip are much higher
compression and decompression speed at the cost of compression ratio. lzop was
designed with reliability, speed, portibility and as a reasonable drop-in
compatiblity to gzip.


%prep
%setup -q


%build
%configure --disable-silent-rules
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall %{?_smp_mflags}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(0644, root, root, 0755)
%attr(0755,root,root) %{_bindir}/lzop
%doc %{_datadir}/doc/%{name}/*
%doc %{_mandir}/man1/lzop.1*


%changelog
* Fri Jun 07 2024 Model Citizen <model.citizen@ps3linux.net> - 1.04-1
- Initial build for Playstation 3 Fedora on Cell/B.E. (sackboy)

