def get_list_authors(authors):
    displayed_authors = []
    for author in authors:
        displayed_authors.append('{} <{}>'.format(
            author['name'], author['email']))
    return displayed_authors


def parse_authors(stdout):
    authors = []
    for author in stdout.strip().split('\n'):
        author_info = author.split(';')
        authors.append({
            'name': author_info[0],
            'email': author_info[1]
        })
    return authors
