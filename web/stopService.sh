pid=`ps -Af |grep '/usr/local/bin/python3.8 manage.py' |grep -v grep |grep -v grep |cut -d ' ' -f 7`
kill $pid
