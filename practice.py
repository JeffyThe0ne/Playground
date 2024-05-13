## A simple Bible database thing ##
import json

# Startup
print('Initializing...')

# Searches the Bible for a given word.  Case-insensitive
def search_bible(word=str):
    '''
    Searches the Bible for a given word.  Case-insensitive
    '''

    results = 0 # Total number of results
    data = [] # Store results to save later

    for line in bible:
        if word.upper() in line.upper():
            print(line)
            data.append(line)
            results += 1
    
    if results == 0:
        print("No results")
        return
    else:
        print('Total results: {}'.format(results))
    
    return data

# Saves search results to a json
def save(data, file=str, mode=str):
    print('Saving data...')

    with open(file, mode) as output:
        json.dump(data, output)
    
    print('Data saved')

# Run
with open("ASV.txt", 'r') as file:
    bible = file.readlines()

print("Initialized")

# Term Search
word = input('What would you like to search for?')
data = search_bible(word)

# Save data to json
save(data, 'bible_search.json', 'w')