%global debug_package %{nil}
%global _build_id_links none
%global __os_install_post %{nil}

Name:           ruff
Version:        0.17.4
Release:        1%{?dist}
Summary:        Extremely fast Python linter and code formatter
License:        MIT
URL:            https://github.com/astral-sh/ruff
Source0:        https://github.com/astral-sh/ruff/releases/download/%{version}/ruff-x86_64-unknown-linux-gnu.tar.gz
Source1:        https://github.com/astral-sh/ruff/releases/download/%{version}/ruff-x86_64-unknown-linux-gnu.tar.gz.sha256
BuildArch:      x86_64

%description
An extremely fast Python linter and code formatter, written in Rust.
Supports linting, formatting, and code quality checks with a unified CLI.

%prep
%setup -q -c -T
# Verify the SHA256 checksum
sha256sum -c %{SOURCE1} || exit 1
# The tarball extracts to a directory named 'ruff-<version>'
mkdir -p ruff
tar -xf %{SOURCE0} -C ruff --strip-components=1

%build
# Prebuilt binary from upstream — nothing to build.

%install
install -Dpm 0755 ruff/ruff %{buildroot}%{_bindir}/ruff

%check
test "$(%{buildroot}%{_bindir}/ruff --version)" = "ruff %{version}"

%files
%license ruff/LICENSE
%doc ruff/README.md
%{_bindir}/ruff

%changelog
* Tue Nov 10 2026 halcyon-linux <aahsnr041@proton.me> - 0.17.4-1
- Package the upstream ruff 0.17.4 binary release