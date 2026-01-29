from odoo import api, fields, models


class ErmImplementasiKeperawatan(models.Model):
    _name = 'cdn.implementasi.keperawatan'
    _description = 'Implementasi Keperawatan'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin'
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base', string='RM', required=True, ondelete='cascade'
    )

    line_ids = fields.One2many(
        'cdn.implementasi.keperawatan.line', 'implementasi_keperawatan_id', string='Implementasi Lines'
    )

    # jam = fields.Datetime('jam')
class ErmImplementasiKeperawatanLine(models.Model):
    _name = 'cdn.implementasi.keperawatan.line'
    _description = 'Implementasi Keperawatan Line'
    _order = 'tanggal ASC'

    _inherit        = [
        'cdn.signature.library',
        ]

    implementasi_keperawatan_id = fields.Many2one('cdn.implementasi.keperawatan', string='Dokumen', ondelete='cascade', required=True)

    tanggal = fields.Datetime(string='Tanggal & Jam', required=True, default=fields.Date.context_today)
    # jam = fields.Float(string='Jam')  # use float time (HH.MM) or change to Char if needed
    implementasi_monitoring = fields.Text(string='Implementasi dan Monitoring')
    # nama_perawat = fields.Char(string='Nama Perawat')
    # tanda_tangan = fields.Binary(string='Tanda Tangan')
    
    jam = fields.Datetime('jam')


    qr_ttd_perawat_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_date         = fields.Date('Date', related='qr_ttd_perawat_id.tanggal_tdd')
    qr_ttd_perawat_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_id.qr_code')
    qr_ttd_perawat_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_id.partner_id', string='Partner')

    def signature_generate(self):
        login = False
        if self.env.user.login:
            login = self.env.user.login or ''

        model_id = self.env['ir.model'].sudo().search([('model', '=', self._name)])
        data = {
            'default_username'      : login,
            'default_field_name'    : self.env.context.get('field_name'),
            'default_model_id'      : model_id.id,
            'default_data_id'       : self.id,
            'default_tipe'          : self.env.context.get('tipe_nakes') or '',
            'default_tipe_dokumen'  : self.env.context.get('tipe_dokumen') or '',
            'default_perihal'       : self.env.context.get('perihal') or '',
        }

        return self.open_wizard_generate_qr_sign(data)