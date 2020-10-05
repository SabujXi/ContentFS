from unittest import TestCase
from ContentFS.pathmatch.fsmatchergroup import FsMatcherGroup
from ContentFS.cpaths.cpath import CPath


class TestFsMatcherGroup(TestCase):
    def test_should_include(self):
        self.fail()

    def test_should_exclude(self):
        self.fail()

    def test_add(self):
        self.fail()

    def test_with_dev_matcher(self):
        matcher_group = FsMatcherGroup().with_dev_matcher()
        self.assertTrue(matcher_group.should_exclude(CPath(".git/")))
        self.assertFalse(matcher_group.should_include(CPath(".git/")))

    def test_without_dev_matcher(self):
        matcher_group = FsMatcherGroup()
        self.assertFalse(matcher_group.should_exclude(CPath(".git/")))
        self.assertTrue(matcher_group.should_include(CPath(".git/")))

    def test_get_matchers(self):
        self.fail()
