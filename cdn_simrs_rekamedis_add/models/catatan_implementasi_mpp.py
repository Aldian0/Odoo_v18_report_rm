from odoo import models, fields, api


class CatatanImplementasiMPP(models.Model):
    _name = 'cdn.catatan.implementasi.mpp'
    _description = 'FORM A - Catatan Implementasi MPP'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
    ]
    _order = 'create_date desc'

    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )
    # DATA DASAR
    rm_base_id      = fields.Many2one(
        'cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
     )
    
    ruangan = fields.Char(string='Ruangan')
     
     # Dukungan Keluarga
    dukungan_keluarga = fields.Selection(
        [
            ('handal', 'Handal'),
            ('dipertanyakan', 'Dipertanyakan'),
            ('krisis', 'Krisis'),
            ('tidak ada', 'Tidak ada'),
        ],
        string='Dukungan Keluarga',

    )
    #Financial/Sumber keuangan
    financial = fields.Selection(
        [
            ('Pegawai negeri', 'Pegawai negeri'),
            ('Buruh', 'Buruh'),
            ('Tidak bekerja', 'Tidak bekerja'),
            ('Wiraswasta', 'Wiraswasta'),
            ('Pensiunan', 'Pensiunan'),
            ('Lainnya', 'Lainnya'),
        ],
        string='Financial/Sumber keuangan',

    )
    #Asuransi
    asuransi = fields.Selection(
        [
            ('ada_aktif', 'Ada - Aktif'),
            ('ada_tidak_aktif', 'Ada - Tidak Aktif'),
            ('tidak_ada', 'Tidak ada')
        ],
        string='Asuransi',
    )
    #Riwayat trauma
    trauma = fields.Selection(
        [
            ('Ya', 'Ya'),
            ('Tidak', 'Tidak')
        ],
        string='Riwayat trauma',
    )
    #Pemahaman Kesehatan
    pemahaman_kesehatan = fields.Selection(
        [
            ('paham_patuh', 'Paham dan patuh'),
            ('paham_tidak_patuh', 'Paham dan tidak patuh'),
            ('tidak_paham_patuh', 'Tidak paham dan patuh'),
            ('tidak_paham_tidak_patuh', 'Tidak paham dan tidak patuh')

        ],
        string='Pemahaman Kesehatan',
    )
    mekanisme_koping = fields.Text(string=' Kemampuan Menerima Mekanisme Koping')
    #Aspek legal
    aspek_legal = fields.Selection(
        [
            ('Ya', 'Ada'),
            ('Tidak', 'Tidak Ada')
        ],
        string='Aspek Legal',

    )

    #Identifikasi Masalah
    risiko_asuhan_tidak_sesuai = fields.Boolean(string='Asuhan Pelayanan Tidak Sesuai Kebutuhan')
    risiko_over_under = fields.Boolean(string='Over/Under utilitas pelayanan sesuai standar yang digunakan')
    risiko_ketidakpatuhan_pasien = fields.Boolean(string='Ketidakpatuhan pasien')
    risiko_edukasi_kurang = fields.Boolean(string='Edukasi / Pemahaman kurang memadai terkait proses penyakit')
    risiko_kurang_dukungan_keluarga = fields.Boolean(string='Kurang dukungan keluarga')
    risiko_penurunan_determinasi = fields.Boolean(string='Penurunan determinasi Pasien')
    risiko_kendala_keuangan = fields.Boolean(string='Kendala Keuangan Ketika Komplikasi Meningkat')
    risiko_kendala_pemulangan = fields.Boolean(string='Pemulangan atau rujukann yang belum memenuhi kriteria atau ditunda')
    risiko_lainnya = fields.Text(string='catatan tambahan')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ], default='draft', string='Status', tracking=True)

    # SBAR / Verifikasi
    is_verifikasi               = fields.Boolean(string='SBAR / Verifikasi', default=False)
    qr_ttd_verifikasi_id        = fields.Many2one(comodel_name='cdn.signature', string='TTD SBAR')
    qr_ttd_verifikasi_date      = fields.Date(string='Tanggal TTD SBAR', related='qr_ttd_verifikasi_id.tanggal_tdd', store=True)
    qr_ttd_verifikasi_code      = fields.Binary(string='QR Code TTD SBAR', related='qr_ttd_verifikasi_id.qr_code', store=True)
    qr_ttd_verifikasi_partner_id = fields.Many2one(comodel_name='res.partner', related='qr_ttd_verifikasi_id.partner_id', string='Partner TTD SBAR', store=True)

    # TBAK / Laporan
    is_laporan                  = fields.Boolean(string='TBAK / Laporan', default=False)
    qr_ttd_laporan_id           = fields.Many2one(comodel_name='cdn.signature', string='TTD TBAK')
    qr_ttd_laporan_date         = fields.Date(string='Tanggal TTD TBAK', related='qr_ttd_laporan_id.tanggal_tdd', store=True)
    qr_ttd_laporan_code         = fields.Binary(string='QR Code TTD TBAK', related='qr_ttd_laporan_id.qr_code', store=True)
    qr_ttd_laporan_partner_id   = fields.Many2one(comodel_name='res.partner', related='qr_ttd_laporan_id.partner_id', string='Partner TTD TBAK', store=True)

    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('rm_base_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.rm_base_id.display_name or 'Catatan Implementasi MPP'
    
    

