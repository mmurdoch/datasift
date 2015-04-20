import marvelous
import sys


try:
    if len(sys.argv) < 3:
        print('Usage: python marvelous.py <public_key> <private_key>')
        exit(0)

    retriever = marvelous.CharacterRetriever(sys.argv[1], sys.argv[2])
    retriever.run()
except KeyboardInterrupt:
    pass
