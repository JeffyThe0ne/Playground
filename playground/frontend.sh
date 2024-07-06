#!/bin/bash

echo "A simple Bible search tool";
echo 'Type your term along with filters, "h" for usage, or "e" to exit';

read var;

run() {
	python3 search.py $var
}


if [ "$var" == "h" ]; then
	echo 'Usage: python3 search.py [term] [--version/-ve {ASV, KJV, WBT}] [--book/-b BOOK] [--verbose/-vo] [--save/-s FILE.json]'

elif [ "$var" == "e" ]; then
	echo "Shutting down..."
	exit

else

	# run

fi;
