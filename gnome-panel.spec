Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Podstawowe programy środowiska graficznego GNOME
Name:		gnome-panel
Version:	2.32.1
Release:	2
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-panel/2.32/%{name}-%{version}.tar.bz2
# Source0-md5:	a228035e1f7026abf296b797f1f7d2f9
Patch0:		%{name}-no_launchers_on_panel.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=552049
Patch1:		%{name}-use-sysconfig-timezone.patch
Patch2:		%{name}-link.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.26.0
BuildRequires:	NetworkManager-devel >= 0.6
BuildRequires:	ORBit2-devel >= 1:2.14.9
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.1.2
BuildRequires:	dbus-glib-devel >= 0.80
BuildRequires:	docbook-dtd412-xml
BuildRequires:	evolution-data-server-devel >= 2.24.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-desktop-devel >= 2.30.0
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gnome-menus-devel >= 2.30.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libbonoboui-devel >= 2.24.0
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libgweather-devel >= 2.28.0
BuildRequires:	librsvg-devel >= 2.22.0
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.26.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15.0
BuildRequires:	polkit-gnome-devel >= 0.93
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper >= 0.3.11
BuildRequires:	xorg-lib-libSM-devel
BuildConflicts:	GConf-devel < 1.0.9-7
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gnome-desktop >= 2.30.0
Requires:	gnome-icon-theme >= 2.28.0
Requires:	tzdata >= 2008b-4
Requires:	xdg-menus
Suggests:	gnome-utils-screenshot
Suggests:	gnome-utils-search-tool
Suggests:	polkit-gnome >= 0.93
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

The gnome-panel packages provides the GNOME panel, menus and some
basic applets for the panel.

%description -l pl.UTF-8
GNOME (GNU Network Object Model Environment) to zestaw przyjaznych dla
użytkownika aplikacji i narzędzi do używania w połączeniu z zarządcą
okien pod X. GNOME ma podobny cel jak CDE i KDE, ale bazuje całkowicie
na wolnym oprogramowaniu.

Ten pakiet dostarcza panel GNOME2, menu oraz podstawowe aplety dla
panelu GNOME2.

%package libs
Summary:	GNOME panel library
Summary(pl.UTF-8):	Biblioteka panelu GNOME
Group:		X11/Libraries
Requires:	librsvg >= 1:2.22.0

%description libs
GNOME panel library.

%description libs -l pl.UTF-8
Biblioteka panelu GNOME.

%package devel
Summary:	GNOME panel includes, and more
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	GConf2-devel >= 2.26.0
Requires:	gtk+2-devel >= 2:2.20.0
Requires:	libbonoboui-devel >= 2.24.0

%description devel
Panel header files for creating GNOME panels.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek panelu GNOME.

%package static
Summary:	GNOME panel static libraries
Summary(pl.UTF-8):	Statyczne biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Panel static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki panelu GNOME.

%package apidocs
Summary:	panel-applet API documentation
Summary(pl.UTF-8):	Dokumentacja API panel-applet
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
panel-applet API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API panel-applet.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

# short circuit stopper (fix me!)
mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%build
%{__gtkdocize}
%{__gnome_doc_prepare}
%{__gnome_doc_common}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-install \
	--disable-silent-rules \
	--enable-eds \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_datadir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

install %{name}/panel-default-setup.entries $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/panel-default-setup.entries
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gnome-panel/modules/*.{a,la}

%find_lang %{name} --with-gnome --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%gconf_schema_install clock.schemas
%gconf_schema_install fish.schemas
%gconf_schema_install panel-compatibility.schemas
%gconf_schema_install panel-general.schemas
%gconf_schema_install panel-global.schemas
%gconf_schema_install panel-object.schemas
%gconf_schema_install panel-toplevel.schemas
%gconf_schema_install window-list.schemas
%gconf_schema_install workspace-switcher.schemas
%update_icon_cache hicolor

%{_bindir}/gconftool-2 --direct \
	--config-source="`%{_bindir}/gconftool-2 --get-default-source`" \
	--load %{_datadir}/%{name}/panel-default-setup.entries > /dev/null
%{_bindir}/gconftool-2 --direct \
	--config-source="`%{_bindir}/gconftool-2 --get-default-source`" \
	--load %{_datadir}/%{name}/panel-default-setup.entries /apps/panel/profiles/default > /dev/null

%preun
%gconf_schema_uninstall clock.schemas
%gconf_schema_uninstall fish.schemas
%gconf_schema_uninstall panel-compatibility.schemas
%gconf_schema_uninstall panel-general.schemas
%gconf_schema_uninstall panel-global.schemas
%gconf_schema_uninstall panel-object.schemas
%gconf_schema_uninstall panel-toplevel.schemas
%gconf_schema_uninstall window-list.schemas
%gconf_schema_uninstall workspace-switcher.schemas

%postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README *ChangeLog
%attr(755,root,root) %{_bindir}/gnome-desktop-item-edit
%attr(755,root,root) %{_bindir}/gnome-panel
%attr(755,root,root) %{_bindir}/panel-test-applets
%attr(755,root,root) %{_bindir}/panel-test-applets-bonobo
%attr(755,root,root) %{_libexecdir}/clock-applet
%attr(755,root,root) %{_libexecdir}/fish-applet
%attr(755,root,root) %{_libexecdir}/gnome-panel-add
%attr(755,root,root) %{_libexecdir}/notification-area-applet
%attr(755,root,root) %{_libexecdir}/wnck-applet
%dir %{_libdir}/gnome-panel
%dir %{_libdir}/gnome-panel/modules
%{_libdir}/gnome-panel/modules/libpanel-applets-bonobo.so
%{_datadir}/dbus-1/services/org.gnome.panel.applet.ClockAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.FishAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.NotificationAreaAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.WnckletFactory.service
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/gnome-panel
%{_datadir}/gnome-panelrc
%{_datadir}/idl/gnome-panel-2.0
%{_desktopdir}/gnome-panel.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/*.1*
%{_sysconfdir}/gconf/schemas/clock.schemas
%{_sysconfdir}/gconf/schemas/fish.schemas
%{_sysconfdir}/gconf/schemas/panel-compatibility.schemas
%{_sysconfdir}/gconf/schemas/panel-general.schemas
%{_sysconfdir}/gconf/schemas/panel-global.schemas
%{_sysconfdir}/gconf/schemas/panel-object.schemas
%{_sysconfdir}/gconf/schemas/panel-toplevel.schemas
%{_sysconfdir}/gconf/schemas/window-list.schemas
%{_sysconfdir}/gconf/schemas/workspace-switcher.schemas

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpanel-applet-2.so.0
%attr(755,root,root) %{_libdir}/libpanel-applet-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpanel-applet-3.so.0
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet-2.so
%attr(755,root,root) %{_libdir}/libpanel-applet-3.so
%{_includedir}/panel-2.0
%{_includedir}/gnome-panel-3.0
%{_pkgconfigdir}/libpanelapplet-2.0.pc
%{_pkgconfigdir}/libpanelapplet-3.0.pc
%{_datadir}/gir-1.0/*.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libpanel-applet-2.a
%{_libdir}/libpanel-applet-2.la
%{_libdir}/libpanel-applet-3.a
%{_libdir}/libpanel-applet-3.la

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/panel-applet
