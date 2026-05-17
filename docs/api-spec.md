# API Spec

## Dashboard

`GET /api/dashboard/summary`

## Events

`GET /api/events?query=&event_name=&status=&limit=100`

`POST /api/events/upload`

CloudTrail JSON 파일을 업로드합니다. `{ "Records": [...] }` 형식을 지원합니다.

## Alerts

`GET /api/alerts?status=&method=&min_risk=`

`PATCH /api/alerts/{alert_id}/status`

```json
{ "status": "in_progress" }
```

## Timeline

`GET /api/timeline/{user_id}`

## Attack Reconstruction

`GET /api/attack/{alert_id}`
