# shifts_app_project
シフトアプリ

### **Docker を使用してコンテナを起動**
```bash
docker-compose up --build
```

### **backend コンテナを一時的に起動し、シェル(sh)を開く**
```bash
docker-compose run --rm backend bash

```

```bash
python manage.py makemigrations

```

```bash
python manage.py migrate

```


```bash
python manage.py show_urls

```



```bash
docker-compose run --rm frontend bash

```

```bash
npm create vite@latest
```

npm install axios
npm install -D sass
npm run dev


#Swagger UI
```bash
http://127.0.0.1:8000/api/docs/swagger/#/

```


### **frontend コンテナを一時的に起動し、シェル(sh)を開く**
```bash
docker-compose run --rm frontend sh
```
