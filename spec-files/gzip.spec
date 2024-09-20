%define platform .PS3

ExclusiveArch:  ppc
Name:           gzip
Version:        1.3.13
Release:        1%{?dist}%{platform}
Summary:        The GNU data compression program
Group:          Applications/File
License:        GPLv2 and GFDL
URL:            http://www.%{name}.org/
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  texinfo
Requires:       /sbin/install-info
Requires:       mktemp less

%description
The gzip package contains the popular GNU gzip data compression program.
Gzipped files have a .gz extension.
Gzip should be installed on your system, because it is a very commonly
used data compression program.


%prep
%setup -q


%build
CC="gcc -m32" CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple" %configure --bindir=/bin --disable-silent-rules
make %{?_smp_mflags}


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}/bin/uncompress
mkdir -p $RPM_BUILD_ROOT%{_bindir}
for file in  zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore ; do
  mv ${RPM_BUILD_ROOT}/bin/$file ${RPM_BUILD_ROOT}%{_bindir}/$file
done
ln -s ../../bin/gzip ${RPM_BUILD_ROOT}%{_bindir}/gzip
ln -s ../../bin/gunzip ${RPM_BUILD_ROOT}%{_bindir}/gunzip
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp -f AUTHORS $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/AUTHORS
cp -f ChangeLog $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/ChangeLog
cp -f NEWS $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/NEWS
cp -f README $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/README
cp -f THANKS $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/THANKS
cp -f TODO $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/TODO


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/bin/gunzip
/bin/gzip
/bin/zcat
%{_bindir}/gunzip
%{_bindir}/gzexe
%{_bindir}/gzip
%{_bindir}/zcmp
%{_bindir}/zdiff
%{_bindir}/zegrep
%{_bindir}/zfgrep
%{_bindir}/zforce
%{_bindir}/zgrep
%{_bindir}/zless
%{_bindir}/zmore
%{_bindir}/znew
%dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/AUTHORS
%doc %{_datadir}/doc/%{name}-%{version}/ChangeLog
%doc %{_datadir}/doc/%{name}-%{version}/NEWS
%doc %{_datadir}/doc/%{name}-%{version}/README
%doc %{_datadir}/doc/%{name}-%{version}/THANKS
%doc %{_datadir}/doc/%{name}-%{version}/TODO
%{_infodir}/gzip.info.gz
%{_mandir}/man1/gunzip.1.gz
%{_mandir}/man1/gzexe.1.gz
%{_mandir}/man1/gzip.1.gz
%{_mandir}/man1/zcat.1.gz
%{_mandir}/man1/zcmp.1.gz
%{_mandir}/man1/zdiff.1.gz
%{_mandir}/man1/zforce.1.gz
%{_mandir}/man1/zgrep.1.gz
%{_mandir}/man1/zless.1.gz
%{_mandir}/man1/zmore.1.gz
%{_mandir}/man1/znew.1.gz


%changelog
* Wed Jul 31 2024 The Model Citizen <model.citizen@ps3linux.net> - 1.3.13-1
- Initial build for Playstation 3 Fedora (Sackboy) on Cell/B.E.

