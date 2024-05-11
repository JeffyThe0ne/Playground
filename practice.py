## A simple Bible database thing ##

# Startup
print("Initializing...")

# Searches the Bible for a given word.  Case-insensitive
def search_bible(word=str):
    '''
    Searches the Bible for a given word.  Case-insensitive
    '''
    results = 0

    for line in bible_lines:
        if word.upper() in line.upper():
            print(line)
            results += 1
    
    if results == 0:
        print("No results")
    else:
        print('Total results: {}'.format(results))


# Run
bible = open("ASV.txt", 'r')
bible_lines = bible.readlines()

print("Initialized")

term = input("What would you like to search for?")

search_bible(term)