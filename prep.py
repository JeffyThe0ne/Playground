## Stuff to prepare search data ##
import json

books_src = ('Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings',
             '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm',
             'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
             'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
             'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
             'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy',
             'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
             'Jude', 'Revelation')

def line_indexes(books_src=tuple):
    with open('ASV.txt') as file:
        bible = file.readlines()
    
    books = {}

    for book in books_src:
        for i in range(len(bible)):
            if book + ' 1' in bible[i]:
                books[book.lower()] = i
                break

    save(books, 'book_indexes.json')

def save(data, file=str):
    print('Saving data...')

    with open(file, 'w') as output:
        json.dump(data, output)
    
    print('Data saved')

# Run to rebuild verse line start indexes
if __name__ == "__main__":

    line_indexes(books_src)

