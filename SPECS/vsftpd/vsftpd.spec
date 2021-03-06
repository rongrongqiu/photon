Summary:	Very secure and very small FTP daemon.
Name:		vsftpd
Version:	3.0.2
Release:	1
License:	GPLv2 with exceptions
URL:		https://security.appspot.com/vsftpd.html
Group:		System Environment/Daemons
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://security.appspot.com/downloads/%{name}-%{version}.tar.gz
%define sha1 vsftpd=f36976bb1c5df25ac236d8a29e965ba2b825ccd0
BuildRequires:	libcap Linux-PAM openssl-devel
Requires:	libcap Linux-PAM openssl
%description
Very secure and very small FTP daemon.
%prep
%setup -q
%build
sed -i -e 's|#define VSF_SYSDEP_HAVE_LIBCAP|//&|' sysdeputil.c
make %{?_smp_mflags}
%install
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/{man5,man8}
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vm 755 vsftpd        %{buildroot}%{_sbindir}/vsftpd
install -vm 644 vsftpd.8      %{buildroot}%{_mandir}/man8/
install -vm 644 vsftpd.conf.5 %{buildroot}%{_mandir}/man5/
cat >> %{buildroot}/etc/vsftpd.conf << "EOF"
background=YES
listen=YES
nopriv_user=vsftpd
secure_chroot_dir=/usr/share/vsftpd/empty
pasv_enable=Yes
pasv_min_port=40000
pasv_max_port=40100
#allow_writeable_chroot=YES
#write_enable=YES
#local_umask=022 
#anon_upload_enable=YES
#anon_mkdir_write_enable=YES
EOF

%post
install -v -d -m 0755 %{_datadir}/vsftpd/empty
install -v -d -m 0755 /home/ftp
if ! getent group vsftpd >/dev/null; then
    groupadd -g 47 vsftpd
fi
if ! getent group ftp >/dev/null; then
    groupadd -g 45 ftp
fi
if ! getent passwd vsftpd >/dev/null; then
    useradd -c "vsftpd User"  -d /dev/null -g vsftpd -s /bin/false -u 47 vsftpd
fi
if ! getent passwd ftp >/dev/null; then
    useradd -c anonymous_user -d /home/ftp -g ftp    -s /bin/false -u 45 ftp
fi

%postun
if getent passwd vsftpd >/dev/null; then
    userdel vsftpd
fi
if getent passwd ftp >/dev/null; then
    userdel ftp
fi
if getent group vsftpd >/dev/null; then
    groupdel vsftpd
fi

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_datadir}/*
%exclude %{_libdir}/debug
%changelog
*	Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 3.0.2-1
-	initial version
