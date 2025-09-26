# Automatic Integration Testing for Copr PRs/Merges

This is a discussion/feature document for [automatic Copr testing][the-issue].

## Use Cases / Story

The [old testing workflow][current-testing-sop] requires significant **manual
effort**, typically at **inconvenient times** (e.g., when [planning a
release][release-sop] or working on a complicated Copr feature).

A prerequisite for running these [Integration tests][current-testing-sop] is a
**well-prepared development instance**, which is the most painful part of
testing.  This preparation involves **building the appropriate RPM package
versions** (have about ten packages as part of the Copr [monorepo][]) and
**deploying them on the appropriate VMs** (there's no 1:1 package to VM mapping;
e.g., `python3-copr-common` is installed on all the infrastructure VMs).

Note that the team also suffers from a **missing staging/development instance**.
A Copr instance requires significant effort to maintain, so we currently only
have two: the **production** one, and another often referred to as the "**dev**"
or "**stage**" instance.  Indeed, it plays two roles:

1.  **Staging Role**: We try to keep it "as close as possible" to our production
    instance.

2.  **Development Role**: When developing a complicated feature that spans
    multiple infrastructure VMs, we tend to try the proposed code on this same
    instance (installing very specifically modified RPM packages on those VMs
    and running Integration tests).

The consequence is that we often **forget to revert the development steps**,
causing the instance to **diverge too much from production** and thus failing to
provide the best **staging** feedback.

This document discusses the future technical approach(es) for **automated
Integration testing**, allowing us to separating the **stage** and **dev** roles
(into ephemeral Copr instances).


# Requirements

* **Automated Execution:** Integration tests must run almost automatically to
  eliminate expensive manual effort.

* **Sufficient Feedback:** A passing (green) result from the Integration tests
  must provide high confidence that the merged code is ready for
  release & deployment to production.

* **Post-Merge CI Integration:** Integration tests must run automatically
  **post-merge** so that if the Continuous Integration (CI) process begins
  failing, it is immediately obvious which pull request (merge event) is
  responsible.

* **On-Demand Pre-Merge Testing:** (nice to have) The Integration tests should
  also be runnable **"on demand"** against the proposed code in a pull request.
  The "on demand" part is crucial; we can't afford to rerun the tests for
  *every* PR update, as a Integration tests run is relatively expensive.


## Out of Scope

* **Unit Testing:**  This document does not cover unit testing.  Unit tests are
  run during the RPM build process, and we already perform comprehensive testing
  for every separate component.  We already build RPMs for every pull-request
  update, and after pull-request merge.

* **Other Release Automation:**  Any other release-time automation activities
  are also outside the scope of this discussion.



## Proposed Change Phases

1. **Single-Host Testing**

   We would install all the necessary packages—the frontend, backend, keygen,
   dist-git, and a (likely containerized) variant of copr-rpmbuild—onto a single
   VM host.  This can be done using Ansible from a Testing-Farm (TF)
   environment.  The major benefit is that we can use the CI-built RPMs
   (currently built via our scripting, but in the future by Packit once it
   supports [eco-building in monorepos][packit-monorepo]).

   **Negatives:** This approach is expected to require some **packaging fixes**
   (e.g., so the frontend and backend can coexist on a single host; currently,
   we use `lighttpd` and `httpd` respectively).

   **Benefits:** The side effect is **cleaner and more stable packaging**.  We
   can utilize the existing Testing Farm tooling (we already use the same
   approach for Mock): start a Fedora VM, install Packit-built pre-release
   packages, and execute the tests.

   N.B. There has also been a prior community request for a single-host Copr
   approach.

2. **Single-Host Testing, Booting from Pre-Built Golden Image**

   This is a follow-up to the previous step.  We would first **build a golden
   image** (containing all the necessary pre-release packages), boot the machine
   from it in Testing Farm, and then run the Integration tests.

   Such a golden image, for instance, post-release time, could be distributed to
   end-users as another **supported artifact**.  Furthermore, pre-release golden
   images would be easily reusable anytime a Copr team member wanted to try
   something destructive (without needing to break the staging instance).


3. **OKD/OpenShift Testing**

   We would build a set of OCI images (for backend, frontend, keygen, distgit,
   and builder), deploy a Copr instance from them (using an OpenShift deployment
   configuration), and run tests.

   At the time of writing this document, it is not entirely clear where we would
   find an OpenShift cluster that matches our needs (at least the builder side
   requires running Mock, which implies root access, at least in a user
   namespace).

   I spent a few hours researching single-host OpenShift/OKD deployments, but
   the situation doesn't seem trivial these days—especially compared to the v3.X
   era where *minishift* used to work like a charm.

   **Benefits here:** Self-hosting the Copr RPM build system in OpenShift would
   be trivial, and the configuration would essentially become a separate
   product for the team.  Making the "Copr-in-OpenShift" use case fully tested
   would pave the way for a future migration of our production instances to a
   more **"GitOps"** model.

Note: Per the team's feedback, single-host testing might not be terribly
cheap to implement.  If this approach proves too expensive, we should fall back
to `podman compose` testing (which implies automatic RPM package rebuilds).

## Definition of Success / Deliverables

The primary problem we aim to address is the costly manual effort involved in
Copr testing.

As such, this project will be considered successful if we achieve the following:

* **Single-Button Trigger:** Create a simple trigger (e.g., a script) that can
  be executed to run our Sanity tests against a reasonably powerful Fedora
  Cloud-based VM (Example: `./run-sanity-tests root@1.2.3.4`).

* **Automated Post-Merge CI:** Our post-merge Continuous Integration (CI) system
  automatically runs the testing script against a machine provisioned by Testing
  Farm.

### Optional (Nice-to-Have)

* **Automatic Pull Request Testing:** Implement automated testing for pull
  requests, such as when a maintainer specifically requests Packit to run the
  tests.


[the-issue]: https://github.com/fedora-copr/copr/issues/3028
[current-testing-sop]: https://docs.pagure.org/copr.copr/sanity_tests.html#sanity-tests
[release-sop]: https://docs.pagure.org/copr.copr/how_to_release_copr.html
[builder-upgrade-sop]: https://docs.pagure.org/copr.copr/how_to_upgrade_builders.html
[monorepo]: https://github.com/fedora-copr/copr
[packit-monorepo]: https://github.com/packit/packit/issues/1997
