import sys
import os
import re
import collections
import fnmatch

RE_TODO = re.compile(r"[Tt][Oo][Dd][Oo]")
RE_NOTE = re.compile(r"[Nn][Oo][Tt][Ee]")
RE_FIXME = re.compile(r"[Ff][Ii][Xx][Mm][Ee]")
RE_XXX = re.compile(r"[Xx]{3}")

TAGS_RE = {
    "todo": RE_TODO,
    "note": RE_NOTE,
    "fixme": RE_FIXME,
    "xxx": RE_XXX
}

Tag = collections.namedtuple('Tag', ['line', 'message'])


def grep_tags(path):
    files_tags = {}
    for f in walk_path(path):
        with open(f, "r") as fh:
            files_tags[f] = find_matches(fh, TAGS_RE)
    return files_tags

def gen_find(filepat,top):
    """from http://www.dabeaz.com/generators-uk/GeneratorsUK.pdf
    """
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist,filepat):
            yield os.path.join(path,name)

def walk_path(path):
    file_tags = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            base, ext = os.path.splitext(filename)
            if ext != '.py':
                continue
            yield os.path.join(dirpath, filename)


def find_matches(source, tags_re):
    tags = {t: [] for t in tags_re.keys()}
    continue_i = None
    for i, line in enumerate(source):
        print(i, line)
        for tag, regex in tags_re.items():
            match = re.search(regex, line)
            if match:
                if continue_i:
                    tags[tag][-1].message.append(line.rstrip('\n'))
                else:
                    tags[tag].append(Tag(i, [line.rstrip('\n')]))

                if '#' in line[:match.start()]:
                    # check for # in next lines
                    continue_i = i
                    tags[tag][-1].message.extend(_find_py_comment(source))
                elif '.. ' in line[:match.start()]:
                    # check indentation of next lines
                    continue_i = i
                    tags[tag][-1].message.extend(_find_sphinx_directive(source))
            else:
                if continue_i:
                    continue_i = None

    return tags


def _find_py_comment(source):
    line0 = next(source)
    message = [line0.rstrip('\n')]
    white = re.match(r"\s*#", line0)
    if white:
        white = white.group()
        for line in source:
            if line.startswith(white):
                message.append(line.rstrip('\n'))
            else:
                break
        return message
    else:
        return []


def _find_sphinx_directive(source):
    line0 = next(source)
    message = [line0.rstrip('\n')]
    white = re.match(r"\s*", line0)
    if white:
        white = white.group()
        #while True:
        #    line = next(source)
        for line in source:
            if line.startswith(white):
                message.append(line.rstrip('\n'))
            else:
                break
        return message
    else:
        return []


