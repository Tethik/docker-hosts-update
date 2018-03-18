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

## Install
```bash
pip3 install -U docker_hosts_update "git+https://github.com/Spielstunde/docker-hosts-update#egg=docker-hosts-update"
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


Future features / ideas:
* configurable host name format
* whitelist / blacklist
* deb package
* user desktop notifications
* ui to toggle whitelist/blacklist 
* completely different package `docker-event-template` (like `consul-template` with a better templating language)
* another os service: hostctl, just for managing the hosts file (with unix socket to communicate over).
* service security
    * https://www.freedesktop.org/software/systemd/man/systemd.exec.html#Capabilities
    * CAP_FOWNER ?