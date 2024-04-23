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