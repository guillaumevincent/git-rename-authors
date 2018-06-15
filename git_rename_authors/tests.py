import collections
import unittest

from authors import get_list_authors, parse_authors
from script import generate_script


class UnitTests(unittest.TestCase):
    def test_parse_authors(self):
        stdout = 'Guillaume Vincent;test@oslab.fr\nGuillaume Vincent;test2@oslab.fr\nGuillaume VINCENT;test2@oslab.fr\n\n'
        expected_authors = [{'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'},
                            {'email': 'test2@oslab.fr', 'name': 'Guillaume Vincent'},
                            {'email': 'test2@oslab.fr', 'name': 'Guillaume VINCENT'}]
        self.assertEqual(expected_authors, parse_authors(stdout))

    def test_get_list_authors(self):
        authors = [{'email': 'test@oslab.fr', 'name': 'Guillaume Vincent'},
                   {'email': 'test2@oslab.fr', 'name': 'Guillaume VINCENT'}]
        expected_authors = ['Guillaume Vincent <test@oslab.fr>', 'Guillaume VINCENT <test2@oslab.fr>']
        self.assertEqual(expected_authors, get_list_authors(authors))

    def test_generate_script(self):
        source_authors = [
            {'email': 'test2@oslab.fr', 'name': 'Guillaume Vincent'}
        ]
        destination_author = 'Guillaume Vincent<test@oslab.fr>'
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
        self.assertTrue(expected_script in generate_script(source_authors, destination_author))

    def test_generate_script_with_two_email(self):
        source_authors = [
            {'email': 'test2@oslab.fr', 'name': 'Guillaume Vincent'},
            {'email': 'test3@oslab.fr', 'name': 'Guillaume Vincent'}
        ]
        destination_author = 'Guillaume <test@oslab.fr>'
        expected_script = """
if [ "$GIT_COMMITTER_EMAIL" = "test2@oslab.fr" ]
then
    export GIT_COMMITTER_NAME="Guillaume"
    export GIT_COMMITTER_EMAIL="test@oslab.fr"
fi
if [ "$GIT_AUTHOR_EMAIL" = "test2@oslab.fr" ]
then
    export GIT_AUTHOR_NAME="Guillaume"
    export GIT_AUTHOR_EMAIL="test@oslab.fr"
fi

if [ "$GIT_COMMITTER_EMAIL" = "test3@oslab.fr" ]
then
    export GIT_COMMITTER_NAME="Guillaume"
    export GIT_COMMITTER_EMAIL="test@oslab.fr"
fi
if [ "$GIT_AUTHOR_EMAIL" = "test3@oslab.fr" ]
then
    export GIT_AUTHOR_NAME="Guillaume"
    export GIT_AUTHOR_EMAIL="test@oslab.fr"
fi
"""
        self.assertTrue(expected_script in generate_script(source_authors, destination_author))


if __name__ == '__main__':
    unittest.main()
