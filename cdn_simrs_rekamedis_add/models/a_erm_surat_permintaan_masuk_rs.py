# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CdnPermintaanMasukRS(models.Model):
    _name = "cdn.permintaan.masuk.rs"
    _description = "Surat Permintaan Masuk Rumah Sakit"
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin'
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base', string='RM', required=True, ondelete='cascade'
    )
    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )

    # Data Pasien & Pengirim


    @api.onchange('pasien_id')
    def _onchange_pasien_id(self):
        if self.pasien_id:
            self.nama_pasien    = self.pasien_id.name
            self.umur_tgl_lahir = f"{self.pasien_id.usia}{self.pasien_id.tanggal_lahir}" if self.pasien_id.tanggal_lahir else ''
            self.no_rm          = self.pasien_id.no_rm
            self.alamat         = self.pasien_id.street
            self.tlp_hp         = self.pasien_id.mobile
            self.no_id_card_ktp = self.pasien_id.nik

    diisi_oleh_dokter = fields.Char(string="Diisi oleh dokter")
    nama_pasien = fields.Char(string="Nama pasien")
    umur_tgl_lahir = fields.Char(string="Umur/Tgl. Lahir")
    no_rm = fields.Char(string="No. RM")
    alamat = fields.Char(string="Alamat")
    tlp_hp = fields.Char(string="Tlp/HP")
    no_id_card_ktp = fields.Char(string="No. ID Card/KTP")
    penjamin_biaya = fields.Selection(
        [("umum", "Umum"), ("bpjs", "BPJS/TC/JKN/In Health"), ("lain", "Lain-lain")],
        string="Penjamin Biaya",
    )
    diagnosa_kerja = fields.Char(string="Diagnosa Kerja")

    # Indikasi Masuk
    indikasi_masuk = fields.Selection(
        [
            ("perbaikan_kondisi", "Perbaikan Kondisi"),
            ("sesak_gizi_buruk", "Sesak atau Gizi Buruk"),
            ("pemberian_injeksi", "Pemberian Injeksi"),
            ("tindakan_medik", "Tindakan Medik"),
            ("operasi_segera", "Operasi Segera"),
            ("lain", "Lainnya"),
        ],
        string="Indikasi Masuk",
    )

    indikasi_lain = fields.Char(string="Keterangan Indikasi Lain-lain")
    keterangan_indikasi = fields.Text(string="Keterangan Indikasi")
    

    # Ruangan yang dituju
    ruangan_dituju  = fields.Char(string="Ruangan yang dituju")
    dpjp            = fields.Char(string="DPJP")
    tlp_hp          = fields.Char(string="Tlp. HP")

    # Tabel Obat yang Sudah Diberikan
    # obat_sudah_diberikan_ids = fields.One2many(
    #     "cdn.permintaan.masuk.rs.obat",
    #     "permintaan_masuk_id",
    #     string="Obat yang Sudah Diberikan",
    # )

    line = fields.One2many(
        "cdn.permintaan.masuk.rs.obat",
        "permintaan_masuk_id",
        string="Obat yang Sudah Diberikan",
    )

    # Tabel Pemeriksaan yang Sudah Ada
    # pemeriksaan_sudah_ada_ids = fields.One2many(
    #     "cdn.permintaan.masuk.rs.pemeriksaan",
    #     "permintaan_masuk_id",
    #     string="Pemeriksaan yang Sudah Ada",
    # )

    # Rencana Tata Laksana Klinis
    rencana_tata_laksana = fields.Text(string="Rencana Tata Laksana Klinis")

    # Tanda tangan
    tempat_tgl = fields.Char(string="Tempat, Tanggal")
    dpjp_signature = fields.Binary(string="Tanda Tangan DPJP")
    pasien_keluarga_signature = fields.Binary(string="Tanda Tangan Pasien/Keluarga")


class ObatSudahDiberikan(models.Model):
    _name = "cdn.permintaan.masuk.rs.obat"
    _description = "Detail Obat yang Sudah Diberikan"

    permintaan_masuk_id = fields.Many2one(
        "cdn.permintaan.masuk.rs", required=True, ondelete="cascade"
    )
    no          = fields.Integer(string="No.")
    keterangan  = fields.Char(string="Keterangan")
    lanjut      = fields.Boolean(string="Lanjut*")
    stop        = fields.Boolean(string="Stop*")

    lab_usg_rongten = fields.Char(string="Lab/USG/Rongten/dll")


class PemeriksaanSudahAda(models.Model):
    _name = "cdn.permintaan.masuk.rs.pemeriksaan"
    _description = "Detail Pemeriksaan yang Sudah Ada"

    permintaan_masuk_id = fields.Many2one(
        "cdn.permintaan.masuk.rs", required=True, ondelete="cascade"
    )
    no = fields.Integer(string="No.")
    lab_usg_rongten = fields.Char(string="Lab/USG/Rongten/dll")
