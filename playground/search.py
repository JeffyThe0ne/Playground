## A simple Bible database thing ##
import argparse
import prep
import json




# Books to grab start and end indexes from "book_indexes.json" if a book is specified
books_src = ('genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges', 'ruth', '1 samuel', '2 samuel', '1 kings', '2 kings', '1 chronices',
             '2 chronicles', 'ezra', 'nehemiah', 'esther', 'job', 'psalms', 'proverbs', 'ecclesiastes', 'song of solomon', 'isaiah', 'jeremiah', 'lamentations',
             'ezekiel', 'daniel', 'hosea', 'joel', 'amos', 'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai', 'zechariah', 'malachi',
             'matthew', 'mark', 'luke', 'john', 'acts', 'romans', '1 corinthians', '2 corinthians', 'galatians', 'ephesians', 'philippians', 'colossians',
             '1 thessalonians', '2 thessalonians', '1 timothy', '2 timothy', 'titus', 'philemon', 'hebrews', 'james', '1 peter', '2 peter', '1 john', '2 john',
             '3 john', 'jude', 'revelation')

# Argument Parsing
parser = argparse.ArgumentParser(description='Search the Bible for a term')

parser.add_argument('terms', nargs='+', help='Word or phrase to search for')                                                # Search terms
parser.add_argument('--version', '-ve', default='ASV', choices=['ASV','KJV','WBT'], help='Bible version you want to use')   # Bible version
parser.add_argument('--book', '-b', default=None, help='Bible book you want to use.  Case-insensitive.')                    # Specific book filter
parser.add_argument('--verbose', '-vo', action='store_true', help='Choose whether verses with search term are displayed')   # Display found verses
parser.add_argument('--save', '-s', default=None, help='Specify which file you wish to save to')


args = parser.parse_args()

def find_line(word, line):
    if word in line: return line

# Searches the Bible for the given term with applied filters
def search (args=argparse.Namespace):
    '''Searches the Bible for the given term with applied filters'''
    word = ' '.join(args.terms)
    data = []
    start = 0 # start index if no book is specified
    end = 31104 # end index if no book is specified

    # Open Bible
    with open(args.version + '.txt') as file:
        bible = file.readlines()

    # If user gives a book to search
    if args.book != None:
        
        book = args.book

        # For case-insensitivity        
        book = book.lower()

        # In case user used a '-' book name like 1-Corinthians
        if '-'in book:
            r = book.index('-')
            book = book[:r] + ' ' + book[r+1:] 
            
        # Corrects Song of Songs and Psalms to be system-friendly
        if book == 'song of songs': book = 'song of solomon'
        if book == 'psalms': book = 'psalm'

        # Quits program if book is not found
        if book not in books_src:
            print('"{}" is not a valid book'.format(book))
            quit()
        
        # Loads indexes json to get start indexes
        with open('book_indexes.json') as file:
            books = json.load(file)

        # Gets start and end indexes
        start = books[book]
        end = books[books_src[books_src.index(book) + 1]]

    # Search for term from start index
    data = []
    
    # Search through Bible
    for i in range(start, end):
        if word.lower() in bible[i].lower(): data.append(bible[i])

            
    # Display number of hits, if any
    hits = len(data)

    if hits == 0:
        print('No results')
    else:
        print('Results: {}'.format(hits))
    
    return data

# Displays all hits
def disp_info(data):
    '''Displays all hits'''
    for line in data:
        print(line)
    
    if len(data) != 0:
        print('Results: {}\n'.format(len(data)))

# Shows how many hits are in each book
def books(data):
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
    
    # Grab total to display percentage values in results
    total_value = 0
    for value in books.values(): total_value += value

    # Display values
    for key,value in books.items():
        print('{0}: {1} ({2:.2f}%)'.format(key, value, (value / total_value) * 100))

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
    if args.save != None: prep.save(data, args.save)
