#!/usr/bin/env python

"""
Summarises issues from a file.
"""

from parse_link import parse_link_value
import requests
import sys
import json

issues = json.load(open('issues.json'))

all_categories = ['-transport', '-recovery', '-http', '-tls', '-ops']

for page in issues:
    for issue in page:
        if issue['state'] == u'closed' and issue.get('pull_request', None) is None:
            labels = [l['name'] for l in issue['labels']]
            if u'editorial' not in labels \
              and u'invalid' not in labels \
              and u'has-consensus' not in labels:
#                print "* #%i: [%s](%s)" % (issue['number'], issue['title'], issue['url'])
                categories = " ".join([c[1:] for c in all_categories if c in labels])
                print "* #%i: %s   (%s)" % (issue['number'], issue['title'], categories)

