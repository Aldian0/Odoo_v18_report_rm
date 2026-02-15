# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class FormDpjp(models.Model):
    _name = 'cdn.form.dpjp'
    _description = 'Form DPJP (Dokter Penanggung Jawab Pelayanan)'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin'
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
    )

    # === INFORMASI PASIEN ===
    nama_pasien = fields.Char(string='Nama Pasien')
    tanggal_lahir = fields.Date(string='Tgl. Lahir')
    jenis_kelamin = fields.Selection([
        ('laki_laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Jenis Kelamin')
    no_rm = fields.Char(string='No. RM')
    tanggal_jam = fields.Datetime(string='Tanggal/Jam', default=fields.Datetime.now)

    # === STATUS ===
    status_asuransi_lain = fields.Boolean(string='Asuransi Lain')
    status_umum = fields.Boolean(string='Umum')
    status_bpjs = fields.Boolean(string='BPJS')

    # === DIAGNOSA MEDIS ===
    diagnosa_medis_1 = fields.Char(string='Diagnosa Medis 1')
    diagnosa_medis_2 = fields.Char(string='Diagnosa Medis 2')
    diagnosa_medis_3 = fields.Char(string='Diagnosa Medis 3')
    diagnosa_medis_4 = fields.Char(string='Diagnosa Medis 4')

    # === DPJP UTAMA ===
    dpjp = fields.Char(string='DPJP')
    ttd_dpjp = fields.Binary(string='Tanda Tangan DPJP')

    # === RAWAT BERSAMA ===
    rawat_bersama_ids = fields.One2many(
        'cdn.form.dpjp.rawat.bersama',
        'form_dpjp_id',
        string='Rawat Bersama'
    )

    # === PERALIHAN DPJP UTAMA ===
    dpjp_peralihan = fields.Char(string='DPJP Peralihan')
    ttd_peralihan = fields.Binary(string='Tanda Tangan Peralihan')
    tanggal_peralihan = fields.Date(string='Tanggal Peralihan')
    alasan_peralihan = fields.Text(string='Alasan Peralihan')
    
    # Persetujuan DPJP Lama
    ttd_dpjp_lama = fields.Binary(string='Tanda Tangan DPJP Lama')
    
    # Manajer Pelayanan Pasien (MPP)
    ttd_mpp = fields.Binary(string='Tanda Tangan MPP (Manajer Pelayanan Pasien)')


class FormDpjpRawatBersama(models.Model):
    _name = 'cdn.form.dpjp.rawat.bersama'
    _description = 'Rawat Bersama - Form DPJP'
    _order = 'sequence, id'

    form_dpjp_id = fields.Many2one(
        'cdn.form.dpjp',
        string='Form DPJP',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(string='Sequence', default=10)

    # === RAWAT BERSAMA ===
    dpjp_utama = fields.Boolean(string='DPJP Utama', default=False)
    nama_dpjp = fields.Char(string='DPJP')
    tanggal_rawat_bersama = fields.Date(string='Tanggal')

