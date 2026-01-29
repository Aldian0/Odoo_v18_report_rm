# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class LaporanHarianRawatInap(models.Model):
    _name = 'cdn.laporan.harian.rawat.inap'
    _description = 'Laporan Harian Rawat Inap'
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

    # === HEADER ===
    tanggal = fields.Date(string='Tanggal', required=True, default=fields.Date.context_today)
    bulan = fields.Integer(string='Bulan', compute='_compute_bulan_tahun', store=True, readonly=False)
    tahun = fields.Integer(string='Tahun', compute='_compute_bulan_tahun', store=True, readonly=False)
    periode_waktu = fields.Char(string='Periode Waktu', default='PUKUL 00.00 s/d 24.00')
    ruangan = fields.Char(string='Ruangan')

    @api.depends('tanggal')
    def _compute_bulan_tahun(self):
        for record in self:
            if record.tanggal:
                # tanggal sudah berupa date object di Odoo
                record.bulan = record.tanggal.month
                record.tahun = record.tanggal.year
            else:
                record.bulan = 0
                record.tahun = 0

    # === PASIEN BARU ===
    pasien_baru_ids = fields.One2many(
        'cdn.laporan.harian.rawat.inap.pasien.baru',
        'laporan_id',
        string='Pasien Baru'
    )

    # === PASIEN KRS/PINDAH RUANG ===
    pasien_krs_pindah_ids = fields.One2many(
        'cdn.laporan.harian.rawat.inap.pasien.krs',
        'laporan_id',
        string='Pasien KRS/Pindah Ruang'
    )

    # === SUMMARY HARIAN ===
    summary_ids = fields.One2many(
        'cdn.laporan.harian.rawat.inap.summary',
        'laporan_id',
        string='Summary Harian'
    )

    # === COMPUTED FIELDS untuk Summary Total (opsional) ===
    total_pasien_awal = fields.Integer(string='Total Pasien Awal', compute='_compute_summary_totals', store=False)
    total_pasien_masuk = fields.Integer(string='Total Pasien Masuk', compute='_compute_summary_totals', store=False)
    total_pasien_masuk_pindahan = fields.Integer(string='Total Pasien Masuk Pindahan', compute='_compute_summary_totals', store=False)
    total_pasien_dipindahkan = fields.Integer(string='Total Pasien Dipindahkan', compute='_compute_summary_totals', store=False)
    total_pasien_keluar_hidup = fields.Integer(string='Total Pasien Keluar Hidup', compute='_compute_summary_totals', store=False)
    total_pasien_keluar_mati_kurang_48 = fields.Integer(string='Total Pasien Keluar Mati < 48 jam', compute='_compute_summary_totals', store=False)
    total_pasien_keluar_mati_lebih_48 = fields.Integer(string='Total Pasien Keluar Mati > 48 jam', compute='_compute_summary_totals', store=False)

    @api.depends('summary_ids')
    def _compute_summary_totals(self):
        for record in self:
            if record.summary_ids:
                record.total_pasien_awal = sum(record.summary_ids.mapped('jumlah_px_awal'))
                record.total_pasien_masuk = sum(record.summary_ids.mapped('jumlah_px_masuk'))
                record.total_pasien_masuk_pindahan = sum(record.summary_ids.mapped('px_masuk_pindahan'))
                record.total_pasien_dipindahkan = sum(record.summary_ids.mapped('px_dipindahkan'))
                record.total_pasien_keluar_hidup = sum(record.summary_ids.mapped('px_keluar_hidup'))
                record.total_pasien_keluar_mati_kurang_48 = sum(record.summary_ids.mapped('px_keluar_mati_kurang_48'))
                record.total_pasien_keluar_mati_lebih_48 = sum(record.summary_ids.mapped('px_keluar_mati_lebih_48'))
            else:
                record.total_pasien_awal = 0
                record.total_pasien_masuk = 0
                record.total_pasien_masuk_pindahan = 0
                record.total_pasien_dipindahkan = 0
                record.total_pasien_keluar_hidup = 0
                record.total_pasien_keluar_mati_kurang_48 = 0
                record.total_pasien_keluar_mati_lebih_48 = 0


