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

// export interface ICampsite {
//   id: number
//   name: string
//   address: string
//   contact_number: string
//   created_at: string // ISO-8601 datetime

//   description: string
//   check_in: string // YYYY-MM-DD
//   check_out: string // YYYY-MM-DD
//   thumbnail_url: string
//   stay_nights: number // 정수로 받음
//   price: number
// }

// export interface ICampsiteResponse {
//   results: Campsite[]
// }

export interface IRegisterPayload {
  email: string
  username: string
  password: string
  password2: string
}

export interface IRegisterResponse {
  user: IUser
  message: string
  access_token: string
}

// --- 목록 페이지용 타입 ---
/**
 * 캠핑장 목록 API 응답에 포함된 개별 캠핑장 아이템 타입
 */
export interface ICampsiteListItem {
  id: number
  name: string
  address: string
  thumbnail_url: string
  price: number
  stay_nights: number
  check_in: string
  check_out: string
}

/**
 * 캠핑장 목록 API 응답 전체 타입
 */
export interface ICampsiteListResponse {
  results: ICampsiteListItem[]
}

/**
 * 캠핑장 이미지 타입
 */
export interface ICampsiteImage {
  id: number
  cloudflare_id: string
  order: number
}

/**
 * 캠핑장 사이트(A1, B5 등) 타입
 */
export interface ISite {
  id: number
  name: string
  camp_type: string
  base_price: string // DecimalField는 보통 문자열로 넘어옴
}

/**
 * 편의시설 타입
 */
export interface IAmenity {
  id: number
  name: string
  icon_url: string
}

/**
 * 운영 정책 타입
 */
export interface IPolicy {
  check_in_time: string // "15:00:00"
  check_out_time: string // "11:00:00"
  manner_time_start: string // "22:00:00"
  manner_time_end: string // "07:00:00"
}

/**
 * 캠핑장 상세 정보 API 응답 전체 타입
 */
export interface ICampsiteDetail {
  id: number
  name: string
  address: string
  description: string
  price: number
  contact_number: string
  check_in: string // "YYYY-MM-DD"
  check_out: string // "YYYY-MM-DD"
  stay_nights: number
  owner: { username: string } // 소유자 정보
  images: ICampsiteImage[] // 이미지 목록
  sites: ISite[] // 사이트 목록
  amenities: IAmenity[] // 편의시설 목록 (M2M)
  policy: IPolicy | null // 운영 정책 (1:1)
}

/**
 * 캠핑장 생성 시 추가 요금 규칙 타입
 */
export interface IPricingRule {
  id: number
  name: string
  start_date: string
  end_date: string
  day_of_week: string[]
  extra_charge: number | null
}

export interface IImageFile {
  id: number
  file: File
  previewSrc: string
  status: 'pending' | 'uploading' | 'success' | 'error'
  progress: number
  cloudflareId?: string // Cloudflare에서 반환된 이미지 ID
}
