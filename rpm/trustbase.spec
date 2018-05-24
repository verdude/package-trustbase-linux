%define version           1.0.0
%define name              trustbase-linux
%define module            trustbase_linux
%define trustbase_config  trustbase.cfg
%define install_dir       %{_libdir}/%{name}
%define local_install_dir build
%define dkms_src_dir      %{_usrsrc}/%{name}-%{version}
%define debug_package     %{nil}
%define startup_options   %{_sysconfdir}/modprobe.d/%{name}.conf
%define startup_conf      %{_sysconfdir}/modules-load.d/%{name}.conf

Name: %{name}
Version: %{version}
Release: 1
License: Public Domain
Group: Security
Summary: Trustbase Kernel Module and addons
URL: https://internet.byu.edu/research/trustbase
# This needs to be updated when a release is actually made
Source0: %{name}-%{version}.tar.gz
Distribution: Linux

# These build tools are required because
# the kernel module is built although it is not packaged
BuildRequires: git
BuildRequires: openssl-devel
BuildRequires: libconfig-devel
BuildRequires: libnl3-devel
BuildRequires: libsqlite3x-devel
BuildRequires: libcap-devel
BuildRequires: python-devel
BuildRequires: libevent-devel
BuildRequires: pyOpenSSL

# The kernel module is built on the end user's
# system and so the build tools are required for them as well
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
Requires: dkms >= 1

%description
This package contains the Trustbase module wrapped
for the DKMS framework.
As well as plugins and configuration for Trustbase.

%prep
%autosetup
git submodule init
git submodule update
# change the install directory prefix from /usr/lib/trustbase-linux to %{local_install_dir}
sed -i 's/^PREFIX = \S*$/PREFIX = %{local_install_dir}/g' Makefile
cp ../dkms.conf .

%build
make -C sslsplit
make addons

%install
make install-addons
mkdir -p %{buildroot}%{install_dir}
cp -r %{local_install_dir}/* %{buildroot}%{install_dir}
mkdir -p %(dirname %{buildroot}%{startup_conf})
mkdir -p %(dirname %{buildroot}%{startup_options})
echo "%{module}" > %{buildroot}%{startup_conf}
echo "options %{module} tb_path=%{install_dir}" > %{buildroot}%{startup_options}
# place the trustbase kernel module code tree in the %{dkms_src_dir} directory for dkms
mkdir -p %{buildroot}%{dkms_src_dir}
for files in loader.{h,c} \
        interceptor/interceptor.{h,c} \
        interceptor/connection_state.{h,c} \
        handshake-handler/handshake_handler.{h,c} \
        handshake-handler/communications.{h,c} \
        util/utils.{h,c} \
        util/ktb_logging.{h,c} \
        policy-engine/policy_response.h \
        Makefile; do
    cp --parents $files %{buildroot}%{dkms_src_dir}
done
cp dkms.conf %{buildroot}%{dkms_src_dir}

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
ln -sf %{install_dir}/policy-engine/%{trustbase_config} %{_sysconfdir}/%{trustbase_config}
modprobe %{module} tb_path="%{_libdir}/%{name}"
exit 0

%preun
modprobe -r %{module}
# remove config symlink
rm -f %{_sysconfdir}/%{trustbase_config}
echo -e
echo -e "Uninstall of %{name} module (version %{version}) beginning:"
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade
exit 0

%files
%defattr(-,root,root)
%{dkms_src_dir}/
%{install_dir}/certs/ca.crt
%{install_dir}/certs/ca.key
%{install_dir}/policy_engine
%{install_dir}/policy-engine/plugin-config/
%{install_dir}/policy-engine/addons/python_plugins.so
%{install_dir}/policy-engine/plugins/
%{install_dir}/sslsplit/sslsplit
%{install_dir}/policy-engine/%{trustbase_config}
%{startup_conf}
%{startup_options}

%changelog
* Wed May 23 2018 Santiago Verdu santiagoverdu01@gmail.com 1.0.0-1
- Initial RPM release

