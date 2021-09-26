#! /bin/bash
# https://github.com/koalaman/shellcheck/wiki/SC1009 -- lol
backup_type=$1
backup_args=zrv

if test $# -ne 0
then
  if [ "$backup_type" == "fast" ]
  then
    backup_args=azrv
  fi
fi

if ! test -f "/bin/pishrink" 2> /dev/null
then
  clear
  echo "pishrink binary not found, installing..."
  wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
  chmod +x pishrink.sh
  sudo mv pishrink.sh /bin/pishrink
  clear
fi
backup_name=$(hostname)-$(dpkg --print-architecture)
backup_path=/media/backups/
backup="$backup_path""$backup_name".img
clear
echo "current backup target: $backup"
read -r -p "enter custom suffix (or enter for none) " suffix

backup="$backup_path""$backup_name""$suffix".img
clear
read -r -p "backup to: $backup? [y/n]" confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]
then
  clear
  exit 1
fi
mkdir "$backup_path" 2> /dev/null
mount -t cifs //10.4.222.20/common /media/backups -o username=fakeuser,noexec,password=FakePassword1!
clear
# bash -c "dd bs=4M if=/dev/mmcblk0 status=progress | gzip > /media/backups/cvminer_x64"
dd bs=4M if=/dev/mmcblk0 of="$backup" status=progress
pishrink -$backup_args "$backup"
echo "operation complete"
