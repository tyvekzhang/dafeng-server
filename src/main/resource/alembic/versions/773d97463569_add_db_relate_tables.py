"""add_db_relate_tables

Revision ID: 773d97463569
Revises: 1516825cee75
Create Date: 2024-11-12 17:07:13.670589

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel # added
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '773d97463569'
down_revision = '1516825cee75'
branch_labels = None
depends_on = None


def upgrade():
    # op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sys_connection',
    sa.Column('id', sa.BigInteger(), nullable=False, comment='主键'),
    sa.Column('connection_name', sa.String(length=32), nullable=True, comment='连接名称'),
    sa.Column('database_type', sa.String(length=16), nullable=True, comment='数据库类型'),
    sa.Column('server_version', sa.String(length=16), nullable=True, comment='数据库版本'),
    sa.Column('host', sa.String(length=16), nullable=True, comment='主机'),
    sa.Column('port', sa.Integer(), nullable=True, comment='端口号'),
    sa.Column('username', sa.String(length=32), nullable=True, comment='用户名'),
    sa.Column('password', sa.String(length=63), nullable=True, comment='密码'),
    sa.Column('sessions', sa.Integer(), nullable=True, comment='活跃连接数'),
    sa.Column('client_character_set', sa.String(length=16), nullable=True, comment='客户端编码'),
    sa.Column('create_time', sa.BigInteger(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.BigInteger(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    comment='连接信息表'
    )
    op.create_index(op.f('ix_sys_connection_connection_name'), 'sys_connection', ['connection_name'], unique=False)
    op.create_index(op.f('ix_sys_connection_id'), 'sys_connection', ['id'], unique=True)
    op.create_table('sys_database',
    sa.Column('id', sa.BigInteger(), nullable=False, comment='主键'),
    sa.Column('connection_id', sa.BigInteger(), nullable=True, comment='连接id'),
    sa.Column('database_name', sa.String(length=32), nullable=True, comment='数据库名称'),
    sa.Column('character_set', sa.String(length=16), nullable=True, comment='字符编码'),
    sa.Column('collation', sa.String(length=16), nullable=True, comment='排序规则'),
    sa.Column('create_time', sa.BigInteger(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.BigInteger(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    comment='数据库信息表'
    )
    op.create_index(op.f('ix_sys_database_database_name'), 'sys_database', ['database_name'], unique=False)
    op.create_index(op.f('ix_sys_database_id'), 'sys_database', ['id'], unique=True)
    op.create_table('sys_field',
    sa.Column('id', sa.BigInteger(), nullable=False, comment='主键'),
    sa.Column('table_id', sa.BigInteger(), nullable=True, comment='表id'),
    sa.Column('name', sa.String(length=64), nullable=True, comment='字段名称'),
    sa.Column('type', sa.String(length=32), nullable=True, comment='类型'),
    sa.Column('length', sa.Integer(), nullable=True, comment='长度'),
    sa.Column('decimals', sa.Integer(), nullable=True, comment='小数位数'),
    sa.Column('not_null', sa.Boolean(), nullable=True, comment='允许为空(0:允许, 1:不允许)'),
    sa.Column('key', sa.Boolean(), nullable=True, comment='是否主键(0:否, 1:是)'),
    sa.Column('remark', sa.String(length=255), nullable=True, comment='备注'),
    sa.Column('create_time', sa.BigInteger(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.BigInteger(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    comment='表字段信息表'
    )
    op.create_index(op.f('ix_sys_field_id'), 'sys_field', ['id'], unique=True)
    op.create_table('sys_index',
    sa.Column('id', sa.BigInteger(), nullable=False, comment='主键'),
    sa.Column('table_id', sa.BigInteger(), nullable=True, comment='表id'),
    sa.Column('name', sa.String(length=32), nullable=True, comment='索引名称'),
    sa.Column('field', sa.String(length=63), nullable=True, comment='索引字段'),
    sa.Column('type', sa.String(length=16), nullable=True, comment='索引类型'),
    sa.Column('method', sa.String(length=16), nullable=True, comment='索引方法'),
    sa.Column('remark', sa.String(length=255), nullable=True, comment='备注'),
    sa.Column('create_time', sa.BigInteger(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.BigInteger(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    comment='索引信息表'
    )
    op.create_index(op.f('ix_sys_index_id'), 'sys_index', ['id'], unique=True)
    op.add_column('sys_table', sa.Column('database_id', sa.BigInteger(), nullable=True, comment='数据库id'))
    op.add_column('sys_table', sa.Column('rows', sa.Integer(), nullable=True, comment='行数'))
    op.add_column('sys_table', sa.Column('index_length', sa.String(length=32), nullable=True, comment='索引长度'))
    op.add_column('sys_table', sa.Column('data_length', sa.String(length=32), nullable=True, comment='数据长度'))
    op.alter_column('sys_table', 'name',
               existing_type=mysql.VARCHAR(length=64),
               comment='表名称',
               existing_comment='字段名称',
               existing_nullable=True)
    op.drop_index('idx_db_name_type', table_name='sys_table')
    op.drop_index('ix_sys_table_db_name', table_name='sys_table')
    op.create_table_comment(
        'sys_table',
        '表结构信息',
        existing_comment='数据库表结构信息',
        schema=None
    )
    op.drop_column('sys_table', 'key')
    op.drop_column('sys_table', 'not_null')
    op.drop_column('sys_table', 'db_name')
    op.drop_column('sys_table', 'decimals')
    op.drop_column('sys_table', 'type')
    op.drop_column('sys_table', 'db_type')
    op.drop_column('sys_table', 'length')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sys_table', sa.Column('length', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='长度'))
    op.add_column('sys_table', sa.Column('db_type', mysql.VARCHAR(length=16), nullable=True, comment='数据库类型'))
    op.add_column('sys_table', sa.Column('type', mysql.VARCHAR(length=32), nullable=True, comment='类型'))
    op.add_column('sys_table', sa.Column('decimals', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='小数位数'))
    op.add_column('sys_table', sa.Column('db_name', mysql.VARCHAR(length=32), nullable=True, comment='数据库名称'))
    op.add_column('sys_table', sa.Column('not_null', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='允许为空(0:允许, 1:不允许)'))
    op.add_column('sys_table', sa.Column('key', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否主键(0:否, 1:是)'))
    op.create_table_comment(
        'sys_table',
        '数据库表结构信息',
        existing_comment='表结构信息',
        schema=None
    )
    op.create_index('ix_sys_table_db_name', 'sys_table', ['db_name'], unique=False)
    op.create_index('idx_db_name_type', 'sys_table', ['db_type', 'db_name'], unique=False)
    op.alter_column('sys_table', 'name',
               existing_type=mysql.VARCHAR(length=64),
               comment='字段名称',
               existing_comment='表名称',
               existing_nullable=True)
    op.drop_column('sys_table', 'data_length')
    op.drop_column('sys_table', 'index_length')
    op.drop_column('sys_table', 'rows')
    op.drop_column('sys_table', 'database_id')
    op.drop_index(op.f('ix_sys_index_id'), table_name='sys_index')
    op.drop_table('sys_index')
    op.drop_index(op.f('ix_sys_field_id'), table_name='sys_field')
    op.drop_table('sys_field')
    op.drop_index(op.f('ix_sys_database_id'), table_name='sys_database')
    op.drop_index(op.f('ix_sys_database_database_name'), table_name='sys_database')
    op.drop_table('sys_database')
    op.drop_index(op.f('ix_sys_connection_id'), table_name='sys_connection')
    op.drop_index(op.f('ix_sys_connection_connection_name'), table_name='sys_connection')
    op.drop_table('sys_connection')
    # ### end Alembic commands ###