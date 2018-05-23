%define version          1.0.0
%define kmod_package     trustbase-linux
%define name             %{kmod_package}-config
%define kmod_name        trustbase_linux
%define trustbase_config trustbase.cfg
%define install_dir      %{_libdir}/%{name}
%define debug_package    %{nil}

Name: %{name}
Version: %{version}
Release: 1
License: Public Domain
Group: Security
Summary: Trustbase Policy Engine and Configuration
URL: https://internet.byu.edu/research/trustbase
# This needs to be updated when a release is actually made
Source0: trustbase-linux-1.0.0.tar.gz
Distribution: Linux

BuildRequires: openssl-devel
BuildRequires: libconfig-devel
BuildRequires: libnl3-devel
BuildRequires: libsqlite3x-devel
BuildRequires: libcap-devel
BuildRequires: python-devel
BuildRequires: libevent-devel
BuildRequires: pyOpenSSL
BuildRequires: kernel-devel >= 4.5
BuildRequires: kernel-headers >= 4.5

%description
Plugins and Config for Trustbase.

%prep
%autosetup -n %{kmod_package}
git submodule init
git submodule update

%build
make -C sslsplit
make

%install
make install
# don't include the kernel module in this package
rm build/trustbase_linux.ko
mkdir -p %{buildroot}%{install_dir}
cp -r build/* %{buildroot}%{install_dir}
mkdir -p %{buildroot}%{_sysconfdir}/modules-load.d/
echo %{kmod_name} tb_path="%{install_dir}"> %{buildroot}%{_sysconfdir}/modules-load.d/%{name}.conf

%post
ln -sf %{install_dir}/policy-engine/%{trustbase_config} %{_sysconfdir}/%{trustbase_config}

%postun
rm -f %{_sysconfdir}/%{trustbase_config}

%files
%{install_dir}/certs/ca.crt
%{install_dir}/certs/ca.key
%{install_dir}/Module.symvers
%{install_dir}/modules.order
%{install_dir}/policy_engine
%{install_dir}/policy-engine/plugin-config/
%{install_dir}/policy-engine/addons/python_plugins.so
%{install_dir}/policy-engine/plugins/
%{install_dir}/sslsplit/sslsplit
%{install_dir}/policy-engine/%{trustbase_config}
%{_sysconfdir}/modules-load.d/%{name}.conf

%changelog
* Mon May 14 2018 Santiago Verdu santiagoverdu@protonmail.com 1.0.0-1
- Initial RPM release

