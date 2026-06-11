# 애니 보고 만화 보고

애니메이션-원작 만화 연동 정보 및 추천 플랫폼

**프로젝트 기획 및 설계 명세서**

---

# 1. 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 서비스명 | 애니 보고 만화 보고 |
| 서비스 유형 | 서브컬처 메타데이터 유틸리티 & 커뮤니티 플랫폼 |
| 핵심 가치 | 애니 시청 후 원작 만화 몇 화부터 봐야 하는지 즉시 해결 |
| 포지셔닝 | 직접 스트리밍 없이 공식 PV 임베드 + 정교한 매핑 데이터 제공 |

## 1.1 서비스 컨셉

애니 보고 만화 보고는 애니메이션 시청 후 원작 만화를 이어서 보고 싶은 사용자의 니즈를 해결하는 매핑 데이터 플랫폼입니다.

직접 영상 스트리밍 기능은 제공하지 않고, 공식 프로모션 영상(PV/트레일러) 임베드와 정교한 메타데이터(애니-만화 매핑, 장르, 제작사, 에피소드 정보)에 집중하여 저작권 리스크를 줄인 서브컬처 유틸리티 서비스로 포지셔닝합니다.

## 1.2 핵심 도메인

- 애니와 만화의 연결 정보: 애니를 본 뒤 원작 만화를 어디서부터 이어 보면 되는지 제공
- 작품 상세 정보: 애니/만화 상세, 에피소드 목록, 미디어(PV, OP, ED)
- 사용자 저장 및 활동 기능: 찜하기, 관심작품 등록, 댓글
- AI 추천 및 챗봇: 취향 기반 추천과 매핑 정보 질의응답

---

# 2. 주요 기능 명세

## A. 메인 홈 및 탐색

- 글로벌 통합 검색: 애니메이션, 만화 작품명 및 매핑 정보를 한 번에 검색
- 메타데이터 기반 필터링: 장르, 태그, 제작사 기준 탐색
- 추천 매핑 정보 큐레이션: `애니 X기 -> 원작 만화 Y권 Z화부터` 형태의 카드형 UI 제공
- AI 애니 추천 진입 버튼: 자연어 입력 기반 맞춤 작품 및 매핑 정보 반환

## B. 작품 상세 및 매핑 정보

- 통합 매핑 인디케이터: `애니 1기 -> 만화 1~4권` 형태의 직관적인 브릿지 UI
- 애니 정보 보기 / 만화 정보 보기 상호 이동 버튼
  - 애니 상세 페이지에서 연결된 만화 상세 페이지로 이동
  - 만화 상세 페이지에서 연결된 애니 상세 페이지로 이동
- 합법적 미디어 제공: 공식 PV, OP, ED를 YouTube iFrame으로 임베드
- 에피소드/단행본 리스트: 회차별 평점, 방영일/발행일, 줄거리 제공
- 찜하기 / 공유하기 기능

## C. AI 챗봇 추천 시스템

- 플로팅 챗봇: 모든 페이지 우측 하단에 AI 챗봇 버튼 제공
- 자연어 추천: `주술회전 다 봤는데 비슷한 거 찾아줘` 같은 입력에 맞춤 추천 반환
- 작품별 챗봇: 상세 페이지에서 해당 작품 관련 질의응답 제공
- AI 엔진: OpenAI API 사용
- 대화 문맥 유지:
  - DB 저장 없이 Django 세션 또는 캐시 레이어에서 대화 히스토리 배열 관리
  - 서버 재시작 시 대화 내용 초기화 허용

> AI 챗봇은 데이터 품질과 기본 탐색 기능이 먼저 갖춰진 뒤 붙이는 것이 적합하므로 3차 기능으로 분리합니다.

## D. 커뮤니티 및 사용자 상호작용

- 작품/에피소드별 댓글
- 매핑 정보 토론 및 감상 공유
- 대댓글 지원
- 소셜 로그인: 구글, 카카오, 네이버 OAuth 기반 간편 로그인

## E. 마이페이지 및 활동 기록

