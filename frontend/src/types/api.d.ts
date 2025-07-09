export interface ITokenResponse {
  access: string
}

export interface IUser {
  id: number
  email: string
  username: string
  phone_number: string
}

export interface ILoginPayload {
  email: string
  password: string
}

export interface ICampsite {
  id: number
  name: string
  address: string
  contact_number: string
  created_at: string // ISO-8601 datetime

  description: string
  check_in: string // YYYY-MM-DD
  check_out: string // YYYY-MM-DD
  thumbnail_url: string
  stay_nights: number // 정수로 받음
  price: number
}

export interface ICampsiteResponse {
  results: Campsite[]
}
