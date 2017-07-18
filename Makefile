#all: clean build install test
disable-services:
	-sudo service loggserver  stop

enable-services: 
	sudo service loggserver start
	sleep 1s

status-services:
	ps -ef | grep -in "loggserver"

clean:
	rm -rf build dist clsa.egg-info

app: 
	sudo python2.7 setup.py install --force

packages: 
	sudo apt-get install python-dev -y
	sudo apt-get install python-pip -y
	sudo pip install -r requirements.txt
	sudo python2.7 setup.py install --force

test:
	python2.7 -m unittest -v test
	nosetests tests

ansible: clean disable-services app enable-services status-services


install: clean disable-services packages enable-services status-services


dist: clean  
	python2.7 setup.py bdist
	python2.7 setup.py sdist
	python2.7 setup.py bdist_egg

