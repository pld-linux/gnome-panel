Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl):	Podstawowe programy ¶rodowiska graficznego GNOME
Name:		gnome-panel
Version:	2.6.0
Release:	0.1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.6/%{name}-%{version}.tar.bz2
# Source0-md5:	9e0ad03c9266d342b99837ca4e947b55
Source1:	pld-desktop-stripe.png
# Source1-md5:	4b8b299a8aa7b95a606e7c4d8debd60c
Patch0:		%{name}-no_launchers_on_panel.patch
Patch1:		%{name}-finalize-memleak.patch
Patch2:		%{name}-locale-names.patch
#Patch3:		%{name}-menu-stripe.patch
Patch4:		%{name}-notification_area_applet.patch
Patch5:		%{name}-applet-categories.patch
Patch6:		%{name}-schemas.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.5.90
BuildRequires:	ORBit2-devel >= 1:2.10.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	evolution-data-server-devel >= 0.0.90
BuildRequires:	gnome-common >= 2.4.0
BuildRequires:	gnome-desktop-devel >= 2.6.0
BuildRequires:	gnome-vfs2-devel >= 2.6.0
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	intltool >= 0.29
BuildRequires:	libart_lgpl-devel >= 2.3.15
BuildRequires:	libglade2-devel >= 1:2.3.6
BuildRequires:	libgnomeui-devel >= 2.6.0
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.6.0
BuildRequires:	pango-devel >= 1.4.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 0.15.0
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper >= 0.3.11
BuildRequires:	zlib-devel
BuildConflicts:	GConf-devel < 1.0.9-7
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	scrollkeeper
Requires(post):	GConf2 >= 2.5.90
Requires:	gnome-desktop >= 2.6.0
Requires:	gnome-icon-theme >= 1.2.0
Requires:	libgnomeui >= 2.6.0
Requires:	librsvg >= 2.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

The gnome-panel packages provides the GNOME panel, menus and some
basic applets for the panel.

%description -l pl
GNOME (GNU Network Object Model Environment) to zestaw przyjaznych
dla u¿ytkownika aplikacji i narzêdzi do u¿ywania w po³±czeniu z
zarz±dc± okien pod X. GNOME ma podobny cel jak CDE i KDE, ale bazuje
ca³kowicie na wolnym oprogramowaniu.

Ten pakiet dostarcza panel GNOME2, menu oraz podstawowe aplety dla
panelu GNOME2.

%package devel
Summary:	GNOME panel includes, and more
Summary(pl):	Pliki nag³ówkowe biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk-doc-common
Requires:	libgnomeui-devel >= 2.6.0

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
%patch1 -p1
%patch2 -p1
##%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

mv po/{no,nb}.po

%build
intltoolize --copy --force
%{__libtoolize}
glib-gettextize --copy --force
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--enable-eds \
	--disable-schemas-install

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

install %{name}/panel-default-setup.entries $RPM_BUILD_ROOT%{_datadir}/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}

install -d $RPM_BUILD_ROOT%{_datadir}/gnome/capplets
mv $RPM_BUILD_ROOT%{_datadir}/control-center-2.0/capplets/*.desktop $RPM_BUILD_ROOT%{_datadir}/gnome/capplets

mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
scrollkeeper-update
%gconf_schema_install
%{_bindir}/gconftool-2 --direct \
--config-source="`%{_bindir}/gconftool-2 --get-default-source`" \
--load %{_datadir}/%{name}/panel-default-setup.entries > /dev/null

%postun
/sbin/ldconfig
scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README *ChangeLog
%config %{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/fish-applet-2
%attr(755,root,root) %{_libdir}/libpanel-applet*.so.*.*
%attr(755,root,root) %{_libdir}/clock-applet
%attr(755,root,root) %{_libdir}/wnck-applet
%attr(755,root,root) %{_libdir}/notification-area-applet
%{_libdir}/bonobo/servers/*
%{_datadir}/gnome/capplets/*
%{_datadir}/gnome/panel
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/gnome-panel
%{_datadir}/gnome-panelrc
%{_datadir}/idl/gnome-panel-2.0
%{_pixmapsdir}/*
%{_omf_dest_dir}/%{name}
%{_mandir}/man1/*

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
