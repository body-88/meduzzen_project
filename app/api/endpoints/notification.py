from fastapi import APIRouter, Depends
from app.schemas.user import Result, UserResponse
from app.api.deps import get_current_user
from app.servises.notification import NotificationService, get_notification_service
from app.servises.user import UserService, get_user_service
from app.servises.quiz import QuizService, get_quiz_service
from app.servises.company import CompanyService, get_company_service


router = APIRouter()


@router.get("/unread", response_model=Result, status_code=200, response_description="Unread notifications returned")
async def get_notifications_unread(service: NotificationService = Depends(get_notification_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    notifications = await service.get_all_notifications_unread(current_user_id=current_user.user_id)
    return Result(result={"notifications": notifications})


@router.get("/read", response_model=Result, status_code=200, response_description="Read notifications returned")
async def get_notifications_read(service: NotificationService = Depends(get_notification_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    notifications = await service.get_all_notifications_read(current_user_id=current_user.user_id)
    return Result(result={"notifications": notifications})


@router.put("/{notification_id}/status", response_model=Result, status_code=200, response_description="Notification status changed")
async def read_notification(notification_id: int,
                    service: NotificationService = Depends(get_notification_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.manage_notification(notification_id=notification_id,
                                            current_user_id=current_user.user_id)
    return Result(result=result, message="success")


@router.get("/test", response_model=Result, status_code=200, response_description="test")
async def test(service: NotificationService = Depends(get_notification_service), 
                    current_user: UserResponse = Depends(get_current_user),
                    user_service: UserService = Depends(get_user_service),
                    quiz_service: QuizService = Depends(get_quiz_service),
                    company_service:CompanyService = Depends(get_company_service),) -> Result:
    notifications = await service.check_quiz_notification(quiz_service=quiz_service, company_service=company_service, user_service=user_service)
    return Result(result={"notifications": notifications})
