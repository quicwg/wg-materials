#!/usr/bin/env python3

"""
Summarise a set of issues, based upon their labels.
"""

import sys
import time

import requests

from parse_link import parse_link_value


def get_issues(url, issues=None):
    sys.stderr.write("* %s\n" % url)
    if not issues:
        issues = []
    res = requests.get(url)
    if res.status_code >= 400:
        now = time.time()
        sys.stderr.write("   ERROR: %s\n" % res.status_code)
        sys.stderr.write(
            "   Reset: %i seconds\n"
            % (int(res.headers.get("x-ratelimit-reset", now)) - now)
        )
        sys.exit(1)
    sys.stderr.write(
        "   Remaining: %s\n" % res.headers.get("x-ratelimit-remaining", "-")
    )
    issues.append(res.json()[:])

    if "link" in res.headers:
        links = parse_link_value(res.headers["link"])
        rel_next = rel_last = None
        for link, params in links.items():
            rel = params.get("rel", None)
            if rel == "next":
                rel_next = link
            elif rel == "last":
                rel_last = link
        if rel_next:
            get_issues(rel_next, issues)
        elif rel_last:
            get_issues(rel_last, issues)
    return issues


def summarise_issues(issues):
    output = []
    for page in issues:
        for issue in page:
            if issue.get("pull_request", None) is None:
                # labels = [l["name"] for l in issue["labels"]]
                # print "* #%i: [%s](%s)" % (issue['number'], issue['title'], issue['url'])
                output.append("* #%i: %s" % (issue["number"], issue["title"]))
    return output


def run():
    import argparse

    parser = argparse.ArgumentParser(description="Summarise issues by label.")
    parser.add_argument(
        "-r",
        "--repo",
        dest="repo",
        action="store",
        required=True,
        help="repo name in org/repo format",
    )
    parser.add_argument(
        "-s",
        "--state",
        dest="state",
        action="store",
        default="open",
        help="issue state (default: open)",
    )
    parser.add_argument(
        "-l",
        "--labels",
        dest="labels",
        action="store",
        required=True,
        help="comma-separated labels to filter on",
    )
    args = parser.parse_args()
    repo_url = "https://api.github.com/repos/{repo}/issues?state={state}&labels={labels}".format(
        repo=args.repo, state=args.state, labels=args.labels
    )
    print("\n".join(summarise_issues(get_issues(repo_url))))


if __name__ == "__main__":
    run()
