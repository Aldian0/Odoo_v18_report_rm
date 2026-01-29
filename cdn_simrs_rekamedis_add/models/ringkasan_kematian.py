# cdn_simrs_rekamedis_add/models/ringkasan_kematian.py

from odoo import _, api, fields, models


class RingkasanKematian(models.Model):
    _name = 'cdn.ringkasan.kematian'
    _description = 'Ringkasan Penyebab Kematian'
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
    # PENYEBAB KEMATIAN
    # =========================================
    penyakit_langsung = fields.Text(
        string='a. Penyakit atau keadaan yang langsung mengakibatkan kematian',
        help='  Penyakit atau keadaan yang langsung mengakibatkan kematian',
        tracking=True
    )

    penyakit_lantaran = fields.Text(
        string='b. Penyakit yang menjadi lantaran timbulnya sebab kematian pada (a)',
        help='Penyakit yang menjadi dasar penyebab kematian pada (a)',
        tracking=True
    )

    penyakit_ruang_a = fields.Text(
        string='a. Penyakit dalam ruang (a) disebabkan/diakibatkan oleh (b)',
        help='Penyakit dalam ruang (a) disebabkan oleh penyakit (b)',
        tracking=True
    )

    penyakit_ruang_b = fields.Text(
        string='b. Penyakit dalam ruang (b) disebabkan/diakibatkan oleh (c)',
        help='Penyakit dalam ruang (b) disebabkan oleh penyakit (c)',
        tracking=True
    )

    penyakit_ruang_c = fields.Text(
        string='c. Penyakit dalam ruang (c), jika ada',
        help='Penyakit dalam ruang (c) jika ada',
        tracking=True
    )

    lamanya_sakit_a = fields.Char(
        string='a.',
        help='Durasi sakit untuk penyakit (a)',
        tracking=True
    )

    lamanya_sakit_b = fields.Char(
        string='b.',
        help='Durasi sakit untuk penyakit (b)',
        tracking=True
    )

    lamanya_sakit_c = fields.Char(
        string='c.',
        help='Durasi sakit untuk penyakit (c)',
        tracking=True
    )

    penyakit_lain = fields.Text(
        string='Penyakit lain yang berarti dan berpengaruh pada kematiannya, tetapi bukan penyebab a, b, atau c',
        help='Penyakit lain yang mempengaruhi kematian tetapi bukan penyebab utama',
        tracking=True
    )

    # =========================================
    # KEMATIAN RUDA PAKSA (VIOLENT DEATH)
    # =========================================
    macam_ruda_paksa = fields.Char(
        string='a. Macam ruda paksa',
        help='Jenis kematian ruda paksa',
        tracking=True
    )

    cara_kejadian = fields.Text(
        string='b. Cara kejadian ruda paksa',
        help='Cara terjadinya kematian ruda paksa',
        tracking=True
    )

    kerusakan_tubuh = fields.Text(
        string='c. Kerusakan tubuh',
        help='Deskripsi kerusakan tubuh akibat ruda paksa',
        tracking=True
    )

    jenis_kekerasan = fields.Selection([
        ('bunuh_diri', 'Bunuh diri'),
        ('pembunuhan', 'Pembunuhan'),
        ('kecelakaan', 'Kecelakaan'),
        ('kekerasan', 'Kekerasan'),
    ], string='d. Bunuh diri / pembunuhan / kecelakaan / kekerasan', tracking=True)

    keterangan_tambahan = fields.Text(
        string='e. ',
        help='keterangan tambahan',
        tracking=True
    )

    # =========================================
    # KELAHIRAN MATI (STILLBIRTH)
    # =========================================
    janin_lahir_mati = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='a. Janin lahir mati', tracking=True)

    sebab_kelahiran_mati = fields.Text(
        string='b. Sebab kelahiran mati',
        help='Penyebab kelahiran mati',
        tracking=True
    )

    # =========================================
    # TANDA TANGAN DAN PENGESAHAN
    # =========================================

    nama_pemberi_keterangan = fields.Char(
        string='Nama Pemberi Keterangan Sebab Kematian',
        help='Nama dokter yang memberikan keterangan sebab kematian',
        tracking=True
    )

    tanda_tangan_pemberi_keterangan = fields.Binary(
        string='Tanda Tangan Pemberi Keterangan',
        help='Tanda tangan pemberi keterangan sebab kematian',
    )

    tempat_pengesahan = fields.Char(
        string='Tempat',
        help='Tempat pengesahan',
        tracking=True
    )

    tanggal_pengesahan = fields.Date(
        string='Tanggal',
        default=fields.Date.today(),
        help='Tanggal pengesahan',
        tracking=True
    )