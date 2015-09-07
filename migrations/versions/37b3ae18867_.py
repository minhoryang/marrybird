"""Census(Reply[Book]+Question[Book]+Comment) Done. [MODIFIED].

Revision ID: 37b3ae18867
Revises: 2268f15c3f9
Create Date: 2015-08-28 23:36:30.809734

"""

# revision identifiers, used by Alembic.
revision = '37b3ae18867'
down_revision = '2268f15c3f9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import application
from application.models import _external_types


def upgrade(engine_name):
    if engine_name in db_names:
        globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    if engine_name in db_names:
        globals()["downgrade_%s" % engine_name]()


db_names = ['', 'comment', 'file', 'response', 'record', 'questionbook', 'notice', 'progress', 'request', 'met', 'selfstory', 'replybook', 'reply', 'question', 'phone', 'selfstorylike', 'review', 'score', 'user']



def upgrade_():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_comment():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commented_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('question_book_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('nickname', sa.String(length=50), nullable=True),
    sa.Column('photo_url', sa.String(length=50), nullable=True),
    sa.Column('content', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade_comment():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    ### end Alembic commands ###


def upgrade_file():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_file():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_response():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_response():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_record():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_record():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_questionbook():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('photo_url', sa.String(length=50), nullable=True),
    sa.Column('brief_description', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('compute_type', sa.String(length=50), nullable=False),
    sa.Column('questions', application.models._external_types.ScalarListType(), nullable=True),
    sa.Column('num_of_questions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade_questionbook():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question_book')
    ### end Alembic commands ###


def upgrade_notice():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_notice():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_progress():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_progress():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_request():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_request():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_met():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_met():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_selfstory():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_selfstory():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_replybook():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reply_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('question_book_id', sa.Integer(), nullable=False),
    sa.Column('max_question_id', sa.Integer(), nullable=False),
    sa.Column('requested_at', sa.DateTime(), nullable=True),
    sa.Column('compute_id', sa.Integer(), nullable=True),
    sa.Column('computed_at', sa.DateTime(), nullable=True),
    sa.Column('computed_result', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade_replybook():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reply_book')
    ### end Alembic commands ###


def upgrade_reply():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reply',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('question_book_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('replied_at', sa.DateTime(), nullable=True),
    #sa.Column('answer', sa.String(length=200), nullable=False),  # [MODIFIED]
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade_reply():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reply')
    ### end Alembic commands ###


def upgrade_question():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=200), nullable=True),
    sa.Column('_expected_answers', application.models._external_types.JSONType(), nullable=True),
    sa.Column('e_a_json', sa.String(length=200), nullable=True),
    sa.Column('expected_answer_count', sa.Integer(), nullable=False),
    sa.Column('_compute_rules', application.models._external_types.JSONType(), nullable=True),
    sa.Column('c_r_json', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade_question():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question')
    ### end Alembic commands ###


def upgrade_phone():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_phone():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_selfstorylike():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_selfstorylike():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_review():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_review():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_score():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_score():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_user():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_user():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###