- 유저 프로필: 닉네임, 프로필 이미지, 가입일, 저장 수치 대시보드
- 찜한 콘텐츠: 애니/만화 북마크
- 콘텐츠 상태 뱃지: 연재중, 완결, NEW 등
- 나의 활동: 댓글 작성 이력

---

# 3. 기술 스택 및 아키텍처

| 분류 | 기술 | 선택 이유 |
| --- | --- | --- |
| Frontend | Vue.js (SPA) | 매끄러운 페이지 전환 및 챗봇 상태 관리 |
| Backend | Python / Django + DRF | REST API 서버, 관리자 패널 기본 제공 |
| Database | SQLite -> PostgreSQL | 초기 개발은 SQLite, 배포 환경은 PostgreSQL |
| LLM API | OpenAI API | 자연어 챗봇 추천 엔진 |
| 영상 데이터 | YouTube Data API v3 | 공식 PV 및 트레일러 URL 수집 |
| 만화 데이터 | 수동 시드 데이터 + 외부 참고 데이터 | 초기 MVP에서는 검증된 수동 데이터 중심으로 구축 |

## 3.1 데이터 수집 원칙

외부 데이터는 자동 수집보다 검증된 수동 시드 데이터를 우선합니다.

특히 애니-만화 매핑 정보는 서비스의 핵심 신뢰 자산이므로, 출처가 불분명한 데이터를 무분별하게 가져오기보다 관리자 검수 또는 수동 입력을 전제로 설계합니다.

## 3.2 챗봇 아키텍처

```text
[Vue.js 프론트] -> (메시지 전송) -> [Django API 서버]
                                         |
                                         v
                              Django 세션/캐시에서
                              conversation_history 배열 조회
                                         |
                                         v
                              OpenAI API 호출
                              전체 히스토리 배열 전달
                                         |
                                         v
                              응답 수신 후 히스토리 배열 업데이트
                              DB 저장 없음
                                         |
                                         v
                        [Vue.js 프론트] <- (응답 반환)
```

---

# 4. MVP 구현 우선순위

## 4.1 1차 MVP: 핵심 탐색 및 매핑

1차 MVP의 목표는 로그인 없이도 서비스의 핵심 가치인 `애니를 본 뒤 만화를 어디서부터 보면 되는지`를 확인할 수 있게 만드는 것입니다.

| 기능 | 관련 테이블 |
| --- | --- |
| 홈 화면 및 추천 매핑 카드 | animes, mangas, anime_manga_mappings, metadata_tags |
| 통합 검색 | animes, mangas, anime_manga_mappings |
| 애니 상세 조회 | animes, anime_manga_mappings |
| 만화 상세 조회 | mangas, manga_episodes, anime_manga_mappings |
| 애니 -> 만화 정보 보기 | anime_manga_mappings |
| 만화 -> 애니 정보 보기 | anime_manga_mappings |

## 4.2 2차 MVP: 사용자 기능

| 기능 | 관련 테이블 |
| --- | --- |
| 소셜 로그인 | users, social_accounts |
| 찜 / 관심작품 | users, favorites |
| 마이페이지 찜 목록 | users, favorites |
| 프로필 조회 및 수정 | users |

## 4.3 3차 기능

- 댓글 및 대댓글
- 나의 활동 이력
- 트레일러 및 테마곡 미디어 확장
- AI 추천 챗봇
- 관리자 페이지 고도화

---

# 5. 데이터베이스 설계

## 5.1 테이블 구성

### 1차 MVP 필수 테이블

| 테이블명 | 설명 |
| --- | --- |
| animes | 애니메이션 작품 메타데이터 |
| mangas | 만화 작품 메타데이터 |
| manga_episodes | 만화 단행본/화 목록, 평점, 발행일 |
| anime_manga_mappings | 애니-만화 연결 핵심 브릿지 테이블 |
| metadata_tags | 장르, 태그, 제작사 등 탐색용 메타데이터 |
| anime_tags | 애니-메타데이터 N:M 중간 테이블 |
| manga_tags | 만화-메타데이터 N:M 중간 테이블 |

