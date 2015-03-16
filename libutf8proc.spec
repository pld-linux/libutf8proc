#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	libutf8proc
Summary(pl.UTF-8):	Biblioteka libutf8proc
Name:		libutf8proc
Version:	1.1.6
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	2782ab67e722f6f61ba263f9ef5b858c
URL:		http://www.netsurf-browser.org/projects/libutf8proc/
BuildRequires:	netsurf-buildsystem >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the Public software group utf8proc library [1] repackaged as a
conveniance library for NetSurf. Previously this library was simply
copied into the NetSurf sources.

This takes the unicode 5 capable version 1.1.6 of the library and
converts it to the NetSurf build system. additional API has been added
with a normalisation function but there are no data changes from
upstream.

All the Makefiles and changes are licenced as per the utf8proc
source using the MIT "expat" licence.

[1] http://www.public-software-group.org/utf8proc

%package devel
Summary:	libutf8proc library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libutf8proc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the include files and other resources you can
use to incorporate libutf8proc into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libutf8proc w swoich
programach.

%package static
Summary:	libutf8proc static library
Summary(pl.UTF-8):	Statyczna biblioteka libutf8proc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libutf8proc library.

%description static -l pl.UTF-8
Statyczna biblioteka libutf8proc.

%prep
%setup -q

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog LICENSE
%attr(755,root,root) %{_libdir}/libutf8proc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libutf8proc.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libutf8proc.so
%{_includedir}/libutf8proc
%{_pkgconfigdir}/libutf8proc.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libutf8proc.a
%endif
