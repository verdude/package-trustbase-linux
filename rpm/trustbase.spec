%define version     1.0.0
%define name        trustbase
%define install_dir /usr/lib

Name: %{name}
Version: %{version}
Release: 1
License: GPL
Group: Security
Summary: An OS service to repair and strengthen TLS certificate validation
URL: https://owntrust.org
Source0: %{name}-%{version}.tar.gz
Distribution: Linux

BuildRequires: openssl-devel
BuildRequires: libconfig-devel
BuildRequires: libnl3-devel
BuildRequires: libsqlite3x-devel
BuildRequires: libcap-devel
BuildRequires: python-devel
BuildRequires: libevent-devel
BuildRequires: pyOpenSSL
BuildRequires: git

%description
TrustBase is an operating system service that grants administrators strict controls over how all incoming TLS certificates are validated. It installs a loadable kernel module (LKM) that transparently captures TLS (and SSL) handshake messages sent between the local machine and a remote host. It then extracts certificate and other relevant information and validates them according to adminisrator preferences, as indicated by a configuration file. Administrators may install additional "plugins", services that perform additional or replacement certificate validation, and also control how validation decisions from these plugins are aggregated.

%global debug_package %{nil}

%prep
%autosetup -n trustbase-linux
git submodule init
git submodule update

%build
cd sslsplit
make
cd ..
make

%install
make install
mkdir -p %{buildroot}%{install_dir}
cp -r build/* %{buildroot}%{install_dir}

%files
# include all of the files in the install dir
%{install_dir}/

