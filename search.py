## A simple Bible database thing ##
import json
import argparse
import re
import time

# Argument Parsing
parser = argparse.ArgumentParser(description='Search the Bible for a term')

parser.add_argument('terms', metavar='t', nargs='+', help='Word or phrase to search for')
parser.add_argument('--version', '-v', default='ASV', choices=['ASV'], help='Bible version you want to use')

args = parser.parse_args()

# Searches the Bible for a given word.  Case-insensitive
def search_lines(args=argparse.Namespace):
    '''
    Searches the Bible for a given word.  Case-insensitive
    '''
    
    with open(args.version + '.txt', 'r') as file:
        bible = file.readlines()

    # Converts the term lst into a string
    word = ' '.join(args.terms)

    results = 0 # Total number of results
    data = [] # Store results to save later

    # file.tell() - returns the file pointer's current index

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

# Searches file as a single large string
def search_string(args=argparse.Namespace):
    with open(args.version + '.txt', 'r') as file:
        bible = file.read()

    word = ' '.join(args.terms)

    last = bible.rfind(' ' or '\n')
    hits = []
    index = 0
    results = 0

    while index < last:
        if word in bible[index:bible.find(' ' or '\n', index)]:
            if index <= 400:
                start = 0
            else:
                start = index - 400

            hits.append(bible[bible.rfind('\n', start, index):bible.find('\n', index)])
            results += 1

            index = bible.find('\n', index) + 1
            
        else:
            index = bible.find(' ' or '\n', index) + 1
        
        if index >= last:
            break

    print(hits)
    print('Total results: {}'.format(results))

# Saves search results to a json
def save(data, file=str, mode=str):
    print('Saving data...')

    with open(file, mode) as output:
        json.dump(data, output)
    
    print('Data saved')

# Run
if __name__ == "__main__":
 
     # Line Search
    start_time1 = time.time()

    search_lines(args)

    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    

    # String Search
    start_time2 = time.time()
    
    search_string(args)

    end_time2 = time.time()
    elapsed_time2 = end_time2 - start_time2

    # Final times
    print('Line search finished in {} seconds'.format(elapsed_time1))
    print("String search finished in {} seconds".format(elapsed_time2))

    # Save data to json
    # save(data, 'bible_search.json', 'w')

