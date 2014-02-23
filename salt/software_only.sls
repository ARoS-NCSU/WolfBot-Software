/wolfbot/agent:
    file.recurse:
        - name: /wolfbot/agent
        - source: salt://files/wolfbot/agent  # change to github tree on pm?
        - clean: True
        
/wolfbot/config:
    file.recurse:
        - name: /wolfbot/config
        - source: salt://files/wolfbot/config
        - clean: True
        
/wolfbot/setup:
    file.recurse:
        - name: /wolfbot/setup
        - source: salt://files/wolfbot/setup
        - clean: True
        - file_mode: 755
        
/wolfbot/util:
    file.recurse:
        - name: /wolfbot/util
        - source: salt://files/wolfbot/util
        - clean: True
        - file_mode: 755
        
/wolfbot/demos:
    file.recurse:
        - name: /wolfbot/demos
        - source: salt://files/wolfbot/demos
        - clean: True
        - file_mode: 755
        
/wolfbot/lib:
    file.recurse:
        - name: /wolfbot/lib
        - source: salt://files/wolfbot/lib
        - clean: True
        - file_mode: 755

# vim: set syntax=yaml :
