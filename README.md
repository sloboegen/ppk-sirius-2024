# rAIgov

Задание для участников ППК по информатике в Сириусе (осень 2024).

В рамках данного задания вам предстоит разработать сервис для определения предметов одежды на фотографии. То есть пользователь будет загружать фотографию, а сервис в ответ выдаст отдельные фотографии предметов одежды, присутствующие на загруженном фото. 


## Описание каталогов

Ниже приведена зона ответственности некоторых каталогов в данном проекте:

- `src` хранит в себе логику приложения. В частности, в `src/domains/find_clothes` должны хранится файлы, которые относятся к функциональности «Найти предметы одежды на фото». Сейчас там только неполное описание API, но в рамках выполнения задания там должна появиться и сама логика поиска одежды на фотографии;
- `static` хранит различные `css`-файлы или картинки (если в них будет необходимость);
- `templates` хранит `jinja`-шаблоны, то есть будущие HTML-страницы нашего приложения.


## Установка зависимостей

1. Для работы с проектом вам потребуется установить `python3.12`:

```bash
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update && sudo apt install -y python3.12
$ sudo apt install -y python3.12-venv
```

2. Далее необходимо создать виртуальное окружение и установить нужные библиотеки:

```bash
$ python3.12 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install -r requirements.txt
```

Вероятно, это займёт продолжительное время (около 15 минут).


3. На данном этапе мы можем локально запустить наш проект командой `(.venv) $ fastapi dev src/app.py`. В браузере по адресу `http://localhost:8000` (либо тот, который задан явно) можно увидеть стартовую страницу приложения.

2. Для того чтобы запускать модели и использовать датасеты с [HuggingFace](https://huggingface.co/) нам потребуется получить Access Token. Например, в [данной инструкции](https://obnimorda.ru/guides/huggingface/gated-models/#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0) описан процесс создания токена. После его создания необходимо добавить запись `HF_TOKEN=<your_token>` в `.env` файл в корне проекта (`.env` файл нужно создать).
