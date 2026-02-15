# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DokumentasiInformHecting(models.Model):
    _name = "cdn.dokumentasi.inform.hecting"
    _description = "Dokumentasi Pemberian Informasi dan Tindakan Hecting (Jahit Luka)"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    # ===== INFORMASI PELAKSANA =====
    dokter_pelaksana_tindakan = fields.Char(string="Dokter Pelaksana Tindakan")
    pemberi_informasi = fields.Char(string="Pemberi Informasi")
    penerima_informasi = fields.Char(
        string="Penerima Informasi / Pemberi Persetujuan",
        help="Bila Pasien tidak kompeten menerima informasi, maka penerima informasi adalah wali atau keluarga terdekat",
    )

    # ===== 10 JENIS INFORMASI (dengan default value untuk HECTING) =====
    # 1. Diagnosis (WD dan DD)
    info_diagnosis_terberi = fields.Boolean(string="Diagnosis (WD dan DD)", default=False)
    isi_info_diagnosis = fields.Text(
        string="Isi Informasi Diagnosis",
        default="Vulnus Appertum"
    )

    # 2. Dasar Diagnosis
    info_dasar_diagnosis_terberi = fields.Boolean(
        string="Dasar Diagnosis", default=False
    )
    isi_info_dasar_diagnosis = fields.Text(
        string="Isi Informasi Dasar Diagnosis",
        default="Terdapat luka terbuka di anggota tubuh"
    )

    # 3. Tindakan Kedokteran
    info_tindakan_kedokteran_terberi = fields.Boolean(
        string="Tindakan Kedokteran", default=False
    )
    isi_info_tindakan_kedokteran = fields.Text(
        string="Isi Informasi Tindakan Kedokteran",
        default="Tindakan operasi kecil yang bertujuan menyatukan jaringan yang terputus, meningkatkan proses penyambungan jaringan, serta mencegah luka terbuka yang akan mengakibatkan masuknya mikroorganisme atau infeksi."
    )

    # 4. Indikasi Tindakan
    info_indikasi_tindakan_terberi = fields.Boolean(
        string="Indikasi Tindakan", default=False
    )
    isi_info_indikasi_tindakan = fields.Text(
        string="Isi Informasi Indikasi Tindakan",
        default="Penanganan luka baru yang terbuka sepati luka superfisial, luka yang bersih, ataupun luka operasi"
    )

    # 5. Tata Cara
    info_tata_cara_terberi = fields.Boolean(string="Tata Cara", default=False)
    isi_info_tata_cara = fields.Text(
        string="Isi Informasi Tata Cara",
        default="Jarum ditusukkan pada kulit sisi pertama dengan sudut sekitar 90 derajat masuk ke dalam jaringan subkutan, melewati bagian tengah luka, kemudian ditusukkan lebih lanjut melalui jaringan subkutan di bawah kulit dan menembus kulit pada sisi lainya tersebut."
    )

    # 6. Tujuan
    info_tujuan_terberi = fields.Boolean(string="Tujuan", default=False)
    isi_info_tujuan = fields.Text(
        string="Isi Informasi Tujuan",
        default="Untuk merapatkan luka yang terbuka guna mempercepat proses penyembuhan."
    )

    # 7. Risiko
    info_risiko_terberi = fields.Boolean(string="Risiko", default=False)
    isi_info_risiko = fields.Text(
        string="Isi Informasi Risiko",
        default="Necrotik"
    )

    # 8. Komplikasi
    info_komplikasi_terberi = fields.Boolean(string="Komplikasi", default=False)
    isi_info_komplikasi = fields.Text(
        string="Isi Informasi Komplikasi",
        default="Komplikasi immediate diantaranya adalah terjadinya penibentukan hematoma sekunder akibat teknik hemostasis yang tidak benar atau infeksi pada luka. Komplikasi delayed, atau late complication diantaranya adalah terbentuknya jaringan parut akibat penjahitan yang tidak benar, terjadinya hipertrofi jaringan parut atau keloid pada individu tertentu, tanda bekas jahitan, dan nekrosis ada luka."
    )

    # 9. Prognosis
    info_prognosis_terberi = fields.Boolean(string="Prognosis", default=False)
    isi_info_prognosis = fields.Text(
        string="Isi Informasi Prognosis",
        default="Ad bonam"
    )

    # 10. Alternatif
    info_alternatif_terberi = fields.Boolean(string="Alternatif", default=False)
    isi_info_alternatif = fields.Text(string="Isi Informasi Alternatif")

    # ===== PERNYATAAN DOKTER =====
    nama_dokter_dpjp = fields.Char(string="Nama Dokter DPJP")
    ttd_dpjp = fields.Binary(string="TTD DPJP")
    tgl_pkl_dpjp = fields.Datetime(string="Tgl/Pkl DPJP")

    # ===== PERNYATAAN PASIEN/KELUARGA =====
    nama_penerima_informasi = fields.Char(string="Nama Penerima Informasi")
    tgl_lahir_penerima_informasi = fields.Date(string="Tgl. Lahir Penerima Informasi")
    hubungan_dengan_pasien = fields.Selection(
        [
            ("diri_sendiri", "Diri Sendiri"),
            ("orang_tua", "Orang Tua"),
            ("anak", "Anak"),
            ("istri", "Istri"),
            ("suami", "Suami"),
            ("saudara", "Saudara"),
            ("pengantar", "Pengantar"),
        ],
        string="Hubungan dengan Pasien",
    )
    ttd_pasien_keluarga = fields.Binary(string="TTD Pasien/Keluarga")
    tgl_pkl_pasien_keluarga = fields.Datetime(string="Tgl/Pkl Pasien/Keluarga")
    saksi_pasien_keluarga = fields.Char(string="Saksi")
    tgl_pkl_saksi_pasien_keluarga = fields.Datetime(
        string="Tgl/Pkl Saksi Pasien/Keluarga"
    )

    # ===== PERNYATAAN PERSETUJUAN/PENOLAKAN =====
    jenis_keputusan = fields.Selection(
        [("persetujuan", "Persetujuan"), ("penolakan", "Penolakan")],
        string="Jenis Keputusan",
    )
    tindakan_yang_dilakukan = fields.Text(string="Tindakan yang Dilakukan")
    nama_pasien_keputusan = fields.Char(string="Nama Pasien")
    tgl_lahir_pasien_keputusan = fields.Date(string="Tgl. Lahir Pasien")
    jenis_kelamin_pasien_keputusan = fields.Selection(
        [("L", "Laki-laki"), ("P", "Perempuan")], string="Jenis Kelamin"
    )
    alamat_pasien_keputusan = fields.Text(string="Alamat Pasien")
    ttd_pasien_keluarga_keputusan = fields.Binary(
        string="TTD Pasien/Keluarga (Keputusan)"
    )
    tgl_pkl_pasien_keluarga_keputusan = fields.Datetime(
        string="Tgl/Pkl Pasien/Keluarga (Keputusan)"
    )
    saksi_keputusan = fields.Char(string="Saksi (Keputusan)")
    tgl_pkl_saksi_keputusan = fields.Datetime(string="Tgl/Pkl Saksi (Keputusan)")

    # ===== STATUS =====
    state = fields.Selection(
        [("draft", "Draft"), ("signed", "Ditandatangani"), ("cancelled", "Dibatalkan")],
        string="Status",
        default="draft",
        tracking=True,
    )

    display_name = fields.Char(compute="_compute_display_name", store=True)

    @api.depends("nama_penerima_informasi", "rm_base_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nama_penerima_informasi or ''} - {rec.rm_base_id.display_name or ''}"
            )
