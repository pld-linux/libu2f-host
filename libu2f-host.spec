#
# Conditional build:
%bcond_without	apidocs		# gtk-doc API documentation
%bcond_without	static_libs	# static library
#
Summary:	Yubico Universal 2nd Factor (U2F) Host C Library
Summary(pl.UTF-8):	Biblioteka C hosta Universal 2nd Factor (U2F) Yubico
Name:		libu2f-host
Version:	1.1.10
Release:	1
License:	LGPL v2.1+ (library and tool), GPL v3+ (tests)
Group:		Libraries
Source0:	https://developers.yubico.com/libu2f-host/Releases/%{name}-%{version}.tar.xz
# Source0-md5:	7664b0d5c9940bdefc934dce15db1baf
Patch0:		%{name}-json-c.patch
URL:		https://developers.yubico.com/libu2f-host/
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	help2man
BuildRequires:	hidapi-devel >= 0.8.0
BuildRequires:	json-c-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:188
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libu2f-host provides a C library and command-line tool that implements
the host-side of the U2F protocol. There are APIs to talk to a U2F
device and perform the U2F Register and U2F Authenticate operations.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę C libu2f-host oraz narzędzie linii
poleceń implementujące stronę hosta protokołu U2F. Biblioteka zawiera
API do komunikacji z urządzeniem U2F oraz wykonywania operacji U2F
Register i U2F Authenticate.

%package devel
Summary:	Header files for libu2f-host library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libu2f-host
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libu2f-host library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libu2f-host.

%package static
Summary:	Static libu2f-host library
Summary(pl.UTF-8):	Statyczna biblioteka libu2f-host
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libu2f-host library.

%description static -l pl.UTF-8
Statyczna biblioteka libu2f-host.

%package apidocs
Summary:	API documentation for libu2f-host library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libu2f-host
License:	LGPL v2.1+
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libu2f-host library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libu2f-host.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir} \
	--with-udevrulesdir=/lib/udev/rules.d
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libu2f-host.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS doc/*.adoc
%attr(755,root,root) %{_bindir}/u2f-host
%attr(755,root,root) %{_libdir}/libu2f-host.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libu2f-host.so.0
/lib/udev/rules.d/70-u2f.rules
%{_mandir}/man1/u2f-host.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libu2f-host.so
%{_includedir}/u2f-host
%{_pkgconfigdir}/u2f-host.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libu2f-host.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/u2f-host
%endif
