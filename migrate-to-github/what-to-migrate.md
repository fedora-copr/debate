## What we want to migrate

#### Git history (obviously)

#### Match IDs (important)

#### Migrate labels

### Issues

- Link to a corresponding archived issue in Pagure
- Transfer labels
- Migrate them as they are in Pagure


Issue's headers (top of the body) will be in format:

```
Original issue: https://pagure.io/copr/copr/issue/2355
Opened: 2022-10-29
Opened by: @praiskup
```

and then the rest of the body and comments

### PRs

- Link to a corresponding archived PR in Pagure
- Transfer labels

Options (depends on the time difficulty of creating PR):

- Migrate PRs as PRs: preserve the PR diff and comments or just create empty PR
- Migrate PRs as Issues:
  - Create empty issue with link to a corresponding archived PR in Pagure, or

PR's headers (top of the body) format will be:

```
Original pull request: https://pagure.io/copr/copr/pull-request/123
Opened: 2022-10-29
Opened by: @praiskup
In case of any problem, feel free to take a look at the archived repo [here](archived-repo).
```

### Opened PRs

We should merge them first

### Assignees

Assign Copr maintainers to corresponding Issues/PRs in Github once they are migrated.
