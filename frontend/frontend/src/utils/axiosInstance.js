import axios from 'axios';

// JWTトークンをローカルストレージから取得する関数
function getAccessToken() {
    return localStorage.getItem('access_token');
}

// Axiosインスタンスの作成
const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/', // DjangoバックエンドのAPIのベースURL
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// リクエスト時にJWTトークンをヘッダーに追加
axiosInstance.interceptors.request.use(
    (config) => {
        const token = getAccessToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// 統一されたレスポンス処理（code, message, data形式）
axiosInstance.interceptors.response.use(
    (response) => {
        const { code, message, data } = response.data;
        if (code >= 400) {
            console.error("APIエラー:", message);
        }
        return data; // 必要なデータだけを返す
    },
    (error) => {
        if (error.response) {
            console.error("サーバーエラー:", error.response.data.message || "不明なエラー");
        } else {
            console.error("ネットワークエラー:", error.message);
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;