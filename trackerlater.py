#! /usr/bin/env python
import os
import sys

import requests
import json

BASE_URL = 'https://www.pivotaltracker.com/services/v5/'
API_TOKEN = os.environ['API_TOKEN']


class Project():
    def __init__(self, id):
        self.id = id
        self.url = BASE_URL + "projects/%s" % self.id
        self.stories = Stories(self.url)


class Stories():
    def __init__(self, project_url):
        self.url = "%s/%s" % (project_url, "stories")
        self.all = self.get()

    def get(self):
        print("Requesting %s" % self.url)
        r = requests.get(self.url, headers={"X-TrackerToken": API_TOKEN})
        data = json.loads(r.text)
        return [Story(self.url, d) for d in data]


class Story():
    def __init__(self, stories_url, data):
        self.data = data
        self.url = "%s/%s" % (stories_url, self.id)

    @property
    def id(self):
        return self.data["id"]

    @property
    def labels(self):
        return self.data['labels']


def main():
    if len(sys.argv) != 2:
        print("Usage: trackerlater.py PROJECT_ID")
        return(1)
    project_id = sys.argv[1]
    print("Project id: %s" % project_id)
    stories = Project(project_id).stories.all
    for story in stories:
        print "---\n"
        print story.data
    return(0)


if __name__ == '__main__':
    exit(main())
