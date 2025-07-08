export interface TokenResponse {
  access: string
}

export interface User {
  id: number
  email: string
  username: string
  phone_number: string
}

export interface LoginPayload {
  email: string
  password: string
}
