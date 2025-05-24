export const SET_TOKEN = (token: string) => {
    localStorage.setItem("ACCESS_TOKEN", token)
}

export const GET_TOKEN = () => {
    return localStorage.getItem("ACCESS_TOKEN");
}