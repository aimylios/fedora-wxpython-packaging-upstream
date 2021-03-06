%global py_setup_args WX_CONFIG=/usr/bin/wx-config-3.0 WXPORT=gtk3

Name:           wxPython
Version:        3.0.2.0
Release:        23%{?dist}

Summary:        GUI toolkit for the Python programming language

Group:          Development/Languages
License:        LGPLv2+ and wxWidgets 
URL:            http://www.wxpython.org/
Source0:        http://downloads.sourceforge.net/wxpython/%{name}-src-%{version}.tar.bz2
# Remove Editra - it doesn't work and is technically a bundle.  Thanks to
# Debian for the patch.
Patch0:         fix-editra-removal.patch
Patch1:         wxPython-3.0.0.0-format.patch
# http://trac.wxwidgets.org/ticket/16765
Patch2:         wxPython-3.0.2.0-getxwindowcrash.patch
# http://trac.wxwidgets.org/ticket/16767
Patch3:         wxPython-3.0.2.0-plot.patch
# http://trac.wxwidgets.org/ticket/17160
Patch4:         wxPython-3.0.2.0-listctrl-mixin-edit.patch
# From Debian
Patch5:         wxPython-3.0.2.0-webview-optional.patch
# From Debian
Patch6:         wxPython-3.0.2.0-suppress-version-mismatch-warning.patch
# https://github.com/wxWidgets/wxPython/pull/23
Patch7:         wxPython-3.0.2.0-fix-wxcairo.patch
# make sure to keep this updated as appropriate
BuildRequires:  gcc-c++
BuildRequires:  wxGTK3-devel >= 3.0.0
BuildRequires:  python2-devel

%global _description\
wxPython is a GUI toolkit for the Python programming language. It allows\
Python programmers to create programs with a robust, highly functional\
graphical user interface, simply and easily. It is implemented as a Python\
extension module (native code) that wraps the popular wxWindows cross\
platform GUI library, which is written in C++.

%description %_description

%package -n python2-wxpython
Summary:        %summary
%{?python_provide:%python_provide python2-wxpython}
# Remove before F30
Provides:       wxPython = %{version}-%{release}
Provides:       wxPython%{?_isa} = %{version}-%{release}
Obsoletes:      wxPython < %{version}-%{release}

%description -n python2-wxpython %_description

%package        devel
Group:          Development/Libraries
Summary:        Development files for wxPython add-on modules
Requires:       python2-wxpython = %{version}-%{release}
Requires:       wxGTK3-devel
BuildArch:      noarch

%description devel
This package includes C++ header files and SWIG files needed for developing
add-on modules for wxPython. It is NOT needed for development of most
programs which use the wxPython toolkit.

%package        docs
Group:          Documentation
Summary:        Documentation and samples for wxPython
Requires:       python2-wxpython = %{version}-%{release}
BuildArch:      noarch

%description docs
Documentation, samples and demo application for wxPython.

%if 0%{?fedora} > 25
%package -n python2-wxpython-webview
Group:          Development/Languages
Summary:        WebView add-on for wxPython
Requires:       python2-wxpython%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-wxpython-webview}
# Remove before F30
Provides:       wxPython-webview = %{version}-%{release}
Provides:       wxPython-webview%{?_isa} = %{version}-%{release}
Obsoletes:      wxPython-webview < %{version}-%{release}


%description -n python2-wxpython-webview
This package contains the optional WebView (html2) module for wxPython.
%endif


%prep
%autosetup -p1 -n wxPython-src-%{version}

# fix libdir otherwise additional wx libs cannot be found, fix default optimization flags
sed -i -e 's|/usr/lib|%{_libdir}|' -e 's|-O3|-O2|' wxPython/config.py


%build
cd wxPython
%py2_build


%install
cd wxPython
%py2_install

# this is a kludge....
%if "%{python2_sitelib}" != "%{python2_sitearch}"
mv $RPM_BUILD_ROOT%{python2_sitelib}/wx.pth  $RPM_BUILD_ROOT%{python2_sitearch}
mv $RPM_BUILD_ROOT%{python2_sitelib}/wxversion.py* $RPM_BUILD_ROOT%{python2_sitearch}
%endif


