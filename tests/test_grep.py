
from StringIO import StringIO
from greptag import grep
# call py.test -s

sphinx_todo_single_line = StringIO("""
docstring for dummymodule

.. todo::
    Add some code

this module does nothing
""")
def test_find_sphinx_todo_single_line():
    tags = grep.find_matches(sphinx_todo_single_line, {'todo': grep.RE_TODO})
    assert len(tags['todo']) == 1
    assert tags['todo'][0].line == 3
    assert tags['todo'][0].message[1] == "    Add some code"


comment_todo_single_line = StringIO("""
for i in range(4):
    # TODO review loop
    print(i)
""")
def test_find_comment_todo_single_line():
    tags = grep.find_matches(comment_todo_single_line, {'todo': grep.RE_TODO})
    assert len(tags['todo']) == 1
    assert tags['todo'][0].line == 2
    assert tags['todo'][0].message[0] == "    # TODO review loop"


def test_grep_tag():
    files_tags = grep.grep_tags("tests/dummypackage")
    assert len(files_tags["tests/dummypackage/dummymodule.py"]["todo"]) > 0
    assert len(files_tags["tests/dummypackage/dummymodule.py"]["xxx"]) > 0
    for f, tags in files_tags.items():
        print(f)
        for tag, tag_msg in tags.items():
            print(tag, tag_msg)
