# 애니 보고 만화 보고 구현 명세서

이 문서는 `PROJECT_SPEC.md`를 실제 구현 가능한 단위로 쪼갠 개발 명세서입니다.

기준 기술 스택:

- Frontend: Vue.js SPA
- Backend: Django + Django REST Framework
- Database: SQLite 개발 환경, PostgreSQL 배포 환경
- Auth: OAuth 기반 소셜 로그인
- AI: OpenAI API, 3차 기능에서 구현

---

# 1. 구현 범위

## 1.1 1차 MVP 목표

1차 MVP는 로그인 없이도 서비스의 핵심 가치를 확인할 수 있어야 합니다.

사용자는 다음 흐름을 수행할 수 있습니다.

1. 홈에서 추천 애니-만화 매핑 카드를 본다.
2. 애니 또는 만화 제목으로 검색한다.
3. 애니 상세 페이지에서 원작 만화 매핑 정보를 확인한다.
4. 만화 상세 페이지에서 연결된 애니 매핑 정보를 확인한다.
5. 애니 상세과 만화 상세을 상호 이동한다.

## 1.2 1차 MVP 제외 범위

다음 기능은 1차 MVP 이후 구현합니다.

- 소셜 로그인
- 찜/관심작품
- 마이페이지
- 댓글
- AI 챗봇
- YouTube Data API 자동 수집
- 외부 만화 데이터 자동 수집

---

# 2. 백엔드 구현 명세

## 2.1 Django 앱 구조

권장 앱 구조:

```text
backend/
  config/
    settings.py
    urls.py
  apps/
    works/
      models.py
      serializers.py
      views.py
      urls.py
      admin.py
      services.py
      filters.py
      tests.py
    users/
      models.py
      serializers.py
      views.py
      urls.py
      admin.py
    interactions/
      models.py
      serializers.py
      views.py
      urls.py
    chat/
      views.py
      services.py
  manage.py
```

앱 역할:

| 앱 | 역할 |
| --- | --- |
| works | 애니, 만화, 에피소드, 매핑, 태그 |
| users | 회원, 소셜 계정 |
| interactions | 찜, 댓글 |
| chat | AI 챗봇 |

1차 MVP에서는 `works` 앱만 먼저 구현합니다.

## 2.2 공통 모델 규칙

모든 주요 모델은 아래 공통 필드를 가집니다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| created_at | DateTimeField | 생성일 |
| updated_at | DateTimeField | 수정일 |

권장 추상 모델:

