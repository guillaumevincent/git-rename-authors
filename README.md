[![Build Status](https://travis-ci.org/guillaumevincent/clean-git.svg?branch=master)](https://travis-ci.org/guillaumevincent/clean-git)


# Clean git : clean the authors of your deposit git

Clean git is an interface to help clean authors and emails a repository git. This is an interface to perform an improved version of the github script : https://help.github.com/articles/changing-author-info/



version 0.0.8

![](screenshot.png?raw=true)


## requirements

 - python 3.5 (check with `python3 --version`)
 - pip (check with `pip --version`)
 - git (check with `git --version`)
 - unix system (I haven't tested on windows, it probably works on cygwin)

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



