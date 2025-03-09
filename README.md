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

### **frontend コンテナを一時的に起動し、シェル(sh)を開く**
```bash
docker-compose run --rm frontend sh
```
