#
# TODO
# - fix menu-stripe patch
#   (if nobody cares, it will be removed before 2.12.x)
#
# Conditional build:
%bcond_with     menu_stripe	# build with menu-stripe.patch
#
Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl):	Podstawowe programy ¶rodowiska graficznego GNOME
Name:		gnome-panel
Version:	2.11.90
Release:	3
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-panel/2.11/%{name}-%{version}.tar.bz2
# Source0-md5:	fbf0357b195fb9e2e925f18a3fd6f0b3
Source1:	pld-desktop-stripe.png
# Source1-md5:	4b8b299a8aa7b95a606e7c4d8debd60c
Patch0:		%{name}-finalize-memleak.patch
Patch1:		%{name}-menu-stripe.patch
Patch2:		%{name}-notification_area_applet.patch
Patch3:		%{name}-no_mixer_applet.patch
Patch4:		%{name}-no_launchers_on_panel.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	ORBit2-devel >= 1:2.12.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	evolution-data-server-devel >= 1.2.0
BuildRequires:	gnome-common >= 2.8.0-2
BuildRequires:	gnome-doc-utils >= 0.3.1-2
BuildRequires:	gnome-desktop-devel >= 2.10.0-2
BuildRequires:	gnome-menus-devel >= 2.11.1
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.7.1
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	intltool >= 0.31
BuildRequires:	libart_lgpl-devel >= 2.3.15
BuildRequires:	libglade2-devel >= 1:2.5.0
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.11.91
BuildRequires:	pango-devel >= 1:1.8.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15.0
BuildRequires:	python-libxml2
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper >= 0.3.11
BuildConflicts:	GConf-devel < 1.0.9-7
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	GConf2 >= 2.10.0
Requires(post,postun):	scrollkeeper
Requires:	gnome-desktop >= 2.10.0-2
Requires:	gnome-icon-theme >= 2.10.0
Requires:	gnome-session >= 2.11.90
Requires:	libgnomeui >= 2.10.0-2
Requires:	librsvg >= 1:2.9.5
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
Requires:	%{name} = %{version}-%{release}
Requires:	gtk-doc-common
Requires:	libgnomeui-devel >= 2.10.0-2

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

%prep
%setup -q
%patch0 -p1
%{?with_menu_stripe:%patch1 -p1}
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
gnome-doc-prepare --copy --force
%{__gnome_doc_common}
%{__intltoolize}
%{__libtoolize}
%{__glib_gettextize}
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

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}

# short circuit stopper (fix me!)
mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
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
/sbin/ldconfig
%scrollkeeper_update_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README *ChangeLog
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/clock-applet
%attr(755,root,root) %{_libdir}/fish-applet-2
%attr(755,root,root) %{_libdir}/libpanel-applet*.so.*.*
%attr(755,root,root) %{_libdir}/notification-area-applet
%attr(755,root,root) %{_libdir}/wnck-applet
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/gnome-panel
%{_datadir}/gnome/panel
%{_datadir}/gnome-panelrc
%{_datadir}/idl/gnome-panel-2.0
%{_iconsdir}/*/*/apps/*.png
%{_libdir}/bonobo/servers/*
%{_mandir}/man1/*
%{_omf_dest_dir}/clock
%{_omf_dest_dir}/fish
%{_omf_dest_dir}/%{name}
%{_omf_dest_dir}/window-list
%{_omf_dest_dir}/workspace-switcher
%{_pixmapsdir}/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet*.so
%{_libdir}/*.la
%{_gtkdocdir}/panel-applet
%{_includedir}/panel-2.0
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
