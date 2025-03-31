PULP
====

Base product: "pulpcore"
Plugin Copr needs: pulp_rpm


Glossary
========

- Artifact

    A data blob identified by sha256

- Content

    points at Artifact, but contains additional metadata

- Repository

    Named abstraction for a "repository".  When we add/remove *content*,
    we don't add to a specific repository version.  We add it to
    a *repository* and new *version* is generated.

- Repository version

    Represents *repository* state in a specific time.  When a new
    *content* (rpm) is uploaded and added to *repository*, new *repo
    version* is generated automatically.

    Versions have a linear history, and are defined by set of *content*
    objects.

    Creating a new *repository version* is relatively cheap; new RPM file
    (artifact) needs to be added to the *repository* (a few rows in DB),
    but still - new task is generated, and is taken once the worker
    capacity allows).  But at least no RPM metadata files
    (createrepo-like) are generated, yet.

- Publication

    Point in time when we decide we want to generate RPM repo metadata
    files for given *repository version*.

    (*distribution* points at a specific *publication*, and it determines
    a specific *repository version*).

    Generating publication is expensive; PULP has to generate RPM metadata
    files for given (PG) database state.

- Distribution

    Represents a user consumable content, on a http://some/path/ address

    Points at the last *repository version* through the last *publication*

Every object above has it's own PULP object ID, e.g.
/pulp/api/v3/distributions/rpm/rpm/457ccae4-8b9f-43b3-bb65-076f4c33f5db/


HOW IT WORKS
============

create a "Repo" and "Distribution"

upload RPM1 RPM2 RPM3

add RPM1 to Repo      <=  Repo Version 1

add RPM2 to Repo      <=  Repo Version 2  <= Publication 1  <= Distribution

remove RPM1 from Repo <=  Repo Version 3

add RPM3 to Repo      <=  Repo Version 4  <= Publication 2  <= Distrubution


Prepare environment
===================

```
https://pulpproject.org/pulp-in-one-container/

https://copr.fedorainfracloud.org/coprs/praiskup/pulp-cli/

$ pulp config create --base-url "http://localhost:8080"

$ cat ~/.config/pulp/cli.toml
[cli]
username = "admin"
base_url = "http://localhost:8080"
password = "admin"
api_root = "/pulp/"
cert = ""
key = ""
verify_ssl = true
format = "json"
dry_run = false
timeout = 0
verbose = 0
```


Demo with one possible work-flow
================================

```
$ pulp rpm repository create --retain-repo-versions 3 --name @copr/copr-dev/fedora-rawhide-x86_64
    [--retain-package-versions N]

$ pulp rpm distribution create \
    --name @copr/copr-dev/fedora-rawhide-x86_64-devel \
    --repository @copr/copr-dev/fedora-rawhide-x86_64 \
    --base-path @copr/copr-dev/fedora-rawhide-x86_64-devel

    Creates http://raiskup:8080/pulp/content/@copr/copr-dev/fedora-rawhide-x86_64-devel/
    but 404 for now.

$ pulp rpm publication create --repository @copr/copr-dev/fedora-rawhide-x86_64
    // first repo version, empty (no packages)
    // href: /pulp/api/v3/publications/rpm/rpm/68d6ad95-a7d9-4e15-87a6-55cbc04d1557/

$ pulp rpm distribution create \
    --name @copr/copr-dev/fedora-rawhide-x86_64 \
    --base-path @copr/copr-dev/fedora-rawhide-x86_64 \
    --publication /pulp/api/v3/publications/rpm/rpm/68d6ad95-a7d9-4e15-87a6-55cbc04d1557/

$ pulp artifact upload --file /tmp/quick-package/x86_64/dummy-pkg-20230217_0915-1.fc37.x86_64.rpm
    => "sha256": "9b773c49c9de875b604747c23378de74362c083272ca7e5782b847389946afde",

$ pulp rpm content create \
    --repository "@copr/copr-dev/fedora-rawhide-x86_64" \
    --sha256 9b773c49c9de875b604747c23378de74362c083272ca7e5782b847389946afde \
    --relative-path 05521574-dummy-pkg/dummy-pkg-20230217_0915-1.fc37.x86_64.rpm

    // relative path doesn't work the way we need

$ pulp rpm publication create --repository @copr/copr-dev/fedora-rawhide-x86_64
    // href /pulp/api/v3/publications/rpm/rpm/925e7556-5dcc-4109-8c95-4a37fdd809e3/

$ pulp rpm distribution update \
    --name @copr/copr-dev/fedora-rawhide-x86_64 \
    --publication /pulp/api/v3/publications/rpm/rpm/925e7556-5dcc-4109-8c95-4a37fdd809e3/
```


Other commands
==============

```
$ pulp rpm repository version list --repository @copr/copr-dev/fedora-rawhide-x86_64
$ pulp rpm repository content list --repository @copr/copr-dev/fedora-rawhide-x86_64

$ pulp rpm content -t package list
$ pulp rpm repository destroy --name @copr/copr-dev/fedora-rawhide-x86_64
$ pulp orphan cleanup --protection-time 1
$ pulp rpm distribution destroy --href ...
```
