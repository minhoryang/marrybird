"""Add selfstorylike and selfstory<-title.

Revision ID: 2268f15c3f9
Revises: 272112f86f5
Create Date: 2015-08-25 16:44:01.412746

"""

# revision identifiers, used by Alembic.
revision = '2268f15c3f9'
down_revision = '272112f86f5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from application.models import _external_types


def upgrade(engine_name):
    if engine_name in db_names:
        globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    if engine_name in db_names:
        globals()["downgrade_%s" % engine_name]()


db_names = ['', 'file', 'record', 'response', 'phone', 'notice', 'user', 'met', 'selfstory', 'progress', 'request', 'selfstorylike', 'review', 'score']



def upgrade_():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_file():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_file():
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


def upgrade_response():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_response():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_phone():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_phone():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_notice():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_notice():
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
    op.add_column('self_story', sa.Column('title', sa.String(length=50), nullable=True))
    ### end Alembic commands ###


def downgrade_selfstory():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('self_story', 'title')
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


def upgrade_selfstorylike():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('self_story_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('story_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('nickname', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade_selfstorylike():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('self_story_like')
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

