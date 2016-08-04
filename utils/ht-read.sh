echo "testing ################################### "

nproc=$(grep -i "processor" /proc/cpuinfo | sort -u | wc -l)

phycore=$(cat /proc/cpuinfo | egrep "core id|physical id" | tr -d "\n" | sed s/physical/\\nphysical/g | grep -v ^$ | sort | uniq | wc -l)

if [ -z "$(echo "$phycore *2" | bc | grep $nproc)" ]

then

echo "Does not look like you have HT Enabled"

if [ -z "$( dmidecode -t processor | grep HTT)" ]

 then

echo "HT is also not Possible on this server"

 else

echo "This server is HT Capable,  However it is Disabled"

fi

else

   echo "yay  HT Is working"

fi


echo "testing ################################### "