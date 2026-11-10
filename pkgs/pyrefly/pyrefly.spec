%global debug_package %{nil}
%global _build_id_links none
%global __os_install_post %{nil}

Name:           pyrefly
Version:        1.3.1
Release:        1%{?dist}
Summary:        Fast type checker and language server for Python
License:        MIT
URL:            https://github.com/meta/pyrefly
Source0:        https://github.com/meta/pyrefly/releases/download/%{version}/pyrefly-linux-x86_64.tar.gz
Source1:        https://github.com/meta/pyrefly/releases/download/%{version}/pyrefly-linux-x86_64.tar.gz.sha256
BuildArch:      x86_64

%description
A fast type checker and language server for Python with powerful IDE features.
Provides lightning-fast type checking along with IDE features such as code
navigation, semantic highlighting, and code completion.

%prep
%setup -q -c -T
# Verify the SHA256 checksum
sha256sum -c %{SOURCE1} || exit 1
# The tarball extracts the binary directly
mkdir -p pyrefly
tar -xf %{SOURCE0} -C pyrefly

%build
# Prebuilt binary from upstream — nothing to build.

%install
install -Dpm 0755 pyrefly/pyrefly %{buildroot}%{_bindir}/pyrefly

%check
test "$(%{buildroot}%{_bindir}/pyrefly --version 2>&1)" = "%{version}"

%files
%license pyrefly/LICENSE
%doc pyrefly/README.md
%{_bindir}/pyrefly

%changelog
* Tue Nov 10 2026 halcyon-linux <aahsnr041@proton.me> - 1.3.1-1
- Package the upstream pyrefly 1.3.1 binary release