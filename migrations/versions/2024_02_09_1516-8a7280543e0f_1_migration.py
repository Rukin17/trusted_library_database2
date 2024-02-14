"""1 migration

Revision ID: 8a7280543e0f
Revises:
Create Date: 2024-02-09 15:16:05.219400

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '8a7280543e0f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_authors_id'), 'authors', ['id'], unique=False)
    op.create_index(op.f('ix_authors_name'), 'authors', ['name'], unique=False)
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=True)
    op.create_table('libraries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('APPROVED', 'MALWARE', 'UNTESTED', name='status'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_libraries_id'), 'libraries', ['id'], unique=False)
    op.create_index(op.f('ix_libraries_name'), 'libraries', ['name'], unique=True)
    op.create_index(op.f('ix_libraries_status'), 'libraries', ['status'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('approvers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_approvers_email'), 'approvers', ['email'], unique=True)
    op.create_index(op.f('ix_approvers_fullname'), 'approvers', ['fullname'], unique=False)
    op.create_index(op.f('ix_approvers_id'), 'approvers', ['id'], unique=False)
    op.create_index(op.f('ix_approvers_user_id'), 'approvers', ['user_id'], unique=False)
    op.create_table('association_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('library_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['library_id'], ['libraries.id'], ),
    sa.PrimaryKeyConstraint('id', 'library_id', 'author_id')
    )
    op.create_index(op.f('ix_association_table_author_id'), 'association_table', ['author_id'], unique=False)
    op.create_index(op.f('ix_association_table_library_id'), 'association_table', ['library_id'], unique=False)
    op.create_table('managers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_managers_email'), 'managers', ['email'], unique=True)
    op.create_index(op.f('ix_managers_id'), 'managers', ['id'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('USER', 'APPROVER', 'MANAGER', 'ADMIN', name='rolesenum'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_user_id'), 'roles', ['user_id'], unique=False)
    op.create_table('approved_libraries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('approver_id', sa.Integer(), nullable=False),
    sa.Column('library_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['approver_id'], ['approvers.id'], ),
    sa.ForeignKeyConstraint(['library_id'], ['libraries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_approved_libraries_id'), 'approved_libraries', ['id'], unique=False)
    op.create_index(op.f('ix_approved_libraries_name'), 'approved_libraries', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_approved_libraries_name'), table_name='approved_libraries')
    op.drop_index(op.f('ix_approved_libraries_id'), table_name='approved_libraries')
    op.drop_table('approved_libraries')
    op.drop_index(op.f('ix_roles_user_id'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_managers_id'), table_name='managers')
    op.drop_index(op.f('ix_managers_email'), table_name='managers')
    op.drop_table('managers')
    op.drop_index(op.f('ix_association_table_library_id'), table_name='association_table')
    op.drop_index(op.f('ix_association_table_author_id'), table_name='association_table')
    op.drop_table('association_table')
    op.drop_index(op.f('ix_approvers_user_id'), table_name='approvers')
    op.drop_index(op.f('ix_approvers_id'), table_name='approvers')
    op.drop_index(op.f('ix_approvers_fullname'), table_name='approvers')
    op.drop_index(op.f('ix_approvers_email'), table_name='approvers')
    op.drop_table('approvers')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_libraries_status'), table_name='libraries')
    op.drop_index(op.f('ix_libraries_name'), table_name='libraries')
    op.drop_index(op.f('ix_libraries_id'), table_name='libraries')
    op.drop_table('libraries')
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies')
    op.drop_index(op.f('ix_authors_name'), table_name='authors')
    op.drop_index(op.f('ix_authors_id'), table_name='authors')
    op.drop_table('authors')
    # ### end Alembic commands ###