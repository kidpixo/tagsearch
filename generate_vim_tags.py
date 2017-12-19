# data : all the tags from tagsearch

# flattened tags
tags = list(set(flatten(data.values())))

# print for all tag the corresponding files
for t in tags:
   # formatting for vim tags
   for l in ['i@%s\t%s\t/tags/' % (t,i) for i in search_tag(t)]:
