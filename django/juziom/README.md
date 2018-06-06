1、安装pip  详细文档及使用http://www.ttlsa.com/python/how-to-install-and-use-pip-ttlsa/

     下载pip
     wget "https://pypi.python.org/packages/source/p/pip/pip-7.1.2.tar.gz#md5=3823d2343d9f3aaab21cf9c917710196" --no-check-certificate

     安装pip
     tar -xzvf pip-7.1.2.tar.gz
     cd  pip-7.1.2
     python setup.py install

2、安装saltstack   版本 salt 2015.5.3 (Lithium)

     使用epel源
     安装saltstack
     yum install salt-master
     yum install salt-minion
     yum install salt-api

3、安装cherrypy

     pip install cherrypy==3.8.0
     
4、安装pygit2

     git clone https://github.com/libgit2/libgit2.git
     cd libgit2/
     mkdir build
     cd build/ && cmake .. && cmake --build .
     make install
     pip install pygit2
     ln -s /usr/local/lib/libgit2.so.25 /lib64/

5、配置api

    #cd /etc/pki/tls/certs
    #make testcert
    umask 77 ; \
    /usr/bin/openssl genrsa -aes128 2048 > /etc/pki/tls/private/localhost.key

    Enter pass phrase:    #键入加密短语，4到8191个字符
    Verifying - Enter pass phrase:    #确认加密短语
    umask 77 ; \
        /usr/bin/openssl req -utf8 -new -key /etc/pki/tls/private/localhost.key -x509 -days 365 -out /etc/pki/tls/certs/localhost.crt -set_serial 0
    Enter pass phrase for /etc/pki/tls/private/localhost.key:    #再次输入相同的加密短语
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [XX]:CN    #都可以选填
    State or Province Name (full name) []:Shanghai
    Locality Name (eg, city) [Default City]:Shanghai
    Organization Name (eg, company) [Default Company Ltd]:
    Organizational Unit Name (eg, section) []:
    Common Name (eg, your name or your server's hostname) []:
    Email Address []:xxx@qq.com

    #cd ../private/
    #openssl rsa -in localhost.key -out localhost_nopass.key
    Enter pass phrase for localhost.key:    #输入之前的加密短语
    writing RSA key


    使用系统pam进行认证,添加系统用户和密码
    #useradd -M -s /sbin/nologin saltapi
    passwd juziyule

    用户名:saltapi
    密码:juziyule

    添加saltapi.conf 和 eauth.conf文件
    #cat /etc/salt/master.d/saltapi.conf
        rest_cherrypy:
            port: 8888
            ssl_crt: /etc/pki/tls/certs/localhost.crt
            ssl_key: /etc/pki/tls/private/localhost_nopass.key

    #cat /etc/salt/master.d/eauth.conf
    external_auth:
        pam:
            saltapi:
                - .*
                - test*
                - '@runner'
                - '@wheel'


    /etc/init.d/salt-master restart
    /etc/init.d/salt-api restart
    netstat -tnlp | grep 8888   看到8888端口监听在127.0.0.1上就可以了

    基本用法
    获取token
    #curl -k https://host:8888/login -H "Accept: application/x-yaml" -d username='saltapi' -d password='juziyule' -d eauth='pam'
    #curl -k https://host:8888/ -H "Accept: application/x-yaml" -H "X-Auth-Token: 获取的token" -d client='local' -d tgt='*' -d fun='test.echo' -d arg='hello world'

6、安装及配置Django 和 Django crontab

    pip install Django==1.8.4
    pip install django-crontab
    pip install install mysql-python

    vim settings.py       配置数据库和salt api 认证信息
    DATABASES = {
               'default': {
                   'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                   'NAME': 'saltshaker', # Or path to database file if using sqlite3.
                   'USER': 'root', # Not used with sqlite3.
                   'PASSWORD': 'sina', # Not used with sqlite3.
                   'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
                   'PORT': '3306', # Set to empty string for default. Not used with sqlite3.
        }
    }

    根据添加的系统用户信息,在settings.py 行尾添加如下信息,进行salt api 的认证配置

    # SaltStack API

    SALT_API_URL = 'https://host:8888'
    SALT_API_USER = 'saltapi'
    SALT_API_PASSWD = 'juziyule'


7、异步请求 Celery

    安装 django-celery (3.1.17)

        pip install django-celery==3.1.17

    安装 celery

        pip install celery==3.1.17

    安装 rbbitmq

        详细安装请产看官方文档 ubuntu 安装http://www.rabbitmq.com/install-debian.html
        Centos 安装http://www.rabbitmq.com/install-rpm.html

        添加rbbitmq 仓库

            echo 'deb http://www.rabbitmq.com/debian/ testing main' >> /etc/apt/sources.list

        避免安装时发生警告添加公钥

            wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
            apt-key add rabbitmq-signing-key-public.asc

        apt-get install rabbitmq-server

    开启rabbitmq-management plugin管理插件
    /usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_management

    rabbitmqctl stop
    /etc/init.d/rabbitmq-server start
    此时可以访问 127.0.0.1:15672
    用户名:guest
    密码:guest


    vim settings.py       配置celery和rabbitmq

    # celery + rabbitmq

    platforms.C_FORCE_ROOT = True   # Running a worker with superuser privileges
    djcelery.setup_loader()
    BROKER_HOST = "127.0.0.1"
    BROKER_PORT = 5672
    BROKER_USER = "guest"
    BROKER_PASSWORD = "guest"
    BROKER_VHOST = "/"

8、 启动celery worker

    python manage.py celery worker --loglevel=info -c 5

9、 相关数据库同步

    

10、 启动计划任务

    python manage.py crontab add              添加计划任务用于获取queue队列数

11、 启动服务

    python manage.py runserver 0.0.0.0:8000
    添加用户
    python manage.py createsuperuser
    使用浏览器打开 http://127.0.0.1:8000

12、Rsync服务

    /etc/rsync.passwd  密码配置文件
    
13、关闭selinux

    使用 nginx 和 uwsgi 运行 

    1、pip install uwsgi django-uwsgi
    2、https://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
    3、yum install nginx
