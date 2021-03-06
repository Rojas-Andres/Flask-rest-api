"""empty message

Revision ID: 04a0c887fcae
Revises: 
Create Date: 2021-09-06 21:55:39.302497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04a0c887fcae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=70), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('ventas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username_id', sa.Integer(), nullable=True),
    sa.Column('venta', sa.Integer(), nullable=True),
    sa.Column('ventas_productos', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['username_id'], ['usuario.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ventas')
    op.drop_table('usuario')
    # ### end Alembic commands ###
