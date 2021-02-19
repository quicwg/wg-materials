# Config files for gitdm

The config files in this directory can be used with the
[gitdm](https://lwn.net/Articles/290957/) tool to produce contribution
statistics for our various repositories.

Example:
``` shell
# export GITDM_CONFIG=<location of this directory>
# cd quicwg/base-drafts
# git log -p | gitdm -l 5 -b $GITDM_CONFIG

Grabbing changesets...done
Processed 6322 csets from 84 developers
51 employers found
A total of 86954 lines added, 67192 removed (delta 19762)

Developers with the most changesets
Martin Thomson            2282 (36.1%)
ianswett                  1062 (16.8%)
Mike Bishop                690 (10.9%)
Jana Iyengar               575 (9.1%)
Marten Seemann             183 (2.9%)

Top changeset contributors by employer
Mozilla                   2366 (37.4%)
Google                    1291 (20.4%)
Fastly                     729 (11.5%)
Akamai                     592 (9.4%)
Microsoft                  189 (3.0%)
```

I wasn't able to determine the identiy and/or the employer for a number of
contributors to our various repos. Please submit PRs if you can identify
contributors for which only an email address is show.

Also, contributors that changed employment during the QUIC standardization are
not currently correctly tracked. Please see the comment in `domain-map` for how
to do so, and send PRs.
