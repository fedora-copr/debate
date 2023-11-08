Heterogeneous farm(s) of workers
================================

Several Red Hat teams work with wide range of clouds (AWS, IBM Cloud, GCP,
Azure, OpenStack, ...) to dynamically allocate and provide workers.

This document was crated to compare the solutions and find a common ground.

Artemis
-------

Pros:
    - REST API: https://artemis6.docs.apiary.io/
    - snapshot support
    - post\_install\_script (VM customisation)
    - adapter to GCP

TODOs:

    - "Users request provisioning of guests via REST API, describing the desired
      hardware and software configuration in each request.".  How this is done?
    - what is priority group?
    - compose mapping?  Can that be replaced with "pool tag"?


CKI
---

The team uses GitLab Runners based on Docker Machine.  This is "standard but
abandoned" way to spawn machines the same way in many clouds.

    Docs: https://docs.gitlab.com/runner/
    Future proposal: https://docs.gitlab.com/ee/architecture/blueprints/runner_scaling/

Executor in Runner: https://docs.gitlab.com/ee/architecture/blueprints/runner_scaling/#custom-provider

Custom provisioning script: https://gitlab.com/cki-project/upt

The future proposal is considering allowing multiple tasks on a single resource,
with uncertain benefits, which was never considered in Resalloc or Copr.


Image builder
-------------

GitLab Runner, with custom executor:

- https://github.com/osbuild/gitlab-ci-terraform-executor
- https://github.com/osbuild/gitlab-ci-terraform

- wide variety of environments (e.g. one golden image for every RHEL minor
  version in every cloud)


Resalloc
--------

https://github.com/praiskup/resalloc/blob/main/README.md

Pros:

    - cli
    - working preallocation
    - saving by resource recycling for different tasks (sandboxing)
    - agent-like machines (Kobo compat)


Other tools
-----------

**Pulumi**

- https://github.com/pulumi/pulumi
- doesn't support ibm cloud
- infra as code
- not in Fedora

**Apache LibCloud**

- https://github.com/apache/libcloud
- packaged in Fedora!
- doesn't seem to support cloud.ibm.com
- infra as code
- could be used as "funding" for our `resalloc-aws`, etc. plugins/wrappers

**Cloudify**

- EaaS

**Juju**

- https://juju.is/
