# Detection Rules

| Rule ID | eventName | Risk | 설명 |
|---|---:|---:|---|
| rule-create-user | CreateUser | 70 | 신규 IAM 사용자 생성 |
| rule-attach-user-policy | AttachUserPolicy | 90 | 사용자 정책 연결 |
| rule-admin-policy-attach | AttachUserPolicy + AdministratorAccess | 95 | 관리자 권한 부여 |
| rule-put-user-policy | PutUserPolicy | 85 | 인라인 정책 추가 |
| rule-create-access-key | CreateAccessKey | 80 | 장기 Access Key 생성 |
| rule-assume-role | AssumeRole | 65 | Role 전환 |
| rule-stop-logging | StopLogging | 95 | CloudTrail 비활성화 |
| rule-delete-trail | DeleteTrail | 100 | 감사 로그 삭제 |
| rule-open-security-group | AuthorizeSecurityGroupIngress + 0.0.0.0/0 | 85 | 공개 인바운드 허용 |
| rule-put-bucket-policy | PutBucketPolicy | 75 | S3 Bucket 정책 변경 |


