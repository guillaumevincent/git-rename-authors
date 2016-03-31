[![Build Status](https://travis-ci.org/guillaumevincent/clean-git.svg?branch=master)](https://travis-ci.org/guillaumevincent/clean-git)


# Cleaning author in git repository by changing the Git history using a script

I've created a script that will change any commits that previously had bad email address in its author or committer fields to use the correct name and email address.
Usefull when you want to fix error in graph for example.


version 0.0.7

![](screenshot.png?raw=true)


## requirements

 - python 3.5 (check with `python3 --version`)
 - pip (check with `pip --version`)
 - git (check with `git --version`)
 - unix system (On windows, you probably need cygwin)

**Warning**: This action is destructive to your repository's history. If you're collaborating on a repository with others, it's considered bad practice to rewrite published history. You should only do this in an emergency.


## installing

    pip install cleangit

## running

Create a fresh, bare clone of your repository:

    git clone --bare https://github.com/user/repo.git
    cd repo.git

simply run in a terminal

    clean-git


## License

SmartConfigParser's License is the WTFPL – Do What the Fuck You Want to Public License.

        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. You just DO WHAT THE FUCK YOU WANT TO.



