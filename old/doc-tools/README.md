# Generating documentation from sources

This document exists for the benefit of anyone who wants to generate a new
sets of docs for the GitHub pages for this project.

**Should git ask you to set up your credentials, please follow the instructions it gives you and use your real name and your DataSift email address. Do not use pseudonyms or private email addresses.**

Prerequisites:

* You must use Ubuntu Linux
* You must have a GitHub account
* You must belong to the DataSift user group on GitHub

1. Copy make-docs.sh to your local machine running Ubuntu Linux.

2. Run `make-docs.sh` followed by the name of the branch you want to use as the source for the documentation, e.g. of you want to generate documentation based on the `master` branch, run:

    `sh ./make-docs.sh master`

3. That's it! you can delete the temporary directory now.

    `rm -rf tmp`
