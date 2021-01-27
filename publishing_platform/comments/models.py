from sqlalchemy.dialects.postgresql import UUID

from publishing_platform.app import db

__all__ = [
    "Comment",
]


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(UUID(), nullable=False, primary_key=True)
    author_id = db.Column(UUID(), nullable=True)
    author_name = db.Column(db.String(), nullable=True)
    article_id = db.Column(UUID(), nullable=False)
    reply_to = db.Column(UUID(), nullable=True, default=None)
    text = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    anonymous = db.Column(db.Boolean(), nullable=False)

    __author_id_fk = db.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="SET NULL")
    __article_id_fk = db.ForeignKeyConstraint(["article_id"], ["articles.id"], ondelete="CASCADE")
    __reply_to_id_fk = db.ForeignKeyConstraint(["reply_to"], ["comments.id"], ondelete="CASCADE")
