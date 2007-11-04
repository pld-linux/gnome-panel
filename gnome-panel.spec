Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Podstawowe programy środowiska graficznego GNOME
Name:		gnome-panel
Version:	2.20.1
Release:	2
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-panel/2.20/%{name}-%{version}.tar.bz2
# Source0-md5:	87ef96c2cbb8ecaa328420c0d31cc4c0
Patch0:		%{name}-finalize-memleak.patch
Patch1:		%{name}-no_launchers_on_panel.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.20.0
BuildRequires:	ORBit2-devel >= 1:2.14.9
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	evolution-data-server-devel >= 1.12.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-desktop-devel >= 2.20.0
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gnome-menus-devel >= 2.20.0
BuildRequires:	gnome-vfs2-devel >= 2.20.0
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	intltool >= 0.36.2
BuildRequires:	libart_lgpl-devel >= 2.3.19
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libgnomeui-devel >= 2.20.0
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.20.0
BuildRequires:	pango-devel >= 1:1.18.2
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15.0
BuildRequires:	python-libxml2 >= 1:2.6.30
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper >= 0.3.11
BuildConflicts:	GConf-devel < 1.0.9-7
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gnome-desktop >= 2.20.0
Requires:	gnome-icon-theme >= 2.20.0
Requires:	xdg-menus
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
Requires:	libgnomeui >= 2.20.0
Requires:	librsvg >= 1:2.18.1

%description libs
GNOME panel library.

%description libs -l pl.UTF-8
Biblioteka panelu GNOME.