class LaporanHarianRawatInapPasienBaru(models.Model):
    _name = 'cdn.laporan.harian.rawat.inap.pasien.baru'
    _description = 'Pasien Baru - Laporan Harian Rawat Inap'
    _order = 'sequence, id'

    laporan_id = fields.Many2one(
        'cdn.laporan.harian.rawat.inap',
        string='Laporan',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(string='Sequence', default=10)

    # === DATA PASIEN BARU ===
    nama_pasien = fields.Char(string='Nama Pasien')
    no_reg = fields.Char(string='No. REG')
    tanggal_lahir = fields.Date(string='Tgl. Lahir')
    jenis_kelamin = fields.Selection([
        ('l', 'L'),
        ('p', 'P')
    ], string='L/P')
    kelas = fields.Char(string='KELAS')
    baru_pindahan = fields.Selection([
        ('baru', 'Baru'),
        ('pindahan', 'Pindahan dari Rawat INAP lain')
    ], string='Baru/Pindahan dari Rawat INAP lain')
    diagnosa = fields.Char(string='DIAGNOSA')
    dpjp = fields.Char(string='DPJP')
    rekanan = fields.Char(string='REKANAN')
    perujuk = fields.Char(string='PERUJUK')


class LaporanHarianRawatInapPasienKrs(models.Model):
    _name = 'cdn.laporan.harian.rawat.inap.pasien.krs'
    _description = 'Pasien KRS/Pindah - Laporan Harian Rawat Inap'
    _order = 'sequence, id'

    laporan_id = fields.Many2one(
        'cdn.laporan.harian.rawat.inap',
        string='Laporan',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(string='Sequence', default=10)

    # === DATA PASIEN KRS/PINDAH ===
    nama_pasien = fields.Char(string='Nama Pasien')
    no_reg = fields.Char(string='No. REG')
    tanggal_lahir = fields.Date(string='Tgl. Lahir')
    jenis_kelamin = fields.Selection([
        ('l', 'L'),
        ('p', 'P')
    ], string='L/P')
    kelas = fields.Char(string='KELAS')
    status_keluar = fields.Selection([
        ('hidup', 'Hidup'),
        ('mati', 'Mati'),
        ('pindah_ruang', 'Pindah Ruang Rawat')
    ], string='Hidup/Mati/Pindah Ruang Rawat')
    keterangan = fields.Text(string='KETERANGAN')


class LaporanHarianRawatInapSummary(models.Model):
    _name = 'cdn.laporan.harian.rawat.inap.summary'
    _description = 'Summary Harian - Laporan Harian Rawat Inap'
    _order = 'tanggal_summary, id'

    laporan_id = fields.Many2one(
        'cdn.laporan.harian.rawat.inap',
        string='Laporan',
        required=True,
        ondelete='cascade'
    )
    tanggal_summary = fields.Date(string='Tanggal Summary', default=fields.Date.context_today)

    # === SUMMARY FIELDS ===
    # Label: a
    jumlah_px_awal = fields.Integer(string='Jumlah Px Awal (a)', default=0)
    
    # Label: b
    jumlah_px_masuk = fields.Integer(string='Jumlah Px Masuk (b)', default=0)
    
    # Label: c
    px_masuk_pindahan = fields.Integer(string='Px Masuk Pindahan (c)', default=0)
    
    # Label: d (computed: a+b+c)
    jumlah_px_total = fields.Integer(
        string='Jumlah Px (a+b+c) (d)',
        compute='_compute_jumlah_px_total',
        store=True
    )
    
    # Label: e
    px_dipindahkan = fields.Integer(string='Px Dipindahkan (e)', default=0)
    
    # Label: f
    px_keluar_hidup = fields.Integer(string='Px Keluar Hidup (f)', default=0)
    
    # Label: g
    px_keluar_mati_kurang_48 = fields.Integer(string='Px Keluar Mati < 48 jam (g)', default=0)
    
    # Label: h
    px_keluar_mati_lebih_48 = fields.Integer(string='Px Keluar Mati > 48 jam (h)', default=0)
    
    # Label: i (computed: g+h)
    jumlah_px_mati_total = fields.Integer(
        string='Jumlah Px Mati (g+h) (i)',
        compute='_compute_jumlah_px_mati_total',
        store=True
    )
    
    # Label: j (computed: e+f+i)
    jumlah_px_krs_total = fields.Integer(
        string='Jumlah Px KRS (e+f+i) (j)',
        compute='_compute_jumlah_px_krs_total',
        store=True
    )
    
    # Label: k (computed: d-j, but formula might be different)
    sisa_px = fields.Integer(
        string='Sisa Px (k)',
        compute='_compute_sisa_px',
        store=True
    )

    @api.depends('jumlah_px_awal', 'jumlah_px_masuk', 'px_masuk_pindahan')
    def _compute_jumlah_px_total(self):
        for record in self:
            record.jumlah_px_total = record.jumlah_px_awal + record.jumlah_px_masuk + record.px_masuk_pindahan

    @api.depends('px_keluar_mati_kurang_48', 'px_keluar_mati_lebih_48')
    def _compute_jumlah_px_mati_total(self):
        for record in self:
            record.jumlah_px_mati_total = record.px_keluar_mati_kurang_48 + record.px_keluar_mati_lebih_48

    @api.depends('px_dipindahkan', 'px_keluar_hidup', 'px_keluar_mati_kurang_48', 'px_keluar_mati_lebih_48', 'jumlah_px_mati_total')
    def _compute_jumlah_px_krs_total(self):
        for record in self:
            # Jumlah Px KRS = e + f + i (dipindahkan + keluar hidup + total mati)
            # i = g + h (sudah dihitung di _compute_jumlah_px_mati_total)
            total_mati = record.px_keluar_mati_kurang_48 + record.px_keluar_mati_lebih_48
            record.jumlah_px_krs_total = record.px_dipindahkan + record.px_keluar_hidup + total_mati

    @api.depends('jumlah_px_total', 'jumlah_px_krs_total')
    def _compute_sisa_px(self):
        for record in self:
            # Sisa = Total Pasien - Pasien Keluar
            # Formula: k = d - j = (a+b+c) - (e+f+i)
            record.sisa_px = record.jumlah_px_total - record.jumlah_px_krs_total

