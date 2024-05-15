## A simple Bible database thing ##
import json
import argparse
import re
import time

# Argument Parsing
parser = argparse.ArgumentParser(description='Search the Bible for a term')

parser.add_argument('terms', metavar='t', nargs='+', help='Word or phrase to search for')
parser.add_argument('--version', '-v', default='ASV', choices=['ASV','KJV','WBT'], help='Bible version you want to use')

args = parser.parse_args()

# Searches the Bible for a given word.  Faster than search_string() if the results are low.  Case-insensitive
def search_lines(args=argparse.Namespace):
    '''
    Searches the Bible by splitting verses into lines and then reading each line.  Faster than search_string if the results are low.  Case-insensitive
    '''
    
    # Open file
    with open(args.version + '.txt', 'r') as file:
        bible = file.readlines()

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

    # Open file
    with open(args.version + '.txt', 'r') as file:
        bible = file.read()

    # Converts the term lst into a string
    word = ' '.join(args.terms)

    last = bible.rfind(' ' or '\n') # stop index for the while loop
    hits = [] # data to store
    index = 0 # current pointer index

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

    lines = search_lines(args)

    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    

    # String Search
    start_time2 = time.time()
    
    strings = search_string(args)

    end_time2 = time.time()
    elapsed_time2 = end_time2 - start_time2

    # Final times
    print('Line search finished in {} seconds'.format(elapsed_time1))
    print("String search finished in {} seconds".format(elapsed_time2))

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