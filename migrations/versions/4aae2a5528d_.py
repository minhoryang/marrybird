"""DatingV2

Revision ID: 4aae2a5528d
Revises: 14c49d5238a
Create Date: 2015-09-20 14:12:34.208280

"""

# revision identifiers, used by Alembic.
revision = '4aae2a5528d'
down_revision = '14c49d5238a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import application
from application.models import _external_types
from application.models.dating2.action import ActionType
from application.models.dating2.event import EventType
from application.models.dating2.state import StateType


def upgrade(engine_name):
    if engine_name in db_names:
        globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    if engine_name in db_names:
        globals()["downgrade_%s" % engine_name]()


db_names = ['', 'oldevent', 'progress', 'action', 'resultbook', 'score', 'replybook', 'selfstory', 'user', 'event', 'condition', 'question', 'selfstorylike', 'phone', 'oldreplybook', 'request', 'record', 'review', 'file', 'notice', 'deadaction', 'response', 'deadstate', 'deadevent', 'reply', 'state', 'questionbook', 'oldstate', 'comment', 'oldreply', 'tomarrybird', 'met']



def upgrade_():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_oldevent():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oldevent',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.Column('_type', application.models._external_types.EnumType(EventType), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('_results', application.models._external_types.ScalarListType(), nullable=True),
    sa.Column('at', sa.DateTime(), nullable=True),
    sa.Column('old_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id__')
    )
    ### end Alembic commands ###


def downgrade_oldevent():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oldevent')
    ### end Alembic commands ###


def upgrade_progress():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_progress():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_action():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.Column('_type', application.models._external_types.EnumType(ActionType), nullable=True),
    sa.Column('from_A', sa.String(length=50), nullable=True),
    sa.Column('to_B', sa.String(length=50), nullable=False),
    sa.Column('at', sa.DateTime(), nullable=True),
    sa.Column('_json', application.models._external_types.JSONType(), nullable=True),
    sa.Column('json', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('action_03_askedout',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['action.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('action_05_got_askedout_and_accept',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['action.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('action_06_got_askedout_and_reject',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['action.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('action_08_endofdating',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['action.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('action_09_endofdating_and_feedback',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['action.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    ### end Alembic commands ###


def downgrade_action():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('action_09_endofdating_and_feedback')
    op.drop_table('action_08_endofdating')
    op.drop_table('action_06_got_askedout_and_reject')
    op.drop_table('action_05_got_askedout_and_accept')
    op.drop_table('action_03_askedout')
    op.drop_table('action')
    ### end Alembic commands ###


def upgrade_resultbook():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_resultbook():
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


def upgrade_replybook():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_replybook():
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


def upgrade_user():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_user():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_event():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.Column('_type', application.models._external_types.EnumType(EventType), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('_results', application.models._external_types.ScalarListType(), nullable=True),
    sa.Column('at', sa.DateTime(), nullable=True),
    sa.Column('results', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_00_server_suggested',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_03_askedout',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_04_got_askedout',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_05_got_askedout_and_accept',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_06_got_askedout_and_reject',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_07_askedout_accepted',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_08_endofdating',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_09_endofdating_and_feedback',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('event_99_askedout_rejected',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['event.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    ### end Alembic commands ###


def downgrade_event():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_99_askedout_rejected')
    op.drop_table('event_09_endofdating_and_feedback')
    op.drop_table('event_08_endofdating')
    op.drop_table('event_07_askedout_accepted')
    op.drop_table('event_06_got_askedout_and_reject')
    op.drop_table('event_05_got_askedout_and_accept')
    op.drop_table('event_04_got_askedout')
    op.drop_table('event_03_askedout')
    op.drop_table('event_00_server_suggested')
    op.drop_table('event')
    ### end Alembic commands ###


def upgrade_condition():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_condition():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_question():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_question():
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


def upgrade_phone():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_phone():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_oldreplybook():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_oldreplybook():
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


def upgrade_record():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_record():
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


def upgrade_file():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_file():
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


def upgrade_deadaction():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deadaction',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.Column('_type', application.models._external_types.EnumType(ActionType), nullable=True),
    sa.Column('from_A', sa.String(length=50), nullable=True),
    sa.Column('to_B', sa.String(length=50), nullable=False),
    sa.Column('at', sa.DateTime(), nullable=True),
    sa.Column('_json', application.models._external_types.JSONType(), nullable=True),
    sa.Column('dead_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id__')
    )
    ### end Alembic commands ###


def downgrade_deadaction():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deadaction')
    ### end Alembic commands ###


def upgrade_response():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_response():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_deadstate():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deadstate',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.Column('_state', application.models._external_types.EnumType(StateType), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('at', sa.DateTime(), nullable=True),
    sa.Column('next_state', application.models._external_types.EnumType(StateType), nullable=True),
    sa.Column('old_at', sa.DateTime(), nullable=True),
    sa.Column('dead_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id__')
    )
    ### end Alembic commands ###


def downgrade_deadstate():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deadstate')
    ### end Alembic commands ###


def upgrade_deadevent():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deadevent',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.Column('_type', application.models._external_types.EnumType(EventType), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('_results', application.models._external_types.ScalarListType(), nullable=True),
    sa.Column('at', sa.DateTime(), nullable=True),
    sa.Column('old_at', sa.DateTime(), nullable=True),
    sa.Column('dead_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id__')
    )
    ### end Alembic commands ###


def downgrade_deadevent():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deadevent')
    ### end Alembic commands ###


def upgrade_reply():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_reply():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_state():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('state',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.Column('_state', application.models._external_types.EnumType(StateType), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('state_02_a___',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['state.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('state_04_ab__',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['state.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('state_06_a_c_',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['state.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('state_08_abc_',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['state.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('state_09____d',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['state.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('state_11__b_d',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['state.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('state_13___cd',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['state.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    op.create_table('state_15__bcd',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id__'], ['state.id__'], ),
    sa.PrimaryKeyConstraint('id__')
    )
    ### end Alembic commands ###


def downgrade_state():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('state_15__bcd')
    op.drop_table('state_13___cd')
    op.drop_table('state_11__b_d')
    op.drop_table('state_09____d')
    op.drop_table('state_08_abc_')
    op.drop_table('state_06_a_c_')
    op.drop_table('state_04_ab__')
    op.drop_table('state_02_a___')
    op.drop_table('state')
    ### end Alembic commands ###


def upgrade_questionbook():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_questionbook():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_oldstate():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oldstate',
    sa.Column('id__', sa.Integer(), nullable=False),
    sa.Column('_state', application.models._external_types.EnumType(StateType), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('at', sa.DateTime(), nullable=True),
    sa.Column('next_state', application.models._external_types.EnumType(StateType), nullable=True),
    sa.Column('old_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id__')
    )
    ### end Alembic commands ###


def downgrade_oldstate():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oldstate')
    ### end Alembic commands ###


def upgrade_comment():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_comment():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_oldreply():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_oldreply():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_tomarrybird():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_tomarrybird():
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
