# Backend

## 准备数据库
```
mysql -u root
create database seat_reservation;
use seat_reservation;
source ./sql/create_all_table.sql
```
这里的数据库user, password, database_name需要和app/config.py中的配置一致

## 运行
```
conda create -n backend python=3.10
conda activate backend
pip install -r requirements.txt
cd app
python app.py
```

## 示范
```
❯ curl -X GET http://127.0.0.1:5000                                                        
{
    "message": "Hello, World!"
}

❯ curl -X GET http://127.0.0.1:5000/api/seat
{
    "seats": []
}
```

## 测试
在app目录下运行
```
python -m unittest tests/test_hello.py


.
----------------------------------------------------------------------
Ran 1 test in 0.110s

OK
```

### 测试CI
workflow backend_test.yml steps中添加
```
- name: 🔫 Run test_hello
run: |
    cd app && \
    MYSQL_RESTORE_SOURCE=$RESTORE \
    MYSQL_USER=$MYSQL_USER \
    MYSQL_PASSWORD=$MYSQL_PASSWORD \
    MYSQL_DATABASE=$MYSQL_DATABASE \
    python -m unittest tests/test_hello.py \
```
