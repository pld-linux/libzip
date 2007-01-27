Summary:	C library for reading, creating, and modifying zip archives
Summary(pl):	Biblioteka C do odczytu, zapisu i modyfikacji archiwów zip
Name:		libzip
Version:	0.7.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.nih.at/libzip/%{name}-%{version}.tar.gz
# Source0-md5:	12dd752b5388e4b79a53c2ad86920b17
URL:		http://www.nih.at/libzip/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	zlib-devel >= 1.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libzip is a C library for reading, creating, and modifying zip
archives. Files can be added from data buffers, files or compressed
data copied directly from other zip archives. Changes made without
closing the archive can be reverted.

%description -l pl
libzip jest bibliotek± C do odczytu, zapisu i modyfikacji archiwów
zip. Pliki mog± byæ dodawane z buforów, plików lub skompresowanych
danych kopiowanych bezpo¶rednio z innych archiwów zip. Wykonane zmiany
mog± zostaæ cofniête przed zamkniêciem archiwum.

%package devel
Summary:	Header files for libzip library
Summary(pl):	Pliki nag³ówkowe biblioteki libzip
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel >= 1.1.2

%description devel
Header files for libzip library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libzip.

%package static
Summary:	Static libzip library
Summary(pl):	Statyczna biblioteka libzip
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libzip library.

%description static -l pl
Statyczna biblioteka libzip.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/zipcmp
%attr(755,root,root) %{_bindir}/zipmerge
%attr(755,root,root) %{_libdir}/libzip.so.*.*.*
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzip.so
%{_libdir}/libzip.la
%{_includedir}/zip.h
%{_pkgconfigdir}/libzip.pc
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libzip.a
