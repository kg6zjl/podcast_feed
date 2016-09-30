#sudo yum -y update
#sudo yum -y install git
#sudo yum -y groupinstall "Development Tools"
#sudo yum -y install python-devel
#sudo yum -y install nginx
#sudo yum -y install libxml2-devel
#sudo pip install uWSGI
#sudo pip install flask
#sudo pip install gunicorn

#edit /etc/nginx/nginx.conf
	#change server_names_hash_bucket_size 128;
	
#edit nginx config: /etc/nginx/conf.d/virtual.conf
#add:
#server {
#    listen       80;
#    server_name  ec2-54-149-239-188.us-west-2.compute.amazonaws.com;
#
#    location / {
#        proxy_pass http://127.0.0.1:5001;
#    }
#}


#git init
#git reset --hard
#git fetch https://github.com/steve-smp/podcast_feed.git
#git pull https://github.com/steve-smp/podcast_feed.git
#git clone https://github.com/steve-smp/podcast_feed.git

#sudo pip install -r requirements.txt

###PREVIOUS steps moved to Dockerfile/image

python parse_feed.py

sudo fuser -k 80/tcp # kills anything running on port 80

sudo /etc/init.d/nginx start
kill $(ps aux | grep '[g]unicorn' | awk '{print $2}')
sudo /etc/init.d/nginx restart
gunicorn --bind 0.0.0.0:5001 --workers 16 wsgi &