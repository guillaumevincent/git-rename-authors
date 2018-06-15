def get_name_and_email(author):
    name, email = author.split('<')
    return name.strip(), email.strip().replace('>', '')


def generate_script(source_authors, destination_author):
    env_filter = ''
    good_name, good_email = get_name_and_email(destination_author)
    for author in source_authors:
        env_filter += """
if [ "$GIT_COMMITTER_EMAIL" = "{bad_email}" ]
then
    export GIT_COMMITTER_NAME="{good_name}"
    export GIT_COMMITTER_EMAIL="{good_email}"
fi
if [ "$GIT_AUTHOR_EMAIL" = "{bad_email}" ]
then
    export GIT_AUTHOR_NAME="{good_name}"
    export GIT_AUTHOR_EMAIL="{good_email}"
fi
""".format(bad_email=author['email'], good_name=good_name, good_email=good_email)

    script = """
#!/bin/sh
# https://help.github.com/articles/changing-author-info/
git config user.name "{good_name}"
git config user.email "{good_email}"
git filter-branch -f --env-filter '
{env_filter}
' --tag-name-filter cat -- --branches --tags
    """.format(env_filter=env_filter, good_name=good_name, good_email=good_email)
    return script
