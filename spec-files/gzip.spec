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
Requires:       mktemp, less, /sbin/install-info
ExclusiveArch:  ppc ppc64

%description
The gzip package contains the popular GNU gzip data compression program. Gzipped files have a .gz extension. Gzip should be installed on your system, because it is a very commonly used data compression program.


%prep
%setup -q


%build
%ifarch ppc
CC="gcc -m32"
%else
CC="gcc -m64"
%endif
DEFS="NO_ASM"
CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple"
CPPFLAGS="-DHAVE_LSTAT"
export CC DEFS CFLAGS CPPFLAGS
%configure --bindir=%{_bindir} --disable-silent-rules --disable-year2038
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm -f %{buildroot}%{_infodir}/dir


%check
make %{?_smp_mflags} check


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
- Initial build for Sackboy Linux on Playstation 3 (Cell/B.E.)

