<img width="700" alt="image" src="https://github.com/Django-Wanted-Internship-3-Team/repo2_restaurant_recommend/assets/104830931/9b0e98e9-d711-4a3f-a2f7-86855b4e899d">


## 개요

---

- 본 서비스는 위치를 기반으로 하여 맛집을 추천해주는 웹 서비스입니다.
- 본 서비스의 사용자는 맛집 추천 목록을 `거리순` 또는 `평점순`으로 조회가 가능합니다.
- 본 서비스는 공공 데이터를 활용하여, 지역 음식점 목록을 자동으로 업데이트 하고 이를 활용하여 사용자 위치를 기반으로, `도보`기준 `1km`이내 또는 `교통수단` 기준 `5km`이내의 맛집 및 메뉴를 추천합니다. 또한 사용자는 `시도`, `시군구` 단위로 최신 업데이트한 지역별 맛집 목록을 조회할 수 있습니다.
- 본 서비스의 사용자는 맛집을 이용해 본 경험을 `0 ~ 5 사이의 점수`로 평가할 수 있고, 평가된 모든 점수는 평균 계산되어 본 서비스의 다른 사용자들이 맛집에 대한 정보를 미리 알 수 있습니다.
- 본 서비스의 사용자 중 `점심 추천 서비스` 사용에 동의한 사용자에 한해 점심시간 30분 전, 주변 맛집 목록을 제공합니다.
- 더 나아가 본 서비스는 사용자들에게 다양한 음식 경험을 제공하고, 음식을 좋아하는 사람들 간에 자유로운 소통과 다양한 맛집 탐방 경험 공유를 촉진하고자 합니다.

## 버전

---

### Backend

---

<div align="center">
  <img src="https://img.shields.io/badge/python 3.11.5-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/django 4.2.5-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/django rest framework 3.14.0-092E20?style=for-the-badge&logo=django&logoColor=white">
	<img src="[https://img.shields.io/badge/celery 5.3.4-00FF00?style=for-the-badge&logo=celery&logoColor=white](https://img.shields.io/badge/celery%205.3.4-00FF00?style=for-the-badge&logo=celery&logoColor=white)">
	<img src="https://img.shields.io/badge/DOCKER 20.10.12-3D97FF?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/DOCKER COMPOSE 2.11.2-3D97FF?style=for-the-badge&logo=docker&logoColor=white">
</div>

### Database

---

<div align="center">
	<img src="https://img.shields.io/badge/postgresql 16.0-0000FF?style=for-the-badge&logo=postgresql&logoColor=white">
</div>

### Management

---

<div align="center">
	<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> 
	<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> 
	<img src="https://img.shields.io/badge/github action-3399FF?style=for-the-badge&logo=github&logoColor=white">
</div>


## 설치 및 테스트

---

### 설치

```bash
docker compose up #localhost:8000
```

### 테스트

```bash
docker compose run django poetry run python3 manage.py test restaurants_recommendation
```

<img width="1363" alt="스크린샷 2023-11-19 오후 5 54 21" src="https://github.com/Django-Wanted-Internship-3-Team/repo2_restaurant_recommend/assets/104830931/5ef7b508-561d-4f39-9f9b-271e5530ffcb">

![image](https://github.com/Django-Wanted-Internship-3-Team/repo2_restaurant_recommend/assets/104830931/dedea276-de87-44af-bc29-4256cf07af4a)


## API 명세

---

<img width="725" alt="스크린샷 2023-11-19 오후 5 52 16" src="https://github.com/Django-Wanted-Internship-3-Team/repo2_restaurant_recommend/assets/104830931/f578e844-831e-4cc8-aaec-fbf24abd9ca2">
<img width="728" alt="스크린샷 2023-11-19 오후 5 52 45" src="https://github.com/Django-Wanted-Internship-3-Team/repo2_restaurant_recommend/assets/104830931/f871f0d1-05f5-47b6-82be-9a7589b1805a">


## ERD

---

[restraunt_recommendation](https://www.erdcloud.com/d/k4hLqewZtByfS74Mt)

<img width="699" alt="image" src="https://github.com/Django-Wanted-Internship-3-Team/repo2_restaurant_recommend/assets/104830931/3e7a8330-ceea-4ac2-8e4a-d490f9e75ab9">

## 데이터

```jsx
#data_pipeline
fetch_restaurant_count -> 각 URL의 총 데이터 개수 요청
fetch_restaurant_data -> 총 개수를 바탕으로 page 할당 후 데이터 요청
map_api_data_to_model -> 모델에 맞게 data mapping
save_data_to_db -> mapping된 데이터 db에 저장

apscheduler 이용하여 서버 작동 시매일 오전 2시 30분에 데이터 요청하도록 구현.
```

## 팀 소개 및 회고

---

[박대준](https://determined-chamomile-42b.notion.site/fd81b84f2a7342a4afcfc97823af7df6?pvs=4)

[윤성원](https://determined-chamomile-42b.notion.site/8f971b8f12f848129614fe132078cb94?pvs=4)

[사재혁](https://determined-chamomile-42b.notion.site/0b14b2da4f944bc8976480df4a3f52ec?pvs=4)

[이슬기](https://determined-chamomile-42b.notion.site/d497b80d64fa4606b1056256b5a3af77?pvs=4)

