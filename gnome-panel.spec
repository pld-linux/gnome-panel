#
# Conditional build:
%bcond_without	apidocs	# gtk-doc documentation rebuild
#
Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Podstawowe programy środowiska graficznego GNOME
Name:		gnome-panel
Version:	3.34.1
Release:	2
License:	LGPL v2+ (library), GPL v2+ (the rest)
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-panel/3.34/%{name}-%{version}.tar.xz
# Source0-md5:	cfd5d3fd548a2afdd8bd3bbdf9646bbd
URL:		https://wiki.gnome.org/Projects/GnomePanel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.13
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	dconf-devel >= 0.14.0
BuildRequires:	docbook-dtd412-xml
BuildRequires:	evolution-data-server-devel >= 3.33.2
BuildRequires:	gdk-pixbuf2-devel >= 2.26.0
BuildRequires:	gdm-devel >= 3
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.45.3
BuildRequires:	gnome-desktop-devel >= 3.4.0
BuildRequires:	gnome-menus-devel >= 3.8.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.22.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.25}
BuildRequires:	libgweather-devel >= 3.28.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libwnck-devel >= 3.4.6
BuildRequires:	pango-devel >= 1:1.15.4
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15.0
BuildRequires:	polkit-devel
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	systemd-devel >= 1:230
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3.0
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.45.3
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dconf >= 0.14.0
Requires:	gdk-pixbuf2 >= 2.26.0
Requires:	gnome-desktop >= 3.4.0
Requires:	gnome-icon-theme >= 3.0.0
Requires:	gnome-menus >= 3.8.0
Requires:	hicolor-icon-theme
Requires:	libgweather >= 3.28.0
Requires:	libwnck >= 3.4.6
Requires:	pango >= 1:1.15.4
Requires:	systemd-libs >= 1:230
Requires:	tzdata >= 2008b-4
Requires:	xdg-menus
Requires:	xorg-lib-libXrandr >= 1.3.0
Suggests:	evolution-data-server >= 3.33.2
Suggests:	gnome-screenshot
Suggests:	gnome-search-tool
Suggests:	polkit-gnome >= 0.93
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
Requires:	cairo >= 1.0.0
Requires:	glib2 >= 1:2.45.3
Requires:	gtk+3 >= 3.22.0

%description libs
GNOME panel library.

%description libs -l pl.UTF-8
Biblioteka panelu GNOME.

%package devel
Summary:	GNOME panel includes, and more
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.45.3
Requires:	gtk+3-devel >= 3.22.0

%description devel
Panel header files for creating GNOME panels.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek panelu GNOME.

%package apidocs
Summary:	panel-applet API documentation
Summary(pl.UTF-8):	Dokumentacja API panel-applet
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
panel-applet API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API panel-applet.

%prep
%setup -q

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-eds \
	%{?with_apidocs:--enable-gtk-doc} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpanel-applet.la \
	$RPM_BUILD_ROOT%{_libdir}/gnome-panel/modules/*.la

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr@ije,sr@ijekavian}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md ChangeLog
%attr(755,root,root) %{_bindir}/gnome-panel
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%attr(755,root,root) %{_libdir}/%{name}/modules/clock.so
%attr(755,root,root) %{_libdir}/%{name}/modules/fish.so
%attr(755,root,root) %{_libdir}/%{name}/modules/menu.so
%attr(755,root,root) %{_libdir}/%{name}/modules/notification-area.so
%attr(755,root,root) %{_libdir}/%{name}/modules/separator.so
%attr(755,root,root) %{_libdir}/%{name}/modules/status-notifier.so
%attr(755,root,root) %{_libdir}/%{name}/modules/wncklet.so
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.clock.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.fish.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.initial-settings.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.menu-button.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.window-list.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.applet.workspace-switcher.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.launcher.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.object.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-panel.toplevel.gschema.xml
%{_datadir}/gnome-panel
%{_desktopdir}/gnome-panel.desktop
%{_iconsdir}/hicolor/*x*/apps/gnome-panel*.png
%{_iconsdir}/hicolor/scalable/apps/gnome-panel*.svg
%{_mandir}/man1/gnome-panel.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpanel-applet.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet.so
%{_includedir}/gnome-panel
%{_pkgconfigdir}/libpanel-applet.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libpanel-applet
