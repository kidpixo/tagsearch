# run interactive development enviroment without pycache:
# PYTHONDONTWRITEBYTECODE=1 jupyter-console-3.4 --kernel tagsearch

# basic loading for testing purpose
import tagsearch

data_base_path = tagsearch.data_base_path_checker('notes')
db = tagsearch.load_data_to_tinydb(data_base_path)
result = tagsearch.query_db(arguments['<tags>'], db)
arguments = tagsearch.docopt(tagsearch.__doc__, argv=['spam','!dog', 'foo', '!Monty'])
tagsearch.print_results(arguments, result)
