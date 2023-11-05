packetlist.csv:
	curl https://ukrepeater.net/csvcreate4.php > packetlist.csv

packetlist.json: packetlist.csv transform.py Makefile
	pipenv run python3 transform.py packetlist.csv packetlist.json
