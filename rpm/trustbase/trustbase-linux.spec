%define module trustbase_linux
%define name   trustbase-linux
%define version 1.0.0

Summary: %{name} dkms package
Name: %{name}
Version: %{version}
Release: 2dkms
Vendor: LSI
License: GPL
Packager: Santiago Verdu santiagoverdu@protonmail.com
Group: Security
BuildArch: noarch
Requires: dkms >= 1.00
Requires: bash
# There is no Source# line for dkms.conf since it has been placed
# into the source tarball of SOURCE0
Source0: %{name}-%{version}.tar.gz

Requires: openssl-devel
Requires: libconfig-devel
Requires: libnl3-devel
Requires: libsqlite3x-devel
Requires: libcap-devel
Requires: python-devel
Requires: libevent-devel
Requires: pyOpenSSL
Requires: kernel-devel >= 4.5
Requires: kernel-headers >= 4.5
Requires: %{name}-config >= %{version}

%description
This package contains the trustbase module wrapped
for the DKMS framework.

%prep
%autosetup

%install
mkdir -p %{buildroot}/usr/src/%{name}-%{version}/
cp -rf ./* %{buildroot}/usr/src/%{name}-%{version}

%post
dkms add -m %{name} -v %{version} --rpm_safe_upgrade

if [ `uname -r | grep -c "BOOT"` -eq 0 ] && [ -e /lib/modules/`uname -r`/build/include ]; then
    dkms build -m %{name} -v %{version}
    dkms install -m %{name} -v %{version}
elif [ `uname -r | grep -c "BOOT"` -gt 0 ]; then
    echo -e ""
    echo -e "Module build for the currently running kernel was skipped since you"
    echo -e "are running a BOOT variant of the kernel."
else
    echo -e ""
    echo -e "Module build for the currently running kernel was skipped since the"
    echo -e "kernel headers for this kernel do not seem to be installed."
fi
modprobe %{module} tb_path="%{_libdir}/%{name}-config"
exit 0

%preun
modprobe -r %{module}
echo -e
echo -e "Uninstall of %{name} module (version %{version}) beginning:"
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade
exit 0

%files
%defattr(-,root,root)
/usr/src/%{name}-%{version}/

