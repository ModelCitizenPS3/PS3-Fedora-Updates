Name:           gzip
Version:        1.13
Release:        1%{?dist}%{?platform}
Summary:        The GNU data compression program
Group:          Applications/File
License:        GPLv2 and GFDL
URL:            https://www.gnu.org/software/%{name}/
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  texinfo
Requires:       mktemp, less
Requires:       /sbin/install-info
ExclusiveArch:  ppc

%description
The gzip package contains the popular GNU gzip data compression program.
Gzipped files have a .gz extension. Gzip should be installed on your system,
because it is a very commonly used data compression program.


%prep
%setup -q


%build
%configure --bindir=%{_bindir} --disable-silent-rules --disable-year2038 CC="gcc -m32" CPPFLAGS="-DHAVE_LSTAT" CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple" DEFS="NO_ASM"
make %{?_smp_mflags}


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_bindir}/uncompress


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc NEWS README AUTHORS ChangeLog THANKS TODO
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/gzip.info*


%changelog
* Fri May 31 2024 Model Citizen <model.citizen@ps3linux.net> - 1.13-1
- Initial build for Playstation 3 Fedora on Cell/B.E. (sackboy)

