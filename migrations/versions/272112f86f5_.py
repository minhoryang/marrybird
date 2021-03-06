"""Notice <- created_at

Revision ID: 272112f86f5
Revises: 394d4205f2c
Create Date: 2015-08-25 15:53:00.059862

"""

# revision identifiers, used by Alembic.
revision = '272112f86f5'
down_revision = '394d4205f2c'
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



db_names = ['', 'score', 'met', 'response', 'request', 'user', 'phone', 'file', 'review', 'notice', 'record', 'progress', 'selfstory']


def upgrade_():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_():
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


def upgrade_score():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_score():
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


def upgrade_request():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_request():
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


def upgrade_file():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_file():
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


def upgrade_notice():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notice', sa.Column('created_at', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade_notice():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notice', 'created_at')
    ### end Alembic commands ###


def upgrade_response():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_response():
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


def upgrade_record():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_record():
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

