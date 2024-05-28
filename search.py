## A simple Bible database thing ##
import argparse
import prep
import json


# All books of the Bible.  Psalms is Psalm, Song of Songs is Song of Solomon
book_args = ('Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '1-Samuel', '2 Samuel', '2-Samuel', '1 Kings',
             '1-Kings', '2 Kings', '2-Kings', '1 Chronicles', '1-Chronicles', '2 Chronicles', '2-Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm',
             'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Song of Songs', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
             'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
             'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '1-Corinthians', '2 Corinthians', '2-Corinthians', 'Galatians', 'Ephesians',
             'Philippians', 'Colossians', '1 Thessalonians', '1-Thessalonians', '2 Thessalonians', '2-Thessalonians', '1 Timothy', '1-Timothy', '2 Timothy',
             '2-Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '1-Peter', '2 Peter', '2-Peter', '1 John', '1-John', '2 John', '2-John', '3 John',
             '3-John', 'Jude', 'Revelation')

books_src = ('genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges', 'ruth', '1 samuel', '2 samuel', '1 kings', '2 kings', '1 chronices',
             '2 chronicles', 'ezra', 'nehemiah', 'esther', 'job', 'psalms', 'proverbs', 'ecclesiastes', 'song of solomon', 'isaiah', 'jeremiah', 'lamentations',
             'ezekiel', 'daniel', 'hosea', 'joel', 'amos', 'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai', 'zechariah', 'malachi',
             'matthew', 'mark', 'luke', 'john', 'acts', 'romans', '1 corinthians', '2 corinthians', 'galatians', 'ephesians', 'philippians', 'colossians',
             '1 thessalonians', '2 thessalonians', '1 timothy', '2 timothy', 'titus', 'philemon', 'hebrews', 'james', '1 peter', '2 peter', '1 john', '2 john',
             '3 john', 'jude', 'revelation')

# Argument Parsing
parser = argparse.ArgumentParser(description='Search the Bible for a term')

parser.add_argument('terms', nargs='+', help='Word or phrase to search for')                                             # Search terms
parser.add_argument('--version', '-ve', default='ASV', choices=['ASV','KJV','WBT'], help='Bible version you want to use') # Bible version
parser.add_argument('--book', '-b', default=None, help='Bible book you want to use.  Case-insensitive.')                 # Specific book filter
parser.add_argument('--verbose', '-vo', action='store_true', help='Choose whether verses with search term are displayed') # Display found verses
parser.add_argument('--save', '-s', default=None, help='Specify which file you wish to save to')


args = parser.parse_args()


# Searches through Bible
def search (args=argparse.Namespace):
    '''Searches the Bible in the given version for the given term'''
    word = ' '.join(args.terms)
    data = []
    start = 0 # start index if no book is specified
    end = 31104 # end index if no book is specified

    with open(args.version + '.txt') as file:
        bible = file.readlines()

    if args.book != None:

        # For case-insensitivity
        args.book = args.book.lower()

        # In case they used a '-' book name like 1-Corinthians
        if '-' in args.book: args.book = args.book[0:args.book.index('-')] + ' ' + args.book[args.book.index('-') + 1:]  
            
        # Corrects Song of Songs and Psalms to be system-friendly
        if args.book == 'song of songs': args.book = 'song of solomon'
        if args.book == 'psalms': args.book = 'psalm'
        
        # Loads indexes json to get start indexes
        with open('book_indexes.json') as file:
            books = json.load(file)


        # Gets start index
        start = books[args.book]
        end = books[books_src[books_src.index(args.book) + 1]]

        print(start)
        print(end)


    # Search for term from start index
    data = list(filter(lambda line: word.lower() in line.lower(), bible[start:end]))
                
    hits = len(data)

    if hits == 0:
        print('No results')
    else:
        print('Results: {}'.format(hits))
    
    return data

def disp_info(data = list):
    for line in data:
        print(line)
    
    if len(data) != 0:
        print('Results: {}\n'.format(len(data)))

# Shows how many hits are in each book
def books(data=list):
    '''Shows how many hits are in each book'''
    books = {}

    for line in data:
        book = ''
        index = 0
    
        # Grabs the verse's book name by going from index 0 to the space before the '\t' char
        book = line[0:line.rfind(' ', 0, line.index('\t'))]

        # Add to number of book hits
        if book in books.keys():
            books[book] += 1
        else:
            books[book] = 1
    
    # Print results
    print("Books of results:")
    for key,value in books.items():
        print('{}: {}'.format(key, value))

# Run
if __name__ == "__main__":

    # Search for term
    data = search(args)
    print()

    # Display all hits if verbose is on
    if args.verbose == True: disp_info(data) 

    # Displays books of results if no book was specified
    if args.book == None: books(data)
    
    # Save data to json
    if args.save != None:
        prep.save(data, args.save)
