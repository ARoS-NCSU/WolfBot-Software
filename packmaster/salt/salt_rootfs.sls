/srv/salt/top.sls:
    file.managed:
        - source: salt://salt/top.sls

/srv/salt/wolfbot.sls:
    file.managed:
        - source: salt://salt/wolfbot.sls

# files.recurse broken in salt 17.4!
/srv/salt/_grains:
    file.recurse:
        - source: salt://salt/_grains
        - clean: True

/srv/salt/files:
    file.recurse:
        - source: salt://salt/files
        - clean: True


# vim: set syntax=yaml :
