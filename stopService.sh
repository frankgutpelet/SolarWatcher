pid=`ps -Af |grep SolarServer |grep -v grep |sed 's/\s\s*/ /g' |cut -d ' ' -f2`
kill $pid
