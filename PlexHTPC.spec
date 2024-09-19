%global __requires_exclude ^(libavcodec\\.so.*|libavfilter\\.so.*|libavformat\\.so.*|libavutil\\.so.*|libswscale\\.so.*|libswresample\\.so.*|libmpv\\.so.*|libPlexMediaServer\\.so.*|libQt6.*\\.so.*|libicu.*\\.so.*|libre2\\.so.*|lib.*plugin\\.so.*|libcec\\.so.*)$
%global __provides_exclude ^(libavcodec\\.so.*|libavfilter\\.so.*|libavformat\\.so.*|libavutil\\.so.*|libswscale\\.so.*|libswresample\\.so.*|libmpv\\.so.*|libPlexMediaServer\\.so.*|libQt6.*\\.so.*|libicu.*\\.so.*|libre2\\.so.*|lib.*plugin\\.so.*|libcec\\.so.*)$
%global __provides_exclude_from ^%{_libdir}/%{name}/(lib|plugins)/.*$
%global __requires_exclude_from ^%{_libdir}/%{name}/plugins/.*$

%global debug_package %{nil}
%define _build_id_links none

%global appstream_id tv.plex.PlexHTPC
%global hash 0ab7ab17

Name:           PlexHTPC
Version:        1.67.1.233
Release:        1%{?dist}
Summary:        Plex HTPC client for the big screen
License:        https://www.plex.tv/en-gb/about/privacy-legal/plex-terms-of-service/
URL:            https://www.plex.tv/
ExclusiveArch:  x86_64

Source0:        https://artifacts.plex.tv/plex-htpc-stable/%{version}-%{hash}/linux/PlexHTPC-%{version}-%{hash}-linux-x86_64.tar.bz2
Source1:        https://raw.githubusercontent.com/flathub/%{appstream_id}/master/%{appstream_id}.desktop
Source2:        https://raw.githubusercontent.com/flathub/%{appstream_id}/master/%{appstream_id}.png
Source3:        https://raw.githubusercontent.com/flathub/%{appstream_id}/master/%{appstream_id}.metainfo.xml
Patch0:         %{name}-script.patch

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Recommends:     intel-vaapi-driver
Recommends:     libva-intel-media-driver
Recommends:     libva-nvidia-driver
Recommends:     mesa-va-drivers

%description
Plex HTPC for Linux is your client for playing on your Linux computer connected
to the big screen. It features a 10-foot interface with a powerful playback
engine.

%prep
%autosetup -p1 -c

rm -f lib/libdrm* lib/libEGL* lib/libigdgmm* lib/libpciaccess* lib/libva*
rm -fr lib/dri

chmod +x lib/lib*.so.*

chrpath -d bin/Plex bin/Plex\ Transcoder bin/QtWebEngineProcess
find . -name "*.so*" -exec chrpath -d {} \;

find . -name "*.qml" -exec chmod 644 {} \;
find . -name "*.qmltypes" -exec chmod 644 {} \;
find . -name "qmldir" -exec chmod 644 {} \;
find . -name "*.metainfo" -exec chmod 644 {} \;
find . -name "*.frag" -exec chmod 644 {} \;
find . -name "*.conf" -exec chmod 644 {} \;

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -fra * %{buildroot}%{_libdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
ln -sf ../%{_lib}/%{name}/Plex.sh %{buildroot}%{_bindir}/PlexHTPC

install -m 0644 -p -D %{SOURCE1} %{buildroot}%{_datadir}/applications/%{appstream_id}.desktop
sed -i -e 's/Exec=Plex/Exec=PlexHTPC/g' \
  %{buildroot}%{_datadir}/applications/%{appstream_id}.desktop

install -m 0644 -p -D %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/%{appstream_id}.png
install -m 0644 -p -D %{SOURCE3} %{buildroot}%{_datadir}/metainfo/%{appstream_id}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appstream_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%files
%{_bindir}/PlexHTPC
%{_datadir}/applications/%{appstream_id}.desktop
%{_datadir}/pixmaps/%{appstream_id}.png
%{_datadir}/metainfo/%{appstream_id}.metainfo.xml
%{_libdir}/%{name}

%changelog
* Thu Sep 19 2024 Simone Caronni <negativo17@gmail.com> - 1.67.1.233-1
- Update to version 1.67.1.233-0ab7ab17.

* Sat Aug 24 2024 Simone Caronni <negativo17@gmail.com> - 1.66.1.215-1
- Update to version 1.66.1.215-6343cfaf.

* Sun Aug 04 2024 Simone Caronni <negativo17@gmail.com> - 1.65.4.206-1
- Update to version 1.65.4.206-38ac5fdc.

* Wed Jul 10 2024 Simone Caronni <negativo17@gmail.com> - 1.64.0.170-1
- First build.
