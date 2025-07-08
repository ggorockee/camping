interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  // 추가 VITE_* 변수들 모두 여기에 선언
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
