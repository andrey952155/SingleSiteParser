import json
import os

from transliterate import translit
import urllib.request
from bs4 import BeautifulSoup as bs

from auth import request, URL
from models import Lesson, Course, Content, session
from const import Cfg


class ContentParser(Content):

    def __init__(self, title, path, filename, url):
        self.title: str = title
        self.content_path: str = path
        self.filename: str = filename
        self.url: str = url
        self.download_file()
        session.add(self)
        session.commit()

    def download_file(self):
        urllib.request.urlretrieve(self.url, f'{self.content_path}/{self.filename}')
        print(f'Загрузка завершена - {self.filename}')


class LessonParser(Lesson):

    def __init__(self, course_id, lesson_id_gb, course_path, prefix):
        self.course = course_id
        self.url = f'{prefix}/{lesson_id_gb}'
        r = request(self.url)
        soup = bs(r, "html.parser")
        self.title = soup.find(class_='title').text
        self.create_lesson_folder(course_path)
        self.content_links: list[dict] = []
        self.add_document_link(soup)
        self.add_video_link(prefix, lesson_id_gb)
        session.add(self)
        session.commit()

        self.content_objects: list[ContentParser] = []
        self.create_content_object()

    def create_lesson_folder(self, course_path):
        dir_name = CourseParser.path_name_edit(self.title)
        print(f'{course_path}{dir_name}')
        CourseParser.create_folder(course_path, dir_name)
        self.lesson_path = f'{course_path}{dir_name}'

    def add_document_link(self, soup):
        data = set(soup.find_all(class_='lesson-contents__download-row'))
        for i in data:
            if '.mp4' not in i.get('href'):
                self.content_links.append({'title': i.text, 'link': i.get('href')})

    def add_video_link(self, prefix, lesson_id_gb):
        data = request(f'api/v2/{prefix}/{lesson_id_gb}/playlist')
        data = json.loads(data)
        data = data['playlist']
        links = [i['src'] for el in data for i in el['sources']]
        self.content_links = self.content_links + [{'title': 'Видео', 'link': i} for i in links]

    def create_content_object(self):
        for i in self.content_links:
            filename = f'{CourseParser.path_name_edit(i["title"])}.{i["link"].split(".")[-1]}'
            self.content_objects.append(ContentParser(i['title'], self.lesson_path, filename, i["link"]))


class CourseParser(Course):

    def __init__(self, course_id):
        self.course_id_gb = course_id
        course = json.loads(request('api/v2/education/student'))['attendees'][course_id]
        self.title = course['title']
        CourseParser.create_folder(Cfg.root_path, CourseParser.path_name_edit(self.title))
        self.course_path = f'{Cfg.root_path}/{CourseParser.path_name_edit(self.title)}/'
        self.url = course['courseUrl']
        self.lesson_prefix = list(course['progressItems'])[0]
        self.lesson_list = course['progressItems'][self.lesson_prefix]
        self.lesson_object: list[LessonParser] = []
        session.add(self)
        session.commit()
        self.parse_course()

    def parse_course(self):
        for lesson_id_gb in self.lesson_list:
            self.lesson_object.append(LessonParser(self.id, lesson_id_gb, self.course_path, self.lesson_prefix))

    @staticmethod
    def path_name_edit(name: str) -> str:
        return translit(name, language_code='ru', reversed=True).\
            translate({ord(','): None, ord(':'): None, ord('.'): None, ord("'"): None, ord(' '): '_', ord('/'): '_'})

    @staticmethod
    def create_folder(path, dir_name):
        if dir_name not in os.listdir(path):
            os.mkdir(path + '/' + dir_name)

    @staticmethod
    def show_all_courses():
        r = request('api/v2/education/student')
        r = json.loads(r)
        for i in r['attendees'].values():
            print(i['title'], i.get('progressItems'))

    @staticmethod
    def show_download_courses():
        r = session.query(Course).all()
        for i in r:
            print(f'{i.id} - {i.title} - {i.course_id_gb} - {i.course_path}')

    @staticmethod
    def delete_course(course_id):
        session.query(Course).filter(Course.id == course_id).delete()
        session.commit()

# Список всех доступных курсов
# CourseParser.show_all_courses()

# Список скаченных курсов
# CourseParser.show_download_courses()

# Удалить курс из базы
# CourseParser.delete_course(course_id)

# Скачать курс
# CourseParser('8625428')


print(f'Список всех доступных курсов - all \n'
      f'Список уже скаченных курсов - download \n'
      f'Скачать курс - id \n'
      f'Удалить курс из базы - delete-id')


letter = input('Введите: ')
if letter.isdigit():
    CourseParser(letter)
elif 'delete-' in letter:
    CourseParser.delete_course(letter.replace('delete-', ''))
elif letter == 'all':
    CourseParser.show_all_courses()
elif letter == 'download':
    CourseParser.show_download_courses()