### 2차 MVP 필수 테이블

| 테이블명 | 설명 |
| --- | --- |
| users | 회원 기본 정보 |
| social_accounts | 소셜 로그인 계정 연결 |
| favorites | 찜/관심작품 |

### 3차 이후 추가 테이블

| 테이블명 | 설명 |
| --- | --- |
| anime_media | 애니 트레일러, OP, ED YouTube URL 저장 |
| anime_comments | 애니 댓글 |
| manga_comments | 만화 댓글 |

## 5.2 핵심 테이블 상세 설계

### users

| 컬럼 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| id | BIGINT | PK | 회원 ID |
| nickname | VARCHAR(50) | NOT NULL, UNIQUE | 닉네임 |
| email | VARCHAR(255) | UNIQUE, NULL | 이메일 |
| profile_image_url | VARCHAR(500) | NULL | 프로필 이미지 |
| role | VARCHAR(20) | NOT NULL | USER, ADMIN |
| status | VARCHAR(20) | NOT NULL | ACTIVE, DELETED, BANNED |
| joined_at | DATETIME | NOT NULL | 가입일 |
| created_at | DATETIME | NOT NULL | 생성일 |
| updated_at | DATETIME | NOT NULL | 수정일 |
| deleted_at | DATETIME | NULL | 탈퇴일 |

소셜 로그인 중심 구조이므로 password 컬럼은 우선 제외합니다. 일반 로그인 추가 시 `password_hash` 컬럼을 추가합니다.

### social_accounts

| 컬럼 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| id | BIGINT | PK | 소셜 계정 ID |
| user_id | BIGINT | FK -> users | 회원 ID |
| provider | VARCHAR(20) | NOT NULL | KAKAO, NAVER, GOOGLE |
| provider_user_id | VARCHAR(255) | NOT NULL | 소셜 플랫폼 사용자 ID |
| email | VARCHAR(255) | NULL | 소셜 이메일 |
| created_at | DATETIME | NOT NULL | 생성일 |
| updated_at | DATETIME | NOT NULL | 수정일 |

- `UNIQUE(provider, provider_user_id)` 복합 유니크 제약을 둡니다.

### animes

| 컬럼 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| id | BIGINT | PK | 애니 ID |
| title | VARCHAR(255) | NOT NULL | 제목 |
| original_title | VARCHAR(255) | NULL | 원제 |
| poster_image_url | VARCHAR(500) | NULL | 포스터 이미지 |
| banner_image_url | VARCHAR(500) | NULL | 상세 대표 이미지 |
| type | VARCHAR(30) | NULL | TVA, MOVIE, OVA |
| release_year | INT | NULL | 방영 연도 |
| episode_count | INT | NULL | 총 에피소드 수 |
| status | VARCHAR(30) | NOT NULL | ONGOING, COMPLETED, UPCOMING |
| studio | VARCHAR(100) | NULL | 제작사명 |
| synopsis | TEXT | NULL | 줄거리 |
| rating_avg | DECIMAL(2,1) | DEFAULT 0 | 평균 평점 |
| rating_count | INT | DEFAULT 0 | 평점 수 |
| favorite_count | INT | DEFAULT 0 | 찜 수 |
| created_at | DATETIME | NOT NULL | 생성일 |
| updated_at | DATETIME | NOT NULL | 수정일 |

### mangas

| 컬럼 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| id | BIGINT | PK | 만화 ID |
| title | VARCHAR(255) | NOT NULL | 제목 |
| original_title | VARCHAR(255) | NULL | 원제 |
| cover_image_url | VARCHAR(500) | NULL | 표지 이미지 |
| banner_image_url | VARCHAR(500) | NULL | 상세 배너 이미지 |
| author | VARCHAR(100) | NULL | 작가 |
| illustrator | VARCHAR(100) | NULL | 그림 작가 |
| publisher | VARCHAR(100) | NULL | 출판사 |
| description | TEXT | NULL | 설명 |
| status | VARCHAR(30) | NOT NULL | ONGOING, COMPLETED |
| rating_avg | DECIMAL(2,1) | DEFAULT 0 | 평균 평점 |
| rating_count | INT | DEFAULT 0 | 평점 수 |
| favorite_count | INT | DEFAULT 0 | 관심작품 수 |
| created_at | DATETIME | NOT NULL | 생성일 |
| updated_at | DATETIME | NOT NULL | 수정일 |

