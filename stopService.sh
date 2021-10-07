pid=`ps -Af |grep SolarServer |grep -v grep |cut -d ' ' -f 7`
kill $pid
