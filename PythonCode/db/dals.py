import pathlib
import sys
from typing import Union, Coroutine, Any
import io

import psycopg2
from fastapi import HTTPException
from pydantic import EmailStr
from pylatex import Document, Section, Subsection, Math, Tabular, Center, Package, Command, NewLine, Subsubsection
from pylatex.utils import italic, NoEscape
from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from db.models import User, PortalRole, Event, Application, Comments, Notifications, Article


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, name: str, surname: str, email: str, age: int, hashed_password: str, roles: str,
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            age=age,
            email=email,
            hashed_password=hashed_password,
            roles=roles,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def create_article(
            self, user_id: str, article_name: str, engl_article_name: str, authors: str, engl_authors: str,
            author_city_first: str, author_city_second: str, engl_author_city_first: str, engl_author_city_second: str,
            annotation: str, keywords: str, engl_annotation: str, engl_keywords: str, introduction: str, theory: str,
            results: str, conclusion: str, thanks: str, list_of_sources: str
    ) -> Article:
        annotation1 = 'Аннотация. ' + annotation
        keywords1 = 'Ключевые слова: ' + keywords
        engl_annotation1 = 'Abstract. ' + engl_annotation
        engl_keywords1 = 'Keywords: ' + engl_keywords
        margins = {'tmargin': '20mm', 'lmargin': '25mm', 'rmargin': '25mm', 'bmargin': '20mm'}
        doc = Document(documentclass='article', document_options=None, fontenc=['T2A', 'T1'], lmodern=None,
                       textcomp=None, page_numbers=None, indent=True, font_size='normalsize', data=None,
                       geometry_options=margins)
        doc.packages.add(Package('babel', options=['english', 'russian']))
        doc.packages.add(Package('newtxtext, newtxmath'))
        doc.packages.add(Package('substitutefont'))
        doc.preamble.append(NoEscape(r'\substitutefont{T2A}{/familydefault}{Tempora-TLF}'))
        doc.packages.add(Package('lastpage'))
        doc.packages.add(Package('indentfirst'))
        doc.preamble.append(Command(r'linespread', arguments='1.5'))
        doc.preamble.append(NoEscape(r'\setlength{\parindent}{5ex}'))
        doc.preamble.append(NoEscape(r'\setlength{\parskip}{1ex}'))
        doc.append(NoEscape(r'\pretolerance=10000'))
        doc.append(NoEscape(r'\fontsize{12}{12pt}\selectfont'))

        with doc.create(Center()) as center:
            with center.create(Section(article_name, numbering=False)):
                pass
            with center.create(Section(engl_article_name, numbering=False)):
                pass
            with center.create(Subsection(authors, numbering=False)):
                pass
            with center.create(Subsection(author_city_first, numbering=False)):
                pass
            with center.create(Subsection(author_city_second, numbering=False)):
                pass
            with center.create(Subsection(engl_authors, numbering=False)):
                pass
            with center.create(Subsection(engl_author_city_first, numbering=False)):
                pass
            with center.create(Subsection(engl_author_city_second, numbering=False)):
                pass

        doc.append(NoEscape(r'\par'))
        doc.append(annotation1)
        doc.append(NewLine())
        doc.append(NoEscape(r'\par'))
        doc.append(keywords1)
        doc.append(NewLine())
        doc.append(NoEscape(r'\par'))
        doc.append(engl_annotation1)
        doc.append(NewLine())
        doc.append(NoEscape(r'\par'))
        doc.append(engl_keywords1)
        doc.append(NewLine())

        with doc.create(Subsection('Введение', numbering=False)):
            # doc.append(Command('centering'))
            doc.append(introduction)

        with doc.create(Subsection('Теория', numbering=False)):
            pass
        doc.append(theory)
        with doc.create(Subsection('Результаты', numbering=False)):
            pass
        doc.append(results)
        with doc.create(Subsection('Выводы и заключение', numbering=False)):
            pass
        doc.append(conclusion)
        with doc.create(Subsection('Источник финансирования. Благодарности', numbering=False)):
            pass
        doc.append(thanks)
        with doc.create(Subsection('Список источников', numbering=False)):
            pass
        doc.append(list_of_sources)
        doc.generate_pdf('images_article/image', clean_tex=False, compiler='pdflatex')
        pdf_path = pathlib.Path("images_article/image.pdf")

        doc_article = pdf_path.read_bytes()

        # f = open("images_article/image.pdf", 'rb')
        # dat = f.read()
        # binary = psycopg2.Binary(dat)

        new_article = Article(
            user_id=user_id,
            article_name=article_name,
            engl_article_name=engl_article_name,
            authors=authors,
            engl_authors=engl_authors,
            author_city_first=author_city_first,
            author_city_second=author_city_second,
            engl_author_city_first=engl_author_city_first,
            engl_author_city_second=engl_author_city_second,
            annotation=annotation,
            keywords=keywords,
            engl_annotation=engl_annotation,
            engl_keywords=engl_keywords,
            introduction=introduction,
            theory=theory,
            results=results,
            conclusion=conclusion,
            thanks=thanks,
            list_of_sources=list_of_sources,
            doc_article=doc_article
        )
        self.db_session.add(new_article)
        await self.db_session.flush()
        return new_article

    async def create_manager(
            self, name: str, surname: str, email: str, hashed_password: str, roles: str
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
            roles=roles,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def create_application(
            self, event_id: str, user_id: str, content: str, event_name: str, application_name: str
    ) -> Application:
        new_application = Application(
            event_id=event_id,
            user_id=user_id,
            event_name=event_name,
            content=content,
            application_name=application_name
        )
        self.db_session.add(new_application)
        await self.db_session.flush()
        return new_application

    async def create_comment(
            self, application_id: str, manager_id: str, manager_name: str, manager_surname: str, content: str
    ) -> Comments:
        new_comment = Comments(
            application_id=application_id,
            manager_id=manager_id,
            manager_name=manager_name,
            manager_surname=manager_surname,
            content=content
        )
        self.db_session.add(new_comment)
        await self.db_session.flush()
        return new_comment

    async def create_notification(
            self, user_id: str, application_name: str, application_id: str
    ) -> Notifications:
        new_notification = Notifications(
            application_id=application_id,
            application_name=application_name,
            user_id=user_id,
        )
        self.db_session.add(new_notification)
        await self.db_session.flush()
        return new_notification

    async def create_event(
            self, name: str, content: str, date: str
    ) -> Event:
        new_event = Event(
            name=name,
            content=content,
            date=date
        )
        self.db_session.add(new_event)
        await self.db_session.flush()
        return new_event

    async def delete_user(self, user_id: UUID) -> Union[User, None]:
        query = update(User).where(and_(User.user_id == user_id, User.is_active == True)).values(
            is_active=False).returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def delete_event(self, event_id: UUID) -> Union[Event, None]:
        query = update(Event).where(and_(Event.event_id == event_id, Event.is_active == True)).values(
            is_active=False).returning(Event.event_id)
        res = await self.db_session.execute(query)
        deleted_event_id_row = res.fetchone()
        if deleted_event_id_row is not None:
            return deleted_event_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(and_(User.user_id == user_id))
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_event_by_id(self, event_id: UUID) -> Union[Event, None]:
        query = select(Event).where(and_(Event.event_id == event_id))
        res = await self.db_session.execute(query)
        event_row = res.fetchone()
        if event_row is not None:
            return event_row[0]

    async def get_comment_by_application_id(self, application_id: UUID) -> list[Comments]:
        query = f"""SELECT * FROM comments where application_id::text = '{application_id}'"""
        res = await self.db_session.execute(query)
        comment_row = list(res.fetchall())
        if comment_row is not None:
            return comment_row

    async def get_application_by_user_id(self, user_id: UUID) -> list[Application]:
        query = f"""SELECT * FROM applications where user_id::text = '{user_id}'"""
        res = await self.db_session.execute(query)
        application_row = list(res.fetchall())
        if application_row is not None:
            return application_row

    async def get_application_by_application_id(self, application_id: UUID) -> list[Application]:
        query = f"""SELECT * FROM applications where id::text = '{application_id}'"""
        res = await self.db_session.execute(query)
        application_row = list(res.fetchall())
        if application_row is not None:
            return application_row

    async def get_article_by_user_id(self, user_id: UUID) -> list[Article]:
        query = f"""SELECT article_id, user_id,article_name,engl_article_name,authors,engl_authors,author_city_first,author_city_second,engl_author_city_first,engl_author_city_second,annotation,keywords,engl_annotation,engl_keywords,introduction,theory,results,conclusion,thanks,list_of_sources FROM article where user_id::text = '{user_id}'"""
        res = await self.db_session.execute(query)
        article_row = list(res.fetchall())
        if article_row is not None:
            return article_row

    async def get_article_by_article_id(self, article_id: UUID) -> list[Article]:
        query = f"""SELECT article_id, user_id,article_name,engl_article_name,authors,engl_authors,author_city_first,author_city_second,engl_author_city_first,engl_author_city_second,annotation,keywords,engl_annotation,engl_keywords,introduction,theory,results,conclusion,thanks,list_of_sources FROM article where article_id::text = '{article_id}'"""
        res = await self.db_session.execute(query)
        article_row = list(res.fetchall())
        if article_row is not None:
            return article_row

    async def get_old_applications(self) -> list[Application]:
        query = f"""SELECT * FROM applications where status != 'Заявка не осмотрена'"""
        res = await self.db_session.execute(query)
        application_row = list(res.fetchall())
        if application_row is not None:
            return application_row

    async def get_articles(self) -> list[Article]:
        query = f"""SELECT article_id, user_id,article_name,engl_article_name,authors,engl_authors,author_city_first,author_city_second,engl_author_city_first,engl_author_city_second,annotation,keywords,engl_annotation,engl_keywords,introduction,theory,results,conclusion,thanks,list_of_sources FROM article"""
        res = await self.db_session.execute(query)
        article_row = list(res.fetchall())
        if article_row is not None:
            return article_row

    async def get_doc_articles(self, article_id) -> bytes:
        query = f"""SELECT doc_article FROM article WHERE article_id::text = '{article_id}'"""
        res = await self.db_session.execute(query)
        article_row = res.fetchone()
        if article_row is not None:
            return article_row[0]

    async def get_new_applications(self) -> list[Application]:
        query = f"""SELECT * FROM applications where status = 'Заявка не осмотрена'"""
        res = await self.db_session.execute(query)
        application_row = list(res.fetchall())
        if application_row is not None:
            return application_row

    async def get_notification_by_user_id(self, user_id: UUID) -> list[Notifications]:
        query = f"""SELECT * FROM notifications where user_id::text = '{user_id}' and status='true'"""
        res = await self.db_session.execute(query)
        notification_row = list(res.fetchall())
        if notification_row is not None:
            return notification_row

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(and_(User.email == email))
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, name: str, surname: str, email: EmailStr, user_id: UUID):
        if surname is None or name is None or email is None:
            raise HTTPException(
                status_code=418,
                detail="I'm a teapot",
            )
        sql_update_query = f"""Update users set name = '{name}', surname = '{surname}', email = '{email}' where user_id::text = '{user_id}'"""
        await self.db_session.execute(sql_update_query, (name, surname, email, str(user_id)))

    async def update_event(self, name: str, content: str, event_id: UUID):
        if content is None or name is None:
            raise HTTPException(
                status_code=418,
                detail="I'm a teapot",
            )
        sql_update_query = f"""Update events set name = '{name}', content = '{content}' where event_id::text = '{event_id}'"""
        await self.db_session.execute(sql_update_query, (name, content, str(event_id)))

    async def update_notifications(self, user_id: UUID):
        a = 'aaa'
        sql_update_query = f"""Update notifications set status = 'false' where id::text = '{user_id}'"""
        await self.db_session.execute(sql_update_query, (a, str(user_id)))

    async def delete_notifications(self, user_id: UUID):
        a = 'aaa'
        sql_update_query = f"""Delete from notifications where user_id::text = '{user_id}'"""
        await self.db_session.execute(sql_update_query, (a, str(user_id)))

    async def update_appplication(self, id: UUID, status: str):
        if status is None:
            raise HTTPException(
                status_code=418,
                detail="I'm a teapot",
            )
        sql_update_query = f"""Update applications set status = '{status}' where id::text = '{id}'"""
        await self.db_session.execute(sql_update_query, (status, str(id)))

    async def grant_admin_roles(self, user_id: UUID):
        a = 'aaa'
        sql_update_query = f"""Update users set roles = 'ROLE_PORTAL_ADMIN' where user_id::text = '{user_id}'"""
        await self.db_session.execute(sql_update_query, (str(user_id), a))

    async def revoke_admin_roles(self, user_id: UUID):
        a = 'aaa'
        sql_update_query = f"""Update users set roles = 'ROLE_PORTAL_USER' where user_id::text = '{user_id}'"""
        await self.db_session.execute(sql_update_query, (str(user_id), a))

    async def grant_manager_roles(self, user_id: UUID):
        a = 'aaa'
        sql_update_query = f"""Update users set roles = 'ROLE_PORTAL_MANAGER' where user_id::text = '{user_id}'"""
        await self.db_session.execute(sql_update_query, (str(user_id), a))

    async def get_all_users(self) -> list[User]:
        query = f"""SELECT * FROM users where roles = 'ROLE_PORTAL_MANAGER' AND is_active = true"""
        res = await self.db_session.execute(query)
        user_row = list(res.fetchall())
        if user_row is not None:
            return user_row

    async def get_all_events(self) -> list[Event]:
        query = f"""SELECT * FROM events where is_active = true"""
        res = await self.db_session.execute(query)
        event_row = list(res.fetchall())
        if event_row is not None:
            return event_row
