from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import ProjectDonateBase


class Donation(ProjectDonateBase):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return f'<Donation by {self.user_id} for {self.full_amount}>'
