High performance builders
=========================

The problem is that our builders are too slow to build e.g. Chromium package
quickly enough.  Such builds take 24h and more (our limit is 48h).  With the
cloud era, it really makes sense to have more powerful machines -> even though
they cost more $$/hour, we spend less amount of time on them.

The problem
-----------

The thing is that, as of now, every builder in Copr is started by Resalloc "in
advance", or "preallocated".  The builders are preallocated even though they are
not _immediately_ used, and stay idle till someone takes them (if there's no
demand for days, they stay allocated).  When taken, system allocates additional
resources (so we get more and more machines if there's actual demand for them).

This system works well for normal builders, because they are typically taken
very quickly (the more tasks in queue the faster they are taken; the smaller the
"prealloc" quota number for resalloc pool is the faster they are taken).  And
even if they are not taken for a while, we can actually afford keeping a few of
them allocated because the instances are not overly expensive.

There's though a demand to have a more (maybe ridiculously) powerful instances;
having just one of them allocated but unused could be quite expensive matter.
Even if we used for a low-demanding task.


The proposal overview
---------------------

Let's have on-demand resources/pools in Resalloc.  In such pools there would be
**no preallocated resource** by default, as long as there's no demand for them.
Client will have a possibility to ask for them via special "on demand" tagged
tickets.

We need to have a configuration option with allow-listed builds that will
unconditionally request the powerful builders.

We need to control "how many powerful builders" can be started by one user at
one time, so users don't lock the other users out.  Likely a simple modification
of the [BuildTagLimit](https://github.com/fedora-copr/copr/blob/7442ec4303f2e0ba2e31a6555c4da34b96de0ee1/backend/copr_backend/rpm_builds.py#L136).

Resalloc Implementation
-----------------------

When a ticket with such a tag is taken from Resalloc, the resource manager would
register such a ticket and then start allocating the expensive resource.

Multiple pools can provide "on demand" resources with the same tag.  But once
the tag is marked "on demand" in one pool, it must be on-demand in all.
TODO: how difficult is to relax this rule?

If the ticket is closed early (user/copr changed the mind), the machine would be
deallocated to save the money.

The client API is unchanged, just using this as normally:

    $ resalloc ticket --tag arch_x86_64 --tag extra_powerful
    ID
    $ ticket close ID


Resalloc proposal: https://github.com/praiskup/resalloc/pull/118


Copr implementation
-------------------

Copr frontend will have a new configuration option with "regex patterns"
that will automatically add the "on demand" tags to the tickets taken from
Resalloc:

    EXTRA_BUILDER_TAGS = {
        "extra_powerful": [
            "praiskup/ping/fedora-.*-.*/chromium",
            "@copr/copr-pull-requests/.*/copr-cli",
        ],
    }


Possible Ehnahncements
----------------------

- Low-priority on-demand tags for builds "in containers" -> some users/projects
  might want to switch to container builds to gain throughput.
- Source builds might want this tagging as well
- Per-team cloud budget and "on demand" tags might be implemented using this?
- We can have pools with builders having "more swap" (so fare we always enlarged
  the swap for all the builders to have homogeneous behavior, possibly wasting a
  lot of volume storage)
