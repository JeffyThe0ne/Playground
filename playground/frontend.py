# A frontend for Docker containers

term = input("What do you want to search for?")

filters = input('Any additional arguments? "help" for info')

filters = filters.lower()

if filters == 'help':
    print('--version/-ve KJV: Sets Bible version to KJV.  Default is ASB, supports ASB, KJV, and WBT',
        '\n--book/-b: Searches through only the given book',
        '\n--verbose/-vo: Displays all verses with the given term',
        '\n--save/-s: Saves file to a json')