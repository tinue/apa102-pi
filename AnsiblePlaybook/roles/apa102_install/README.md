apa102-install
==============

The role will clone the apa102 library from Github, and prepare a working Python virtual environment for the code to run in.
It will also enable SPI (bus 0).


Role Variables
--------------

* `apa102_install_dev_dir`: Directory relative to home into which the apa102 library is getting checked out. Default is 'Development'.


Example Playbook
----------------

Install the library to `~/Development/apa102-pi`: 

```
- name: Install apa-102
  hosts: ledpi.local
  roles:
    - role: apa102_install
```

Install the library to `~/projects/apa102-pi`: 

```
- name: Install apa-102
  hosts: ledpi.local
  roles:
    - role: apa102_install
      vars:
        apa102_install_dev_dir: projects
```

License
-------

GPLv3
