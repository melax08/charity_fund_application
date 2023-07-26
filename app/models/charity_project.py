from sqlalchemy import Column, String, Text

from app.core.db import ProjectDonateBase
from app.core.constants import MAX_PROJECT_NAME


class CharityProject(ProjectDonateBase):
    name = Column(String(MAX_PROJECT_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'<Project {self.name}>'
