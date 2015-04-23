from marvel.marvel import Marvel
import sys

m = Marvel(sys.argv[1], sys.argv[2])

character_data_wrapper = m.get_characters(orderBy="name,-modified", limit="5", offset="15")
print character_data_wrapper.status
print character_data_wrapper.data.total

for character in character_data_wrapper.data.results:
    print character.name
