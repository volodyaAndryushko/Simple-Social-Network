from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKeyConstraint, PrimaryKeyConstraint

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


class Like(Base):
    __tablename__ = "like"

    post_id = Column("post_id", Integer, nullable=False)
    liked_by_id = Column("liked_by_id", Integer, nullable=False)
    created_time = Column("created_time", DateTime, default=datetime.utcnow)

    __table_args__ = (
        PrimaryKeyConstraint("post_id", "liked_by_id", "created_time"),
        ForeignKeyConstraint(("liked_by_id",), ("user.id",), name="fk_like_liked_by", ondelete="CASCADE"),
        ForeignKeyConstraint(("post_id",), ("post.id",), name="fk_like_post_id", ondelete="CASCADE"),
    )

    def __repr__(self):
        return f"<Like on post #{self.post_id} - by: User #{self.liked_by_id}>"
