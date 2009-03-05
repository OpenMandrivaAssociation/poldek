%define name poldek
%define major 0

%define libname %mklibname %name %major
%define develname %mklibname %name -d

Summary:	PLD RPM packages management helper tool
Name:		%name
Version:	0.20
Release:	%mkrel 55562
License:	GPLv2
Group:		System/Configuration/Packaging
URL:		http://poldek.pld-linux.org/
Source0:	http://poldek.pld-linux.org/download/%{name}-%{version}.tar.bz2
Patch0:     poldek-0.20-oldtag.patch
Patch1:     poldek-0.20-sourcepackage.patch
Patch2:     poldek-rpm-4.4.8.patch
Patch3:     poldek-0.20-fix-rpmlib-detection.patch
Patch4:     poldek-0.20-fix-check-detection.patch
Patch5:     poldek-0.20-fix-format-errors.patch
Patch6:     poldek-0.20-fix-underlinking.patch
Patch7:     poldek-0.20-add-missing-header.patch
Patch8:     poldek-0.20-rpm-4.6-compatibility.patch
BuildRequires:	bzip2-devel
BuildRequires:	rpm-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	pcre-devel
BuildRequires:  ncurses-devel
BuildRequires:  db4-devel
BuildRequires:	gettext-devel
BuildRequires:	libxml2-devel
BuildRoot:	%_tmppath/%name-%version-%release-root

%description
poldek is an RPM package management tool which allows you to easily
perform package verification, installation (including system
installation from scratch), upgrading, and removal. 

Program can be used in batch (like apt-get from Debian's
APT) or interactive mode. The interactive mode puts you into a
readline interface with command line autocompletion and history,
similar to the shell mode of Perl's CPAN.

%package -n %libname
Summary: Library from poldek
Group: System/Libraries
Provides: lib%name = %version-%release

%description -n %libname
poldek is an RPM package management tool which allows you to easily
perform package verification, installation (including system
installation from scratch), upgrading, and removal.

This package contain libraries from poldek

%package -n %develname
Summary: Development files from poldek
Group: Development/Other
Provides: %name-devel = %version-%release
Obsoletes:  develname %mklibname %name -d 0
Requires: %libname = %version-%release

%description -n %develname
poldek is an RPM package management tool which allows you to easily
perform package verification, installation (including system
installation from scratch), upgrading, and removal.

This package contain development files need to build programs using
poldek library.

%prep 
%setup -q
%patch0 -p0 -b .oldtag~
%patch1 -p0 -b .sourcepackage~
%patch2 -p0 -b .rpm-448~
%patch3 -p1 -b .rpmlib~
%patch4 -p1 -b .check~
%patch5 -p1 -b .format~
%patch6 -p1 -b .link~
%patch7 -p1 -b .header~
%patch8 -p1 -b .rpm46~

%build
autoreconf -f -i
%configure2_5x %{?_with_static:--enable-static}
echo "#define _RPM_4_4_COMPAT 1" >> config.h
%make

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_sysconfdir}

%{__make} install DESTDIR=%{buildroot}

perl -pi -e 's/_distro\s+=\s+pld/_distro = %_vendor/' %buildroot/%_sysconfdir/%name/%name.conf

cat > %buildroot/%_sysconfdir/%name/%_vendor-source.conf <<EOF

# Your mandriva version
_mdv_version = %mandriva_release
# Your 
_mdv_arch = %mandriva_arch

# Setup path to repository
#_prefix = ftp://server/.../MandrivaLinux/devel

[source]
name   = main
type   = hdrl
url    = %{_prefix}/%{_mdv_version}/%{_mdv_arch}/media/main/media_info/hdlist.cz
prefix = %{_prefix}/%{_mdv_version}/%{_mdv_arch}/media/main

[source]
name   = contrib
type   = hdrl
url    = %{_prefix}/%{_mdv_version}/%{_mdv_arch}/media/contrib/media_info/hdlist.cz
prefix = %{_prefix}/%{_mdv_version}/%{_mdv_arch}/media/contrib

#[source]
#name   = jpackage
#type   = hdrl
#url    = %{_prefix}/%{_mdv_version}/%{_mdv_arch}/media/jpackage/media_info/hdlist.cz
#prefix = %{_prefix}/%{_mdv_version}/%{_mdv_arch}/media/jpackage

EOF

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%_install_info %name.info

%postun
%_remove_install_info %name.info

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc README* *sample* NEWS TODO
%dir %{_sysconfdir}/%{name}
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/%{name}*
%{_mandir}/pl/man1/%{name}*
%{_infodir}/poldek.*

%files -n %libname
%defattr(-,root,root)
%doc README* *sample* NEWS TODO
%_libdir/*.so.*
%_libdir/poldek

%files -n %develname
%defattr(-,root,root)
%doc README* *sample* NEWS TODO
%_includedir/*
%_libdir/*.a
%_libdir/*.la
%_libdir/*.so
