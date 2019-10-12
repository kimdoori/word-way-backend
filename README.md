# 글길 백엔드

개요
---

글길 백엔드 저장소입니다.


요구사항
-----

- [Python](https://www.python.org/) 3.7+


설치하는 법
--------

- virtualenv 세팅
(다른 라이브러리를 사용하셔도 무방합니다)
    ```
    $ mkvirtualenv -a `pwd` -p $(which python) venv
    ```


- dependencies 설치
   ```
   $ ./install.sh
   ```


실행하는 법
--------

웹 서버를 실행합니다.
   ```
   $ ./run.py -d -c dev
   ```

 ### Docker로 실행하기

 1. 이미지를 빌드합니다.

    ```bash
    docker build -t word-way/backend .
    ```

 1. 컨테이너를 실행합니다.

    ```bash
    docker run --rm -d -p <Port Number You Want>:2222 -v $PWD/word_way:/app/word_way word-way/backend:latest
    ```
