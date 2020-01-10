%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: An utility for manipulating storage encryption keys and passphrases
Name: volume_key
Version: 0.3.1
Release: 5%{?dist}
License: GPLv2
Group: Applications/System
URL: https://fedorahosted.org/volume_key/
Requires: volume_key-libs = %{version}-%{release}

Source0: https://fedorahosted.org/releases/v/o/volume_key/volume_key-%{version}.tar.bz2
# Committed upstrean
Patch0: volume_key-0.3.1-empty-passphrase.patch
# Merged upstream
Patch1: volume_key-0.3.1-l10n-update.patch
# Upstream commit 3486c1c8112bd625bfe6bde55c337c4edbd75277
Patch2: volume_key-0.3.1-man-device.patch
# Upstream commit a2ab2a3546f3ee5937bb4272f4f26650f31f42bb
Patch3: volume_key-0.3.1-sslerrs.patch
# Upstream commits 82f476f614ff8492231e730b6ceffaa7242481cc,
# b66602b8ef4e6ef8325c0b97fce821e183a2ae84 and
# 1dcafdcd6f3097487b92f86e9db3e5412c266ee5
Patch4: volume_key-0.3.1-passphrase-dialogs.patch
# Upstream commit 40e5330c076f9f4e149c2091900602d3de41b119
Patch5: volume_key-0.3.1-check-cert-first.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: cryptsetup-luks-devel, gettext-devel, glib2-devel, gnupg
BuildRequires: gpgme-devel, libblkid-devel, nss-devel, python-devel

%description
This package provides a command-line tool for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package devel
Summary: A library for manipulating storage encryption keys and passphrases
Group: Development/Libraries
Requires: volume_key-libs = %{version}-%{release}

%description devel
This package provides libvolume_key, a library for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package libs
Summary: A library for manipulating storage encryption keys and passphrases
Group: System Environment/Libraries

%description libs
This package provides libvolume_key, a library for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package -n python-volume_key
Summary: Python bindings for libvolume_key
Group: System Environment/Libraries
Requires: volume_key-libs = %{version}-%{release}

%description -n python-volume_key
This package provides Python bindings for libvolume_key, a library for
manipulating storage volume encryption keys and storing them separately from
volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

volume_key currently supports only the LUKS volume encryption format.  Support
for other formats is possible, some formats are planned for future releases.

%prep
%setup -q
%patch0 -p1 -b .empty-passphrase
%patch1 -p1 -b .l10n-update
%patch2 -p1 -b .man-device
%patch3 -p1 -b .sslerrs
%patch4 -p1 -b .passphrase-dialogs
%patch5 -p1 -b .check-cert-first

%build
# For volume_key-0.3.1-l10n-update.patch: Make sure .gmo files are (re)generated
# for the new/updated files.
touch po/volume_key.pot

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%find_lang volume_key

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/volume_key
%{_mandir}/man8/volume_key.8*

%files devel
%defattr(-,root,root,-)
%{_includedir}/volume_key
%exclude %{_libdir}/libvolume_key.la
%{_libdir}/libvolume_key.so

%files libs -f volume_key.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS
%{_libdir}/libvolume_key.so.*

%files -n python-volume_key
%defattr(-,root,root,-)
%exclude %{python_sitearch}/_volume_key.la
%{python_sitearch}/_volume_key.so
%{python_sitearch}/volume_key.py*

%changelog
* Thu Jan 20 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.1-5
- Rebuild for fastrack
  Related: #636541 #638732 #641111 #643897

* Fri Jan 14 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.1-4
- Clarify documentation about which block device to use as an argument
  Resolves: #636541
- Report readable error messages instead of random characters in some cases
  Resolves: #638732
- Make passphrase prompts interruptable, report incorrect passphrases
  Resolves: #641111
- Ask for passphrases only after checking for easily detectable problems
  Resolves: #643897

* Wed Apr 28 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.1-3
- Update translations
  Resolves: #585836

* Fri Feb  5 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.1-2
- Fix a crash when an empty passphrase is provided
  Resolves: #558410

* Fri Dec 11 2009 Miloslav Trmač <mitr@redhat.com> - 0.3.1-1
- Update to volume_key-0.3.1.

* Wed Sep 30 2009 Miloslav Trmač <mitr@redhat.com> - 0.3-1
- Update to volume_key-0.3.
- Drop bundled libcryptsetup.

* Sat Aug  8 2009 Miloslav Trmač <mitr@redhat.com> - 0.2-3
- Handle changed "TYPE=crypto_LUKS" from libblkid
- Preserve file timestamps during installation

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Miloslav Trmač <mitr@redhat.com> - 0.2-1
- Initial build.
