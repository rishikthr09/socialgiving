from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
messages = Table('messages', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('message', String(length=100)),
    Column('from_id', Integer),
    Column('to_id', Integer),
    Column('item_id', Integer),
    Column('created_on', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['messages'].columns['item_id'].create()
    post_meta.tables['messages'].columns['message'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['messages'].columns['item_id'].drop()
    post_meta.tables['messages'].columns['message'].drop()
