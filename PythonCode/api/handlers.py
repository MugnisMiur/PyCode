import shutil
from logging import getLogger
from typing import Annotated, List, Optional
from uuid import UUID
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import get_current_user_from_token
from api.actions.user import _create_new_user, _delete_user, _get_user_by_id, _update_user, _get_all_users, \
    _create_new_manager, _create_new_event, \
    _get_all_events, _update_event, _get_event_by_id, _delete_event, check_user_event_permissions, \
    _create_new_application, _create_new_comment, _update_application, \
    _create_new_notification, _get_notification_by_user_id, _update_notifications, _get_comment_by_application_id, \
    _get_application_by_user_id, \
    _get_new_applications, _get_old_applications, _delete_notifications, _get_application_by_application_id, \
    _create_new_article, _get_articles, _get_doc_articles, _get_article_by_user_id, _get_article_by_article_id
from api.models import DeleteEventResponse
from api.models import UserCreate, ShowUser, DeleteUserResponse, \
    UpdateUserNameRequest, EventCreate, ShowEvent, UpdateEventRequest, \
    ApplicationCreate, ShowApplication, CommentCreate, ShowComment, UpdateStatusApplication, NotificationCreate, \
    ArticleCreate, ShowArticle
from db.models import User, PortalRole
from db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/create")
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.post("/create_article")
async def create_article(body: ArticleCreate = Form(...), images: UploadFile = File(...),  db: AsyncSession = Depends(get_db)):
    # global image
    # # res = []
    #
    # for image in images:
    #     image.filename = image.filename.lower()
    #
    # path = f"get_media/{image.filename}"
    #
    # with open(path, 'wb+') as buffer:
    #     shutil.copyfileobj(image.file, buffer)

    # res.append(image)
    try:
        return await _create_new_article(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.post("/create_event")
async def create_event(body: EventCreate, db: AsyncSession = Depends(get_db)) -> ShowEvent:
    try:
        return await _create_new_event(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.post("/create_manager")
async def create_manager(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_manager(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.post("/create_application")
async def create_application(body: ApplicationCreate, db: AsyncSession = Depends(get_db)) -> ShowApplication:
    try:
        return await _create_new_application(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.post("/create_comment")
async def create_comment(body: CommentCreate, body1: NotificationCreate,
                         db: AsyncSession = Depends(get_db)) -> ShowComment:
    notification = await _create_new_notification(body1, db)
    try:
        return await _create_new_comment(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.get("/file/download")
async def download_file(article_id: UUID, db: AsyncSession = Depends(get_db)):
    await _get_doc_articles(db, article_id)
    return FileResponse(path='download_images_article/image2.pdf', filename='СТАТЬЯ.pdf', media_type='multipart/form-data')


@user_router.delete("/delete", response_model=DeleteUserResponse)
async def delete_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_event_permissions(
            current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden0.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.delete("/delete_event", response_model=DeleteEventResponse)
async def delete_event(
        event_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> DeleteEventResponse:
    event_for_deletion = await _get_event_by_id(event_id, db)
    if event_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"Event with id {event_id} not found."
        )
    if not check_user_event_permissions(
            current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden0.")
    deleted_event_id = await _delete_event(event_id, db)
    if deleted_event_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {event_id} not found."
        )
    return DeleteEventResponse(deleted_event_id=deleted_event_id)


@user_router.get("/this", response_model=ShowUser)
async def get_user_by_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user


@user_router.get("/this", response_model=ShowUser)
async def get_user_by_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user


@user_router.get("/this_comment", )
async def get_comment_by_application_id(
        application_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    application = await _get_comment_by_application_id(application_id, db)
    if application is None:
        raise HTTPException(status_code=404, detail=f"Comment with application_id {application_id} not found.")
    return application


@user_router.get("/this_application")
async def get_application_by_user_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    application = await _get_application_by_user_id(user_id, db)
    if application is None:
        raise HTTPException(status_code=404, detail=f"Application with user_id {user_id} not found.")
    return application


@user_router.get("/this_application_by_id")
async def get_application_by_application_id(
        application_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    application = await _get_application_by_application_id(application_id, db)
    if application is None:
        raise HTTPException(status_code=404, detail=f"Application with user_id {application_id} not found.")
    return application


@user_router.get("/this_article_by_id")
async def get_article_by_user_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    article = await _get_article_by_user_id(user_id, db)
    if article is None:
        raise HTTPException(status_code=404, detail=f"Article with user_id {user_id} not found.")
    return article


@user_router.get("/this_article_by_article_id")
async def get_article_by_article_id(
        article_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    article = await _get_article_by_article_id(article_id, db)
    if article is None:
        raise HTTPException(status_code=404, detail=f"Article with user_id {article_id} not found.")
    return article


@user_router.get("/this_old_application")
async def get_old_applications(
        db: AsyncSession = Depends(get_db),
):
    application = await _get_old_applications(db)
    return application


@user_router.get("/this_articles")
async def get_articles(
        db: AsyncSession = Depends(get_db),
):
    articles = await _get_articles(db)
    return articles


@user_router.get("/this_new_application")
async def get_new_applications(
        db: AsyncSession = Depends(get_db),
):
    application = await _get_new_applications(db)
    return application


@user_router.get("/this_notification")
async def get_notification_by_user_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    notification = await _get_notification_by_user_id(user_id, db)
    if notification is None:
        raise HTTPException(status_code=404, detail=f"Notification with user_id {user_id} not found.")
    return notification


@user_router.get("/all", )
async def get_users(
        db: AsyncSession = Depends(get_db)
):
    users = await _get_all_users(db)
    return users


@user_router.get("/all_events", )
async def get_events(
        db: AsyncSession = Depends(get_db)
):
    events = await _get_all_events(db)
    return events


@user_router.patch("/edit")
async def update_user_by_id(
        user_id: UUID,
        body: UpdateUserNameRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    if user_id != current_user.user_id:
        if not (
                PortalRole.ROLE_PORTAL_ADMIN,
                PortalRole.ROLE_PORTAL_SUPERADMIN,
        ):
            raise HTTPException(status_code=403, detail="Forbidden.")
    updated_user_id = await _update_user(
        name=body.name, surname=body.surname, email=body.email, session=db, user_id=user_id
    )


@user_router.patch("/edit_event")
async def update_event_by_id(
        event_id: UUID,
        body: UpdateEventRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    if event_id != current_user.user_id:
        if not (
                current_user.roles == 'ROLE_PORTAL_ADMIN'
        ):
            raise HTTPException(status_code=403, detail="Forbidden.")
    updated_event_id = await _update_event(
        name=body.name, content=body.content, session=db, event_id=event_id
    )


@user_router.patch("/edit_notifications")
async def update_notification_by_user_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    updated_event_id = await _update_notifications(
        session=db, user_id=user_id
    )


@user_router.delete("/delete_notifications")
async def delete_notification_by_user_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    deleted_event_id = await _delete_notifications(
        session=db, user_id=user_id
    )


@user_router.patch("/edit_application")
async def update_application_by_user_id(
        id: UUID,
        body: UpdateStatusApplication,
        body1: NotificationCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    if not (
            current_user.roles == 'ROLE_PORTAL_ADMIN',
            current_user.roles == 'ROLE_PORTAL_MANAGER'
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    updated_application_status = await _update_application(
        id=id, status=body.status, session=db
    )
    notification = await _create_new_notification(body1, db)
