en_US.UTF-8:
    locale.system

America/New_York:
    timezone.system:
        - utc: True

ntp:
    pkg:
        - installed
    service:
        - running
        - enable: True
        - watch:
            - file: /etc/ntp.conf
    file.managed:
        - name: /etc/ntp.conf
        - source: salt://files/etc/ntp.conf
        - user: root
        - group: root
        - mode: 644

saltstack_repo:
  pkgrepo.managed:
    - name: deb http://debian.saltstack.com/debian wheezy-saltstack main
    - file: /etc/apt/sources.list.d/saltstack.list
    - gpgkey: http://debian.saltstack.com/debian-salt-team-joehealy.gpg.key 
    - require_in:
        - pkg: salt-minion
    - require:
        - pkg: python-apt

salt-minion:
    pkg.installed:
        - version: 0.17.4-1~bpo70+1~dst.1
        - skip_verify: True
    service:
        - running
        - enable: True
        - watch:
            - file: /etc/salt/minion

/etc/salt/minion:
    file.managed:
        - source: salt://files/etc/salt/minion

python-apt:
    pkg.installed

# only install during bootstrap?
/etc/salt/pki/minion/minion_master.pub:
    file.managed:
        - source: salt://files/etc/salt/pki/minion/minion_master.pub

# vim: set syntax=yaml :