%package devel
Summary:	GNOME panel includes, and more
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libgnomeui-devel >= 2.20.0

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

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
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
%attr(755,root,root) %{_libdir}/notification-area-applet
%attr(755,root,root) %{_libdir}/wnck-applet
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/gnome-panel
%{_datadir}/gnome-panelrc
%{_datadir}/idl/gnome-panel-2.0
%{_desktopdir}/gnome-panel.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_libdir}/bonobo/servers/*
%{_mandir}/man1/*
%{_sysconfdir}/gconf/schemas/clock.schemas
%{_sysconfdir}/gconf/schemas/fish.schemas
%{_sysconfdir}/gconf/schemas/panel-compatibility.schemas
%{_sysconfdir}/gconf/schemas/panel-general.schemas
%{_sysconfdir}/gconf/schemas/panel-global.schemas
%{_sysconfdir}/gconf/schemas/panel-object.schemas
%{_sysconfdir}/gconf/schemas/panel-toplevel.schemas
%{_sysconfdir}/gconf/schemas/window-list.schemas
%{_sysconfdir}/gconf/schemas/workspace-switcher.schemas
%dir %{_omf_dest_dir}/clock
%{_omf_dest_dir}/clock/clock-C.omf
%lang(ca) %{_omf_dest_dir}/clock/clock-ca.omf
%lang(de) %{_omf_dest_dir}/clock/clock-de.omf
%lang(el) %{_omf_dest_dir}/clock/clock-el.omf
%lang(es) %{_omf_dest_dir}/clock/clock-es.omf
%lang(fr) %{_omf_dest_dir}/clock/clock-fr.omf
%lang(it) %{_omf_dest_dir}/clock/clock-it.omf
%lang(ja) %{_omf_dest_dir}/clock/clock-ja.omf
%lang(ko) %{_omf_dest_dir}/clock/clock-ko.omf
%lang(nl) %{_omf_dest_dir}/clock/clock-nl.omf
%lang(oc) %{_omf_dest_dir}/clock/clock-oc.omf
%lang(pa) %{_omf_dest_dir}/clock/clock-pa.omf
%lang(ru) %{_omf_dest_dir}/clock/clock-ru.omf
%lang(sr) %{_omf_dest_dir}/clock/clock-sr.omf
%lang(sv) %{_omf_dest_dir}/clock/clock-sv.omf
%lang(uk) %{_omf_dest_dir}/clock/clock-uk.omf
%lang(zh_CN) %{_omf_dest_dir}/clock/clock-zh_CN.omf
%lang(zh_TW) %{_omf_dest_dir}/clock/clock-zh_TW.omf
%dir %{_omf_dest_dir}/fish
%{_omf_dest_dir}/fish/fish-C.omf
%lang(ca) %{_omf_dest_dir}/fish/fish-ca.omf
%lang(el) %{_omf_dest_dir}/fish/fish-el.omf
%lang(es) %{_omf_dest_dir}/fish/fish-es.omf
%lang(fr) %{_omf_dest_dir}/fish/fish-fr.omf
%lang(it) %{_omf_dest_dir}/fish/fish-it.omf
%lang(ko) %{_omf_dest_dir}/fish/fish-ko.omf
%lang(oc) %{_omf_dest_dir}/fish/fish-oc.omf
%lang(sv) %{_omf_dest_dir}/fish/fish-sv.omf
%lang(uk) %{_omf_dest_dir}/fish/fish-uk.omf
%dir %{_omf_dest_dir}/gnome-panel
%lang(de) %{_omf_dest_dir}/gnome-panel/fish-applet-2-de.omf
%lang(ja) %{_omf_dest_dir}/gnome-panel/fish-applet-2-ja.omf
%lang(zh_CN) %{_omf_dest_dir}/gnome-panel/fish-applet-2-zh_CN.omf
%lang(zh_TW) %{_omf_dest_dir}/gnome-panel/fish-applet-2-zh_TW.omf
%lang(de) %{_omf_dest_dir}/gnome-panel/window-list-de.omf
%lang(ja) %{_omf_dest_dir}/gnome-panel/window-list-ja.omf
%lang(zh_TW) %{_omf_dest_dir}/gnome-panel/window-list-zh_TW.omf
%lang(de) %{_omf_dest_dir}/gnome-panel/workspace-switcher-de.omf
%lang(ja) %{_omf_dest_dir}/gnome-panel/workspace-switcher-ja.omf
%lang(zh_CN) %{_omf_dest_dir}/gnome-panel/workspace-switcher-zh_CN.omf
%lang(zh_TW) %{_omf_dest_dir}/gnome-panel/workspace-switcher-zh_TW.omf
%dir %{_omf_dest_dir}/window-list
%{_omf_dest_dir}/window-list/window-list-C.omf
%lang(ca) %{_omf_dest_dir}/window-list/window-list-ca.omf
%lang(de) %{_omf_dest_dir}/window-list/window-list-de.omf
%lang(el) %{_omf_dest_dir}/window-list/window-list-el.omf
%lang(es) %{_omf_dest_dir}/window-list/window-list-es.omf
%lang(fr) %{_omf_dest_dir}/window-list/window-list-fr.omf
%lang(it) %{_omf_dest_dir}/window-list/window-list-it.omf
%lang(ko) %{_omf_dest_dir}/window-list/window-list-ko.omf
%lang(oc) %{_omf_dest_dir}/window-list/window-list-oc.omf
%lang(pa) %{_omf_dest_dir}/window-list/window-list-pa.omf
%lang(ru) %{_omf_dest_dir}/window-list/window-list-ru.omf
%lang(sv) %{_omf_dest_dir}/window-list/window-list-sv.omf
%lang(uk) %{_omf_dest_dir}/window-list/window-list-uk.omf
%lang(zh_CN) %{_omf_dest_dir}/window-list/window-list-zh_CN.omf
%dir %{_omf_dest_dir}/workspace-switcher
%{_omf_dest_dir}/workspace-switcher/workspace-switcher-C.omf
%lang(ca) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-ca.omf
%lang(de) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-de.omf
%lang(el) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-el.omf
%lang(es) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-es.omf
%lang(fr) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-fr.omf
%lang(it) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-it.omf
%lang(ko) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-ko.omf
%lang(nl) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-nl.omf
%lang(oc) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-oc.omf
%lang(pa) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-pa.omf
%lang(ru) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-ru.omf
%lang(sv) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-sv.omf
%lang(uk) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-uk.omf
%lang(vi) %{_omf_dest_dir}/workspace-switcher/workspace-switcher-vi.omf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpanel-applet-2.so.*.*.*

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
