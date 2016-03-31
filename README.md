# Cleaning author in git repository by changing the Git history using a script

I've created a script that will change any commits that previously had bad email address in its author or committer fields to use the correct name and email address.

## requirements

 - python 3.5 (check with `python3 --version`)
 - pip (check with `pip --version`)
 - git (check with `git --version`)
 - unix system (On windows, you probably need cygwin)

**Warning**: This action is destructive to your repository's history. If you're collaborating on a repository with others, it's considered bad practice to rewrite published history. You should only do this in an emergency.


## installing

    pip install clean-git

## running

Create a fresh, bare clone of your repository:

    git clone --bare https://github.com/user/repo.git
    cd repo.git

simply run in a terminal

    clean-git


