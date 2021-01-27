from sqlalchemy.dialects.postgresql import UUID

from publishing_platform.app import db

__all__ = [
    "Article",
]


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(UUID(), nullable=False, primary_key=True)
    author_id = db.Column(UUID(), nullable=True)
    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)

    __author_id_fk = db.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="SET NULL")
