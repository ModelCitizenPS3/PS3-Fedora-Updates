# BUILD COMMAND: rpmbuild -ba --target noarch --define "platform .PS3" fedora-release.spec

%define release_name Constantine
%define dist_version 12

Summary:        Fedora release files
Name:           fedora-release
Version:        12
Release:        3%{?platform}
License:        GPLv2
Group:          System Environment/Base
URL:            http://fedoraproject.org
Source:         %{name}-%{version}.tar.gz
Obsoletes:      redhat-release
Provides:       redhat-release
Provides:       system-release = %{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Fedora release files such as yum configs and various /etc/ files that define the release.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc
echo "Fedora release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
echo "cpe:/o:fedoraproject:fedora:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/fedora-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for arch in i386 x86_64 ppc ppc64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora-$arch
done
ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora
popd
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in *.repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
%%fedora            %{dist_version}
%%dist              .fc%{dist_version}
%%fc%{dist_version} 1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc GPL 
%dir %{_sysconfdir}/pki/rpm-gpg
%dir %{_sysconfdir}/yum.repos.d
%config %attr(0644,root,root) %{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%config %attr(0644,root,root) %{_sysconfdir}/system-release-cpe
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/issue
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/issue.net
%config %attr(0644,root,root) %{_sysconfdir}/rpm/macros.dist
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Mon May 13 2024 Model Citizen <model.citizen@ps3linux.net> - 12-3
- Initial buils for Sackboy Linux on Playstatopn 3 (Cell/B.E.)

