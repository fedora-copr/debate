# Pulp playbooks in Fedora Infra ansible repo

I successfully migrated Copr pulp playbooks from our private
repository to the Fedora Infra ansible repository. This is a quick
dump of my brain before I move on.


## Infra tickets

There are two relevant Infra tickets (closed, done)

- https://pagure.io/fedora-infrastructure/issue/11395
- https://pagure.io/fedora-infrastructure/issue/11396


## The old repo

The old repository (private)
https://github.com/fedora-copr/ansible-pulp
is now depracated, not used anymore, and should be archived.
(Don't delete completely, there still might be some useful information
in the README).


## Provisioning a new instance from scratch

Follow the [How to upgrade persistent instances (Amazon
AWS)](https://docs.pagure.org/copr.copr/how_to_upgrade_persistent_instances.html)
documentation like you would for any other Copr instance.

The only exception is, we need RHEL 8, CentOS 8, CentOS Stream 8, or
any RHEL 8 clone for this instance. At this moment I am using

```
ami-032adca51e5a08384
```

## Running a playbook

From batcave:

```
sudo rbac-playbook -l copr-pulp-dev.aws.fedoraproject.org groups/copr-pulp.yml
```

## Client configuration

Install pulp-cli:

```
pip3 install pulp-cli
```

Configure pulp-cli:

```
mkdir -p ~/.config/pulp/
vim ~/.config/pulp/cli.toml
```

The config should look like this:

```
[cli]
base_url = "http://localhost:24817"
verify_ssl = false
format = "json"
username = "admin"
password = "..."
```

You can find the password in our Bitwarden


## Testing

Create repository:

```
/usr/local/bin/pulp rpm repository create \
    --name @copr/copr-dev/fedora-rawhide-x86_64
```

Create distribution:

```
/usr/local/bin/pulp rpm distribution create \
    --name @copr/copr-dev/fedora-rawhide-x86_64-devel \
    --repository @copr/copr-dev/fedora-rawhide-x86_64 \
    --base-path @copr/copr-dev/fedora-rawhide-x86_64-devel
```

Publish:

```
/usr/local/bin/pulp rpm publication create \
    --repository @copr/copr-dev/fedora-rawhide-x86_64
```

Consume:

```
# Careful, a different port number than for API!
lftp http://localhost:24816/pulp/content/@copr/copr-dev/fedora-rawhide-x86_64-devel/
```
