# Packaging wxPython with GTK2 for Fedora

As of March 2018 the [Fedora wxPython package](https://src.fedoraproject.org/rpms/wxPython) is built against GTK3, and no additional compatibility package is provided to add wxPython for GTK2 (see RedHat Bugzilla [#1519989](https://bugzilla.redhat.com/show_bug.cgi?id=1519989) for details). This makes it difficult to build and install software that requires GTK2.

As a workaround I decided to build my own wxPython-GTK2 RPM, with GTK2 instead of GTK3 support. This is not the optimal solution, but should be sufficient for my personal needs. I did some testing with the current development version of [KiCad](http://kicad-pcb.org/) and could not find any issues.

It is currently not possible to install the python2-wxpython-gtk2 package in parallel to the upstream python2-wxpython (which needs to be removed before installation, including all other packages that depend on it). I'm also working on a compat-wxPython-GTK2 package that supplements the upstream package and should thus avoid any incompatibilities.

This repository includes the SPEC description file for the wxPython-GTK2 package, all required patches, and, for convenience, also the wxPython source tarball, which was copied from [Sourceforge](https://sourceforge.net/projects/wxpython/files/wxPython/3.0.2.0/). A ready-made RPM is included in my personal [aimylios/kicad-nightly](https://copr.fedorainfracloud.org/coprs/aimylios/kicad-nightly/) Copr repository.
