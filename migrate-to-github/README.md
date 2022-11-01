Check the [what-to-migrate.md]() file first, please.

### How we want to do it

We will use the XXX tool (not released yet).
  - still thinking about its name :D I think about two possibilities:
    - `volagit` or `forgit` -> these are just random names containing `git`... I think
       about them because they sounds cool :D

### What tools it will use

- [Ogr](https://github.com/packit/ogr)
  - A tool which wraps Pagure, Gitlab and Github API into one API
  - There's 95% of API calls we need to use 
- [GitPython](https://gitpython.readthedocs.io/en/stable/)
  - A tool which wraps git cli to a Python api
  - only when Github, Gitlab API doesn't allow something (e.g. `git reset`). In other cases Ogr
    includes all the stuff we need.
- That's it
  
### What we need to use to achieve the goals in [what-to-migrate.md]()

- Archive Pagure repo
- Create a bot account which will transfer the PRs/Issues to Github
- Reuse Copr's Github mirror
  - we need to skip N (30 cca) first Issues/PRs because the mirror has some PRs
- Give this bot rights to write to Copr project
- Create Github API token for this bot account
  - Security: Give the token minimal amount of privileges -> it won't need to delete
    something so don't enable this! (but on the other hand if something will be
    screwed up - it's still just a new mirror repo so no big deal :D) And delete
    the token once migration is done.
  - The API token needs to read and write, check these options when creating API 
    (I am still checking if we really needs all of these):
  - https://docs.github.com/en/developers/apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes
    - public_repo
    - read:project
    - read:user (for migrating assignees)
- Create Pagure API token
  - Security: the same reason as above
  - The API token needs only to read the project, nothing else.
  - Documentation missing???:
    - ???
- Create a config for the script
- Run the script
- Have a cup of coffee and relax
- Make the Pagure repo read only (`Project settings` -> `Project Options` -> 
  enable `Issue tracker read only` and `Pull request access only`)

#### What is done and what needs to be done (some kind of progressbar about the script):

- [x] Logic of transferring between git forges
- [x] Some king of parser which will decide how to parse data to another forge
- [ ] Transfer issues logic:
  - [ ] Transfer comments (should be easy using the Ogr API)
  - [x] Everything else
- [ ] Transfer PRs logic (we probably want to do this via Issues)
  - [x] Asynchronously create branches for making a PR
  - [x] Transfer PR's body and diff
  - [ ] Transfer PR's comment
    - transferring the content is easy, but some comments may not be relevant (after rebase
      they may react to a line which is not valid to the comment anymore) 
- [x] Match ids
- [ ] Migrate labels - should be easy to do - Ogr provides API
- [ ] Test it on some dummy project
- [ ] Archive Pagure's repo
- [ ] Be actually able to run the script (glue the methods which are already done together)
