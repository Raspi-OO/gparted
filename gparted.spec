Summary:	Gnome Partition Editor
Name:		gparted
Version:	1.1.0
Release:	1
License:	GPLv2+
URL:		http://gparted.org
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:	gtkmm30-devel
BuildRequires:	parted-devel
BuildRequires:	libuuid-devel
BuildRequires:	gettext
BuildRequires:	perl(XML::Parser)
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	polkit
BuildRequires:	libappstream-glib
BuildRequires:	itstool
BuildRequires:	gcc-c++

Requires:	PolicyKit-authentication-agent

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to
libparted. Among other features it supports creating, resizing, moving
and copying of partitions. Also several (optional) filesystem tools provide
support for filesystems not included in libparted. These optional packages
will be detected at runtime and don't require a rebuild of GParted

%prep
%setup -q

%build
%configure --enable-libparted-dmraid --enable-online-resize --enable-xhost-root
%make_build

%install
%make_install

sed -i 's#_X-GNOME-FullName#X-GNOME-FullName#' %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i 's#sbin#bin#' %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install --delete-original			\
	--dir %{buildroot}%{_datadir}/applications	\
	--mode 0644					\
	--add-category X-Fedora				\
	--add-category GTK				\
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# install appdata file
mkdir -p %{buildroot}%{_datadir}/metainfo
%{__install} -p -m755 %{name}.appdata.xml %{buildroot}%{_datadir}/metainfo

appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%{_sbindir}/gpartedbin
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/gparted.*
%{_datadir}/polkit-1/actions/org.gnome.gparted.policy
%{_datadir}/appdata/gparted.appdata.xml
%{_datadir}/help/*/gparted/*
%{_mandir}/man8/gparted.*

%changelog
* Fri Sep 25 2020 Luke Yue <lukedyue@gmail.com> - 1.1.0-1
- Initial package
