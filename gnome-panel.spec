Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl):	Podstawowe programy ¶rodowiska graficznego GNOME
Name:		gnome-panel
Version:	2.15.91
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-panel/2.15/%{name}-%{version}.tar.bz2
# Source0-md5:	c65487c43ed633ceb026f9b98115114d
Patch0:		%{name}-finalize-memleak.patch
Patch1:		%{name}-no_launchers_on_panel.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.12.0
BuildRequires:	ORBit2-devel >= 1:2.14.2
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	evolution-data-server-devel >= 1.7.91
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gnome-doc-utils >= 0.7.2
BuildRequires:	gnome-desktop-devel >= 2.15.91
BuildRequires:	gnome-menus-devel >= 2.15.91
BuildRequires:	gnome-vfs2-devel >= 2.15.91
BuildRequires:	gtk+2-devel >= 2:2.10.1
BuildRequires:	gtk-doc >= 1.6
BuildRequires:	intltool >= 0.35
BuildRequires:	libart_lgpl-devel >= 2.3.15
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.15.91
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.15.91
BuildRequires:	pango-devel >= 1:1.13.5
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15.0
BuildRequires:	python-libxml2 >= 1:2.6.26
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper >= 0.3.11
BuildConflicts:	GConf-devel < 1.0.9-7
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	scrollkeeper
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hicolor-icon-theme
Requires:	gnome-desktop >= 2.15.91
Requires:	gnome-icon-theme >= 2.15.91
Requires:	xdg-menus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

The gnome-panel packages provides the GNOME panel, menus and some
basic applets for the panel.

%description -l pl
GNOME (GNU Network Object Model Environment) to zestaw przyjaznych dla
u¿ytkownika aplikacji i narzêdzi do u¿ywania w po³±czeniu z zarz±dc±
okien pod X. GNOME ma podobny cel jak CDE i KDE, ale bazuje ca³kowicie
na wolnym oprogramowaniu.

Ten pakiet dostarcza panel GNOME2, menu oraz podstawowe aplety dla
panelu GNOME2.

%package devel
Summary:	GNOME panel includes, and more
Summary(pl):	Pliki nag³ówkowe biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libgnomeui-devel >= 2.15.91

%description devel
Panel header files for creating GNOME panels.

%description devel -l pl
Pliki nag³ówkowe bibliotek panelu GNOME.

%package static
Summary:	GNOME panel static libraries
Summary(pl):	Statyczne biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Panel static libraries.

%description static -l pl
Statyczne biblioteki panelu GNOME.

%package libs
Summary:	GNOME panel library
Summary(pl):	Biblioteka panelu GNOME
Group:		X11/Libraries
Requires:	libgnomeui >= 2.15.91
Requires:	librsvg >= 1:2.15.90

%description libs
GNOME panel library.

%description libs -l pl
Biblioteka panelu GNOME.

%package apidocs
Summary:	panel-applet API documentation
Summary(pl):	Dokumentacja API panel-applet
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
panel-applet API documentation.

%description apidocs -l pl
Dokumentacja API panel-applet.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gnome_doc_prepare}
%{__gnome_doc_common}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
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

# short circuit stopper (fix me!)
mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/panel-default-setup.entries

%find_lang %{name} --with-gnome --all-name

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

%banner %{name} -e << EOF
For full functionality, you need to install
gnome-utils-screenshot and gnome-utils-search-tool.
EOF

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
%doc AUTHORS NEWS README *ChangeLog
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/clock-applet
%attr(755,root,root) %{_libdir}/fish-applet-2
%attr(755,root,root) %{_libdir}/notification-area-applet
%attr(755,root,root) %{_libdir}/wnck-applet
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/gnome-panel
%{_datadir}/gnome/panel
%{_datadir}/gnome-panelrc
%{_datadir}/idl/gnome-panel-2.0
%{_iconsdir}/*/*/apps/*
%{_libdir}/bonobo/servers/*
%{_mandir}/man1/*
%{_omf_dest_dir}/clock
%{_omf_dest_dir}/fish
%{_omf_dest_dir}/%{name}
%{_omf_dest_dir}/window-list
%{_omf_dest_dir}/workspace-switcher
%{_sysconfdir}/gconf/schemas/clock.schemas
%{_sysconfdir}/gconf/schemas/fish.schemas
%{_sysconfdir}/gconf/schemas/panel-compatibility.schemas
%{_sysconfdir}/gconf/schemas/panel-general.schemas
%{_sysconfdir}/gconf/schemas/panel-global.schemas
%{_sysconfdir}/gconf/schemas/panel-object.schemas
%{_sysconfdir}/gconf/schemas/panel-toplevel.schemas
%{_sysconfdir}/gconf/schemas/window-list.schemas
%{_sysconfdir}/gconf/schemas/workspace-switcher.schemas

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet*.so
%{_libdir}/*.la
%{_includedir}/panel-2.0
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet*.so.*.*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/panel-applet
