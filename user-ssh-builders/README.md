# Give users SSH access to builders

Author: [@FrostyX](https://github.com/frostyx)


## Motivation

Users sometimes need SSH access to a builder instance to debug Copr-only
build failures. We want them to be able to get the access without
admin intervention.

See also https://github.com/fedora-copr/copr/issues/2364


## Limits

Obviously, Copr resources aren't unlimited so we need to allocate them
wisely.

- Only 1 running instance per user
    - Having 1 instance per project would be too much
    - Having more than 1 instance per user isn't needed, users can
      team up for debugging issues that need more builders at once
    - No need for group instances, users can do whatever they want,
      including adding access to their team members

- Builders need to have a limited lifespan, e.g. 48 hours
    - When submitting a build in Copr, we allow to adjust the timeout
      to 30 hours at most. That means the lifespan needs to be at
      least 30 hours.
    - I propose 48 hours because we want to give users enough time for
      debugging after the build finishes
    - Alternatively, we can do a 24-hours lifespan and add an "extend"
      button to Copr WebUI or to add a `copr-builder-extend` command
      to the instance.

- Users can do whatever they want with the builder instance ... but
  not really. Users cannot violate any rules defined in
  [What I can build in Copr?][what-can-i-build] and cannot use the
  instance for torrents, exploits, bitcoin mining, ... I don't want to
  give you ideas ... and neither for a personal VPS. We should print
  some fancy legal text and make users agree with it by clicking the
  button to obtain the login instructions.


## Workflow

### Option 1 - Button

For failed builds, there could be a button on the build detail
page. Clicking it would show the information about this feature,
rules, instance type selection, etc., and a button to actually spawn
the instance. The instance would be fresh and it would be up to the
user to reproduce the failure manually. Once the builder spawns, the
page will show instructions on how to connect to it.

### Option 2 - Keep alive after failure

There could be a checkbox when submitting a build (or alternatively
in project/package/chroot settings) to keep the builder alive after
the build fails. This option seems easier from the user perspective
but:

- It will probably be confusing when using the checkbox while some
  instance is already running. We don't want to kill it and spawn a
  new one. We probably need to print it was not possible to spawn a
  new instance into the builder-live/backend log
- Where to print the instructions on how to connect to the builder?
- If the build fails in multiple chroots, which one of those builders
  should be kept alive? We can't keep them all.
- Inability to select an instance type in advance so it may be hard
  to debug builds where e.g. Amazon AWS Spot instance is needed
  and nothing else.

### Common ground

Since the workflow starts from a failed build, we could create a MOTD
on the builder showing instructions on how to reproduce the particular
build using `copr-rpmbuild`.


## Instance type

This is probably relevant only for `Workflow Option 1 - Button`.

It is not enough to give acess to a random builder. Users needs to be
able to specify at least an architecture. But that is IMHO not good
enough. For example we have x86_64 builders our own hypervisors and in
Amazon AWS. Historically, we had issues that appeared only on builders
from one of them.

Even though it architectonically doesn't make any sense for Copr to
know about resalloc pools, I think we should let users select a resalloc
pool from which to spawn the builder. We can point them to the
[Resalloc Pools][resalloc-pools] page for details.

We have the resalloc `pools.yaml` in ansible, so it shouldn't be hard
to query only their names from the config and store them into some
config file on copr-frontend.


## Auth

### Option 1 - SSH key

There is a [FAS API][fas-api] and it can query each user and their
SSH key, e.g. [mine is here][fas-api-frostyx]. But it requires auth,
not sure if `fkinit` or recently logging into some Fedora service,
but try it in an anonymous window, it doesn't work.

Anyway, Copr already fetches some user information from FAS so I think
we can assume we will be able to fetch the SSH keys as well.

Alternativelly, we could allow users to specify a public URL to their
SSH key, upload it, or copy-paste it to some Copr form, but I don't
like any of these options.


### Option 2 - Passwords

Much easier option to implement would be generating an unique password
for each instance and show it in instructions. If users want, they
could change the password after logging-in, upload their SSH key,
whatever they want.

Personally, I prefer `Option 2 - Passwords`.


## Security

We need to make sure that:

- It is not possible to override a status of an already finished build
- Users cannot take a build from the queue (maybe not even theirs) and
  process it



[what-can-i-build]: https://docs.pagure.org/copr.copr/user_documentation.html#what-i-can-build-in-copr
[fas-api]: https://fasjson.fedoraproject.org/docs/v1/
[fas-api-frostyx]: https://fasjson.fedoraproject.org/v1/users/frostyx/
[resalloc-pools]: https://copr-be.cloud.fedoraproject.org/resalloc/pools
