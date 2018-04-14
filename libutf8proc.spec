#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	utf8proc library for NetSurf
Summary(pl.UTF-8):	Biblioteka utf8proc dla projektu NetSurf
Name:		libutf8proc
Version:	1.3.1
Release:	4
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-3-src.tar.gz
# Source0-md5:	c427797a2e3172a0ebef68b37b682124
Patch0:		%{name}-build.patch
URL:		http://www.netsurf-browser.org/projects/libutf8proc/
BuildRequires:	netsurf-buildsystem >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the Public Software Group utf8proc library [1] repackaged as a
conveniance library for NetSurf. Previously this library was simply
copied into the NetSurf sources.

This takes the Unicode 5 capable version 1.1.6 of the library and
converts it to the NetSurf build system. Additional API has been added
with a normalisation function but there are no data changes from
upstream.

All the Makefiles and changes are licenced as per the utf8proc
source using the MIT "expat" licence.

[1] http://www.public-software-group.org/utf8proc

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę utf8proc [1] opublikowaną przez Public
Software Group, przepakowaną jako bibliotekę pomocniczą dla projektu
NetSuft. Wcześniej biblioteka była po prostu skopiowana do źródeł
NetSurfa.

Pakiet zawiera wersję 1.1.6 biblioteki z obsługą Unicode 5,
przekształconą do systemu budowania NetSurfa. Zostało dodane dodatkowe
API z funkcją normalizującą, ale nie ma zmian w danych w stosunku do
wersji oryginalnej.

Wszystkie pliki Makefile oraz zmiany są licencjonowane tak samo, jak
źródła biblioteki utf8proc, z użyciem licencji MIT w wersji "expat".

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
Pliki nagłówkowe pozwalające na używanie biblioteki libutf8proc w
swoich programach.

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
%setup -q -n %{name}-%{version}-3
%patch0 -p1

%build
export AR="%{__ar}"
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

export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

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
%doc LICENSE.md NEWS.md README.md 
%attr(755,root,root) %{_libdir}/libutf8proc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libutf8proc.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libutf8proc.so
%{_includedir}/utf8proc.h
%{_pkgconfigdir}/libutf8proc.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libutf8proc.a
%endif
