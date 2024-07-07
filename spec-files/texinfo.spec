%define platform .PS3

ExclusiveArch:      ppc
Name:               texinfo
Version:            5.0
Release:            1%{?dist}%{platform}
Summary:            Tools needed to create Texinfo format documentation files
Group:              Applications/Publishing
License:            GPLv3+
URL:                https://www.gnu.org/%{name}/
Source0:            http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:      zlib-devel ncurses-devel
Requires(post):     /sbin/install-info
Requires(preun):    /sbin/install-info
Obsoletes:          %{name} < %{version}

%description
Texinfo is a documentation system that can produce both online information and
printed output from a single source file. The GNU Project uses the Texinfo
file format for most of its documentation. Install texinfo if you want a
documentation system for producing bothonline and print documentation from the
same source file and/or if you are going to write documentation for the GNU Project.

%package tex
Summary:            Tools for formatting Texinfo documentation files using TeX
Group:              Applications/Publishing
Requires:           texinfo = %{version}-%{release}
Requires:           tetex
Requires(post):     %{_bindir}/texconfig-sys
Requires(postun):   %{_bindir}/texconfig-sys
Obsoletes:          %{name}-tex < %{version}

%description tex
Texinfo is a documentation system that can produce both online information and
printed output from a single source file. The GNU Project uses the Texinfo file
format for most of its documentation. The texinfo-tex package provides tools to
format Texinfo documents for printing using TeX.

%package -n info
Summary:    A stand-alone TTY-based reader for GNU texinfo documentation
Group:      System Environment/Base
Obsoletes:  info < %{version}

%description -n info
The GNU project uses the texinfo file format for much of its documentation. The
info package provides a standalone TTY-based browser program for viewing texinfo
files.


%prep
%setup -q


%build
%configure --disable-nls
make %{?_smp_mflags}


%check
make %{?_smp_mflags} check


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%{_datadir}/texmf/tex/texinfo
mv -f $RPM_BUILD_ROOT%{_bindir}/install-info $RPM_BUILD_ROOT/sbin/
install -p -m644 doc/texinfo.tex doc/txi-??.tex $RPM_BUILD_ROOT%{_datadir}/texmf/tex/texinfo/


%clean
rm -rf $RPM_BUILD_ROOT


%post
echo "Rebuilding texinfo dir file..."
rm -f %{_infodir}/dir.*
rm -f %{_infodir}/dir
for f in %{_infodir}/* ; do
  /sbin/install-info $f  %{_infodir}/dir 2>/dev/null ;
done
echo "Done."
if [ -f %{_infodir}/texinfo ]; then
  /sbin/install-info %{_infodir}/texinfo %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
  if [ -f %{_infodir}/texinfo ]; then
    /sbin/install-info --delete %{_infodir}/texinfo %{_infodir}/dir || :
  fi
fi

%post tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%postun tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%post -n info
if [ -f %{_infodir}/info-stnd.info ]; then
  /sbin/install-info %{_infodir}/info-stnd.info %{_infodir}/dir
fi
if [ -x /bin/sed ]; then
  /bin/sed -i '/^This is.*produced by makeinfo.*from/d' %{_infodir}/dir || :
fi

%preun -n info
if [ $1 = 0 ]; then
  if [ -f %{_infodir}/info-stnd.info ]; then
    /sbin/install-info --delete %{_infodir}/info-stnd.info %{_infodir}/dir || :
  fi
fi


%files
%defattr(-,root,root,-)
%doc ABOUT-NLS AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/makeinfo
%{_bindir}/pod2texi
%{_bindir}/texi2any
%{_datadir}/texinfo
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man1/pod2texi.1*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man5/texinfo.5*


%files tex
%defattr(-,root,root,-)
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/pdftexi2dvi
%{_mandir}/man1/texindex.1*
%{_mandir}/man1/texi2dvi.1*
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/pdftexi2dvi.1*
%{_datadir}/texmf/tex/texinfo/


%files -n info
%defattr(-,root,root,-)
%config(noreplace) %verify(not md5 size mtime) %{_infodir}/dir
%doc COPYING
%{_bindir}/info
%{_bindir}/infokey
%{_infodir}/info.info*
%{_infodir}/info-stnd.info*
/sbin/install-info
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*


%changelog
* Fri Jul 5 2024 The Model Citizen <model.citizen@ps3linux.net> 5.0-1
- Initial build for PS3 Fedora (Sackboy) on Cell/B.E. (www.ps3linux.net)

