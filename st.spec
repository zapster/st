Name:           st
Version:        0.1.1
Release:        3%{?dist}
Summary:        A simple terminal implementation for X
Group:          User Interface/X
License:        BSD
URL:            http://st.suckless.org/
Source0:        http://hg.suckless.org/%{name}/archive/%{version}.tar.gz
Source1:        %{name}.desktop
# Generate debuginfo
Patch0:         st-0.1.1-debug.patch
# Make sure we use an unicode capable font
Patch1:         st-0.1.1-terminus.patch
BuildRequires:  libX11-devel
BuildRequires:  ncurses
BuildRequires:  desktop-file-utils
Requires:       terminus-fonts
# /usr/bin/st, rhbz#693363
Conflicts:      openstack-swift

%description
A simple virtual terminal emulator for X which sucks less.

%prep
%setup -q
%patch0 -p1 -b .debug
%patch1 -p1 -b .terminus
# Do not install terminfo into the build environment
sed -i '/@tic -s st.info/d' Makefile

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_datadir}/terminfo/s
tic -s -o %{buildroot}%{_datadir}/terminfo/ %{name}.info
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/terminfo/s
%{_datadir}/applications

%changelog
* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for glibc bug#747377

* Mon May 23 2011 Petr Sabata <psabata@redhat.com> - 0.1.1-2
- We have a conflict with openstack-swift (#693363)

* Mon Apr  4 2011 Petr Sabata <psabata@redhat.com> - 0.1.1-1
- Initial import
