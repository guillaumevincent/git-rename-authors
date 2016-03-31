import collections
import unittest

from authors import get_list_authors, merge_authors, parse_authors
from script import get_script


class CleanGitRepoTestCase(unittest.TestCase):
    def test_parse(self):
        stdout = 'Guillaume Vincent;test@oslab.fr\nGuillaume Vincent;test2@oslab.fr\nGuillaume VINCENT;test2@oslab.fr\n\n'
        expected_authors = [{'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'},
                            {'email': 'test2@oslab.fr', 'name': 'Guillaume Vincent'},
                            {'email': 'test2@oslab.fr', 'name': 'Guillaume VINCENT'}]
        self.assertEqual(expected_authors, parse_authors(stdout))

    def test_get_author(self):
        authors = [{'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'},
                   {'email': 'test2@oslab.fr', 'name': 'Guillaume VINCENT'}]
        expected_authors = ['Guillaume Vincent <test@oslab.fr>', 'Guillaume VINCENT <test2@oslab.fr>']
        self.assertEqual(expected_authors, get_list_authors(authors))

    def test_merge_authors(self):
        authors = [{'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'},
                   {'email': 'test2@oslab.fr', 'name': 'Guillaume Vincent'}]
        expected_merged_authors = {
            'test2@oslab.fr': {'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'}
        }
        self.assertDictEqual(expected_merged_authors, merge_authors(authors, ids_to_merge=[0, 1], merge_to_id=0))
        self.assertEqual(expected_merged_authors, merge_authors(authors, ids_to_merge=[1], merge_to_id=0))

    def test_merge_authors_same_email(self):
        authors = [{'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'},
                   {'email': 'test@oslab.fr', 'name': 'Guillaume VINCENT'}]
        expected_merged_authors = {
            'test@oslab.fr': {'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'}
        }
        self.assertDictEqual(expected_merged_authors, merge_authors(authors, ids_to_merge=[0, 1], merge_to_id=0))
        self.assertEqual(expected_merged_authors, merge_authors(authors, ids_to_merge=[1], merge_to_id=0))

    def test_sh_generated(self):
        merged_authors = {
            'test2@oslab.fr': {'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'}
        }
        expected_script = """
if [ "$GIT_COMMITTER_EMAIL" = "test2@oslab.fr" ]
then
    export GIT_COMMITTER_NAME="Guillaume Vincent"
    export GIT_COMMITTER_EMAIL="test@oslab.fr"
fi
if [ "$GIT_AUTHOR_EMAIL" = "test2@oslab.fr" ]
then
    export GIT_AUTHOR_NAME="Guillaume Vincent"
    export GIT_AUTHOR_EMAIL="test@oslab.fr"
fi
"""
        self.assertTrue(expected_script in get_script(merged_authors))

    def test_sh_generated_with_two_email(self):
        merged_authors = collections.OrderedDict()
        merged_authors['test2@oslab.fr'] = {'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'}
        merged_authors['test3@oslab.fr'] = {'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'}
        expected_script = """
if [ "$GIT_COMMITTER_EMAIL" = "test2@oslab.fr" ]
then
    export GIT_COMMITTER_NAME="Guillaume Vincent"
    export GIT_COMMITTER_EMAIL="test@oslab.fr"
fi
if [ "$GIT_AUTHOR_EMAIL" = "test2@oslab.fr" ]
then
    export GIT_AUTHOR_NAME="Guillaume Vincent"
    export GIT_AUTHOR_EMAIL="test@oslab.fr"
fi

if [ "$GIT_COMMITTER_EMAIL" = "test3@oslab.fr" ]
then
    export GIT_COMMITTER_NAME="Guillaume Vincent"
    export GIT_COMMITTER_EMAIL="test@oslab.fr"
fi
if [ "$GIT_AUTHOR_EMAIL" = "test3@oslab.fr" ]
then
    export GIT_AUTHOR_NAME="Guillaume Vincent"
    export GIT_AUTHOR_EMAIL="test@oslab.fr"
fi
"""
        self.assertTrue(expected_script in get_script(merged_authors))


if __name__ == '__main__':
    unittest.main()
