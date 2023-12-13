%define _unpackaged_files_terminate_build 1

Name: adt-tool-example
Version: 0.0.1
Release: alt1

Summary: Example tool for ADT.
License: GPLv2+
Group: Other
URL: https://github.com/AlexSP0/adt-tool-example

BuildArch: noarch

Source0: %name-%version.tar

%description
Example tool for ADT.

%prep
%setup

%install
mkdir -p %buildroot%_libexecdir/%name
mkdir -p %buildroot%_datadir/alterator/backends
mkdir -p %buildroot%_datadir/alterator/objects/%name

install -v -p -m 755 -D adt-tool-example %buildroot%_libexecdir/%name
install -v -p -m 644 -D adt-example.backend %buildroot%_datadir/alterator/backends
install -v -p -m 655 -D adt-example.alterator %buildroot%_datadir/alterator/objects/%name

%files
%_libexecdir/%name/adt-tool-example
%_datadir/alterator/backends/adt-example.backend
%_datadir/alterator/objects/%name/adt-example.alterator

%changelog
* Tue Dec 12 2023 Aleksey Saprunov <sav@altlinux.org> 0.0.1-alt1
- initial build
