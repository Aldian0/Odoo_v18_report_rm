# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class IdentifikasiBayi(models.Model):
    _name = "cdn.identifikasi.bayi"
    _description = "Identifikasi Bayi"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    # ===== DATA IDENTITAS BAYI =====
    nama_lengkap_ibu = fields.Char(string="Nama Lengkap Ibu", required=True)
    nama_lengkap_ayah = fields.Char(string="Nama Lengkap Ayah", required=True)
    
    nama_lengkap_bayi = fields.Char(string="Nama Lengkap Bayi", required=True)
    ruang_kelahiran = fields.Char(string="Ruang Kelahiran", required=True)
    
    tanggal_lahir_bayi = fields.Date(string="Tanggal Lahir Bayi", required=True)
    jam_lahir_bayi = fields.Char(string="Jam Lahir Bayi")
    jenis_kelamin_bayi = fields.Selection(
        [("L", "Laki-laki"), ("P", "Perempuan")],
        string="Jenis L/P",
        required=True
    )

    # ===== TANDA TANGAN KAKI BAYI =====
    tanda_tangan_kaki_bayi = fields.Binary(string="Tanda Tangan Kaki Bayi")
    tanda_tangan_kaki_kanan_bayi = fields.Binary(string="Tanda Tangan Kaki Kanan Bayi")

    # ===== DATA BADAN BAYI =====
    berat_badan_bayi = fields.Float(string="Berat Badan", help="dalam gram")
    berat_badan_unit = fields.Selection(
        [("gram", "gram"), ("kg", "kg")],
        string="Satuan Berat",
        default="gram"
    )
    
    panjang_badan_bayi = fields.Float(string="Panjang Badan", help="dalam cm")
    panjang_badan_unit = fields.Selection(
        [("cm", "cm"), ("m", "m")],
        string="Satuan Panjang",
        default="cm"
    )
    
    lingkar_kepala_bayi = fields.Float(string="Lingkar Kepala", help="dalam cm")
    lingkar_kepala_unit = fields.Selection(
        [("cm", "cm"), ("m", "m")],
        string="Satuan Lingkar Kepala",
        default="cm"
    )

    # ===== CATATAN KHUSUS =====
    catatan_khusus_ibu_bayi = fields.Text(
        string="Cap Ibu jari tangan kanan Ibu Bayi",
        help="Tempat untuk mencatat tanda tangan atau cap ibu jari ibu bayi"
    )
    catatan_khusus_kanan_bayi = fields.Text(
        string="Tanda tangan kanan kanan Bayi",
        help="Tempat untuk mencatat tanda tangan kanan bayi"
    )

    # ===== TANDA TANGAN PETUGAS =====
    tanda_tangan_dokter_bidan = fields.Binary(string="Tanda Tangan Dokter/Bidan")
    nama_dokter_bidan = fields.Char(string="Nama Dokter/Bidan")
    
    tanda_tangan_perawat_bidan_ruang = fields.Binary(string="Tanda Tangan Perawat/Bidan Ruang")
    nama_perawat_bidan_ruang = fields.Char(string="Nama Perawat/Bidan Ruang")

    # ===== PERNYATAAN ORANG TUA =====
    pernyataan_orang_tua = fields.Text(
        string="Pernyataan Orang Tua",
        default="Saya menyatakan bahwa pada saat pulang telah menerima Bayi. Saya menerima bayi berikut bayi saya. Saya mengecek pada saat pulang bahwa bayi yang saya terima adalah bayi saya sendiri."
    )

    # ===== TANDA TANGAN ORANG TUA =====
    tanda_tangan_ibu = fields.Binary(string="Tanda Tangan Ibu")
    nama_ibu_penanda_tangan = fields.Char(string="Nama Ibu (Penanda Tangan)")
    
    tanda_tangan_ayah = fields.Binary(string="Tanda Tangan Ayah")
    nama_ayah_penanda_tangan = fields.Char(string="Nama Ayah (Penanda Tangan)")

    # ===== STATUS =====
    state = fields.Selection(
        [("draft", "Draft"), ("signed", "Ditandatangani"), ("cancelled", "Dibatalkan")],
        string="Status",
        default="draft",
        tracking=True,
    )

    display_name = fields.Char(compute="_compute_display_name", store=True)

    @api.depends("nama_lengkap_bayi", "rm_base_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nama_lengkap_bayi or ''} - {rec.rm_base_id.display_name or ''}"
            )

    @api.constrains("tanggal_lahir_bayi")
    def _check_tanggal_lahir_bayi(self):
        for record in self:
            if record.tanggal_lahir_bayi:
                from datetime import date
                if record.tanggal_lahir_bayi > date.today():
                    raise ValidationError(
                        _("Tanggal lahir bayi tidak boleh lebih besar dari hari ini.")
                    )

    @api.constrains("berat_badan_bayi", "panjang_badan_bayi", "lingkar_kepala_bayi")
    def _check_ukuran_bayi(self):
        for record in self:
            if record.berat_badan_bayi and record.berat_badan_bayi < 0:
                raise ValidationError(_("Berat badan bayi tidak boleh negatif."))
            if record.panjang_badan_bayi and record.panjang_badan_bayi < 0:
                raise ValidationError(_("Panjang badan bayi tidak boleh negatif."))
            if record.lingkar_kepala_bayi and record.lingkar_kepala_bayi < 0:
                raise ValidationError(_("Lingkar kepala bayi tidak boleh negatif."))
