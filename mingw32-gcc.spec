%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global DATE 20091114
%global SVNREV 154179

Name:           mingw32-gcc
Version:        4.4.2
Release:        3%{?dist}.1
Summary:        MinGW Windows cross-compiler (GCC) for C

License:        GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group:          Development/Languages

# We use the same source as Fedora's native gcc.
URL:            http://gcc.gnu.org
Source0:        gcc-%{version}-%{DATE}.tar.bz2
Source1:        libgcc_post_upgrade.c
Source2:        README.libgcjwebplugin.so
Source3:        protoize.1

# Patches from Fedora's native gcc.
Patch0:         gcc44-hack.patch
Patch1:         gcc44-build-id.patch
Patch2:         gcc44-c++-builtin-redecl.patch
Patch3:         gcc44-ia64-libunwind.patch
Patch4:         gcc44-java-nomulti.patch
Patch5:         gcc44-ppc32-retaddr.patch
Patch6:         gcc44-pr33763.patch
Patch7:         gcc44-rh330771.patch
Patch8:         gcc44-rh341221.patch
Patch9:         gcc44-java-debug-iface-type.patch
Patch10:        gcc44-i386-libgomp.patch
Patch11:        gcc44-sparc-config-detection.patch
Patch12:        gcc44-libgomp-omp_h-multilib.patch
Patch13:        gcc44-libtool-no-rpath.patch
Patch14:        gcc44-cloog-dl.patch
Patch16:        gcc44-unwind-debug-hook.patch
Patch17:        gcc44-pr38757.patch
Patch18:        gcc44-libstdc++-docs.patch
Patch19:        gcc44-ppc64-aixdesc.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  texinfo
BuildRequires:  mingw32-filesystem >= 49
# Need mingw32-binutils which support %gnu_unique_object >= 2.19.51.0.14
BuildRequires:  mingw32-binutils >= 2.19.51.0.14
BuildRequires:  mingw32-runtime
BuildRequires:  mingw32-w32api
BuildRequires:  mingw32-pthreads
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  libgomp
BuildRequires:  flex

# NB: Explicit mingw32-filesystem dependency is REQUIRED here.
Requires:       mingw32-filesystem >= 48
# Need mingw32-binutils which support %gnu_unique_object
Requires:       mingw32-binutils >= 2.19.51.0.14
Requires:       mingw32-runtime
Requires:       mingw32-w32api
Requires:       mingw32-cpp
# libgomp dll is linked with pthreads, but since we don't run the
# automatic dependency scripts, it doesn't get picked up automatically.
Requires:       mingw32-pthreads

# We don't run the automatic dependency scripts which would
# normally detect and provide the following DLL:
Provides:       mingw32(libgcc_s_sjlj-1.dll)
Provides:       mingw32(libgomp-1.dll)


%description
MinGW Windows cross-compiler (GCC) for C.


%package -n mingw32-cpp
Summary: MinGW Windows cross-C Preprocessor
Group: Development/Languages

%description -n mingw32-cpp
MinGW Windows cross-C Preprocessor


%package c++
Summary: MinGW Windows cross-compiler for C++
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description c++
MinGW Windows cross-compiler for C++.


%package objc
Summary: MinGW Windows cross-compiler support for Objective C
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
#Requires: mingw32-libobjc = %{version}-%{release}

%description objc
MinGW Windows cross-compiler support for Objective C.


%package objc++
Summary: MinGW Windows cross-compiler support for Objective C++
Group: Development/Languages
Requires: %{name}-c++ = %{version}-%{release}
Requires: %{name}-objc = %{version}-%{release}

%description objc++
MinGW Windows cross-compiler support for Objective C++.


%package gfortran
Summary: MinGW Windows cross-compiler for FORTRAN
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description gfortran
MinGW Windows cross-compiler for FORTRAN.


