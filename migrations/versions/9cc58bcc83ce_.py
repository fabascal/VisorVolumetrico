"""empty message

Revision ID: 9cc58bcc83ce
Revises: b166237955c8
Create Date: 2022-03-02 12:01:55.518831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cc58bcc83ce'
down_revision = 'b166237955c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reporte_lineas_compras', sa.Column('capacidadTotalTanque', sa.Float(), nullable=True))
    op.add_column('reporte_lineas_compras', sa.Column('capacidadOperativaTanque', sa.Float(), nullable=True))
    op.add_column('reporte_lineas_compras', sa.Column('capacidadUtilTanque', sa.Float(), nullable=True))
    op.add_column('reporte_lineas_compras', sa.Column('capacidadFondajeTanque', sa.Float(), nullable=True))
    op.add_column('reporte_lineas_compras', sa.Column('volumenMinimoOperacion', sa.Float(), nullable=True))
    op.add_column('reporte_lineas_compras', sa.Column('estadoTanque', sa.String(length=1), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reporte_lineas_compras', 'estadoTanque')
    op.drop_column('reporte_lineas_compras', 'volumenMinimoOperacion')
    op.drop_column('reporte_lineas_compras', 'capacidadFondajeTanque')
    op.drop_column('reporte_lineas_compras', 'capacidadUtilTanque')
    op.drop_column('reporte_lineas_compras', 'capacidadOperativaTanque')
    op.drop_column('reporte_lineas_compras', 'capacidadTotalTanque')
    # ### end Alembic commands ###