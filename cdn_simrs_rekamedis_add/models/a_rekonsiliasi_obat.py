# cdn_simrs_rekamedis_add/models/rekonsiliasi_obat.py

from odoo import _, api, fields, models

class RekonsiliasiObatSaatAdmisi(models.Model):
    _name = 'cdn.rekonsiliasi.obat.saat.admisi'
    _description = 'Formulir Rekonsiliasi Obat'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin'  # hapus jika tidak ada
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
    )
    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )

    # === PENGGUNAAN OBAT SEBELUM ADMISI ===
    penggunaan_obat_sebelum_admisi = fields.Selection([
        ('ya', 'Ya, dengan rincian sebagai berikut'),
        ('tidak', 'Tidak menggunakan obat sebelum admisi'),
    ], string='Penggunaan obat sebelum admisi')

    # === TABEL REKONSILIASI OBAT (One2many) ===
    line_ids = fields.One2many(
        comodel_name    ='cdn.rekonsiliasi.obat.saat.admisi.line',
        inverse_name    ='rekonsiliasi_id',
        string          ='Rincian Obat'
    )

    # === FIELD APOTEKER ===
    apoteker_tanggal_jam    = fields.Datetime(string='Tanggal/Jam')
    apoteker_nama           = fields.Char(string='Apoteker Yang Melakukan Rekonsiliasi Obat')


class RekonsiliasiObatSaatAdmisiLine(models.Model):
    _name = 'cdn.rekonsiliasi.obat.saat.admisi.line'
    _description = 'Baris Rekonsiliasi Obat Saat Admisi'
    _order = 'sequence, id'

    rekonsiliasi_id = fields.Many2one(
        comodel_name='cdn.rekonsiliasi.obat.saat.admisi',
        string      ='Dokumen',
        required    =True,
        ondelete    ='cascade'
    )

    sequence = fields.Integer(string='No', default=1)
    nama_obat = fields.Char(string='Nama Obat')
    dosis = fields.Char(string='Dosis')
    frekuensi = fields.Char(string='Frekuensi')
    cara_pemberian = fields.Char(string='Cara Pemberian')

    tindak_lanjut = fields.Selection([
        ('sama', 'Lanjut aturan pakai sama'),
        ('berubah', 'Lanjut aturan pakai berubah'),
        ('stop', 'Stop'),
    ], string='Tindak Lanjut oleh DPJP')

    perubahan_aturan_pakai = fields.Text(string='Perubahan Aturan Pakai')
