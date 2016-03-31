def get_list_authors(authors):
    displayed_authors = []
    for author in authors:
        displayed_authors.append('{} <{}>'.format(author['name'], author['email']))
    return displayed_authors


def merge_authors(authors, ids_to_merge, merge_to_id):
    merged_authors = {}
    for idx in ids_to_merge:
        email = authors[idx]['email']
        name = authors[idx]['name']
        destination_email = authors[merge_to_id]['email']
        destination_name = authors[merge_to_id]['name']
        if email != destination_email or name != destination_name:
            merged_authors[email] = authors[merge_to_id]
    return merged_authors


def parse_authors(stdout):
    authors = []
    for author in stdout.strip().split('\n'):
        author_info = author.split(';')
        authors.append({
            'name': author_info[0],
            'email': author_info[1]
        })
    return authors
