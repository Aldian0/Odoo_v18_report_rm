
from odoo import _, fields, models

class AsesmenUlangNyeri(models.Model):
    _name = "cdn.asesmen.ulang.nyeri"
    _description = "Asesmen Ulang Nyeri"

    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }

    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

    rm_base_id = fields.Many2one(
        "cdn.erm.base", 
        string="RM",
        required=True,
        ondelete="cascade",
    )

    # Detail Asesmen (One2Many untuk mencatat multiple observations)
    detail_asesmen_ids = fields.One2many(
        "cdn.asesmen.ulang.nyeri.detail",
        "asesmen_id",
        string="Detail Asesmen",
    )

    # Skor Nyeri FLACC / NRS
    skor_nyeri_flacc = fields.Selection([
        ('tidak_ada_nyeri', '0: Tidak ada nyeri'),
        ('nyeri_ringan', '1-3: Nyeri Ringan'),
        ('nyeri_sedang', '4-6: Nyeri Sedang'),
        ('nyeri_berat', '7-10: Nyeri Berat'),
    ], string="Skor Nyeri FLACC/NRS")

    # Skor Sedasi
    skor_sedasi = fields.Selection([
        ('0', '0 - Sedasi Penuh'),
        ('1', '1 - Sedasi Ringan'),
        ('2', '2 - Sedasi Sedang'),
        ('3', '3 - Sedasi Berat'),
        ('S', 'S - Tidur Normal'),
    ], string="Skor Sedasi")

    intervenci_non_farmakologi = fields.Selection(
        string="Intervensi Non-Farmakologi",
        selection=[
            ('1', '1 - Dingin'),
            ('2', '2 - Pijat'),
            ('3', '3 - Posisi'),
            ('4', '4 - Pijat'),
            ('5', '5 - Musik'),
            ('6', '6 - TENS'),
            ('7', '7 - Relaksasi &amp; Pernafasan'),
        ],
    )

    pengkajian_ulang = fields.Selection(
        string="Pengkajian Ulang",
        selection=[
            ('1', '1 - 15 menit setelah intervenci obat injeksi'),
            ('2', '2 - 1 jam setelah obat oral/sublingual'),
            ('3', '3 - 1x/shift bila skor nyeri 1-3'),
            ('4', '4 - Setiap 3 jam bila skor nyeri 4-6'),
            ('5', '5 - Setiap 1 jam bila skor nyeri 7-10'),
            ('6', '6 - Diidentikan bila nyeri 0'),
            ('7', '7 - Sesuai skala nyeri, bila menggunakan gol opioid, perhatikan'),
            ('8', '8 - Skor sedasi diidentikan jika pasien sudah tidak mengguna obat gol opioid dan sedasi'),
        ],
    )
class AsesmenUlangNyeriDetail(models.Model):
    _name = "cdn.asesmen.ulang.nyeri.detail"
    _description = "Detail Asesmen Ulang Nyeri"

    _inherit        = [
        'cdn.signature.library',
        ]

    asesmen_id = fields.Many2one(
        "cdn.asesmen.ulang.nyeri",
        string="Asesmen Ulang Nyeri",
        ondelete="cascade",
    )

    # Tanggal/Waktu
    tanggal_waktu = fields.Datetime(
        string="Tgl/Waktu",
    )

    score_nyeri = fields.Integer( string="Skor Nyeri")


    score_sedasi = fields.Integer( string="Skor")


    # Tekanan Darah Sistolik (mmHg)
    td_sistolik = fields.Integer(
        string="TD",
        help="Tekanan Darah Sistolik (mmHg)"
    )

    # Nadi (x/menit)
    nadi = fields.Integer(
        string="N",
        help="Nadi (x/menit)"
    )

    # Suhu (°C)
    suhu = fields.Float(
        string="S",
        help="Suhu (°C)"
    )

    # Respirasi (x/menit)
    respirasi = fields.Integer(
        string="RR",
        help="Respirasi (x/menit)"
    )

    # Perawan/Bidan Nama
    perawat_bidan_nama = fields.Char(
        string="Perawat/Bidan Nama",
    )

    # Perawan/Bidan Paraf
    perawat_bidan_paraf = fields.Char(
        string="Perawat/Bidan Paraf",
    )

    # Intervensi Farmakologi
    intervensi_farmakologi_tgl = fields.Datetime(
        string="Tgl/Waktu (Farmakologi)",
    )

    intervensi_farmakologi_nama = fields.Char(
        string="Nama Obat",
    )

    intervensi_farmakologi_dosis = fields.Char(
        string="Dosis & Frekuensi",
    )

    intervensi_farmakologi_rute = fields.Char(
        string="Rute",
    )

    # Intervensi Non-Farmakologi
    intervensi_non_farmakologi = fields.Text(
        string="Intervensi Non-Farmakologi",
    )

    # Waktu Kaji Ulang
    waktu_kaji_ulang = fields.Char(
        string="Waktu Kaji Ulang",
    )


    qr_ttd_perawat_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_date         = fields.Date('Date', related='qr_ttd_perawat_id.tanggal_tdd')
    qr_ttd_perawat_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_id.qr_code')
    qr_ttd_perawat_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_id.partner_id', string='Partner')

    qr_ttd_perawat2_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat2_date         = fields.Date('Date', related='qr_ttd_perawat2_id.tanggal_tdd')
    qr_ttd_perawat2_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat2_id.qr_code')
    qr_ttd_perawat2_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat2_id.partner_id', string='Partner')
    
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
    

