import axios from '../utils/axiosInstance';

// ユーザー一覧を取得するAPI
export const fetchUsers = () => {
    return axios.get('user/users/');
};

// 新規ユーザー登録API
export const registerUser = (data) => {
    return axios.post('user/register/', data);
};

// ログインAPI（名前とパスワードでログイン）
export const loginUser = (name, password) => {
    return axios.post('user/login/', { name, password });
};

// ログアウトやパスワード変更等のAPIがあれば、ここに追加
