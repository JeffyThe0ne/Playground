## A simple Bible database thing ##
import json
import argparse
import time

# All books of the Bible.  Psalms is Psalm, Song of Songs is Song of Solomon
books_src = ('Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
            'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
            'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
             'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians',
             '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation')

# Argument Parsing
parser = argparse.ArgumentParser(description='Search the Bible for a term')

parser.add_argument('terms', nargs='+', help='Word or phrase to search for')
parser.add_argument('--version', '-v', default='ASV', choices=['ASV','KJV','WBT'], help='Bible version you want to use')
parser.add_argument('--book', '-b', default=None, choices=(books_src),
                    help='Bible book you want to use.  Case-sensitive.\nSpecific book names here:\nPsalms: use Psalm\nSong of Songs: use Song of Solomon')

args = parser.parse_args()

# Opens Bible
def open_bible(args=argparse.Namespace, mode=str):
    bible = ''
    
    # Open file with readlines()
    if mode == 'l':
        with open(args.version + '.txt', 'r') as file:
            bible = file.readlines()
    # Open with read()
    elif mode == 's':
        with open(args.version + '.txt', 'r') as file:
            bible = file.read()

    return bible

# Searches the Bible for a given word.  Faster than search_string() if the results are low.  Case-insensitive
def search_lines(args=argparse.Namespace):
    '''
    Searches the Bible by splitting verses into lines and then reading each line.  Faster than search_string if the results are low.  Case-insensitive
    '''
    
    # Open Bible
    bible = open_bible(args, 's')

    # Converts the term lst into a string
    word = ' '.join(args.terms)

    results = 0 # Total number of results
    data = [] # Store results to save later

    # Read and process search
    for line in bible:
        if word.upper() in line.upper():
            print(line)
            data.append(line)
            results += 1
    
    # Prints total results
    if results == 0:
        print("No results")
        return
    else:
        print('Total results: {}'.format(results))
    
    return data

# Searches the Bible by reading it as one large string.  Faster than search_lines() if the results are high.  Case-insentitive
def search_string(args=argparse.Namespace):
    '''
    Searches the Bible by reading it as one large string. Faster than search_lines() if the results are high.  Case-insensitive
    '''

    # Open Bible
    bible = open_bible(args, 's')
    
    # Converts the term lst into a string
    word = ' '.join(args.terms)

    # Start and stop indexes for the while loop
    last = int # stop index for the while loop
    hits = [] # data to store
    index = 0 # current pointer index

    if args.book == None:
        last = bible.rfind(' ' or '\n')
        index = 0
    else:
        with open(args.version + '_indexes.json') as file:
            books = json.load(file)
        
        index = books[args.book][0]
        last = books[args.book][1]

    while index < last:
        if word.upper() in bible[index:bible.find(' ' or '\n', index)].upper():
            
            # Longest verse in the Bible is close to 400 chars.  Start is used to find where the hit's verse starts
            if index <= 400:
                start = 0
            else:
                start = index - 400

            hits.append(bible[bible.rfind('\n', start, index):bible.find('\n', index)]) # appends the text around the hit between its closest \n chars

            index = bible.find('\n', index) + 1 # Skips to next line to increase efficiency
            
        else:
            index = bible.find(' ' or '\n', index) + 1 # Skips to next word/line for same reason
        
        if index >= last: # Ends loop at last \n char
            break

    print(hits)
    print('Total results: {}'.format(len(hits)))
    return hits


# Shows how many hits are in each book
def books(data=list):
    books = {}
    book = ""

    for line in data:
        book = ''
        index = 0
        
        line = line.strip() # Ensures compatibility with both search methods

        while True:
            if index == 0 or not line[index].isdigit():
                book += line[index]
                index += 1
            else:
                book.strip()
                break

        if book in books.keys():
            books[book] += 1
        else:
            books[book] = 1
        
    

    print("Books of results:")
    for key,value in books.items():
        print('{} : {}'.format(key, value))

# Used to find where each book starts        
def book_indexes(args=argparse.Namespace, books_src=tuple):
    # Open Bible
    bible = open_bible(args, 's')

    indexes = ()

    books = {}

    # Finds "<Book> 1" to ensure finding a verse as beginning
    for i in range(len(books_src) - 1):
        book = books_src[i]
        
        start = bible.find(books_src[i] + ' 1')
        stop = bible.find(books_src[i + 1] + ' 1') - 2

        books[book] = (start, stop)

    start = (bible.find(books_src[-1]))
    stop = bible.rfind('\n') - 1

    books[books_src[-1]] = (start, stop)

    # Prints out verses at the indexes as a test
    for index in books.values():
        print(bible[index[0]:bible.find('\n', index[0])])
        print(bible[index[1]])
    
    # Save to JSON
    save(books, '{}_indexes.json'.format(args.version), 'w')

# Saves search results to a json
def save(data, file=str, mode=str):
    print('Saving data...')

    with open(file, mode) as output:
        json.dump(data, output)
    
    print('Data saved')

# Run
if __name__ == "__main__":
 
    # Line Search
    # start_time1 = time.time()

    # lines = search_lines(args)

    # end_time1 = time.time()
    # elapsed_time1 = end_time1 - start_time1
    

    # String Search
    # start_time2 = time.time()
    
    strings = search_string(args)
    print()
    books(strings)

    # end_time2 = time.time()
    # elapsed_time2 = end_time2 - start_time2

    # Final times
    # print('Line search finished in {} seconds'.format(elapsed_time1))
    # print("String search finished in {} seconds".format(elapsed_time2))

    # Save data to json
    # save(data, 'bible_search.json', 'w')

    # Tests for discrepancies between the two methods
    # discrepancies = []
    
    # for i in range(0, len(lines)):
    #    lines[i] = lines[i].strip()

    # for i in range(0, len(strings)):
    #    strings[i] = strings[i].strip()

    #for line in lines:
    #    for phrase in strings:
    #        if line not in strings:
    #            discrepancies.append(line)
    #            break

    #print(len(discrepancies))