Summary:	Synchronization for TeX
Summary(pl.UTF-8):	Synchronizacja dla TeXa
Name:		synctex
%define	gitref	3131eee3509298751a5991a4a748bcaa8b51f56c
%define	snap	20171128
%define	rel	1
Version:	1.21
Release:	1.%{snap}.%{rel}
License:	MIT
Group:		Applications/Text
Source0:	https://github.com/jlaurens/synctex/archive/%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	419ba7bbca0714bd16246b66f92b2153
URL:		https://github.com/jlaurens/synctex
BuildRequires:	libtool
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SyncTeX is a utility which enables synchronization between your source
document and the PDF output.

%description -l pl.UTF-8
SyncTeX to narzędzie pozwalające na synchronizację między dokumentem
źródłowym a wyjściem PDF.

%package libs
Summary:	SyncTeX parser library
Summary(pl.UTF-8):	Biblioteka analizatora SyncTeX
Group:		Libraries

%description libs
SyncTeX parser library.

%description libs -l pl.UTF-8
Biblioteka analizatora SyncTeX.

%package devel
Summary:	Header files for synctex library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki synctex
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	zlib-devel

%description devel
Header files for synctex library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki synctex.

%package static
Summary:	Static synctex library
Summary(pl.UTF-8):	Statyczna biblioteka synctex
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static synctex library.

%description static -l pl.UTF-8
Statyczna biblioteka synctex.

%prep
%setup -q -n %{name}-%{gitref}

cat >synctex_parser_c-auto.h <<EOF
#define HAVE_FMAX 1
#define HAVE_LOCALE_H 1
#define SETLOCALE 1
#define SYNCTEX_INLINE inline
EOF

%build
libtool --mode=compile %{__cc} %{rpmcflags} %{rpmcppflags} -I. -c synctex_parser.c
libtool --mode=compile %{__cc} %{rpmcflags} %{rpmcppflags} -I. -c synctex_parser_utils.c
libtool --mode=compile %{__cc} %{rpmcflags} %{rpmcppflags} -I. -D__SYNCTEX_WORK__ -c synctex_main.c

libtool --mode=link %{__cc} %{rpmldflags} %{rpmcflags} -o libsynctex.la -rpath %{_libdir} -no-undefined -version-info 22:0:21 synctex_parser.lo synctex_parser_utils.lo -lz -lm
libtool --mode=link %{__cc} %{rpmldflags} %{rpmcflags} -o synctex synctex_main.lo libsynctex.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/synctex,%{_pkgconfigdir}}

libtool --mode=install install libsynctex.la $RPM_BUILD_ROOT%{_libdir}
libtool --mode=install install synctex $RPM_BUILD_ROOT%{_bindir}

cp -p synctex_parser.h synctex_parser_utils.h $RPM_BUILD_ROOT%{_includedir}/synctex

cat >>$RPM_BUILD_ROOT%{_pkgconfigdir}/synctex.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: synctex
Description: SyncTeX parser library
Version: %{version}
Requires.private: zlib
Libs: -L${libdir} -lsynctex
Cflags: -I${includedir}/synctex
EOF

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsynctex.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md synctex_parser_readme.md
%attr(755,root,root) %{_bindir}/synctex

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsynctex.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsynctex.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsynctex.so
%{_includedir}/synctex
%{_pkgconfigdir}/synctex.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsynctex.a
