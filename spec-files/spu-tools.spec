%define platform .PS3

ExclusiveArch:  ppc
Name:           spu-tools
Version:        2.3.0.136
Release:        1%{?dist}%{platform}
Summary:        SPU tools for the Cell CPU (Playstation 3)
License:        GPLv2
URL:            https://sourceforge.net/projects/libspe/files/libspe/libspe2/
Source0:        %{name}-%{version}.tar.gz
Patch0:         %{name}_makefile-edit.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  help2man

%description
SPU tools (spu-top and spu-ps) for the Cell Broadband Engine CPU on
Playstation 3. Also IBM's QS20 and QS21 blade servers had Cell CPUs.


%prep
%setup -q -n spu-tools
%patch0 -p 1


%build
%ifarch ppc
export CC="gcc -m32"
%else
export CC="gcc -m64"
%endif
cd src
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd src
make %{_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc src/COPYING
%{_bindir}/spu-ps
%{_bindir}/spu-top
%{_mandir}/man1/spu-ps.1.*
%{_mandir}/man1/spu-top.1.*


%changelog
* Wed Jul 24 2024 The Model Citizen <model.citizen@ps3linux.net> - 2.3.0.136-1
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

