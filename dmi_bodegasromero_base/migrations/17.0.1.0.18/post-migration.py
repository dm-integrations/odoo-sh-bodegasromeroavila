from odoo import SUPERUSER_ID, api


def migrate(cr, version: str) -> None:
    """Recalcula ``partner_share`` tras restaurar ``res.partner.user_ids``.

    Mientras ``user_ids`` estuvo redefinido como Many2many de seguidores, el
    campo almacenado se calculó con los seguidores en lugar de con los usuarios
    reales del contacto.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    partners = env["res.partner"].with_context(active_test=False).search([])
    env.add_to_compute(partners._fields["partner_share"], partners)
    env["res.partner"].flush_model(["partner_share"])
