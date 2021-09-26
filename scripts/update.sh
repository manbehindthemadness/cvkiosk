#! /bin/bash

backup_path=/media/backups/
backup_folder=node_backups
backup_location="$backup_path""$backup_folder"
py=/opt/venv/bin/python

mkdir /media/git 2> /dev/null
mount -t cifs //10.4.222.20/git /media/git -o username=fakeuser,noexec,password=FakePassword1!

bkp_name=$(hostname)_cfg_$(date +%M-%H-%d-%m-%Y).ini

mkdir "$backup_path" 2> /dev/null
mount -t cifs //10.4.222.20/common /media/backups -o username=fakeuser,noexec,password=FakePassword1!

bkp="$backup_location"/cvkiosk
mkdir -p $bkp

cd /opt/kiosk || return
cp cfg.ini "$bkp/$bkp_name" 2> /dev/null

git pull

if ! test -f "/usr/src/graphiend" 2> /dev/null
then
  cd /usr/src || return
  git clone /media/git/graphiend
else
  cd /usr/src/graphiend || return
  git pull
fi
cd /usr/src/graphiend || return
$py setup.py install

if ! test -f "/usr/src/cvclient" 2> /dev/null
then
  cd /usr/src || return
  git clone /media/git/cvclient
else
  cd /usr/src/cvclient || return
  git pull
fi
cd /usr/src/cvclient|| return
$py setup.py install

systemctl daemon-reload

umount /media/git
rm -fd /media/git

umount /media/backups
rm -fd /media/backups

chmod -R +x /opt/cvkiosk/scripts/*
find . -name "*.service" -exec chmod -x {} \;

rm -f /bin/update_c* 2> /dev/null

cp /opt/cvkiosk/scripts/update.sh /bin/update_cvkiosk
cp /opt/cvkiosk/scripts/backup_system.sh /bin/backup_system
