from odoo import _, api, fields, models

class CdnErmBase(models.Model):
    _inherit = 'cdn.erm.base'

    # ========= TTD BIDAN ==========
    qr_ttd_bidan_id           = fields.Many2one(comodel_name='cdn.signature', string='Bidan')

    qr_ttd_bidan_date         = fields.Date('Date', related='qr_ttd_bidan_id.tanggal_tdd')
    qr_ttd_bidan_code         = fields.Binary(string='QR Code', related='qr_ttd_bidan_id.qr_code')
    qr_ttd_bidan_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_bidan_id.partner_id', string='Partner')


    qr_ttd_pendamping_dokter_id           = fields.Many2one(comodel_name='cdn.signature', string='informan')
    qr_ttd_pendamping_dokter_date         = fields.Date('Date', related='qr_ttd_pendamping_dokter_id.tanggal_tdd')
    qr_ttd_pendamping_dokter_code         = fields.Binary(string='QR Code', related='qr_ttd_pendamping_dokter_id.qr_code')
    qr_ttd_pendamping_dokter_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_pendamping_dokter_id.partner_id', string='Partner')


    qr_ttd_informan_id           = fields.Many2one(comodel_name='cdn.signature', string='informan')
    qr_ttd_informan_date         = fields.Date('Date', related='qr_ttd_informan_id.tanggal_tdd')
    qr_ttd_informan_code         = fields.Binary(string='QR Code', related='qr_ttd_informan_id.qr_code')
    qr_ttd_informan_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_informan_id.partner_id', string='Partner')