### manga_episodes

| 컬럼 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| id | BIGINT | PK | 에피소드 ID |
| manga_id | BIGINT | FK -> mangas | 만화 ID |
| volume_number | INT | NULL | 권 번호 |
| chapter_number | INT | NULL | 화 번호 |
| title | VARCHAR(255) | NULL | 에피소드 제목 |
| published_at | DATE | NULL | 발행일 |
| rating_avg | DECIMAL(2,1) | DEFAULT 0 | 평균 평점 |
| created_at | DATETIME | NOT NULL | 생성일 |
| updated_at | DATETIME | NOT NULL | 수정일 |

### anime_manga_mappings

| 컬럼 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| id | BIGINT | PK | 매핑 ID |
| anime_id | BIGINT | FK -> animes | 애니 ID |
| manga_id | BIGINT | FK -> mangas | 만화 ID |
| anime_season_label | VARCHAR(50) | NULL | Season 1, Part 2 등 |
| anime_episode_from | INT | NULL | 애니 시작 회차 |
| anime_episode_to | INT | NULL | 애니 종료 회차 |
| manga_volume_from | INT | NULL | 만화 시작 권 |
| manga_volume_to | INT | NULL | 만화 종료 권 |
| manga_chapter_from | INT | NULL | 만화 시작 화 |
| manga_chapter_to | INT | NULL | 만화 종료 화 |
| continue_volume | INT | NULL | 애니 이후 이어볼 권 |
| continue_chapter | INT | NULL | 애니 이후 이어볼 화 |
| mapping_text | VARCHAR(500) | NOT NULL | 화면 표시용 매핑 문구 |
| description | TEXT | NULL | 상세 설명 |
| source_note | VARCHAR(500) | NULL | 데이터 출처 또는 검수 메모 |
| created_at | DATETIME | NOT NULL | 생성일 |
| updated_at | DATETIME | NOT NULL | 수정일 |

예시:

- `애니 1기: 원작 코믹스 1~5권`
- `애니 2기 이후: 원작 만화 8권 45화부터`

### favorites

| 컬럼 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| id | BIGINT | PK | 찜 ID |
| user_id | BIGINT | FK -> users | 회원 ID |
| target_type | VARCHAR(20) | NOT NULL | ANIME, MANGA |
| target_id | BIGINT | NOT NULL | 애니 ID 또는 만화 ID |
| status_label | VARCHAR(50) | NULL | 시청중, 완결, 읽는중 등 |
| created_at | DATETIME | NOT NULL | 생성일 |

- `UNIQUE(user_id, target_type, target_id)` 제약을 둡니다.
- DB 레벨 FK 없이 앱 레벨에서 target 존재 여부를 검증합니다.
- Django MVP에서는 단순한 `target_type + target_id` 방식을 우선 사용합니다.

### metadata_tags / anime_tags / manga_tags

| 컬럼 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| metadata_tags.id | BIGINT | PK | 메타데이터 ID |
| metadata_tags.name | VARCHAR(50) | NOT NULL, UNIQUE | 액션, 판타지, MAPPA 등 |
| metadata_tags.type | VARCHAR(20) | NOT NULL | GENRE, TAG, STUDIO |
| anime_tags.anime_id | BIGINT | FK + UNIQUE(anime_id, tag_id) | 애니 N:M 연결 |
| anime_tags.tag_id | BIGINT | FK + UNIQUE(anime_id, tag_id) | 태그 N:M 연결 |
| manga_tags.manga_id | BIGINT | FK + UNIQUE(manga_id, tag_id) | 만화 N:M 연결 |
| manga_tags.tag_id | BIGINT | FK + UNIQUE(manga_id, tag_id) | 태그 N:M 연결 |

