Summary:	The core programs for the GNOME GUI desktop environment
Summary(pl):	Podstawowe programy ¶rodowiska graficznego GNOME
Name:		gnome-panel
Version:	2.3.4.1
Release:	2
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.3/%{name}-%{version}.tar.bz2
# Source0-md5:	dc7f01f874633f9c9eab4a7c9edbd6e5
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.3.0
BuildRequires:	ORBit2-devel >= 2.7.5-1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.2.0
BuildRequires:	gnome-common >= 1.2.4
BuildRequires:	gnome-desktop-devel >= 2.3.4-2
BuildRequires:	gtk+2-devel >= 2.2.0
BuildRequires:  gtk-doc >= 1.0
BuildRequires:	intltool >= 0.23
BuildRequires:	libart_lgpl-devel >= 2.3.11
BuildRequires:	libglade2-devel >= 2.0.1
BuildRequires:	libgnomeui-devel >= 2.3.3.1-2
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.3.0
BuildRequires:	pkgconfig >= 0.12.0
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper >= 0.3.11
BuildConflicts:	GConf-devel < 1.0.9-7
Requires(post,postun): /sbin/ldconfig
Requires(post,postun): scrollkeeper
Requires(post):	GConf2 >= 2.3.0
Requires:	gnome-desktop >= 2.3.4-2
Requires:	libgnomeui >= 2.3.3.1-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

The GNOME panel packages provides the gnome panel, menus and some
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
Requires:	%{name} = %{version}
Requires:	libgnomeui-devel >= 2.3.3.1-2
Requires:	gtk-doc-common

%description devel
Panel header files for creating GNOME panels.

%description devel -l pl
Pliki nag³ówkowe bibliotek panelu GNOME.

%package static
Summary:	GNOME panel static libraries
Summary(pl):	Statyczne biblioteki panelu GNOME
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Panel static libraries.

%description static -l pl
Statyczne biblioteki panelu GNOME.

%prep
%setup -q

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
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT 

install %{name}/panel-default-setup.entries $RPM_BUILD_ROOT%{_datadir}/%{name}

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
%attr(755,root,root) %{_libdir}/libclock-applet*.so
%attr(755,root,root) %{_libdir}/wnck-applet
%attr(755,root,root) %{_libdir}/notification-area-applet
%{_libdir}/bonobo/servers/*
%{_datadir}/control-center-2.0/capplets/*
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
