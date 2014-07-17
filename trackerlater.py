#! /usr/bin/env python
import os
import sys

import requests
import json

BASE_URL = 'https://www.pivotaltracker.com/services/v5/'
API_TOKEN = os.environ['API_TOKEN']


class Project():
    def __init__(self, id, stories=None):
        self.id = id
        self.url = BASE_URL + "projects/%s" % self.id
        self.stories = stories

    def get_stories(self):
        stories_url = "%s/%s" % (self.url, "stories")
        print("Requesting %s" % stories_url)
        r = requests.get(stories_url, headers={"X-TrackerToken": API_TOKEN})
        data = json.loads(r.text)
        if hasattr(data, 'keys') and 'error' in data.keys():
            print("Pivotal Tracker API Error: %s" % data)
            exit(1)
        self.stories = [Story(stories_url, d) for d in data]


class Story():
    def __init__(self, stories_url, data):
        self.data = data
        self.url = "%s/%s" % (stories_url, self.id)

    @property
    def id(self):
        return self.data["id"]

    @property
    def labels(self):
        return self.data.get('labels', [])

    @property
    def name(self):
        return self.data['name']


def main():
    if len(sys.argv) != 2:
        print("Usage: trackerlater.py PROJECT_ID")
        return(1)
    project_id = sys.argv[1]
    print("Project id: %s" % project_id)
    project = Project(project_id)
    project.get_stories()
    for story in project.stories:
        print "---\n"
        print story.data
    return(0)


if __name__ == '__main__':
    exit(main())
