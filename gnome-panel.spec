Summary:	The core programs for the GNOME GUI desktop environment.
Name:		gnome-panel
Version:	1.5.18
Release:	0.1
License:	LGPL
Group:		X11/Applications
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
URL:		http://www.gnome.org/
BuildRequires:	pkgconfig
BuildRequires:	ORBit2-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libwnck-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	libglade2-devel
BuildRequires:	gnome-vfs2-devel

%define         _prefix         /usr/X11R6
%define         _mandir         %{_prefix}/man
%define         _sysconfdir     /etc/X11/GNOME2
%define         _omf_dest_dir   %(scrollkeeper-config --omfdir)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software. The
gnome-core package includes the basic programs and libraries that are
needed to install GNOME.

The GNOME panel packages provides the gnome panel, menu's and some
basic applets for the panel.

%package devel
Summary:	GNOME panel libraries, includes, and more.
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Panel libraries and header files for creating GNOME panels.

%package static
Summary:	GNOME panel libraries, includes, and more.
Group:		Development/Libraries
Requires:	%{name} = %{version}-devel

%description static
Panel libraries and header files for creating GNOME panels.

%prep
%setup -q

%build
if [ -f %{_pkgconfigdir}/libpng12.pc ] ; then
        CPPFLAGS="`pkg-config libpng12 --cflags`"
fi

%configure \
	--enable-gtk-doc=no
%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}/%{name} \
	pkgconfigdir=%{_pkgconfigdir}

gzip -9nf AUTHORS ChangeLog NEWS README

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
for SCHEMAS in clock.schemas fish.schemas mailcheck.schemas pager.schemas panel-global-config.schemas panel-per-panel-config.schemas tasklist.schemas; do
	/usr/X11R6/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$SCHEMAS > /dev/null 2>&1
done

%postun
/sbin/ldconfig
/usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%config %{_sysconfdir}/gconf/schemas/*
%config %{_sysconfdir}/sound/events/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/bonobo/servers/*
%{_datadir}/applications/*
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/gen_util
%{_datadir}/gnome/panel
%{_datadir}/gnome-2.0
%{_datadir}/gnome-panel
%{_datadir}/gtk-doc/html/panel-applet
%{_datadir}/idl/gnome-panel-2.0
%{_datadir}/pixmaps/fish
%{_datadir}/pixmaps/mailcheck
%{_datadir}/pixmaps/*.png
%{_omf_dest_dir}/%{name}
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.??
%{_includedir}/panel-2.0
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
