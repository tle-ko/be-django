export BASEDIR=$(dirname $(dirname $(dirname "$0")))
export PATH=$BASEDIR/venv/bin/:$PATH

cd $BASEDIR/app

apt-get -y update
apt-get -y install nginx

ln -f .config/uwsgi.service /etc/systemd/system/uwsgi.service

cp -f .config/nginx.conf /etc/nginx/sites-available/tle.conf
ln -sf /etc/nginx/sites-available/tle.conf /etc/nginx/sites-enabled/tle.conf

if [ -e /etc/nginx/sites-enabled/default ]
then
    rm /etc/nginx/sites-enabled/default
fi

./manage.py collectstatic --noinput
./manage.py migrate

systemctl daemon-reload
systemctl enable uwsgi
systemctl restart uwsgi nginx
