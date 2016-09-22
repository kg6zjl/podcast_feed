sudo yum -y update
sudo yum -y install git
sudo yum -y groupinstall "Development Tools"
sudo yum -y install python-devel
sudo yum -y install nginx
#sudo pip install uWSGI
#sudo pip install flask
#sudo pip install gunicorn

#edit nginx config: /etc/nginx/conf.d
#echo server {
#    listen       80;
#    server_name  ec2-52-26-62-78.us-west-2.compute.amazonaws.com;
#
#    location / {
#        proxy_pass http://127.0.0.1:5000;
#    }
#}

mkdir -p app
cd app

git pull https://github.com/steve-smp/quotes_db.git

sudo pip install -r requirements.txt
sudo /etc/init.d/nginx start
kill $(ps aux | grep '[g]unicorn' | awk '{print $2}')
sudo /etc/init.d/nginx restart
gunicorn --bind 0.0.0.0:5000 --workers 16 wsgi &