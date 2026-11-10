%global debug_package %{nil}
%global _build_id_links none
%global __os_install_post %{nil}

Name:           ty
Version:        0.0.100
Release:        1%{?dist}
Summary:        Extremely fast Python type checker and language server
License:        MIT
URL:            https://github.com/astral-sh/ty
Source0:        https://github.com/astral-sh/ty/releases/download/%{version}/ty-x86_64-unknown-linux-gnu.tar.gz
Source1:        https://github.com/astral-sh/ty/releases/download/%{version}/ty-x86_64-unknown-linux-gnu.tar.gz.sha256
BuildArch:      x86_64

%description
An extremely fast Python type checker and language server, written in Rust.
Provides comprehensive diagnostics with rich contextual information,
configurable rule levels, and first-class editor integrations.

%prep
%setup -q -c -T
# Verify the SHA256 checksum
sha256sum -c %{SOURCE1} || exit 1
# The tarball extracts to a directory named 'ty-<version>'
mkdir -p ty
tar -xf %{SOURCE0} -C ty --strip-components=1

%build
# Prebuilt binary from upstream — nothing to build.

%install
install -Dpm 0755 ty/ty %{buildroot}%{_bindir}/ty

%check
test "$(%{buildroot}%{_bindir}/ty --version)" = "ty %{version}"

%files
%license ty/LICENSE
%doc ty/README.md
%{_bindir}/ty

%changelog
* Tue Nov 10 2026 halcyon-linux <aahsnr041@proton.me> - 0.0.100-1
- Package the upstream ty 0.0.100 binary release