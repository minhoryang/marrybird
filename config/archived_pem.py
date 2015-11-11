"""Archive .pem and tag it.

$ cat me_marrybird_app_ios_v1-PRODUCTION.pem | git hash-object -w --stdin
0000000000000000000000000
$ git tag -a me_marrybird_app_ios_v1_PRODUCTION_pem 0000000000000000000000000
$ # git push --tags
$ git show me_marrybird_app_ios_v1_PRODUCTION_pem
"""

from dulwich.repo import Repo
repo = Repo('.')  # .git located
tag = 'me_marrybird_app_ios_v1-PRODUCTION_pem'

def get_content_of_tag(repo, tag):
    tag = repo.refs.read_ref('refs/tags/' + tag)
    commit = repo.get_object(tag)
    pemfile = repo.get_object(commit.object[1]).as_raw_string()
    return pemfile