기존 `genres`라는 이름은 장르만 담는 것처럼 보이므로, 장르/태그/제작사를 함께 다루는 목적에 맞춰 `metadata_tags`로 변경합니다.

## 5.3 테이블 관계 요약

| 관계 | 카디널리티 | 설명 |
| --- | --- | --- |
| users -> social_accounts | 1 : N | 한 회원이 여러 소셜 계정 연결 가능 |
| users -> favorites | 1 : N | 한 회원이 여러 찜 보유 |
| users -> anime_comments / manga_comments | 1 : N | 한 회원이 여러 댓글 작성 |
| animes <-> mangas | M : N | anime_manga_mappings 브릿지 테이블로 연결 |
| animes / mangas <-> metadata_tags | M : N | anime_tags / manga_tags 중간 테이블 |
| animes -> anime_media | 1 : N | PV, OP, ED 미디어 |
| mangas -> manga_episodes | 1 : N | 단행본/화 에피소드 |
| animes -> anime_comments | 1 : N | 댓글 및 대댓글 |
| mangas -> manga_comments | 1 : N | 댓글 및 대댓글 |

---

# 6. 설계 및 구현 주의사항

## 6.1 favorites 다형성 구조

favorites 테이블은 `target_type + target_id` 조합으로 애니와 만화를 단일 테이블에서 관리합니다.

장점:

- 마이페이지에서 애니/만화를 하나의 찜 목록으로 통합 관리 가능
- 테이블 구조가 단순함

단점:

- DB 레벨 FK 직접 설정이 어려움
- 서비스 레이어에서 target 존재 여부를 반드시 검증해야 함

## 6.2 댓글 Soft Delete 권장

댓글 삭제 시 실제 삭제 대신 `status = DELETED`와 `deleted_at` 처리를 권장합니다.

대댓글이 있는 경우 부모 댓글을 물리 삭제하면 댓글 트리가 깨질 수 있으므로, 화면에서는 `삭제된 댓글입니다` 형태로 노출합니다.

## 6.3 Django 목록 조회 최적화

홈/목록 화면에서 모든 연관관계를 한 번에 로드하면 성능 이슈가 발생할 수 있습니다.

Django에서는 다음 방식을 우선 사용합니다.

- `select_related`: FK, 1:1 관계 최적화
- `prefetch_related`: N:M, 역참조 관계 최적화
- `annotate`: 찜 수, 댓글 수, 평점 등 집계
- 화면별 Serializer 분리: 목록용/상세용 응답 필드 구분
- 필요한 경우 별도 QuerySet 또는 service 함수로 조회 로직 분리

## 6.4 매핑 정보 별도 테이블 분리 원칙

애니 보고 만화 보고의 핵심 기능인 애니-만화 매핑 정보는 단순 문자열로 `animes` 테이블에 넣지 않고, `anime_manga_mappings`로 분리합니다.

이렇게 해야 아래 기능을 안정적으로 구현할 수 있습니다.

- 애니에서 만화 찾기
- 만화에서 애니 찾기
- 홈 추천 매핑 카드 구성
- 검색 결과에서 매핑 정보 노출
- AI 챗봇의 매핑 정보 기반 답변 생성
- 하나의 만화에 여러 애니 시즌이 연결되는 케이스 처리

## 6.5 AI 챗봇 대화 문맥 관리

OpenAI API 호출 시 대화 히스토리를 DB에 저장하지 않고 Django 서버 세션 또는 캐시 레이어에서 `conversation_history` 배열로 관리합니다.

- 사용자별 세션 키에 대화 배열 저장
- 예시: `chat_history_{user_id}` 또는 비로그인 세션 키 기반 저장
- 서버 재시작 시 대화 내용 초기화 허용
- DB 부하 없이 짧은 문맥 유지 가능

