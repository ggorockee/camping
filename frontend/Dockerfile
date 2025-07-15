# frontend/Dockerfile

# ----------------- STAGE 1: 빌드 환경 (Builder) -----------------
# Node.js 18-alpine 이미지를 빌드 환경으로 사용합니다. 'alpine' 버전은 가벼움
FROM node:lts-alpine AS builder

# 컨테이너 내의 작업 디렉토리를 설정합니다.
WORKDIR /app

# package.json과 lock 파일을 먼저 복사하여 Docker의 레이어 캐싱을 활용
# 의존성이 변경되지 않았다면, 이 단계의 캐시를 재사용하여 빌드 속도를 높일 수 잇음
COPY package*.json ./

# 프로젝트 의존성을 설치
RUN npm install

# 나머지 모든 소스 코드를 작업 디렉토리로 복사
COPY . .


# --build-arg로 전달받을 인자 선언
ARG VITE_CLOUDFLARE_ACCOUNT_HASH

# 전달받은 인자를 빌드 시점의 환경 변수로 설정
ENV VITE_CLOUDFLARE_ACCOUNT_HASH=$VITE_CLOUDFLARE_ACCOUNT_HASH



# React 애플리케이션을 프로덕션 모드로 빌드
# 빌드 결과물은 /app/build 디렉토리에 생성
RUN npm run build

# ----------------- STAGE 2: 프로덕션 환경 (Production) -----------------
# 경량 Nginx 이미지를 최종 배포 환경으로 사용
FROM nginx:mainline-alpine AS production

RUN apk add --no-cache nginx-module-geoip

# builder 단계의 /app/dist 디렉토리에서 생성된 결과물을 Nginx의 기본 서빙 디렉토리로 복사
COPY --from=builder /app/dist /usr/share/nginx/html

# 커스텀 Nginx 설정을 Nginx의 설정 디렉토리에 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 컨테이너의 80번 포트를 외부에 노출
EXPOSE 80

# Nginx 서버를 포그라운드에서 실행
CMD ["nginx", "-g", "daemon off;"]