# TODO:
# - NetworkManager bcond
#
Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Podstawowe programy środowiska graficznego GNOME
Name:		gnome-panel
Version:	2.23.1
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-panel/2.23/%{name}-%{version}.tar.bz2
# Source0-md5:	315e85cbd56c838d538fefe7f4aa9868
Patch0:		%{name}-no_launchers_on_panel.patch
Patch1:		%{name}-use-sysconfig-timezone.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.22.0
BuildRequires:	NetworkManager-devel >= 0.6
BuildRequires:	ORBit2-devel >= 1:2.14.9
BuildRequires:	PolicyKit-gnome-devel >= 0.7
BuildRequires:	autoconf
BuildRequires:	automake > 1:1.9
BuildRequires:	dbus-devel >= 1.1.2
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	evolution-data-server-devel >= 2.22.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-desktop-devel >= 2.22.0
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gnome-menus-devel >= 2.22.0
BuildRequires:	gtk+2-devel >= 2:2.12.5
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.37.0
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libgnomeui-devel >= 2.22.0
BuildRequires:	libgweather-devel >= 2.22.1.1
BuildRequires:	librsvg-devel >= 2.18.2
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.22.0
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15.0
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper >= 0.3.11
BuildRequires:	sed >= 4.0
BuildConflicts:	GConf-devel < 1.0.9-7
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gnome-desktop >= 2.22.0
Requires:	gnome-icon-theme >= 2.22.0
Requires:	tzdata >= 2008b-4
Requires:	xdg-menus
Suggests:	PolicyKit-gnome >= 0.7
Suggests:	gnome-utils-screenshot
Suggests:	gnome-utils-search-tool
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
Requires:	libgnomeui >= 2.22.0
Requires:	librsvg >= 1:2.18.2

%description libs
GNOME panel library.

%description libs -l pl.UTF-8
Biblioteka panelu GNOME.

%package devel
Summary:	GNOME panel includes, and more
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libgnomeui-devel >= 2.22.0

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

sed -i -e 's#sr@Latn#sr@latin#' po/LINGUAS
mv po/sr@{Latn,latin}.po

# short circuit stopper (fix me!)
mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%build
%{__gnome_doc_prepare}
%{__gnome_doc_common}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-install \
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

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/panel-default-setup.entries

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ps

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
%attr(755,root,root) %{_libdir}/clock-applet
%attr(755,root,root) %{_libdir}/fish-applet-2
%attr(755,root,root) %{_libdir}/gnome-clock-applet-mechanism
%attr(755,root,root) %{_libdir}/notification-area-applet
%attr(755,root,root) %{_libdir}/wnck-applet
%{_datadir}/PolicyKit/policy/org.gnome.clockapplet.mechanism.policy
%{_datadir}/dbus-1/system-services/org.gnome.ClockApplet.Mechanism.service
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/gnome-panel
%{_datadir}/gnome-panelrc
%{_datadir}/idl/gnome-panel-2.0
%{_desktopdir}/gnome-panel.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_libdir}/bonobo/servers/*.server
%{_mandir}/man1/*.1*
%{_sysconfdir}/dbus-1/system.d/org.gnome.ClockApplet.Mechanism.conf
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

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet-2.so
%{_libdir}/libpanel-applet-2.la
%{_includedir}/panel-2.0
%{_pkgconfigdir}/libpanelapplet-2.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpanel-applet-2.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/panel-applet
