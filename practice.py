## A simple Bible database thing ##

# Startup
print("Initializing...")

# Searches the Bible for a given word.  Case-insensitive
def search_bible(word=str):
    '''
    Searches the Bible for a given word.  Case-insensitive
    '''
    results = 0

    for line in bible:
        if word.upper() in line.upper():
            print(line)
            results += 1
    
    if results == 0:
        print("No results")
    else:
        print('Total results: {}'.format(results))

# Searches the Webster 1828 Dictionary for the word's entry if it exists
def search_dictionary(word=str):
    '''
    Searches the Webster 1828 Dictionary for the word entry if it exists
    '''

    for line in d:
        if word.upper() + ', ' == line[0:len(word) + 2]:
            print(line)
    else:
        print('No results')



# Run
with open("ASV.txt", 'r') as fileb:
    bible = fileb.readlines()

with open("Webster.txt", 'r', encoding='utf-8') as filed:
    d = filed.readlines()

print("Initialized")

word = input("What would you like to search for?")

search_dictionary(word)