def get_script(merged_authors):
    env_filter = ''
    for key, value in merged_authors.items():
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
""".format(bad_email=key, good_name=value['name'], good_email=value['email'])

    script = """
#!/bin/sh
# https://help.github.com/articles/changing-author-info/
git filter-branch -f --env-filter '
{env_filter}
' --tag-name-filter cat -- --branches --tags
    """.format(env_filter=env_filter)
    return script
