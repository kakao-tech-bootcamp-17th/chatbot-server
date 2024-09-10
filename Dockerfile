# Stage 1: 빌드 단계
FROM python:3.12-slim AS builder

WORKDIR /app

# 의존성 파일을 컨테이너로 복사
COPY requirements.txt .

# 의존성 설치 (빌드 단계에서만 사용)
RUN pip install --no-cache-dir --user -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Stage 2: 최종 런타임 단계
FROM python:3.12-slim

WORKDIR /app

# 빌드 단계에서 설치된 의존성을 최종 이미지로 복사
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Python 패키지들이 올바르게 실행되도록 PATH 설정
ENV PATH=/root/.local/bin:$PATH

# 애플리케이션 실행 명령어
CMD ["python", "run.py"]
