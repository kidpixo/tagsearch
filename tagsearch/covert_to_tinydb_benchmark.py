%%timeit
metadatas = {}
for file in basepath.rglob('*md'):
    with file.open() as f:
        metadata, content = frontmatter.parse(f.read())
        if len(metadata['tags']) == 0:
           metadata['tags'] = ['']
        metadatas[file.name] = metadata
db = tdb.TinyDB(storage=tdb.storages.MemoryStorage)
db.insert_multiple(metadatas)
10    : 6.4 ms ± 474 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
100   : 54.1 ms ± 1.84 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
1000  : 517 ms ± 13.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
10000 : 7.43 s ± 826 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit
db = tdb.TinyDB(storage=tdb.storages.MemoryStorage)
for file in basepath.rglob('*md'):
    with file.open() as f:
        metadata, content = frontmatter.parse(f.read())
        metadata['file'] = str(file)
        try:
            tmp = db.insert(metadata)
        except ValueError:
            metadata['tags'] = ''
            tmp = db.insert(metadata)
10    : 6.99 ms ± 1.05 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)
100   : 69.9 ms ± 4.08 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
1000  : 1.41 s ± 137 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
10000 :

%%timeit
db = tdb.TinyDB(storage=tdb.storages.MemoryStorage)
for file in basepath.rglob('*md'):
    with file.open() as f:
        metadata, content = frontmatter.parse(f.read())
        metadata['file'] = str(file.name)
        if len(metadata['tags']) == 0:
            metadata['tags'] = ['']
        tmp = db.insert(metadata)
10 entry : 6.45 ms ± 425 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
100      : 71.7 ms ± 11.4 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
1000     : 1.58 s ± 94 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
10000    :
