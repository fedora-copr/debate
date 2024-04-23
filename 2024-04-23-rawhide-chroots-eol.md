How to Gently Remove Useless Rawhide Chroots
============================================

This RFC aims to address the issue raised in [this Copr issue](https://github.com/fedora-copr/copr/issues/2933).

Proposal
--------

Currently, there's an [EOL policy for old Fedora releases](https://docs.pagure.org/copr.copr/how_to_manage_chroots.html#eol-deactivation-process).
This is essentially implemented through [CoprChroot.delete_after](https://github.com/fedora-copr/copr/blob/df6548c8bd605cd944c88a8a5682af494061b624/frontend/coprs_frontend/commands/alter_chroot.py#L61).

Let's use the same field for the Fedora Rawhide EOL process as the
implementation detail. The field would be set for (not just for Rawhide) Copr
chroots to "NOW()+N months" value using Copr automation if:

1. The cron/automation job is enabled (Copr admin opt-in).
2. No BuildChroot in CoprChroot has occurred in the last M months.  We need to
   be careful; build chroots might be deleted by user and the overall
   calculation would be affected - so we should somehow "touch" a new timestamp
   field like `CoprChroot.last_build` and use it (Mirek proposes to only touch
   this when build is actually deleted to minimize concurrency).
3. [Optional] The user doesn't disable this cleanup mechanism, either per
   project or per CoprChroot.  Pavel proposes to not implement this, at least
   not at the beginning.
4. User get's informed about the chroot EOL situation (using the old way, EOL
   policy emails), and can prolong the chroot validity, either with the +6
   months option as normally, or doing a new fresh build (which needs to NULL
   the `delete_after` field!).

Let's "generalize" this feature for any "rolling" chroots, not just Fedora
Rawhide (some openSUSE or Mandriva chroots might require similar treatment).
We'll have a new `MockChroot.rolling = True|False` field in DB for this.
The `N` and `M` fields will be configurable in the Frontend's config file.
