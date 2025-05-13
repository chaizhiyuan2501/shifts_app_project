
export interface registerForm {
    username: string,
    email: string,
    password: string,
}

export interface loginForm {
    username: string,
    password: string,
}

interface dataType {
    token: string
}

export interface loginResponseData {
    code: number,
    data: dataType
}

interface user {
    id: number,
    name: string,
    email: string,
    is_staff: boolean,
    is_active: boolean
}

export interface userResponseData {
    code: number,
    data: user
}

export interface UserDetail {

}