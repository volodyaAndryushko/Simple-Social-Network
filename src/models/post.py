from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKeyConstraint

from src.app import Base


class Post(Base):
    __tablename__ = "post"

    id = Column("id", Integer, primary_key=True)
    author_id = Column("author_id", Integer, nullable=False)
    title = Column("title", String(60), nullable=False)
    content = Column("content", Text)
    created_time = Column("created_time", DateTime, default=datetime.utcnow)

    __table_args__ = (
        ForeignKeyConstraint(("author_id",), ("user.id",), name="fk_post_author_id", ondelete="CASCADE"),
    )

    def __repr__(self):
        return f"<Post #{self.id} - by: {self.author_id}>"

    def as_dict(self):
        return dict(id=self.id, title=self.title, content=self.content, created_time=self.created_time)
