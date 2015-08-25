<%!
import re

%>"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

from alembic import op
import sqlalchemy as sa
from application.models import _external_types
${imports if imports else ""}

def upgrade(engine_name):
    if engine_name in db_names:
        globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    if engine_name in db_names:
        globals()["downgrade_%s" % engine_name]()

<%
    from flask import current_app
    db_names = [''] + list(current_app.config.get("SQLALCHEMY_BINDS").keys())
%>
db_names = ${db_names}

## generate an "upgrade_<xyz>() / downgrade_<xyz>()" function
## for each database name in the ini file.

% for db_name in db_names:

def upgrade_${db_name}():
    ${context.get("%s_upgrades" % db_name, "pass")}


def downgrade_${db_name}():
    ${context.get("%s_downgrades" % db_name, "pass")}

% endfor
