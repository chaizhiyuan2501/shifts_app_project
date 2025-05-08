import axios from '../utils/axiosInstance';

export const fetchRoles = () => {
    return axios.get("staff/roles/");
}

export const createRoles = (data) => {
    return axios.post("staff/roles/", data)
}

export const detailRoles = (id) => {
    return axios.get("staff/roles/{id}")
}