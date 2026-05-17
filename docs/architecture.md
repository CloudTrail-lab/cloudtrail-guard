# Architecture

```text
CloudTrail JSON / S3 Object
        ↓
Backend Parser
        ↓
Normalizer
        ↓
Risk Engine
        ↓
Alert Generator / Timeline Builder / Attack Reconstructor
        ↓
FastAPI
        ↓
React UI
```

## 책임 분리

- Frontend: 시각화, 필터 UI, 상세 패널, 페이지 전환
- Backend: CloudTrail 파싱, 정규화, 위험도 계산, Alert/Timeline/Attack Graph 생성
- Sample Data: 공개 가능한 sanitized CloudTrail 예제
- Infra: Docker Compose, 향후 Terraform 확장
