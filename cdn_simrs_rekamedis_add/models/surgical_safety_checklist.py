from odoo import api, fields, models, _


class SurgicalSafetyChecklist(models.Model):
    _name = 'cdn.surgical.safety.checklist'
    _description = 'Surgical Safety Checklist'
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

    # =========================================
    # IDENTITAS PASIEN
    # =========================================
    nama_pasien = fields.Char(
        string='Nama',
        help='Nama pasien'
    )
    tanggal_lahir = fields.Date(
        string='Tanggal Lahir',
        help='Tanggal lahir pasien'
    )
    no_rm = fields.Char(
        string='No. RM',
        help='Nomor rekam medis'
    )
    ruang = fields.Char(
        string='Ruang',
        help='Ruang/unit rawat pasien'
    )
    tanggal_masuk = fields.Date(
        string='Tgl MRS',
        help='Tanggal masuk rumah sakit'
    )

    # =========================================
    # SIGN IN - Sebelum Anestesi
    # =========================================
    sign_in_verifikasi_identitas = fields.Boolean(string='Verifikasi Identitas')
    sign_in_verifikasi_prosedur = fields.Boolean(string='Verifikasi Prosedur Operasi')
    sign_in_verifikasi_lokasi = fields.Boolean(string='Verifikasi Lokasi Operasi')
    sign_in_puasa = fields.Boolean(string='Status Puasa Dicek')
    sign_in_puasa_catatan = fields.Char(string='Catatan Puasa')
    sign_in_checklist_alat = fields.Text(string='Daftar Peralatan (Sign In)')
    sign_in_kelengkapan_dokumen = fields.Boolean(string='Dokumen Lengkap')
    sign_in_catatan = fields.Text(string='Catatan Sign In')

    # =========================================
    # TIME OUT - Sebelum Insisi
    # =========================================
    timeout_konfirmasi_tim = fields.Boolean(string='Konfirmasi Seluruh Tim')
    timeout_antibiotik_profilaksis = fields.Boolean(string='Antibiotik Profilaksis Diberikan')
    timeout_antibiotik_jam = fields.Datetime(string='Waktu Pemberian Antibiotik')
    timeout_resiko_komplikasi = fields.Text(string='Risiko Komplikasi Khusus')
    timeout_kesiapan_alat = fields.Boolean(string='Kesiapan Peralatan Utama')
    timeout_daftar_instrumen = fields.Text(string='Daftar Instrumen Operasi')
    timeout_lab_penting = fields.Boolean(string='Hasil Lab Penting Dicek')
    timeout_catatan = fields.Text(string='Catatan Time Out')

    # =========================================
    # SIGN OUT - Sebelum Keluar Ruang Operasi
    # =========================================
    signout_perhitungan_instrumen = fields.Boolean(string='Perhitungan Instrument Lengkap')
    signout_daftar_instrumen_kembali = fields.Text(string='Instrumen Kembali (Detail)')
    signout_spesimen_label = fields.Boolean(string='Label Spesimen Lengkap')
    signout_spesimen_ket = fields.Text(string='Keterangan Spesimen')
    signout_ada_masalah = fields.Boolean(string='Ada Masalah Teknis/Klinis?')
    signout_masalah_keterangan = fields.Text(string='Keterangan Masalah')
    signout_rencana_lanjutan = fields.Text(string='Rencana Pasca Operasi')
    signout_catatan = fields.Text(string='Catatan Sign Out')

    # =========================================
    # PETUGAS & TANDA TANGAN
    # =========================================

    # ========= TTD DOKTER BEDAH ==========
    qr_ttd_dokter_bedah_id                        = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_dokter_bedah_date                      = fields.Date('Date', related='qr_ttd_dokter_bedah_id.tanggal_tdd')
    qr_ttd_dokter_bedah_code                      = fields.Binary(string='QR Code', related='qr_ttd_dokter_bedah_id.qr_code')
    qr_ttd_dokter_bedah_partner_id                = fields.Many2one(comodel_name='res.partner',related='qr_ttd_dokter_bedah_id.partner_id', string='Partner')
    
    # ========= TTD DOKTER ANESTESI ==========
    qr_ttd_dokter_anestesi_id                     = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_dokter_anestesi_date                   = fields.Date('Date', related='qr_ttd_dokter_anestesi_id.tanggal_tdd')
    qr_ttd_dokter_anestesi_code                   = fields.Binary(string='QR Code', related='qr_ttd_dokter_anestesi_id.qr_code')
    qr_ttd_dokter_anestesi_partner_id             = fields.Many2one(comodel_name='res.partner',related='qr_ttd_dokter_anestesi_id.partner_id', string='Partner')

    # ========= TTD PERAWAT SIRKULASI SIGN IN ==========
    qr_ttd_perawat_sirkulasi_sign_in_id               = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_sirkulasi_sign_in_date         = fields.Date('Date', related='qr_ttd_perawat_sirkulasi_sign_in_id.tanggal_tdd')
    qr_ttd_perawat_sirkulasi_sign_in_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_sirkulasi_sign_in_id.qr_code')
    qr_ttd_perawat_sirkulasi_sign_in_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_sirkulasi_sign_in_id.partner_id', string='Partner')

    # ========= TTD PERAWAT SIRKULASI TIME OUT ==========
    qr_ttd_perawat_sirkulasi_time_out_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_sirkulasi_time_out_date         = fields.Date('Date', related='qr_ttd_perawat_sirkulasi_time_out_id.tanggal_tdd')
    qr_ttd_perawat_sirkulasi_time_out_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_sirkulasi_time_out_id.qr_code')
    qr_ttd_perawat_sirkulasi_time_out_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_sirkulasi_time_out_id.partner_id', string='Partner')

    # ========= TTD PERAWAT SIRKULASI SIGN OUT ==========
    qr_ttd_perawat_sirkulasi_sign_out_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_sirkulasi_sign_out_date         = fields.Date('Date', related='qr_ttd_perawat_sirkulasi_sign_out_id.tanggal_tdd')
    qr_ttd_perawat_sirkulasi_sign_out_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_sirkulasi_sign_out_id.qr_code')
    qr_ttd_perawat_sirkulasi_sign_out_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_sirkulasi_sign_out_id.partner_id', string='Partner')

    # =========================================
    # LOG WAKTU
    # =========================================
    sign_in_time = fields.Datetime(string='Waktu Sign In')
    time_out_time = fields.Datetime(string='Waktu Time Out')
    sign_out_time = fields.Datetime(string='Waktu Sign Out')

    # =========================================
    # STATUS & TRACKING
    # =========================================
    status_checklist = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'Dalam Proses'),
        ('done', 'Selesai'),
    ], default='draft', string='Status', tracking=True, compute='_compute_check_complete', store=True)

    @api.depends('sign_in_verifikasi_identitas', 'timeout_konfirmasi_tim', 'signout_perhitungan_instrumen')
    def _compute_check_complete(self):
        """Logika untuk status otomatis berdasarkan checklist"""
        for rec in self:
            if rec.sign_in_verifikasi_identitas and rec.timeout_konfirmasi_tim and rec.signout_perhitungan_instrumen:
                rec.status_checklist = 'done'
            else:
                rec.status_checklist = 'in_progress'