%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch0 -p0 -b .hack~
%patch1 -p0 -b .build-id~
%patch2 -p0 -b .c++-builtin-redecl~
%patch3 -p0 -b .ia64-libunwind~
%patch4 -p0 -b .java-nomulti~
%patch5 -p0 -b .ppc32-retaddr~
%patch6 -p0 -b .pr33763~
%patch7 -p0 -b .rh330771~
%patch8 -p0 -b .rh341221~
%patch9 -p0 -b .java-debug-iface-type~
%patch10 -p0 -b .i386-libgomp~
%patch11 -p0 -b .sparc-config-detection~
%patch12 -p0 -b .libgomp-omp_h-multilib~
%patch13 -p0 -b .libtool-no-rpath~
%patch14 -p0 -b .cloog-dl~
%patch16 -p0 -b .unwind-debug-hook~
%patch17 -p0 -b .pr38757~
%patch18 -p0 -b .libstdc++-docs~
%patch19 -p0 -b .ppc64-aixdesc~

sed -i -e 's/4\.4\.3/%{version}/' gcc/BASE-VER
echo 'Fedora MinGW %{version}-%{release}' > gcc/DEV-PHASE


%build
mkdir -p build
pushd build

# GNAT is required to build Ada.  Don't build GCJ.
#languages="c,c++,objc,obj-c++,java,fortran,ada"
languages="c,c++,objc,obj-c++,fortran"

CC="%{__cc} ${RPM_OPT_FLAGS}" \
../configure \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir} \
  --datadir=%{_datadir} \
  --build=%_build --host=%_host \
  --target=%{_mingw32_target} \
  --with-gnu-as --with-gnu-ld --verbose \
  --without-newlib \
  --disable-multilib \
  --enable-libgomp \
  --with-system-zlib \
  --disable-nls --without-included-gettext \
  --disable-win32-registry \
  --enable-version-specific-runtime-libs \
  --with-sysroot=%{_mingw32_sysroot} \
  --enable-languages="$languages" \
  --with-bugurl=http://bugzilla.redhat.com/bugzilla

make %{?_smp_mflags} all

popd


%install
rm -rf $RPM_BUILD_ROOT

pushd build
make DESTDIR=$RPM_BUILD_ROOT install

