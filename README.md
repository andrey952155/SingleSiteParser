# SingleSiteParser
Парсер одного сайта

Установить зависимости - pip install -r requirements.txt
Добавить в переменные окружения или файл const.py логин, пароль, адрес сайта
и каталог куда будем сохранять. 

Base.metadata.create_all(engine)    Создать базу и таблицы в файле models.py
Base.metadata.drop_all(engine)      Удалить базу

При первом запросе в папку проекта добавится файл с куками.
Если нужно перелогинится, или пропала авторизация, файл удалить

Справка по коммандам находится в файле parser.py

буткем продакт манагер с ошибкой!!!!-------------