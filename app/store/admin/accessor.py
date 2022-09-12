import typing

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> typing.Union[Admin, None]:
        async with self.app.database.session() as session:
            admin = await session.execute(
                select(AdminModel).where(AdminModel.email == email)
            )
            if admin:
                for admin in admin.scalars():
                    return Admin(
                        id=admin.id, email=admin.email, password=admin.password
                    )
            return None

    async def create_admin(self, email: str, password: str) -> Admin:
        async with self.app.database.session() as session:
            async with session.begin():
                session.add(AdminModel(email=email, password=password))
