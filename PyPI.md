# PyPI

Upload your package to PyPI Test

Run:

    python setup.py register -r pypitest

This will attempt to register your package against PyPI's test server, just to make sure you've set up everything correctly.

Then, run:

    python setup.py sdist upload -r pypitest

You should get no errors, and should also now be able to see your library in the test PyPI repository.
Upload to PyPI Live

Once you've successfully uploaded to PyPI Test, perform the same steps but point to the live PyPI server instead. To register, run:

    python setup.py register -r pypi

Then, run:

    python setup.py sdist upload -r pypi


more: http://peterdowns.com/posts/first-time-with-pypi.html