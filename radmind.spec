Summary:	Remotely administer the file systems of multiple unix machines
Name:		radmind
Version:	1.11.1
Release:	%mkrel 7
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
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

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
    --with-radminddir=%{_localstatedir}/lib/radmind \
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
install -d %{buildroot}%{_localstatedir}/lib/radmind/command
install -d %{buildroot}%{_localstatedir}/lib/radmind/file
install -d %{buildroot}%{_localstatedir}/lib/radmind/special
install -d %{buildroot}%{_localstatedir}/lib/radmind/tmp
install -d %{buildroot}%{_localstatedir}/lib/radmind/tmp/file
install -d %{buildroot}%{_localstatedir}/lib/radmind/tmp/transcript
install -d %{buildroot}%{_localstatedir}/lib/radmind/transcript

%makeinstall_std

install -m0755 Mandriva/radmind-1.3.2-init %{buildroot}%{_initrddir}/radmind
install -m0644 Mandriva/radmind-1.3.2-sysconfig %{buildroot}%{_sysconfdir}/sysconfig/radmind
install -m0644 Mandriva/radmind-1.3.2-config %{buildroot}%{_localstatedir}/lib/radmind/config
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
%attr(0750,root,root) %dir %{_localstatedir}/lib/radmind
%attr(0644,root,root) %config(noreplace) %{_localstatedir}/lib/radmind/config
%attr(0750,root,root) %dir %{_sysconfdir}/pki/radmind
%{_bindir}/*
%{_sbindir}/*
%attr(0750,root,root) %dir %{_localstatedir}/lib/radmind/command
%attr(0750,root,root) %dir %{_localstatedir}/lib/radmind/file
%attr(0750,root,root) %dir %{_localstatedir}/lib/radmind/special
%attr(0750,root,root) %dir %{_localstatedir}/lib/radmind/tmp
%attr(0750,root,root) %dir %{_localstatedir}/lib/radmind/tmp/file
%attr(0750,root,root) %dir %{_localstatedir}/lib/radmind/tmp/transcript
%attr(0750,root,root) %dir %{_localstatedir}/lib/radmind/transcript
%{_mandir}/man?/*


%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.11.1-7mdv2011.0
+ Revision: 614698
- the mass rebuild of 2010.1 packages

* Tue Apr 13 2010 Funda Wang <fwang@mandriva.org> 1.11.1-6mdv2010.1
+ Revision: 533752
- rebuild

* Tue Sep 08 2009 Thierry Vignaud <tv@mandriva.org> 1.11.1-5mdv2010.0
+ Revision: 433052
- rebuild

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 1.11.1-4mdv2009.0
+ Revision: 260012
- rebuild

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 1.11.1-3mdv2009.0
+ Revision: 247817
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Tue Jan 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1.11.1-1mdv2008.1
+ Revision: 152175
- 1.11.1
- rediffed P0

* Wed Dec 19 2007 Oden Eriksson <oeriksson@mandriva.com> 1.11.0-1mdv2008.1
+ Revision: 134302
- 1.11.0

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 31 2007 Oden Eriksson <oeriksson@mandriva.com> 1.10.0-1mdv2008.0
+ Revision: 77088
- 1.10.0
- conform to the 2008 specs (don't start it per default)

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 1.8.1-2mdv2008.0
+ Revision: 45194
- fix pam file (#31655)
- rebuild with serverbuild macro (-fstack-protector-all)

* Fri May 25 2007 Oden Eriksson <oeriksson@mandriva.com> 1.8.1-1mdv2008.0
+ Revision: 30993
- fix build deps (zlib-devel)
- fix build deps (libsasl-devel)
- Import radmind



* Thu May 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1.8.1-1mdv2008.0
- 1.8.1
- rediffed P0

* Mon Jun 26 2006 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-1mdv2007.0
- 1.6.1
- rediffed P0
- drop upstream patches; P1
- fix deps

* Sun Dec 25 2005 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-1mdk
- 1.5.1 (Minor feature enhancements)

* Thu Dec 01 2005 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-2mdk
- rebuilt against openssl-0.9.8a

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5.0-1mdk
- 1.5.0

* Sun Jan 30 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.4.1-1mdk
- 1.4.1

* Tue Jan 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.4.0-1mdk
- 1.4.0
- rediffed P0 and P1

* Sun Nov 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.3.2-2mdk
- fix deps

* Sun Nov 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.3.2-1mdk
- initial mandrake package
