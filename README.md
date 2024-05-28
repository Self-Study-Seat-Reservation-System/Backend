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

## CD
使用git tag的方式进行发布，见[华为云流水线](https://devcloud.cn-north-4.huaweicloud.com/cicd/project/8ac6cbe6f41648a3a757004f3e2e6ed0/pipeline/history/5456ec71082e45adbb677e4197dd94ac?from=in-project&v=1)，自动推送至华为云容器镜像服务（[backend_db](https://console.huaweicloud.com/swr/?region=cn-north-4#/swr/warehouse/detail/kikor97/seat-reservation-system/backend_db/tag) [backend_backend](https://console.huaweicloud.com/swr/?region=cn-north-4#/swr/warehouse/detail/kikor97/seat-reservation-system/backend_backend/tag)）


## docker使用
- 本地构建
```
docker-compose up --build
```
默认使用5000端口，可以通过修改环境变量的方式指定`export HOST_PORT=5001`

- 使用远端仓库

1. 修改docker-compose.remote.yml中version镜像版本
2. 登录[华为云容器镜像服务](https://console.huaweicloud.com/swr/?region=cn-north-4#/swr/create/experience?kind=pullpush)
```
docker-compose -f docker-compose.remote.yml up
```


推荐使用如下指令
```
docker-compose down -v # 清理数据

docker ps
docker exec -it <container_name_or_id> mysql -uroot -p # 进入docker查看数据库
docker exec -it <container_id_or_name> /bin/bash # 进入docker
```