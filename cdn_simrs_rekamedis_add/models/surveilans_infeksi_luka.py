# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SurveilansInfeksiLuka(models.Model):
    _name = 'cdn.surveilans.infeksi.luka'
    _description = 'Pengumpulan Data Surveilans Infeksi Luka Operasi'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = ['mail.thread', 'mail.activity.mixin', 'cdn.erm.mixin']

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
    )

    # =====================================================
    # DATA OPERASI
    # =====================================================
    tgl_mrs = fields.Date(string='Tgl. MRS', tracking=True)
    no_surat = fields.Char(string='No. Surat', tracking=True)
    
    lama_op = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Lama Op', tracking=True)
    
    is_trauma = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Operasi krn Trauma', tracking=True)
    
    is_multipro_prosedur = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Multipro prosedur dengan Insisi yang sama', tracking=True)

    tgl_operasi = fields.Date(string='Tgl. Operasi', tracking=True)
    
    jenis_op = fields.Selection([
        ('elektif', 'Elektif'),
        ('darurat', 'Darurat')
    ], string='Jenis Op', tracking=True)
    
    urutan_op = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    ], string='Urutan Op', tracking=True)
    
    asa_score = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ], string='ASA Score', tracking=True)

    prosedur_operasi = fields.Selection([
        ('lscs', 'LSCS'),
        ('appendictomy', 'Appendictomy'),
        ('abdominal_hysterectomy', 'Abdominal hysterectomy'),
        ('lainnya', 'Lainnya')
    ], string='Prosedur Operasi', tracking=True)
    prosedur_operasi_lainnya = fields.Char(string='Keterangan Prosedur Lainnya')

    # Kualifikasi Dokter Bedah
    kualifikasi_dokter = fields.Selection([
        ('spesialis', 'Spesialis'),
        ('konsultan', 'Konsultan'),
        ('associated_spesialis', 'Associated Spesialis'),
        ('lainnya', 'Lainnya')
    ], string='Kualifikasi Dokter Bedah', tracking=True)

    # Klasifikasi Luka
    klasifikasi_luka = fields.Selection([
        ('bersih', 'Bersih'),
        ('bersih_terkontaminasi', 'Bersih Terkontaminasi'),
        ('terkontaminasi', 'Terkontaminasi'),
        ('kotor', 'Kotor')
    ], string='Klasifikasi Luka', tracking=True)

    # =====================================================
    # PRE OP
    # =====================================================
    suhu_pasien = fields.Selection([
        ('lebih_38', '>= 38°C'),
        ('kurang_38', '<= 38°C')
    ], string='Suhu Pasien', tracking=True)
    
    gda = fields.Float(string='GDA', tracking=True)
    leukosit = fields.Float(string='Leukosit', tracking=True)
    
    is_merokok = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Merokok', tracking=True)
    
    is_steroid_jangka_panjang = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Steroid jangka panjang', tracking=True)

    mandi_sebelum_op = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Mandi Sebelum Op', tracking=True)
    
    sabun_mandi = fields.Selection([
        ('chlorhexidine', 'chlorhexidine bodywash'),
        ('sabun_lain', 'sabun lain')
    ], string='Jenis Sabun', tracking=True)
    sabun_lain_ket = fields.Char(string='Keterangan Sabun Lain')

    # Penyakit Saat Ini (Checklist)
    penyakit_dm = fields.Boolean(string='DM')
    penyakit_hipertensi = fields.Boolean(string='Hipertensi')
    penyakit_ggk = fields.Boolean(string='GGK')
    penyakit_sepsis = fields.Boolean(string='Sepsis')
    penyakit_lainnya = fields.Char(string='Penyakit Lainnya')

    # Penyakit Infeksi Lain (Checklist)
    infeksi_kulit = fields.Boolean(string='Infeksi kulit')
    infeksi_mata = fields.Boolean(string='Infeksi mata')
    infeksi_paru = fields.Boolean(string='Infeksi paru')
    infeksi_mulut_gigi = fields.Boolean(string='Infeksi mulut gigi')
    infeksi_gi_tract = fields.Boolean(string='Infeksi GI tract')
    infeksi_tht = fields.Boolean(string='Infeksi THT')
    infeksi_lainnya = fields.Char(string='Infeksi Lainnya')

    # Pencukuran
    waktu_pencukuran = fields.Float(string='Waktu Pencukuran (Jam)', digits=(12, 2))
    metode_pencukuran = fields.Selection([
        ('clipper', 'Clipper'),
        ('silet', 'Silet'),
        ('tidak', 'Tidak')
    ], string='Pencukuran', tracking=True)

    # Profilaksis
    profilaksis_nama = fields.Char(string='Nama Profilaksis')
    profilaksis_jam = fields.Float(string='Jam Diberikan', digits=(12, 2))
    profilaksis_dosis = fields.Char(string='Dosis')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ], default='draft', string='Status', tracking=True)

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancelled'

    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('rm_base_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.rm_base_id.display_name or ''} - Surveilans ILO"