장기적인 추천 품질 개선을 위해서는 추후 사용자의 찜, 검색, 조회 이력을 별도 추천 신호로 활용할 수 있습니다.

---

# 7. 화면별 API 호출 요약

## 7.1 홈 화면

| 기능 | API |
| --- | --- |
| 홈 초기 데이터 | GET /api/v1/home |
| 통합 검색 | GET /api/v1/search?keyword= |
| 추천 매핑 더보기 | GET /api/v1/mappings/recommendations |

## 7.2 로그인

| 기능 | API |
| --- | --- |
| 카카오 로그인 URL 발급 | GET /api/v1/auth/oauth/kakao/url |
| 네이버 로그인 URL 발급 | GET /api/v1/auth/oauth/naver/url |
| 구글 로그인 URL 발급 | GET /api/v1/auth/oauth/google/url |
| OAuth 콜백 | GET /api/v1/auth/oauth/{provider}/callback |
| 로그아웃 | POST /api/v1/auth/logout |

## 7.3 애니 상세

| 기능 | API |
| --- | --- |
| 애니 상세 | GET /api/v1/animes/{animeId} |
| 원작 만화 매핑 | GET /api/v1/animes/{animeId}/manga-mappings |
| 트레일러/테마곡 | GET /api/v1/animes/{animeId}/media |
| 댓글 목록 | GET /api/v1/animes/{animeId}/comments |
| 댓글 작성 | POST /api/v1/animes/{animeId}/comments |
| 찜하기 | POST /api/v1/favorites |
| 찜 취소 | DELETE /api/v1/favorites/{favoriteId} |

## 7.4 만화 상세

| 기능 | API |
| --- | --- |
| 만화 상세 | GET /api/v1/mangas/{mangaId} |
| 에피소드 목록 | GET /api/v1/mangas/{mangaId}/episodes |
| 연결 애니 매핑 | GET /api/v1/mangas/{mangaId}/anime-mappings |
| 댓글 목록 | GET /api/v1/mangas/{mangaId}/comments |
| 댓글 작성 | POST /api/v1/mangas/{mangaId}/comments |
| 관심작품 등록 | POST /api/v1/favorites |

## 7.5 마이페이지

| 기능 | API |
| --- | --- |
| 프로필 조회 | GET /api/v1/users/me/profile |
| 프로필 수정 | PATCH /api/v1/users/me/profile |
| 찜한 콘텐츠 | GET /api/v1/users/me/favorites |
| 나의 댓글 활동 | GET /api/v1/users/me/comments |

## 7.6 AI 챗봇

| 기능 | API |
| --- | --- |
| 메시지 전송 및 응답 수신 | POST /api/v1/chat/message |
| 대화 초기화 | DELETE /api/v1/chat/session |

---

# 8. 1차 개발 권장 순서

1. Django 프로젝트 및 앱 구조 생성
2. 핵심 모델 생성: animes, mangas, manga_episodes, anime_manga_mappings, metadata_tags
3. 관리자 페이지에서 작품 및 매핑 데이터 입력 가능하게 구성
4. 홈 추천 매핑 API 구현
5. 통합 검색 API 구현
6. 애니 상세 API 구현
7. 만화 상세 API 구현
8. Vue 라우팅 및 화면 구현
9. MVP seed 데이터 추가
10. 사용자 기능, 댓글, AI 챗봇 순서로 확장

---

# 9. 결론

애니 보고 만화 보고의 핵심 구조를 한 문장으로 정리하면 다음과 같습니다.

**사용자는 애니와 만화를 검색하고, 애니-원작 만화 매핑 정보를 즉시 확인한 뒤, 애니 정보 보기와 만화 정보 보기 버튼으로 연결된 작품을 자유롭게 탐색한다. 이후 찜, 댓글, AI 챗봇을 통해 더 깊은 개인화 경험으로 확장한다.**

따라서 1차 MVP는 작품 정보, 매핑 정보, 에피소드 목록, 검색 기능에 집중하고, 로그인/찜/댓글/AI 챗봇은 단계적으로 확장합니다.
