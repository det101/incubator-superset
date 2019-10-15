切换mysql

1. 起一个新的mysql数据库
2. 修改superset/config.py

ps superset db upgrade  可能会报错
解决方案

```
安装libmysqlclient-dev包即可，如果还有问题，可以安装python-dev。
# apt-get install libmysqlclient-dev python3-dev
```

### 常规步骤

```
# 涉及使用flask-cache需要装redis包
pip install redis

# install for development
# 这个步骤的执行时间比较长,可以退出重试,作用是装了superset所需要的基础依赖包
python setup.py develop

# Create an admin user
fabmanager create-admin --app superset

# Initialize the database
superset db upgrade

# Create default roles and permissions
superset init

# Load some data to play with
superset load_examples

# start a dev web server
flask run -p 8088 --with-threads --reload --debugge or pycharm debug
```