```python
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

## 2.3 works 앱 모델

### Anime

| 필드 | Django 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | CharField(max_length=255) | O | 제목 |
| original_title | CharField(max_length=255, blank=True) | X | 원제 |
| poster_image_url | URLField(max_length=500, blank=True) | X | 포스터 이미지 |
| banner_image_url | URLField(max_length=500, blank=True) | X | 상세 배너 이미지 |
| type | CharField(max_length=30, choices=AnimeType) | X | TVA, MOVIE, OVA |
| release_year | PositiveIntegerField(null=True, blank=True) | X | 방영 연도 |
| episode_count | PositiveIntegerField(null=True, blank=True) | X | 총 에피소드 수 |
| status | CharField(max_length=30, choices=WorkStatus) | O | ONGOING, COMPLETED, UPCOMING |
| studio | CharField(max_length=100, blank=True) | X | 제작사명 |
| synopsis | TextField(blank=True) | X | 줄거리 |
| rating_avg | DecimalField(max_digits=2, decimal_places=1) | O | 평균 평점 |
| rating_count | PositiveIntegerField(default=0) | O | 평점 수 |
| favorite_count | PositiveIntegerField(default=0) | O | 찜 수 |

### Manga

| 필드 | Django 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | CharField(max_length=255) | O | 제목 |
| original_title | CharField(max_length=255, blank=True) | X | 원제 |
| cover_image_url | URLField(max_length=500, blank=True) | X | 표지 이미지 |
| banner_image_url | URLField(max_length=500, blank=True) | X | 상세 배너 이미지 |
| author | CharField(max_length=100, blank=True) | X | 작가 |
| illustrator | CharField(max_length=100, blank=True) | X | 그림 작가 |
| publisher | CharField(max_length=100, blank=True) | X | 출판사 |
| description | TextField(blank=True) | X | 설명 |
| status | CharField(max_length=30, choices=MangaStatus) | O | ONGOING, COMPLETED |
| rating_avg | DecimalField(max_digits=2, decimal_places=1) | O | 평균 평점 |
| rating_count | PositiveIntegerField(default=0) | O | 평점 수 |
| favorite_count | PositiveIntegerField(default=0) | O | 관심작품 수 |

### MangaEpisode

| 필드 | Django 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| manga | ForeignKey(Manga, related_name="episodes") | O | 만화 |
| volume_number | PositiveIntegerField(null=True, blank=True) | X | 권 번호 |
| chapter_number | PositiveIntegerField(null=True, blank=True) | X | 화 번호 |
| title | CharField(max_length=255, blank=True) | X | 에피소드 제목 |
| published_at | DateField(null=True, blank=True) | X | 발행일 |
| rating_avg | DecimalField(max_digits=2, decimal_places=1) | O | 평균 평점 |

정렬 기준:

```python
ordering = ["volume_number", "chapter_number", "id"]
```

### AnimeMangaMapping

| 필드 | Django 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| anime | ForeignKey(Anime, related_name="manga_mappings") | O | 애니 |
| manga | ForeignKey(Manga, related_name="anime_mappings") | O | 만화 |
| anime_season_label | CharField(max_length=50, blank=True) | X | Season 1, Part 2 등 |
| anime_episode_from | PositiveIntegerField(null=True, blank=True) | X | 애니 시작 회차 |
| anime_episode_to | PositiveIntegerField(null=True, blank=True) | X | 애니 종료 회차 |
| manga_volume_from | PositiveIntegerField(null=True, blank=True) | X | 만화 시작 권 |
| manga_volume_to | PositiveIntegerField(null=True, blank=True) | X | 만화 종료 권 |
| manga_chapter_from | PositiveIntegerField(null=True, blank=True) | X | 만화 시작 화 |
| manga_chapter_to | PositiveIntegerField(null=True, blank=True) | X | 만화 종료 화 |
| continue_volume | PositiveIntegerField(null=True, blank=True) | X | 이어볼 권 |
| continue_chapter | PositiveIntegerField(null=True, blank=True) | X | 이어볼 화 |
| mapping_text | CharField(max_length=500) | O | 화면 표시용 문구 |
| description | TextField(blank=True) | X | 상세 설명 |
| source_note | CharField(max_length=500, blank=True) | X | 출처/검수 메모 |

정렬 기준:

```python
ordering = ["anime_id", "anime_episode_from", "id"]
```

### MetadataTag

| 필드 | Django 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| name | CharField(max_length=50, unique=True) | O | 태그명 |
| type | CharField(max_length=20, choices=TagType) | O | GENRE, TAG, STUDIO |

연결:

- Anime.tags = ManyToManyField(MetadataTag, through="AnimeTag")
- Manga.tags = ManyToManyField(MetadataTag, through="MangaTag")

## 2.4 users 앱 모델

2차 MVP에서 구현합니다.

### User

Django 기본 `AbstractUser`를 확장하는 방식을 권장합니다.

| 필드 | 설명 |
| --- | --- |
| nickname | 닉네임 |
| email | 이메일 |
| profile_image_url | 프로필 이미지 |
| role | USER, ADMIN |
| status | ACTIVE, DELETED, BANNED |
| joined_at | 가입일 |
| deleted_at | 탈퇴일 |

### SocialAccount

| 필드 | 설명 |
| --- | --- |
| user | User FK |
| provider | KAKAO, NAVER, GOOGLE |
| provider_user_id | 소셜 플랫폼 사용자 ID |
| email | 소셜 이메일 |

제약:

```python
UniqueConstraint(fields=["provider", "provider_user_id"])
```

## 2.5 interactions 앱 모델

2차 MVP부터 일부 구현합니다.

### Favorite

| 필드 | 설명 |
| --- | --- |
| user | User FK |
| target_type | ANIME, MANGA |
| target_id | 대상 ID |
| status_label | 시청중, 완결, 읽는중 등 |

제약:

```python
UniqueConstraint(fields=["user", "target_type", "target_id"])
```

검증:

- `target_type = ANIME`이면 Anime 존재 여부 확인
- `target_type = MANGA`이면 Manga 존재 여부 확인

---

# 3. API 구현 명세

## 3.1 공통 응답 규칙

성공 응답은 기본적으로 JSON 객체를 반환합니다.

목록 응답:

```json
{
  "count": 20,
  "next": null,
  "previous": null,
  "results": []
}
```

에러 응답:

```json
{
  "detail": "에러 메시지"
}
```

필드 검증 에러:

```json
{
  "field_name": ["에러 메시지"]
}
```

## 3.2 홈 API

### GET /api/v1/home

홈 초기 화면에 필요한 추천 매핑과 인기 작품을 반환합니다.

응답 예시:

```json
{
  "recommended_mappings": [
    {
      "id": 1,
      "mapping_text": "애니 1기 이후 원작 만화 8권 45화부터",
      "anime": {
        "id": 1,
        "title": "주술회전",
        "poster_image_url": "https://example.com/poster.jpg",
        "status": "COMPLETED"
      },
      "manga": {
        "id": 1,
        "title": "주술회전",
        "cover_image_url": "https://example.com/cover.jpg",
        "status": "ONGOING"
      }
    }
  ],
  "popular_animes": [],
  "popular_mangas": []
}
```

구현 기준:

- recommended_mappings는 최신 등록 또는 관리자 추천 기준으로 6개 반환
- 1차 MVP에서는 `favorite_count`, `rating_avg` 기준으로 단순 정렬

## 3.3 통합 검색 API

### GET /api/v1/search?keyword={keyword}

애니, 만화, 매핑 정보를 통합 검색합니다.

응답 예시:

```json
{
  "keyword": "주술",
  "animes": [
    {
      "id": 1,
      "title": "주술회전",
      "poster_image_url": "https://example.com/poster.jpg",
      "release_year": 2020,
      "status": "COMPLETED"
    }
  ],
  "mangas": [
    {
      "id": 1,
      "title": "주술회전",
      "cover_image_url": "https://example.com/cover.jpg",
      "status": "ONGOING"
    }
  ],
  "mappings": [
    {
      "id": 1,
      "mapping_text": "애니 1기 이후 원작 만화 8권 45화부터",
      "anime_title": "주술회전",
      "manga_title": "주술회전"
    }
  ]
}
```

구현 기준:

- keyword가 비어 있으면 400 반환
- 1차 MVP에서는 `icontains` 기반 검색
- 추후 PostgreSQL Full Text Search로 확장 가능

## 3.4 애니 상세 API

### GET /api/v1/animes/{animeId}

애니 상세 정보와 연결된 태그를 반환합니다.

응답 예시:

```json
{
  "id": 1,
  "title": "주술회전",
  "original_title": "呪術廻戦",
  "poster_image_url": "https://example.com/poster.jpg",
  "banner_image_url": "https://example.com/banner.jpg",
  "type": "TVA",
  "release_year": 2020,
  "episode_count": 24,
  "status": "COMPLETED",
  "studio": "MAPPA",
  "synopsis": "작품 줄거리",
  "rating_avg": "4.7",
  "rating_count": 120,
  "favorite_count": 50,
  "tags": [
    {
      "id": 1,
      "name": "액션",
      "type": "GENRE"
    }
  ]
}
```

### GET /api/v1/animes/{animeId}/manga-mappings

애니에서 이어볼 수 있는 원작 만화 매핑을 반환합니다.

응답 예시:

```json
{
  "anime_id": 1,
  "mappings": [
    {
      "id": 1,
      "anime_season_label": "Season 1",
      "anime_episode_from": 1,
      "anime_episode_to": 24,
      "manga_volume_from": 1,
      "manga_volume_to": 8,
      "manga_chapter_from": 1,
      "manga_chapter_to": 63,
      "continue_volume": 8,
      "continue_chapter": 64,
      "mapping_text": "애니 1기 이후 원작 만화 8권 64화부터",
      "description": "애니 1기는 원작 63화까지를 다룹니다.",
      "manga": {
        "id": 1,
        "title": "주술회전",
        "cover_image_url": "https://example.com/cover.jpg"
      }
    }
  ]
}
```

## 3.5 만화 상세 API

### GET /api/v1/mangas/{mangaId}

만화 상세 정보와 연결 태그를 반환합니다.

### GET /api/v1/mangas/{mangaId}/episodes

만화 에피소드 목록을 반환합니다.

쿼리 파라미터:

| 이름 | 설명 |
| --- | --- |
| volume | 특정 권만 조회 |
| page | 페이지 번호 |

응답 예시:

```json
{
  "count": 63,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "volume_number": 1,
      "chapter_number": 1,
      "title": "료멘스쿠나",
      "published_at": "2018-03-05",
      "rating_avg": "4.6"
    }
  ]
}
```

### GET /api/v1/mangas/{mangaId}/anime-mappings

만화와 연결된 애니 매핑 정보를 반환합니다.

## 3.6 추천 매핑 API

### GET /api/v1/mappings/recommendations

홈보다 많은 추천 매핑 목록을 페이지네이션으로 반환합니다.

정렬 기준:

- 기본: 최신 등록순
- 추후: 찜 수, 평점, 조회 수 기반 추천

---

# 4. Serializer 명세

## 4.1 목록용 Serializer

목록에서는 가벼운 필드만 반환합니다.

AnimeListSerializer:

- id
- title
- poster_image_url
- release_year
- status
- rating_avg
- favorite_count

MangaListSerializer:

- id
- title
- cover_image_url
- status
- rating_avg
- favorite_count

MappingCardSerializer:

- id
- mapping_text
- anime summary
- manga summary
- continue_volume
- continue_chapter

## 4.2 상세용 Serializer

상세에서는 태그와 설명 필드를 포함합니다.

AnimeDetailSerializer:

- Anime 기본 필드
- tags

MangaDetailSerializer:

- Manga 기본 필드
- tags

MappingDetailSerializer:

- 매핑 전체 필드
- anime summary
- manga summary

---

# 5. 프론트엔드 구현 명세

## 5.1 권장 폴더 구조

```text
frontend/
  src/
    api/
      client.js
      works.js
      auth.js
      interactions.js
      chat.js
    components/
      common/
      works/
      layout/
    pages/
      HomePage.vue
      SearchPage.vue
      AnimeDetailPage.vue
      MangaDetailPage.vue
      MyPage.vue
    router/
      index.js
    stores/
      auth.js
      chat.js
    styles/
      base.css
      tokens.css
