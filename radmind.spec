Summary:	Remotely administer the file systems of multiple unix machines
Name:		radmind
Version:	1.8.1
Release:	%mkrel 2
License:	BSD-like
Group:		System/Servers
URL:		http://rsug.itd.umich.edu/
Source0:	http://rsug.itd.umich.edu/software/radmind/files/%{name}-%{version}.tar.gz
Source2:	radmind-1.3.2-init
Source3:	radmind-1.3.2-sysconfig
Source4:	radmind-1.3.2-config
Source5:	radmind-1.3.2-pam
Source6:        radmind-1.3.2.pam-0.77
Patch0:		radmind-system_libs.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	diffutils
Requires:	openssl
BuildRequires:	openssl-devel
BuildRequires:	libsnet-devel >= 20060523
BuildRequires:	pam-devel
BuildRequires:	libsasl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
A suite of Unix command-line tools and a server designed to remotely administer
the file systems of multiple Unix machines.

At its core, radmind operates as a tripwire. It is able to detect changes to
any managed filesystem object, e.g. files, directories, links, etc. However,
radmind goes further than just integrity checking: once a change is detected,
radmind can optionally reverse the change.

Each managed machine may have its own loadset composed of multiple, layered
overloads. This allows, for example, the operating system to be described
separately from applications.

Loadsets are stored on a remote server. By updating a loadset on the server,
changes can be pushed to managed machines.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0 -b .system_snet_libs

mkdir -p Mandriva
cp %{SOURCE2} Mandriva/radmind-1.3.2-init
cp %{SOURCE3} Mandriva/radmind-1.3.2-sysconfig
cp %{SOURCE4} Mandriva/radmind-1.3.2-config
%if %{mdkversion} < 200610
cp %{SOURCE5} Mandriva/radmind-1.3.2-pam
%else
cp %{SOURCE6} Mandriva/radmind-1.3.2-pam
%endif

%build
%serverbuild
#export LIBS="$LIBS -lsasl"

%configure2_5x \
    --with-server="localhost" \
    --with-radminddir=%{_localstatedir}/radmind \
    --with-ssl=%{_prefix}

perl -pi -e "s|^GNU_DIFF.*|GNU_DIFF=%{_bindir}/diff|g" Makefile
perl -pi -e "s|^CERTDIR.*|CERTDIR=%{_sysconfdir}/pki/radmind|g" Makefile
perl -pi -e "s|^RADMINDSYSLOG.*|RADMINDSYSLOG=LOG_LOCAL7|g" Makefile

%make \
    OPTOPTS="%{optflags}" \
    VERSION="%{version}-%{release}"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_localstatedir}/radmind/command
install -d %{buildroot}%{_localstatedir}/radmind/file
install -d %{buildroot}%{_localstatedir}/radmind/special
install -d %{buildroot}%{_localstatedir}/radmind/tmp
install -d %{buildroot}%{_localstatedir}/radmind/tmp/file
install -d %{buildroot}%{_localstatedir}/radmind/tmp/transcript
install -d %{buildroot}%{_localstatedir}/radmind/transcript

%makeinstall_std

install -m0755 Mandriva/radmind-1.3.2-init %{buildroot}%{_initrddir}/radmind
install -m0644 Mandriva/radmind-1.3.2-sysconfig %{buildroot}%{_sysconfdir}/sysconfig/radmind
install -m0644 Mandriva/radmind-1.3.2-config %{buildroot}%{_localstatedir}/radmind/config
install -m0644 Mandriva/radmind-1.3.2-pam %{buildroot}%{_sysconfdir}/pam.d/radmind

%post
%_post_service radmind

%preun
%_preun_service radmind

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT README SPEC
%attr(0755,root,root) %{_initrddir}/radmind
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/radmind
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/radmind
%attr(0750,root,root) %dir %{_localstatedir}/radmind
%attr(0644,root,root) %config(noreplace) %{_localstatedir}/radmind/config
%attr(0750,root,root) %dir %{_sysconfdir}/pki/radmind
%{_bindir}/*
%{_sbindir}/*
%attr(0750,root,root) %dir %{_localstatedir}/radmind/command
%attr(0750,root,root) %dir %{_localstatedir}/radmind/file
%attr(0750,root,root) %dir %{_localstatedir}/radmind/special
%attr(0750,root,root) %dir %{_localstatedir}/radmind/tmp
%attr(0750,root,root) %dir %{_localstatedir}/radmind/tmp/file
%attr(0750,root,root) %dir %{_localstatedir}/radmind/tmp/transcript
%attr(0750,root,root) %dir %{_localstatedir}/radmind/transcript
%{_mandir}/man?/*
