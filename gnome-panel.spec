Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl):	Podstawowe programy środowiska graficznego GNOME
Name:		gnome-panel
Version:	2.0.9
Release:	3
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/2.0.1/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0:		%{name}-clock-C_omf.patch
URL:		http://www.gnome.org/
BuildRequires:	ORBit2-devel >= 2.4.3
BuildRequires:	glib2-devel >= 2.0.6
BuildRequires:	gnome-desktop-devel >= 2.0.8
BuildRequires:  gtk-doc
BuildRequires:	gtk+2-devel >= 2.0.6
BuildRequires:	intltool >= 0.22
BuildRequires:	libglade2-devel >= 2.0.1
BuildRequires:	libgnomeui-devel >= 2.0.5
BuildRequires:	libwnck-devel >= 0.17
BuildRequires:	pkgconfig >= 0.12.0
BuildRequires:	scrollkeeper >= 0.3.11
Requires(post,postun): scrollkeeper
Requires(post,postun): /sbin/ldconfig
Requires(post):	GConf2
Requires:	gnome-desktop >= 2.0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/X11R6
%define         _mandir         %{_prefix}/man
%define         _sysconfdir     /etc/X11/GNOME2
%define		_gtkdocdir	%{_defaultdocdir}/gtk-doc/html
%define         _omf_dest_dir   %(scrollkeeper-config --omfdir)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

The GNOME panel packages provides the gnome panel, menus and some
basic applets for the panel.

%description -l pl
GNOME (GNU Network Object Model Environment) to zestaw przyjaznych
dla użytkownika aplikacji i narzędzi do używania w połączeniu z
zarządcą okien pod X. GNOME ma podobny cel jak CDE i KDE, ale bazuje
całkowicie na wolnym oprogramowaniu.

Ten pakiet dostarcza panel GNOME2, menu oraz podstawowe aplety dla
panelu GNOME2.

%package devel
Summary:	GNOME panel includes, and more
Summary(pl):	Pliki nagłówkowe biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	gtk-doc-common

%description devel
Panel header files for creating GNOME panels.

%description devel -l pl
Pliki nagłówkowe bibliotek panelu GNOME.

%package static
Summary:	GNOME panel static libraries
Summary(pl):	Statyczne biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-devel

%description static
Panel static libraries.

%description static -l pl
Statyczne biblioteki panelu GNOME.

%prep
%setup -q
%patch0 -p1

%build
intltoolize --copy --force
%{__libtoolize}
glib-gettextize --copy --force
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-path=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}/%{name} \
	pkgconfigdir=%{_pkgconfigdir} \
	HTML_DIR=%{_gtkdocdir}

mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
scrollkeeper-update
GCONF_CONFIG_SOURCE="`%{_bindir}/gconftool-2 --get-default-source`" \
%{_bindir}/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null 

%postun	
/sbin/ldconfig
scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS *ChangeLog NEWS README
%config %{_sysconfdir}/gconf/schemas/*
%config %{_sysconfdir}/sound/events/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/fish-applet-2
%attr(755,root,root) %{_libdir}/libpanel-applet*.so.*.*
%attr(755,root,root) %{_libdir}/libgen_util_applet*.so
%attr(755,root,root) %{_libdir}/libgen_util_applet*.la
%{_libdir}/bonobo/servers/*
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/gen_util
%{_datadir}/gnome/panel
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/gnome-panel*
%{_datadir}/idl/gnome-panel-2.0
%{_datadir}/pixmaps/*
%{_omf_dest_dir}/%{name}
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet*.??
%{_gtkdocdir}/panel-applet
%{_includedir}/panel-2.0
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
