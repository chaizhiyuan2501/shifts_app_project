# Node.js 18 の公式イメージを使用
FROM node:18

# 作業ディレクトリを設定
WORKDIR /app


# TODO: todo project作成後、コメントアウトを外す
# COPY ./shifts_project/package*.json /app/shifts_project/
# WORKDIR /app/shifts_project
# RUN npm install

# Viteの開発サーバーを起動
CMD ["npm", "run", "dev"]

# ポート5173を公開
EXPOSE 5173