%define platform .PS3

ExclusiveArch:      ppc
Name:               tar
Epoch:              2
Version:            1.35
Release:            1%{?dist}%{platform}
Summary:            A GNU file archiving program
Group:              Applications/Archiving
License:            GPLv3+
URL:                https://www.gnu.org/software/%{name}/
Source0:            https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:      autoconf automake gzip texinfo gettext libacl-devel libselinux-devel gawk rsh
Requires:           ncompress gzip bzip2 lzip xz-lzma-compat lzop xz zstd libacl rmt
Requires(post):     /sbin/install-info
Requires(preun):    /sbin/install-info

%description
The GNU tar program saves many files together in one archive and can restore individual files (or all of the files) from that archive. Tar can also be used to add supplemental files to an archive and to update or list files in the archive. Tar includes multivolume support, automatic archive compression/decompression, the ability to perform remote archives, and the ability to perform incremental and full backups.
If you want to use tar for remote backups, you also need to install the rmt package.


%prep
%setup -q


%build
%configure --bindir=/bin --libexecdir=/sbin --disable-silent-rules --disable-nls --enable-backup-scripts --disable-year2038 --with-packager="The Model Citizen" --with-compress=%{_bindir}/compress --with-gzip=%{_bindir}/gzip --with-bzip2=%{_bindir}/bzip2 --with-lzip=%{_bindir}/lzip --with-lzma=%{_bindir}/lzma --with-lzop=%{_bindir}/lzop --with-xz=%{_bindir}/xz --with-zstd=%{_bindir}/zstd CC="gcc -m32" CFLAGS="-O3 -mcpu=cell -mtune=cell -mno-string -mno-multiple"
make %{?_smp_mflags}


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}/sbin/rmt
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_mandir}/man8
ln -s tar ${RPM_BUILD_ROOT}/bin/gtar
ln -s tar.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/gtar.1


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info %{_infodir}/tar.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/tar.info-1.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/tar.info-2.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/tar.info-3.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/tar.info.gz %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/tar.info-1.gz %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/tar.info-2.gz %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/tar.info-3.gz %{_infodir}/dir || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO
/bin/tar
/bin/gtar
/sbin/backup.sh
/sbin/dump-remind
%{_sbindir}/backup
%{_sbindir}/restore
%{_infodir}/tar.info*
%{_mandir}/man1/*tar.1*


%changelog
* Mon Jul 29 2024 The Model Citizen <model.citizen@ps3linux.net> - 1.35-1
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

