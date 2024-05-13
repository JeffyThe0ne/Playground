## A simple Bible database thing ##
import json

# Startup
print('Initializing...')

# Searches the Bible for a given word.  Case-insensitive
def search_bible(word=str):
    '''
    Searches the Bible for a given word.  Case-insensitive
    '''
    results = 0
    data = []

    for line in bible:
        if word.upper() in line.upper():
            print(line)
            data.append(line)
            results += 1
    
    if results == 0:
        print("No results")
    else:
        print('Total results: {}'.format(results))
    
    return data

# Run
with open("ASV.txt", 'r') as fileb:
    bible = fileb.readlines()

print("Initialized")

# Term Search
word = input('What would you like to search for?')
data = search_bible(word)

# Save data to json
print('Saving data...')

with open('bible_search.json', 'w') as output:
    json.dump(data, output)

print('Data saved')