# These files conflict with existing installed files.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty*
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/*

mkdir -p $RPM_BUILD_ROOT/lib
ln -sf ..%{_prefix}/bin/i686-pc-mingw32-cpp \
  $RPM_BUILD_ROOT/lib/i686-pc-mingw32-cpp

# Not sure why gcc puts this DLL into _bindir, but surely better if
# it goes into _mingw32_bindir.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mv $RPM_BUILD_ROOT%{_bindir}/libgcc_s_sjlj-1.dll \
  $RPM_BUILD_ROOT%{_mingw32_bindir}
# Same goes for this DLL under _libdir.
mv $RPM_BUILD_ROOT%{_libdir}/gcc/i686-pc-mingw32/bin/libgomp-1.dll \
  $RPM_BUILD_ROOT%{_mingw32_bindir}

# Don't want the *.la files.
find $RPM_BUILD_ROOT -name '*.la' -delete

popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/i686-pc-mingw32-gcc
%{_bindir}/i686-pc-mingw32-gcc-%{version}
%{_bindir}/i686-pc-mingw32-gccbug
%{_bindir}/i686-pc-mingw32-gcov
%{_prefix}/i686-pc-mingw32/lib/libiberty.a
%dir %{_libdir}/gcc/i686-pc-mingw32
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}
%{_libdir}/gcc/i686-pc-mingw32/%{version}/crtbegin.o
%{_libdir}/gcc/i686-pc-mingw32/%{version}/crtend.o
%{_libdir}/gcc/i686-pc-mingw32/%{version}/crtfastmath.o
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgcc.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgcc_eh.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgcc_s.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgcov.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgomp.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgomp.dll.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgomp.spec
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libssp.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libssp_nonshared.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libssp.dll.a
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/include
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/include-fixed
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/include/ssp
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include-fixed/README
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include-fixed/*.h
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include/*.h
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include/ssp/*.h
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/install-tools
%{_libdir}/gcc/i686-pc-mingw32/%{version}/install-tools/*
%dir %{_libdir}/gcc/i686-pc-mingw32/bin/
%{_libdir}/gcc/i686-pc-mingw32/bin/libssp-0.dll
%dir %{_libexecdir}/gcc/i686-pc-mingw32/%{version}/install-tools
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/install-tools/*
%{_mingw32_bindir}/libgcc_s_sjlj-1.dll
%{_mingw32_bindir}/libgomp-1.dll
%{_mandir}/man1/i686-pc-mingw32-gcc.1*
%{_mandir}/man1/i686-pc-mingw32-gcov.1*


%files -n mingw32-cpp
%defattr(-,root,root,-)
/lib/i686-pc-mingw32-cpp
%{_bindir}/i686-pc-mingw32-cpp
%{_mandir}/man1/i686-pc-mingw32-cpp.1*
%dir %{_libdir}/gcc/i686-pc-mingw32
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/cc1


%files c++
%defattr(-,root,root,-)
%{_bindir}/i686-pc-mingw32-g++
%{_bindir}/i686-pc-mingw32-c++
%{_mandir}/man1/i686-pc-mingw32-g++.1*
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include/c++/
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libstdc++.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libsupc++.a
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/cc1plus
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/collect2


%files objc
%defattr(-,root,root,-)
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include/objc/
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libobjc.a
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/cc1obj


%files objc++
%defattr(-,root,root,-)
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/cc1objplus


%files gfortran
%defattr(-,root,root,-)
%{_bindir}/i686-pc-mingw32-gfortran
%{_mandir}/man1/i686-pc-mingw32-gfortran.1*
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgfortran.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgfortranbegin.a
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/finclude
%{_libdir}/gcc/i686-pc-mingw32/%{version}/finclude/omp_lib.f90
%{_libdir}/gcc/i686-pc-mingw32/%{version}/finclude/omp_lib.h
%{_libdir}/gcc/i686-pc-mingw32/%{version}/finclude/omp_lib.mod
%{_libdir}/gcc/i686-pc-mingw32/%{version}/finclude/omp_lib_kinds.mod
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/f951


%changelog
* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 4.4.2-3.1
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Sun Dec 26 2010 Andrew Beekhof <abeekhof@redhat.com> - 4.4.2-3
- Import 4.4 in an attempt to build a functional mingw stack
  Related: rhbz#658833

* Thu Dec 17 2009 Chris Bagwell <chris@cnpbagwell.com> - 4.4.2-2
- Enable libgomp support.

* Sun Nov 22 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.2-1
- Update to gcc 4.4.2 20091114 svn 154179, which includes
  VTA backport from 4.5 branch.
- Patches taken from native Fedora gcc-4.4.2-10.

* Fri Sep 18 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-3
- Require mingw32-binutils >= 2.19.51.0.14 for %%gnu_unique_object support.

* Thu Sep 03 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-2
- Update to gcc 4.4.1 20090902 svn 151328.
- Patches taken from native Fedora gcc-4.4.1-8.
- Another license update to keep it in sync with native gcc package.

* Sun Aug 23 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-1
- Update to gcc 4.4.1 20090818 svn 150873.
- Patches taken from native Fedora gcc-4.4.1-6.
- Replaced %%define with %%global and updated %%defattr.
- Changed license to match native Fedora gcc package.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.7
- New native Fedora version gcc 4.4.0 20090319 svn 144967.
- Enable _smp_mflags.

* Wed Mar  4 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.6
- Fix libobjc and consequently Objective C and Objective C++ compilers.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.4
- Rebuild for mingw32-gcc 4.4

* Thu Feb 19 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.2
- Move to upstream version 4.4.0-20090216 (same as Fedora native version).
- Added FORTRAN support.
- Added Objective C support.
- Added Objective C++ support.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-12
- Rebuild against latest filesystem package.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-11
- Remove obsoletes for a long dead package.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-10
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-9
- Rebuild against mingw32-filesystem 36

* Thu Oct 30 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-8
- Don't BR mpfr-devel for RHEL/EPEL-5 (Levente Farkas).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-7
- Rename mingw -> mingw32.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-6
- Use RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-3
- Initial RPM release, largely based on earlier work from several sources.
