Name:           wxPython-GTK2
Version:        3.0.2.0
Release:        100%{?dist}

Summary:        GUI toolkit for the Python programming language

License:        LGPLv2+ and wxWidgets 
URL:            http://www.wxpython.org/
Source0:        https://raw.githubusercontent.com/aimylios/fedora-wxpython-packaging-upstream/aimylios/wxPython-GTK2/wxPython-src-%{version}.tar.bz2
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
BuildRequires:  compat-wxGTK3-gtk2-devel >= 3.0.0
BuildRequires:  python2-devel

%global _description\
wxPython is a GUI toolkit for the Python programming language. It allows\
Python programmers to create programs with a robust, highly functional\
graphical user interface, simply and easily. It is implemented as a Python\
extension module (native code) that wraps the popular wxWindows cross\
platform GUI library, which is written in C++.

%description %_description

%package -n python2-wxpython-gtk2
Summary:        %summary
%{?python_provide:%python_provide python2-wxpython-gtk2}
Conflicts:      python2-wxpython

%description -n python2-wxpython-gtk2 %_description

%package devel
Summary:        Development files for wxPython add-on modules
Requires:       python2-wxpython-gtk2 = %{version}-%{release}
Requires:       compat-wxGTK3-gtk2-devel
BuildArch:      noarch

%description devel
This package includes C++ header files and SWIG files needed for developing
add-on modules for wxPython. It is NOT needed for development of most
programs which use the wxPython toolkit.

%package docs
Group:          Documentation
Summary:        Documentation and samples for wxPython
Requires:       python2-wxpython-gtk2 = %{version}-%{release}
BuildArch:      noarch

%description docs
Documentation, samples and demo application for wxPython.


%if 0%{?fedora} > 27
%global py_setup_args WX_CONFIG=%{_bindir}/wx-config WXPORT=gtk2
%global wx_include_dir wx-3.0
%else
%global py_setup_args WX_CONFIG=%{_bindir}/wx-config-3.0-gtk2 WXPORT=gtk2
%global wx_include_dir wx-3.0-gtk2
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
%if 0%{?fedora} < 28
%{__mv} $RPM_BUILD_ROOT%{_includedir}/wx-3.0/ $RPM_BUILD_ROOT%{_includedir}/%{wx_include_dir}/
%endif


# this is a kludge....
%if "%{python2_sitelib}" != "%{python2_sitearch}"
mv $RPM_BUILD_ROOT%{python2_sitelib}/wx.pth  $RPM_BUILD_ROOT%{python2_sitearch}
mv $RPM_BUILD_ROOT%{python2_sitelib}/wxversion.py* $RPM_BUILD_ROOT%{python2_sitearch}
%endif


%files -n python2-wxpython-gtk2
%license wxPython/licence/*
%{_bindir}/*
%{python2_sitelib}/*
%{python2_sitearch}/*

%files devel
%dir %{_includedir}/%{wx_include_dir}/wx/wxPython
%{_includedir}/%{wx_include_dir}/wx/wxPython/*.h
%dir %{_includedir}/%{wx_include_dir}/wx/wxPython/i_files
%{_includedir}/%{wx_include_dir}/wx/wxPython/i_files/*.i
%{_includedir}/%{wx_include_dir}/wx/wxPython/i_files/*.py*
%{_includedir}/%{wx_include_dir}/wx/wxPython/i_files/*.swg

%files docs
%doc wxPython/docs wxPython/demo wxPython/samples


%changelog
* Fri Mar 16 2018 Aimylios <aimylios@xxx.xx> - 3.0.2.0-100
- Initial release based on wxPython-3.0.2.0-23
