# PRD: Lego Backorder Monitor (Cloud Edition)

## 1. 프로젝트 개요 (Project Overview)
- **명칭**: Lego Backorder Monitor (LBM)
- **목적**: 레고 공식 홈페이지에서 특정 제품의 가용성 상태를 주기적으로 모니터링하고, 백오더 일정 등 핵심 정보를 추출하여 사용자에게 텔레그램 알림을 발송
- **대상 제품**: 77252 APXGP Team Race Car (F1 The Movie)

## 2. 기술 스택 (Technical Stack)
- **Language**: Python 3.10+
- **Automation**: Playwright (w/ Stealth 패키지, User-Agent 위장)
- **Infrastructure**: GitHub Actions (Scheduled Workflow)
- **Notification**: Telegram Bot API

## 3. 상세 요구사항 (Detailed Requirements)

### 3.1. 데이터 추출 (Web Scraping)
- **대상 URL**: `https://www.lego.com/ko-kr/product/apxgp-team-race-car-from-f1-the-movie-77252`
- **추출 타겟**: `span[data-test="product-overview-availability"]`
- **데이터 검증 및 추출 방식**:
  - 선택한 HTML 요소가 제품 상태(품절, 백오더, 재고 있음 등)에 따라 구조가 변하는지 선행 확인 필요.
  - 단순 상태 문자열뿐만 아니라 "2026년 3월 31일 출고 예정" 같은 **날짜 정보**가 누락 없이 파싱되는지 검증 로직 포함.
- **봇 방지 회피**: Playwright `chromium` 브라우저 컨텍스트에 일반 사용자 환경(headers, viewport 등)을 모사하여 `403 Forbidden` 차단을 방지.

### 3.2. 알림 및 스케줄링 (Notification & Scheduling)
- **알림 채널**: Telegram Bot
- **실행 주기**: GitHub Actions Cron 기반 스케줄러를 사용하여 매일 오전 09:00 (KST) 구동. 
  *(주의: GitHub Actions cron은 UTC 기준이며 정확한 실행 시간에 소폭 지연이 있을 수 있음)*
- **보안 설정**: Telegram Bot API Token 및 Chat ID는 저장소에 노출되지 않도록 GitHub Secrets(`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) 환경변수로 런타임에 주입하여 운영.

### 3.3. 예외 및 에러 핸들링 (Error Handling)
- **요소 미발달 (Element Not Found)**: 타겟 HTML 코드가 렌더링되지 않거나 구조가 변경될 시 프로그램 패닉(Timeout)이 발생하므로, `try-except`로 예외를 감지하고 텔레그램으로 "HTML 구조 변경 의심 (요소 찾기 실패)" 관리자 알림 발송.
- **접속 밴 (Blocked Access)**: 레고 서버 측에서 강력하게 해당 IP 대역을 차단하거나 캡챠를 띄울 경우 예외 처리.

## 4. 고도화 계획 (Future Work)
- **상태 변경 시점에만 알림**: 매일 같은 정보를 보내는 피로도를 줄이기 위해, "품절 -> 백오더 가능" 또는 "1월 출고 -> 3월 출고"와 같이 이전 상태에서 변경사항이 감지되었을 때만 즉각 알림을 주는 스마트 알림 체계 도입 검토. (추가 저장소, ex: SQLite or GitHub Gists를 통한 이전 상태 기록 필요)

## 5. 성공 기준 (Acceptance Criteria)
- [ ] 정해진 시간(매일 09:00 KST 전후)에 사용자의 텔레그램 메신저로 제품 상태 및 출고 예정일이 메시지로 도착해야 함.
- [ ] 브라우저 우회 로직이 정상 작동하여 봇 차단(403) 없이 실제 페이지 데이터를 일관되게 읽어올 수 있어야 함.
