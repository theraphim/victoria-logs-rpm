%define debug_package %{nil}
%define __strip /bin/true

%global forgeurl https://github.com/VictoriaLogs/VictoriaLogs
Name:     VictoriaLogs
Version:  1.33.1
%forgemeta
Release:  %autorelease
Summary:  High-performance, cost-effective and scalable logs storage.
License:  Proprietary
URL:      https://victoriametrics.com/
Source:  %{forgesource}
Source100: victoria-logs.service
Source200: victoria-logs.sysusers
Source300: victoria-logs.sysconfig
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

%description
High-performance, cost-effective and scalable logs storage.

%prep
%forgesetup

%build
make BUILDINFO_TAG=%{version} victoria-logs vlogscli vlagent

%pre
%sysusers_create_compat %{SOURCE200}

%post
%systemd_post victoria-logs.service

%preun
%systemd_preun victoria-logs.service

%postun
%systemd_postun_with_restart victoria-logs.service

%install
%{__install} -v -D -t $RPM_BUILD_ROOT%{_unitdir} %{SOURCE100}

%{__install} -m 0755 -v -D -t %{buildroot}%{_bindir} bin/victoria-logs bin/vlogscli bin/vlagent
%{__install} -p -D -m 0644 %{SOURCE201} %{buildroot}%{_sysusersdir}/victoria-logs.conf

%{__install} -d -m 0755 %{buildroot}%{_sharedstatedir}/victoria-logs

%{__install} -p -D -m 644 %{SOURCE301} %{buildroot}%{_sysconfdir}/sysconfig/victoria-logs

%files
%{_sysusersdir}/victoria-logs.conf
%{_unitdir}/victoria-logs.service
%{_bindir}/victoria-logs
%{_bindir}/vlogscli
%{_bindir}/vlagent
%dir %attr(-,victoria-logs,victoria-logs) %{_sharedstatedir}/victoria-logs
%config(noreplace) %{_sysconfdir}/sysconfig/victoria-logs

%license 
%doc 

%changelog
%autochangelog
