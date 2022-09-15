pid=`ps -Af |grep '/usr/bin/python3 manage.py' |grep -v grep |grep -v grep |sed 's/\s\s*/ /g' |cut -d ' ' -f 3`
kill $pid