%files -n python2-wxpython
%license wxPython/licence/*
%{_bindir}/*
%{python2_sitelib}/*
%if 0%{?fedora} > 25
%exclude %{python2_sitearch}/wx-3.0-gtk3/wx/*html2.*
%endif
%{python2_sitearch}/*

%files devel
%dir %{_includedir}/wx-3.0/wx/wxPython
%{_includedir}/wx-3.0/wx/wxPython/*.h
%dir %{_includedir}/wx-3.0/wx/wxPython/i_files
%{_includedir}/wx-3.0/wx/wxPython/i_files/*.i
%{_includedir}/wx-3.0/wx/wxPython/i_files/*.py*
%{_includedir}/wx-3.0/wx/wxPython/i_files/*.swg

%files docs
%doc wxPython/docs wxPython/demo wxPython/samples

%if 0%{?fedora} > 25
%files -n python2-wxpython-webview
%{python2_sitearch}/wx-3.0-gtk3/wx/*html2.*
%endif


%changelog
* Mon Feb 19 2018 Scott Talbert <swt@techie.net> - 3.0.2.0-23
- Add missing BR for gcc-c++

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 Scott Talbert <swt@techie.net> - 3.0.2.0-21
- Add patch to fix wxcairo for pycairo 1.11.1+

* Wed Sep 20 2017 Scott Talbert <swt@techie.net> - 3.0.2.0-20
- Make -devel noarch to resolve issue with conflicting archful pkgs (#1493233)

* Sun Sep 03 2017 Scott Talbert <swt@techie.net> - 3.0.2.0-19
- Suppress warning about release version mismatch (since wxGTK3 3.0.3 update)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.2.0-18
- Fix internal requires (case was wrong)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.2.0-17
- Fix internal Requires and add Provides for the old name without %%_isa

* Thu Aug 10 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.2.0-16
- Main Python 2 binary package renamed to python2-wxpython,
  and wxPython-webview renamed to python2-wxpython-webview.
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Oct 08 2016 Scott Talbert <swt@techie.net> - 3.0.2.0-12
- Add a -webview subpackage in F26+

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2.0-11
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Scott Talbert <swt@techie.net> - 3.0.2.0-9
- Modernize python packaging and general cleanup

* Sun Dec 27 2015 Scott Talbert <swt@techie.net> - 3.0.2.0-8
- Replace define macros with global ones

* Tue Sep 29 2015 Scott Talbert <swt@techie.net> - 3.0.2.0-7
- Add patch to workaround TextCtrl height issue in ListCtrl mixin (#1264698)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 3.0.2.0-5
- Indicate that this package bundles scintilla 3.2.1.

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.0.2.0-4
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 19 2015 Devrim Gunduz <devrim@gunduz.org> - 3.0.2.0-3
- Rebuild for new GCC to fix C++ ABI issues.

* Sun Jan 04 2015 Scott Talbert <swt@techie.net> - 3.0.2.0-2
- Added patches for fixing crash in GetXWindow() and wx.lib.plot bugs

* Tue Dec 23 2014 Scott Talbert <swt@techie.net> - 3.0.2.0-1
- New upstream release 3.0.2.0, built against wxGTK3

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Dan Horák <dan[at]danny.cz> - 2.8.12.0-6
- fix FTBFS due -Werror=format-security
- modernize spec

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 26 2011 Dan Horák <dan[at]danny.cz> - 2.8.12.0-1
- update to 2.8.12.0 (#699207)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.8.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Dan Horák <dan@danny.cz> - 2.8.11.0-3
- rebuilt against wxGTK-2.8.11-2

* Sun Jul 11 2010 Lubomir Rintel <lkundrak@v3.sk> - 2.8.11.0-2
- Include egg-info when build on recent RHEL

* Mon May 31 2010 Dan Horák <dan[at]danny.cz> - 2.8.11.0-1
- update to 2.8.11.0 (#593837, #595936, #597639)

* Sun May  2 2010 Dan Horák <dan[at]danny.cz> - 2.8.10.1-3
- rebuilt with wxGTK 2.8.11

* Wed Mar 17 2010 Dan Horák <dan[at]danny.cz> - 2.8.10.1-2
- add missing module (#573961)

* Sat Jan 16 2010 Dan Horák <dan[at]danny.cz> - 2.8.10.1-1
- update to 2.8.10.1
- backport to wxGTK 2.8.10 API
- cleaned up BRs

* Thu Jan  7 2010 Hans de Goede <hdegoede@redhat.com> - 2.8.9.2-4
- Change python_foo macros to use %%global as the new rpm will break
  using %%define here, see:
  https://www.redhat.com/archives/fedora-devel-list/2010-January/msg00093.html

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 10 2009 Dan Horák <dan[at]danny.cz> - 2.8.9.2-2
- add patch to fix compile failure for contrib/gizmos/_treelist.i

* Fri Apr 10 2009 Dan Horák <dan[at]danny.cz> - 2.8.9.2-1
- update to 2.8.9.2
- create noarch docs subpackage

* Thu Mar  5 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.8.9.1-4
- Rebuilt for newer wxgtk package

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.8.9.1-2
- Rebuild for Python 2.6

* Tue Sep 30 2008 Dan Horak <dan[at]danny.cz> - 2.8.9.1-1
- update to 2.8.9.1
- fix libdir for additional wx libraries (#306761)

* Mon Sep 29 2008 Dan Horak <dan[at]danny.cz> - 2.8.9.0-1
- update to 2.8.9.0

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.8.0-2
- fix license tag

* Thu Jul 31 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.8.0-1
- update to 2.8.8.0 (bug #457408)
- a fix for bug #450073 is included in the upstream release, so
  dropping that patch.

* Thu Jun 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.8.7.1-5
- Fix an attribute error when importing wxPython (compat) module
  (redhat bugzilla 450073, 450074)

* Sat Jun  7 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7.1-4
- gratuitously bump package release number to work around build system
  glitch. again, but it will work this time.

* Wed Jun  4 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7.1-3
- gratuitously bump package release number to work around build system
  glitch

* Thu Feb 21 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7.1-2
- include egg-info files for fedora 9 or greater

* Wed Feb 20 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7.1-1
- update to 2.8.7.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.8.4.0-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.8.4.0-2
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.4.0-1
- update to 2.8.4.0
- obsolete compat-wxPythonGTK

* Sun Apr 15 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.3.0-1
- update to 2.8.3.0

* Fri Dec 15 2006 Matthew Miller <mattdm@mattdm.org> - 2.8.0.1-1
- update to 2.8.0.1
- make buildrequire wxGTK of version-wxpythonsubrelease
- add wxaddons to filelist

* Mon Dec 11 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.2-3
- bump release for rebuild against python 2.5.

* Mon Aug 28 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.2-2
- bump release for FC6 rebuild

* Thu Apr 13 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.2-1
- version 2.6.3.2
- move wxversion.py _into_ lib64. Apparently that's the right thing to do. :)
- upstream tarball no longer includes embedded.o (since I finally got around
  to pointing that out to the developers instead of just kludging it away.)
- buildrequires to just libGLU-devel instead of mesa-libGL-devel

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-4
- grr. bump relnumber.

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-3
- oh yeah -- wxversion.py not lib64.

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-2
- buildrequires mesa-libGLU-devel

* Thu Mar 30 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-1
- update to 2.6.3.0
- wxGTK and wxPython versions are inexorably linked; make BuildRequires
  be exact, rather than >=.
- make devel subpackage as per comment #7 in bug #163440.

* Thu Nov 24 2005 Matthew Miller <mattdm@mattdm.org> - 2.6.1.0-1
- update to 2.6.0.0
- merge in changes from current extras 2.4.x package
- Happy Thanksgiving
- build animate extention again -- works now.

* Thu Apr 28 2005 Matthew Miller <mattdm@bu.edu> - 2.6.0.0-bu45.1
- get rid of accidental binaries in source tarball -- they generates
  spurious dependencies and serve no purpose
- update to 2.6.0.0 and build for Velouria
- switch to Fedora Extras base spec file
- enable gtk2 and unicode and all the code stuff (as FE does)
- disable BUILD_ANIMATE extension from contrib -- doesn't build
- files are in a different location now -- adjust to that
- zap include files (needed only for building wxPython 3rd-party modules),
  because I don't think this is likely to be very useful. Other option
  would be to create a -devel package, but I think that'd be confusing.

* Tue Feb 08 2005 Thorsten Leemhuis <fedora at leemhuis dot info> 0:2.4.2.4-4
- remove included disutils - it is not multilib aware; this
  fixes build on x86_64

* Tue Jan 06 2004 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.3
- rename package to wxPythonGTK2, provide wxPython (see bug 927)
- dont ship binaries in /usr/share

* Thu Nov 20 2003 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.2
- add missing buildrequires: python-devel, wxGTK2-gl

* Sun Nov 02 2003 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.1
- Initial RPM release.
~
