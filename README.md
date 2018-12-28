# Readme

`docker_hosts_update` is a small program that automatically updates your `/etc/hosts` file,
giving your docker containers hostnames.

By default the containers will be given a hostname of `{container name}.{network name}`.
E.g. The `hello-world` container running in the `corp.internal` network and the `nginx` container
running in the default `bridge` network will be written to your hosts file something like the following. 
```
172.19.0.3   hello-world.corp.internal
172.17.0.4   nginx.bridge
```

## Compatibility
⚠️ Currently this program is only known to work on Linux. 

It will not work on Windows because Windows uses a different location for the hosts file.

Mac OS does not seem to work due to some differences in how the hosts file is written. I'm unsure what these differences are,
but Mac OS will not correctly apply the changes.

If you are a Mac/Windows user and you want to use this program, let us know that you are interested.
Of course, we would also appreciate it if you could to contribute the necessary changes.


## Install
```bash
sudo pip3 install -U "git+https://github.com/Tethik/docker-hosts-update#egg=docker-hosts-update"
```


## Usage
```bash
Usage: docker_hosts_update [OPTIONS]

  Program that automatically updates your `/etc/hosts` file based on your
  running docker containers.

Options:
  --hosts-file TEXT    The hosts file to update.
  --once               Run the update script once only.
  --initial            Run the update script one time before hooking into the
                       docker event stream.
  -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --help               Show this message and exit.
```

Running it in a shell:
```
sudo docker_hosts_update
```

Systemd init script to run it as a service:
```
[Unit]
Description=Updates /etc/hosts based on running docker containers.
After=network.target

[Service]
ExecStart=/usr/local/bin/docker-hosts-update
Restart=on-failure # or always, on-abort, etc

[Install]
WantedBy=multi-user.target
```