```

## 5.2 라우팅

| 경로 | 화면 | MVP |
| --- | --- | --- |
| / | 홈 | 1차 |
| /search?keyword= | 검색 결과 | 1차 |
| /animes/:id | 애니 상세 | 1차 |
| /mangas/:id | 만화 상세 | 1차 |
| /login | 로그인 | 2차 |
| /mypage | 마이페이지 | 2차 |

## 5.3 주요 컴포넌트

### 공통

| 컴포넌트 | 역할 |
| --- | --- |
| AppHeader | 로고, 검색창, 로그인/마이페이지 진입 |
| AppFooter | 서비스 정보 |
| SearchBar | 통합 검색 입력 |
| TagBadge | 장르/태그/제작사 표시 |
| StatusBadge | 연재중/완결/방영예정 표시 |
| LoadingState | 로딩 표시 |
| EmptyState | 결과 없음 표시 |

### 작품 관련

| 컴포넌트 | 역할 |
| --- | --- |
| MappingCard | 추천 매핑 카드 |
| AnimeCard | 애니 목록 카드 |
| MangaCard | 만화 목록 카드 |
| MappingIndicator | 애니-만화 매핑 브릿지 UI |
| EpisodeList | 만화 에피소드 목록 |
| DetailHero | 상세 상단 대표 영역 |

## 5.4 화면별 UI 요구사항

### HomePage

필수 요소:

- 상단 검색창
- 추천 매핑 카드 목록
- 인기 애니 섹션
- 인기 만화 섹션

동작:

- 검색어 입력 후 Enter 또는 검색 버튼 클릭 시 `/search?keyword=검색어` 이동
- 매핑 카드 클릭 시 애니 상세 또는 매핑 상세 영역으로 이동

### SearchPage

필수 요소:

- 검색어 표시
- 애니 결과 탭/섹션
- 만화 결과 탭/섹션
- 매핑 결과 섹션
- 결과 없음 상태

### AnimeDetailPage

필수 요소:

- 애니 대표 이미지, 제목, 원제, 상태, 제작사, 줄거리
- 태그 목록
- 매핑 인디케이터
- `만화 정보 보기` 버튼

동작:

- `만화 정보 보기` 클릭 시 연결된 `/mangas/:id`로 이동
- 매핑이 여러 개인 경우 매핑 리스트로 제공

### MangaDetailPage

필수 요소:

- 만화 표지, 제목, 원제, 작가, 출판사, 설명
- 태그 목록
- 연결 애니 매핑 인디케이터
- 에피소드 목록
- `애니 정보 보기` 버튼

동작:

- `애니 정보 보기` 클릭 시 연결된 `/animes/:id`로 이동
- 에피소드 목록은 페이지네이션 또는 권별 필터 제공

---

# 6. 상태 관리 명세

## 6.1 1차 MVP

1차 MVP에서는 전역 상태를 최소화합니다.

전역 상태 후보:

- 검색어
- 최근 검색어

대부분의 데이터는 페이지 진입 시 API로 조회하고 페이지 컴포넌트 로컬 상태에서 관리합니다.

## 6.2 2차 이후

Pinia store 권장:

| Store | 역할 |
| --- | --- |
| authStore | 로그인 사용자, 토큰, 로그아웃 |
| favoriteStore | 찜 상태 변경 |
| chatStore | 챗봇 열림 상태, 대화 목록 |

---

# 7. 관리자 페이지 명세

1차 MVP에서는 Django Admin을 적극 활용합니다.

## 7.1 등록 가능 데이터

- Anime
- Manga
- MangaEpisode
- AnimeMangaMapping
- MetadataTag

## 7.2 Admin 편의 기능

Anime admin:

- title 검색
- status 필터
- studio 필터
- release_year 필터

Manga admin:

- title 검색
- status 필터
- publisher 필터

AnimeMangaMapping admin:

- anime 검색
- manga 검색
- anime_season_label 필터
- continue_volume, continue_chapter 표시

---

# 8. Seed 데이터 명세

1차 MVP 시연을 위해 최소 5개 작품 세트를 등록합니다.

작품 세트 예시:

| 애니 | 만화 | 매핑 예시 |
| --- | --- | --- |
| 주술회전 | 주술회전 | 애니 1기 이후 원작 만화 8권 64화부터 |
| 귀멸의 칼날 | 귀멸의 칼날 | 무한열차편 이후 원작 만화 8권 67화부터 |
| 진격의 거인 | 진격의 거인 | Final Season Part 2 이후 원작 만화 32권부터 |
| 체인소 맨 | 체인소 맨 | 애니 1기 이후 원작 만화 5권 39화부터 |
| 스파이 패밀리 | 스파이 패밀리 | 애니 1기 이후 원작 만화 7권부터 |

주의:

- 실제 매핑 데이터는 등록 전 검수합니다.
- 불확실한 매핑은 `source_note`에 확인 필요 표시를 남깁니다.

---

# 9. 테스트 명세

## 9.1 백엔드 테스트

1차 MVP 필수 테스트:

- Anime 목록/상세 조회
- Manga 목록/상세 조회
- MangaEpisode 목록 조회
- Anime -> Manga 매핑 조회
- Manga -> Anime 매핑 조회
- 통합 검색 keyword 필수 검증
- 통합 검색 결과 반환

## 9.2 프론트엔드 테스트

1차 MVP 확인 항목:

- 홈 화면 렌더링
- 검색어 입력 후 검색 결과 페이지 이동
- 애니 상세에서 만화 상세 이동
- 만화 상세에서 애니 상세 이동
- 매핑 정보가 없는 경우 빈 상태 표시
- API 실패 시 에러 상태 표시

---

# 10. 개발 순서

## 10.1 백엔드 1차 구현 순서

1. Django 프로젝트 생성
2. `works` 앱 생성
3. 공통 TimeStampedModel 작성
4. Anime, Manga 모델 작성
5. MangaEpisode 모델 작성
6. MetadataTag, AnimeTag, MangaTag 모델 작성
7. AnimeMangaMapping 모델 작성
8. Admin 등록
9. Serializer 작성
10. API View/ViewSet 작성
11. URL 연결
12. Seed 데이터 작성
13. 백엔드 테스트 작성

## 10.2 프론트엔드 1차 구현 순서

1. Vue 프로젝트 생성
2. Router 설정
3. API client 설정
4. 공통 레이아웃 구현
5. 홈 화면 구현
6. 검색 결과 화면 구현
7. 애니 상세 화면 구현
8. 만화 상세 화면 구현
9. 매핑 인디케이터 컴포넌트 구현
10. 로딩/빈 상태/에러 상태 처리

---

# 11. 환경 변수

## 11.1 Backend

```text
DJANGO_SECRET_KEY=
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
CORS_ALLOWED_ORIGINS=http://localhost:5173
OPENAI_API_KEY=
```

1차 MVP에서는 `OPENAI_API_KEY`를 사용하지 않습니다.

## 11.2 Frontend

```text
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

# 12. 배포 전 체크리스트

- DEBUG=false 적용
- ALLOWED_HOSTS 설정
- CORS 허용 도메인 제한
- PostgreSQL 연결 확인
- 정적 파일 collectstatic 확인
- 관리자 계정 생성
- Seed 데이터 검수
- API 에러 응답 형식 확인
- 모바일 화면 확인

---

# 13. 완료 기준

1차 MVP 완료 기준:

- 홈에서 추천 매핑 카드가 보인다.
- 검색으로 애니/만화/매핑 결과를 확인할 수 있다.
- 애니 상세에서 원작 만화 이어보기 정보를 확인할 수 있다.
- 만화 상세에서 연결 애니 정보를 확인할 수 있다.
- 애니 상세과 만화 상세 간 이동이 가능하다.
- 관리자 페이지에서 작품과 매핑 데이터를 등록/수정할 수 있다.
- 최소 5개 작품 세트의 seed 데이터가 등록되어 있다.
