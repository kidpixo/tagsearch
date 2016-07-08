import random
import yaml

tags_bag = ['spaces',  'bar',  'test',  'foo',  'dog',  'python',  '42',  'fish',  'Monty']

n_notes = 50

outtext = '''
# Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet,  consectetur adipiscing elit. Fusce consequat suscipit auctor. Quisque accumsan ex in auctor dignissim. In id.

## Neque porro quisquam est qui dolorem ipsum quia dolor sit amet

- Lorem ipsum dolor sit amet,  consectetur adipiscing elit.
- Suspendisse scelerisque nisl id risus accumsan pharetra.
- Donec aliquet felis ut orci viverra,  eu volutpat nisi eleifend.

'''

for i in range(n_notes):
    ntags = random.randint(0, 5)
    filename = 'notes/notes %s.md' % i
    tags_local = random.sample(tags_bag, ntags)
    with open(filename,  'w') as file:
        file.write('---\n')
        file.write('tags : '+yaml.dump(tags_local))
        file.write('---\n')
        file.write(outtext)
