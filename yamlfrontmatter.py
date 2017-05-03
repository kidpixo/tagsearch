#!/Users/damo_ma/.virtualenvs/yamlfrontmatter/bin/python
# -*- coding: UTF-8 -*-
# [Python Frontmatter — Python Frontmatter 0.4.2 documentation](http://python-frontmatter.readthedocs.io/en/latest/)
import frontmatter
import os
# import json
import sys

basedir = os.path.expanduser("~") + "/.notes/"

metadatas = {}

for file in os.listdir(basedir):
    if file.endswith(".md"):
        # print(os.path.join(basedir, file))
        with open(os.path.join(basedir, file)) as f:
            metadata, content = frontmatter.parse(f.read())
            metadatas[file] = metadata

# Data structure:
# {'file 1.md'    : {'tags' : ['ricetta']},
# [...]
#  'file n-1.md'  : {'tags' : ['rss']},
#  'file n.md'    : {'tags' : []}}
# Translate to :
# {'tag1'= set(file1, file2, file3)}

tags = {}
for filename, filetags in metadatas.items():
    # print(filename)
    tmp_filetags = filetags.get('tags')
    if tmp_filetags is not None:
        for t in tmp_filetags:
            # print (t)
            files_with_tag = tags.get(t)
            if files_with_tag:
                # print('tag already present in ',files_with_tag)
                files_with_tag.add(filename)
            else:
                # print('tag not yet present, addig',filename )
                tags[t] = set([filename])

# print(tags.get(*sys.argv[1:]))

# to do : chek if all sys.argv[1:] in tags.keys()
searchlist = [el for el in sys.argv[1:] if tags.get(el)]
print('tags : ', searchlist)
import pprint
pprint.pprint(set.intersection(*[tags[l] for l in searchlist]))

# print(json.dumps(metadatas, ensure_ascii=False))
