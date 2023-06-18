<a name="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][forks-shield]][forks-url]
[![stars][stars-shield]][stars-url]
[![forks][license-shield]][license-url]

<br />
<div align="center">
  <a href="https://github.com/kit-teamcook-2023">
    <img src="https://github.com/kit-teamcook-2023/teamcook-front/assets/63646062/0aceb80e-5cfb-4ed2-bd77-053c2798aa06" alt="Logo" width="500" height="100">
  </a>

<h3 align="center">Gpple 가스비 측정 & 커뮤니티 앱 백엔드</h3>

  <p align="center">
    Gpple 프론트엔드 코드 보러가기
    <br />
    <a href="https://github.com/kit-teamcook-2023/teamcook-backend"><strong>Explore the frontend »</strong></a>
    <br />
    <br />
    Gpple 디바이스 코드 보러가기
    <br />
    <a href="https://github.com/kit-teamcook-2023/teamcook-raspberry"><strong>Explore the device »</strong></a>
    <br />
    <br />
    <a href="http://34.215.66.235:8000/docs">Request Docs</a>
    ·
    <a href="https://github.com/kit-teamcook-2023/teamcook-backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/kit-teamcook-2023/teamcook-backend/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#프로젝트-소개">프로젝트 소개</a>
      <ul>
        <li><a href="#기술-스택">기술 스택</a></li>
      </ul>
    </li>
    <li>
      <a href="#시작하기">시작하기</a>
      <ul>
        <li><a href="#시스템-요구사항">시스템 요구사항</a></li>
        <li><a href="#설치">설치</a></li>
      </ul>
    </li>
  </ol>
</details>

## 프로젝트 소개

### 기술 스택

[![Python][Python_b]][Python-url]
[![FastAPI][FastAPI_b]][FastAPI-url]
[![MySQL][MySQL_b]][MySQL-url]
[![Firebase][Firebase_b]][Firebase-url]
[![EC2][EC2_b]][EC2-url]
[![Ubuntu][Ubuntu_b]][Ubuntu-url]

## 시작하기

### 시스템 요구사항
* Python 3.10.6
* Ubuntu 22.04.2 LTS
<br>

### 설치

1. Clone repository

```
git clone https://github.com/kit-teamcook-2023/teamcook-backend.git
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Write your API in `.env`

    - path /

    ```
    ELEC_RATE_PAGE="elec-base-url"

    GAS_RATE_PAGE="gas-base-url"

    CLIENT_ID="your-kakao-login-api"
    CLIENT_SECRET="your-kakao-login-secret"
    ```

    - path /test

    ```
    MYSQL_ID="your-database-id"
    MYSQL_PW="yout-database-password"
    MYSQL_DB_USER="writing_table"
    MYSQL_DB_CHAT="chatting"

    FIREBASE_SDK="yout-firebase-key"
    DB_URL="yout-firebase-realtime_database-url"
    ```

    - path /auth
    ```
    secret="your-jwt-secert"
    algorithm="jwt-algorithm"
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/kit-teamcook-2023/teamcook-backend.svg?style=for-the-badge
[contributors-url]: https://github.com/kit-teamcook-2023/teamcook-backend/graphs/contributors

[issues-shield]: https://img.shields.io/github/issues/kit-teamcook-2023/teamcook-backend.svg?style=for-the-badge
[issues-url]: https://github.com/kit-teamcook-2023/teamcook-backend/issues

[forks-shield]: https://img.shields.io/github/forks/kit-teamcook-2023/teamcook-backend.svg?style=for-the-badge
[forks-url]: https://github.com/kit-teamcook-2023/teamcook-backend/issues

[stars-shield]: https://img.shields.io/github/stars/kit-teamcook-2023/teamcook-backend.svg?style=for-the-badge
[stars-url]: https://github.com/kit-teamcook-2023/teamcook-backend/issues

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt


[Python_b]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[FastAPI_b]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/

[MySQL_b]: https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white
[MySQL-url]: https://www.mysql.com/

[Firebase_b]: https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black
[Firebase-url]: https://firebase.google.com/

[EC2_b]: https://img.shields.io/badge/Amazon%20EC2-232F3E?style=for-the-badge&logo=AmazonEC2
[EC2-url]: https://aws.amazon.com/ec2/

[Ubuntu_b]: https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white
[Ubuntu-url]: https://ubuntu.com/download/desktop