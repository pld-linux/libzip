Summary:	C library for reading, creating, and modifying zip archives
Summary(pl.UTF-8):	Biblioteka C do odczytu, zapisu i modyfikacji archiwów zip
Name:		libzip
Version:	1.4.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.nih.at/libzip/%{name}-%{version}.tar.xz
# Source0-md5:	b411f3ebfa735d33a390f80c8e939029
Patch0:		libzip-upstream.patch
Patch1:		libzip-rpath.patch
Patch2:		libzip-multilib.patch
URL:		http://www.nih.at/libzip/
BuildRequires:	cmake
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.1.2
Requires:	zlib >= 1.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libzip is a C library for reading, creating, and modifying zip
archives. Files can be added from data buffers, files or compressed
data copied directly from other zip archives. Changes made without
closing the archive can be reverted.

%description -l pl.UTF-8
libzip jest biblioteką C do odczytu, zapisu i modyfikacji archiwów
zip. Pliki mogą być dodawane z buforów, plików lub skompresowanych
danych kopiowanych bezpośrednio z innych archiwów zip. Wykonane zmiany
mogą zostać cofnięte przed zamknięciem archiwum.

%package devel
Summary:	Header files for libzip library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libzip
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel >= 1.1.2

%description devel
Header files for libzip library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libzip.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%{cmake} ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md NEWS.md THANKS LICENSE AUTHORS
%attr(755,root,root) %{_bindir}/zipcmp
%attr(755,root,root) %{_bindir}/zipmerge
%attr(755,root,root) %{_bindir}/ziptool
%attr(755,root,root) %{_libdir}/libzip.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libzip.so.5
%{_mandir}/man1/zipcmp.1*
%{_mandir}/man1/zipmerge.1*
%{_mandir}/man1/ziptool.1*

%files devel
%defattr(644,root,root,755)
%doc API-CHANGES.md TODO.md
%attr(755,root,root) %{_libdir}/libzip.so
%{_includedir}/zip.h
%{_includedir}/zipconf.h
%{_pkgconfigdir}/libzip.pc
%{_mandir}/man3/ZIP_SOURCE_GET_ARGS.3*
%{_mandir}/man3/libzip.3*
%{_mandir}/man3/zip_*.3*
