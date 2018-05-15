%define version       1.0.0
%define name          trustbase-linux
%define kmod          trustbase_linux
%define install_dir   %{_libdir}/%{name}
%define module_dir    /lib/modules/%(uname -r)/kernel/net/%{name}
%define debug_package %{nil}

Name: %{name}
Version: %{version}
Release: 1
License: Public Domain
Group: Security
Summary: An OS service to repair and strengthen TLS certificate validation
URL: https://internet.byu.edu/research/trustbase
# This needs to be updated when a release is actually made
Source0: https://github.com/markoneill/%{name}/archive/%{name}-%{version}.tar.gz
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
TLS certificate validation.

%prep
%autosetup -n %{name}
git submodule init
git submodule update

%build
make -C sslsplit
make

%install
make install
mkdir -p %{buildroot}%{install_dir}
cp -r build/* %{buildroot}%{install_dir}
mkdir -p %{buildroot}/etc/modules-load.d/
echo %{install_dir}/%{kmod}.ko \\> %{buildroot}/etc/modules-load.d/%{name}.conf

%post
# Create directory in which to store the kernel module
# insmod does not detect symlinked files
# insmod won't load the module if it is not in /lib/modules/%(uname -r)/
mkdir -p %{module_dir}
cp %{install_dir}/%{kmod}.ko %{module_dir}/%{kmod}.ko
insmod %{module_dir}/%{kmod}.ko tb_path=%{install_dir}

%postun
rmmod %{module_dir}/%{kmod}.ko
rm %{module_dir}/%{kmod}.ko
rmdir %{module_dir}

%files
%defattr(644,root,root,755)
%{install_dir}/
/etc/modules-load.d/%{name}.conf

%changelog
* Mon May 14 2018 Santiago Verdu santiagoverdu@protonmail.com 1.0.0-1
- Initial RPM release

