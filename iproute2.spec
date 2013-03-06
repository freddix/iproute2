Summary:	Utility to control Networking behavior in.X kernels
Name:		iproute2
Version:	3.8.0
Release:	2
License:	GPL
Group:		Networking/Admin
Source0:	http://www.kernel.org/pub/linux/utils/net/iproute2/%{name}-%{version}.tar.xz
# Source0-md5:	951622fd770428116dc165acba375414
Patch0:		%{name}-LDFLAGS.patch
Patch1:		%{name}-fhs.patch
URL:		http://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	flex
BuildRequires:	iptables-devel
BuildRequires:	linux-libc-headers >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/iproute2

%description
Linux maintains compatibility with the basic configuration utilities
of the network (ifconfig, route) but a new utility is required to
exploit the new characteristics and features of the kernel. This
package includes the new utilities.

%package -n libnetlink-devel
Summary:	Library for the netlink interface
Group:		Development/Libraries

%description -n libnetlink-devel
This library provides an interface for kernel-user netlink interface.

%prep
%setup -q
rm -rf include-glibc include/linux
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}"		\
	HOSTCC="%{__cc}"	\
	LD="%{__cc}"		\
	LDFLAGS="%{rpmldflags}"	\
	LIBDIR="%{_libdir}"	\
	OPT="%{rpmcflags}"	\
	SUBDIRS="lib ip misc"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT	\
	LIBDIR="%{_libdir}"

install lib/libnetlink.a $RPM_BUILD_ROOT%{_libdir}
install include/libnetlink.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.decnet README.iproute2+tc README.lnstat
%attr(755,root,root) %{_sbindir}/arpd
%attr(755,root,root) %{_sbindir}/bridge
%attr(755,root,root) %{_sbindir}/ctstat
%attr(755,root,root) %{_sbindir}/genl
%attr(755,root,root) %{_sbindir}/ifcfg
%attr(755,root,root) %{_sbindir}/ifstat
%attr(755,root,root) %{_sbindir}/ip
%attr(755,root,root) %{_sbindir}/lnstat
%attr(755,root,root) %{_sbindir}/nstat
%attr(755,root,root) %{_sbindir}/routef
%attr(755,root,root) %{_sbindir}/routel
%attr(755,root,root) %{_sbindir}/rtacct
%attr(755,root,root) %{_sbindir}/rtmon
%attr(755,root,root) %{_sbindir}/rtpr
%attr(755,root,root) %{_sbindir}/rtstat
%attr(755,root,root) %{_sbindir}/ss
%attr(755,root,root) %{_sbindir}/tc

%dir %{_libdir}/tc
%attr(755,root,root) %{_libdir}/tc/*.so

%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_datadir}/tc
%{_mandir}/man8/*

%files -n libnetlink-devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/*.h

