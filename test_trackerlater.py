import sys
import unittest

from trackerlater import Project, Story, BASE_URL, main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.orig_args = sys.argv
        sys.argv = []

    def tearDown(self):
        sys.argv = self.orig_args

    def testMain_withEmptyArgs(self):
        self.assertEqual(1, main())

    def testMain_withTooManyArgs(self):
        sys.argv.extend(range(3))
        self.assertEqual(1, main())

    def testMain_withAProjectIdArg(self):
        sys.argv.extend(["yada", "123"])
        self.assertEqual(0, main())


class TestProject(unittest.TestCase):
    def testProject_HasAnId(self):
        project = Project(123)
        self.assertEqual(123, project.id)

    def testProject_HasAUrl(self):
        project = Project(123)
        expected_url = "%sprojects/123" % BASE_URL
        self.assertEqual(expected_url, project.url)

    def testProject_HasStories(self):
        project = Project(1)
        project.stories_json = '[{"name": "story 1"}, {"name": "story 2"}]'
        self.assertEqual("story 1", project.stories[0].name)
        self.assertEqual("story 2", project.stories[1].name)


class TestStory(unittest.TestCase):

    def testHasAnId(self):
        story = Story("some/url", {"id": 123})
        self.assertEqual(123, story.id)

    def testHasAUrl(self):
        story = Story("some/url", {"id": 123})
        expected_url = "some/url/123"
        self.assertEqual(expected_url, story.url)

    def testLabels(self):
        story = Story("some/url",
                      {"id": "yada",
                       u'labels': [{u'kind': u'label',
                                    u'name': u'yada',
                                    u'created_at': u'2014-06-05T16:09:38Z',
                                    u'updated_at': u'2014-06-05T16:09:38Z',
                                    u'project_id': 1095054,
                                    u'id': 8612860}]})
        self.assertEqual(1, len(story.labels))
        self.assertEqual("yada", story.labels[0]['name'])
