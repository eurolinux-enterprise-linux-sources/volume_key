%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: An utility for manipulating storage encryption keys and passphrases
Name: volume_key
Version: 0.3.9
Release: 9%{?dist}
# License fix: lib/{SECerrs,SSLerrs}.h are both licensed under MPLv1.1, GPLv2 and LGPLv2
License: GPLv2 and (MPLv1.1 or GPLv2 or LGPLv2)
Group: Applications/System
URL: https://pagure.io/%{name}/
Requires: volume_key-libs%{?_isa} = %{version}-%{release}

Source0: https://releases.pagure.org/%{name}/%{name}-%{version}.tar.xz
# Upstream commit 04991fe8c4f77c4e5c7874c2db8ca32fb4655f6e
Patch1: volume_key-0.3.9-fips-crash.patch
Patch2: volume_key-0.3.9-translation-updates.patch
# Upstream commit 8f8698aba19b501f01285e9eec5c18231fc6bcea
Patch3: volume_key-0.3.9-config.h.patch
# Upstream commit ecef526a51c5a276681472fd6df239570c9ce518
Patch4: volume_key-0.3.9-dont-use-crypt_get_error.patch
# Upstream commit 23a1ff087a11ceefdfd709b151bfd4f3b75b0dc8
Patch5: volume_key-0.3.9-fix-confusing-error-message-on-missing-private-key.patch
BuildRequires: cryptsetup-luks-devel, gettext-devel, glib2-devel, /usr/bin/gpg
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
Requires: volume_key-libs%{?_isa} = %{version}-%{release}

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
Requires: /usr/bin/gpg

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
Requires: volume_key-libs%{?_isa} = %{version}-%{release}

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

%patch1 -p1 -b .fips-crash
%patch2 -p2 -b .translation-updates
%patch3 -p1 -b .config.h
%patch4 -p1 -b .no-crypt_get_error
%patch5 -p1 -b .error-message
# The patch touches both .pot and .po files, make sure the .pot file is older
# to avoid po/Makefile running (msgmerge --update); otherwise the set of
# (msgemrge --update)'d files changes from build to build, depending on precise
# timing, and causes multilib differences.
touch -d '-1 minute' po/volume_key.pot

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%find_lang volume_key

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README contrib
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
* Tue Mar 19 2019 Jiri Kucera <jkucera@redhat.com> - 0.3.9-9
- Backport ecef526 (Stop using crypt_get_error)
  Backport 23a1ff0 (Fix nonsensical error messages on missing keys)
  Fix License, URL and Source0 tags
  Resolves: #1502399, #1574988, #1593855, #1454358

* Mon Oct 09 2017 skisela@redhat.com - 0.3.9-8
- Don't #include <config.h> in libvolume_key.h
  Resolves: #1498783

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.3.9-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.3.9-6
- Mass rebuild 2013-12-27

* Mon Dec  2 2013 Miloslav Trmač <mitr@redhat.com> - 0.3.9-5
- Avoid multilib confilicts introduced by applying the previous patch
  Related: #1030387

* Fri Nov 29 2013 Miloslav Trmač <mitr@redhat.com> - 0.3.9-4
- Include updated translations
  Resolves: #1030387

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.9-2
- Fix a crash when trying to use passphrase encryption in FIPS mode

* Sat Sep 22 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.9-1
- Update to volume_key-0.3.9

* Mon Aug  6 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.8-4
- Use BuildRequires: /usr/bin/gpg instead of gnupg, for compatibility with RHEL

* Mon Jul 23 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.8-3
- Add Requires: /usr/bin/gpg
  Resolves: #842074

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar  3 2012 Miloslav Trmač <mitr@redhat.com> - 0.3.8-1
- Update to volume_key-0.3.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.7-2
- Rebuild with newer libcryptsetup

* Wed Aug 24 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.7-1
- Update to volume_key-0.3.7

* Fri Jun 10 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.6-2
- Fix a typo
  Resolves: #712256

* Thu Mar 31 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.6-1
- Update to volume_key-0.3.6

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Miloslav Trmač <mitr@redhat.com> - 0.3.5-2
- Use %%{?_isa} in Requires:

* Wed Nov 24 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.5-1
- Update to volume_key-0.3.5

* Mon Oct 18 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.4-4
- Tell the user if asking for the same passphrase again
  Resolves: #641111
- Check certificate file before interacting with the user
  Resolves: #643897

* Fri Oct  8 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.4-3
- Make it possible to interrupt password prompts
  Resolves: #641111

* Wed Sep 29 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.4-2
- Clarify which block device should be passed as an argument
  Resolves: #636541
- Recognize SSL error messages from NSS as well
  Resolves: #638732

* Fri Aug 27 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.4-1
- Update to volume_key-0.3.4

* Mon Jul 26 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 22 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.3-3
- Fix build with new gpgme

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Mar 26 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.3-1
- Update to volume_key-0.3.3

* Thu Mar  4 2010 Miloslav Trmač <mitr@redhat.com> - 0.3.2-1
- Update to volume_key-0.3.2
- Drop no longer necessary references to BuildRoot:

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
