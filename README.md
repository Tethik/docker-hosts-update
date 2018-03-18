# Readme

`docker_hosts_update` is a script that automatically updates your `/etc/hosts` file 

By default the containers will be given a hostname of `{container name}.{network nake}`.
E.g. The `hello-world` container running in the `corp.internal` network and the `nginx` container
running in the default `bridge` network will be written to your hosts file something like the following. 
```
172.19.0.3   hello-world.corp.internal
172.17.0.4   nginx.bridge
```

Install:
```bash

```


Usage:
```bash
sudo docker_hosts_update
```




Todo before publish:
* document readme
* click document for usage.
* pypi publish 
* systemd config
* tests for main

Future features / ideas:
* configurable host name format
* whitelist / blacklist
* deb package
* user desktop notifications!
* completely different package `docker-event-template` (like `consul-template` with a better templating language)