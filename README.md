Application for managing labels for GitHub Pull Requests

```
Usage: filabel.py [OPTIONS] [REPOSLUGS]...

  CLI tool for filename-pattern-based labeling of GitHub PRs

Options:
  -s, --state [open|closed|all]   Filter pulls by state.  [default: open]
  -d, --delete-old / -D, --no-delete-old
                                  Delete labels that do not match anymore.
                                  [default: True]
  -b, --base BRANCH               Filter pulls by base (PR target) branch
                                  name.
  -a, --config-auth FILENAME      File with authorization configuration.
  -l, --config-labels FILENAME    File with labels configuration.
  --help                          Show this message and exit.
```
