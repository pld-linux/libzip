#
# Conditional build:
%bcond_with	gnutls	# GnuTLS instead of OpenSSL for AES

Summary:	C library for reading, creating, and modifying zip archives
Summary(pl.UTF-8):	Biblioteka C do odczytu, zapisu i modyfikacji archiwów zip
Name:		libzip
Version:	1.11.4
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://libzip.org/download/%{name}-%{version}.tar.xz
# Source0-md5:	5b53072471ef2ef03505fc6ac06f5835
Patch0:		%{name}-pc.patch
URL:		https://libzip.org/
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 3.10
BuildRequires:	groff
# also mbedtls >= 1.0 supported
%{?with_gnutls:BuildRequires:	gnutls-devel}
%{?with_gnutls:BuildRequires:	nettle-devel >= 3.0}
%{!?with_gnutls:BuildRequires:	openssl-devel}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel >= 1:5.2
BuildRequires:	zlib-devel >= 1.1.2
BuildRequires:	zstd-devel >= 1.4.0
Requires:	zlib >= 1.1.2
Requires:	xz-libs >= 1:5.2
Requires:	zstd >= 1.4.0
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
Requires:	bzip2-devel
%{?with_gnutls:Requires:	gnutls-devel}
%{?with_gnutls:Requires:	nettle-devel >= 3.0}
%{!?with_gnutls:Requires:	openssl-devel}
Requires:	xz-devel >= 1:5.2
Requires:	zlib-devel >= 1.1.2
Requires:	zstd-devel >= 1.4.0
Obsoletes:	libzip-static < 1.4.0

%description devel
Header files for libzip library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libzip.

%prep
%setup -q
%patch -P0 -p1

%build
install -d build
cd build
# .pc file generation expects dirs relative to CMAKE_INSTALL_PREFIX
%cmake .. \
	-DCMAKE_INSTALL_BINDIR=bin \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DENABLE_COMMONCRYPTO=OFF \
	%{!?with_gnutls:-DENABLE_GNUTLS=OFF} \
	%{?with_gnutls:-DENABLE_OPENSSL=OFF}

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
%doc AUTHORS LICENSE NEWS.md README.md THANKS
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
%{_libdir}/cmake/libzip
%{_pkgconfigdir}/libzip.pc
%{_mandir}/man3/ZIP_SOURCE_GET_ARGS.3*
%{_mandir}/man3/libzip.3*
%{_mandir}/man3/zip_*.3*
# FIXME: should be man3
%{_mandir}/man5/zip.5*
%{_mandir}/man5/zip_error.5*
%{_mandir}/man5/zip_file.5*
%{_mandir}/man5/zip_source.5*
