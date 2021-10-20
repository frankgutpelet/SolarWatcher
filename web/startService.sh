export PYTHONPATH=/home/frank/projects/SolarWatcher/web/
ipaddress=`ifconfig wlan0 |grep netmask | sed 's/\s\s*/ /g' |cut -d ' ' -f3`
python3 manage.py runserver $ipaddress:80 > log/Django.log 2>&1&
