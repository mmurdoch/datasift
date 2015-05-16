import argparse
import operator
from marvelous import MarvelWsClient

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sort', default='name',
    choices=['name', 'min', 'mean', 'max', 'count'],
    help='column on which to sort (default: sort by name)')
parser.add_argument('-r', action='store_true', help='sort in reverse order')
parser.add_argument('-f', '--filter',
    choices=['min', 'mean', 'max', 'count'],
    help='column on which to filter (default: none)')
parser.add_argument('-o', '--operator',
    choices=['lt', 'le', 'eq', 'gt', 'ge'], default='ge',
    help='filter operator (ignored unless -f/--filter specified, default: >=)')
parser.add_argument('-v', '--value', type=int, default=10,
    help='value to filter by (ignored unless -f/--filter specified, default: 10)')
args = parser.parse_args()

client = MarvelWsClient()
character_stats = client.get_statistics()

if args.filter:
    operators = {
        'lt': operator.lt, 'le': operator.le, 'eq': operator.eq,
        'ge': operator.ge, 'gt': operator.gt
    }
    op = operators[args.operator]

    character_stats = filter(lambda row: op(row[args.filter], args.value),
        character_stats)

character_stats = sorted(
    character_stats, key=lambda row: row[args.sort], reverse=args.r)

max_name_length = 0
if character_stats:
    max_name_length = reduce(lambda a,b: max(a,b),
        map(lambda s: len(s['name']), character_stats))

print('Name{0} Count Min Max Mean Std. dev.'.format(' ' * (max_name_length-4)))
for stat in character_stats:
    print('{0}{1} {2}     {3}   {4}   {5}    {6}'.format(
        stat['name'], ' ' * (max_name_length-len(stat['name'])),
        stat['count'], stat['min'], stat['max'],
        round(stat['mean'],2), round(stat['stddev'],2)))
