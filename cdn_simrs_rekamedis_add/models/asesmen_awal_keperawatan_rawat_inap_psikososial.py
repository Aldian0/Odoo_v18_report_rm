# cdn_simrs_rekamedis_add/models/asesmen_awal_keperawatan_rawat_inap_psikososial.py

from odoo import _, api, fields, models


class AsesmenAwalKeperawatanRawatInapPsikososial(models.Model):
    _name = "cdn.asesmen.awal.keperawatan.rawat.inap.psikososial"
    _description = "Asesmen Awal Keperawatan Rawat Inap - Psikososial & Komunikasi"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    # === PSIKOSOSIAL, SOSIAL, SPIRITUAL ===
    # Status Psikologis
    status_psikologis = fields.Selection(
        [
            ("tenang", "Tenang"),
            ("cemas", "Cemas"),
            ("takut", "Takut"),
            ("marah", "Marah"),
            ("sedih", "Sedih"),
            ("kecenderungan_bunuh_diri", "Kecenderungan bunuh diri"),
            ("lainnya", "Lainnya"),
        ],
        string="Status Psikologis", tracking=True,
    )
    status_psikologis_lainnya = fields.Char(string="Sebutkan lainnya", tracking=True)

    # Status Mental
    status_mental = fields.Selection(
        [
            ("sadar_orientasi_baik", "Sadar dan Orientasi baik"),
            ("ada_masalah_perilaku", "Ada masalah perilaku"),
            ("perilaku_kekerasan", "Perilaku kekerasan yang dialami pasien sebelumnya"),
        ],
        string="Status Mental", tracking=True,
    )
    status_mental_masalah_perilaku = fields.Text(string="Sebutkan masalah perilaku", tracking=True)
    status_mental_perilaku_kekerasan = fields.Text(string="Sebutkan perilaku kekerasan", tracking=True)

    # Pekerjaan pasien
    pekerjaan_pasien = fields.Char(string="Pekerjaan pasien", tracking=True)

    # Kebutuhan pelayanan kerohanian
    kebutuhan_kerohanian = fields.Selection(
        [
            ("tidak", "Tidak"),
            ("ya", "Ya"),
        ],
        string="Kebutuhan pelayanan kerohanian", tracking=True,
    )
    kebutuhan_kerohanian_detail = fields.Char(string="Detail kebutuhan kerohanian", tracking=True)

    # Status pernikahan
    status_pernikahan = fields.Selection(
        [
            ("belum_menikah", "Belum Menikah"),
            ("sudah_menikah", "Sudah Menikah"),
            ("single_parent", "Single Parent"),
            ("lainnya", "Lainnya"),
        ],
        string="Status pernikahan", tracking=True,
    )
    status_pernikahan_lainnya_sebutkan = fields.Char(string="Sebutkan lainnya", tracking=True)

    # Tinggal Bersama
    tinggal_bersama = fields.Selection(
        [
            ("keluarga_inti", "Keluarga Inti"),
            ("orang_tua", "Orang Tua"),
            ("teman", "Teman"),
            ("sendiri", "Sendiri"),
            ("lainnya", "Lainnya"),
        ],
        string="Tinggal Bersama", tracking=True,
    )
    tinggal_bersama_lainnya_sebutkan = fields.Char(string="Sebutkan lainnya", tracking=True)

    # Orang yang membantu perawatan di rumah
    orang_membantu_perawatan = fields.Char(
        string="Orang yang membantu perawatan di rumah", tracking=True
    )

    # Bentuk bantuan di rumah yang diperlukan
    bentuk_bantuan_rumah = fields.Text(string="Bentuk bantuan di rumah yang diperlukan", tracking=True)

    # Ketersediaan dilibatkan dalam kegiatan Rumah Sakit
    ketersediaan_kegiatan_rs = fields.Selection(
        [
            ("ya", "Ya"),
            ("tidak", "Tidak"),
        ],
        string="Ketersediaan dilibatkan dalam kegiatan Rumah Sakit", tracking=True,
    )

    # === KOMUNIKASI - EDUKASI ===
    # Pendidikan
    pendidikan = fields.Selection(
        [
            ("tidak_sekolah", "Tidak Sekolah"),
            ("sd", "SD"),
            ("smp", "SMP"),
            ("sma", "SMA"),
            ("diploma", "Diploma"),
            ("perguruan_tinggi", "Perguruan Tinggi"),
        ],
        string="Pendidikan", tracking=True,
    )

    # Suku
    suku = fields.Char(string="Suku", tracking=True)

    # Bahasa yang digunakan sehari-hari
    bahasa_sehari_hari = fields.Char(string="Bahasa yang digunakan sehari – hari")

    # Kebutuhan penerjemah
    kebutuhan_penerjemah = fields.Selection(
        [
            ("ya", "Ya"),
            ("tidak", "Tidak"),
        ],
        string="Kebutuhan penerjemah", tracking=True,
    )

    # Nilai Keyakinan / Kepercayaan
    keyakinan_tidak_dirawat_lawan_jenis = fields.Boolean(
        string="Tidak dirawat oleh petugas lawan jenis", tracking=True,
    )
    keyakinan_tidak_konsumsi_babi = fields.Boolean(
        string="Tidak mengkonsumsi daging babi dan derivatnya", tracking=True,
    )
    keyakinan_tidak_pulang_hari_tertentu = fields.Boolean(
        string="Tidak pulang dihari tertentu", tracking=True,
    )
    keyakinan_tidak_mau_transfusi = fields.Boolean(
        string="Tidak mau dilakukan transfusi", tracking=True,
    )
    keyakinan_vegetarian = fields.Boolean(string="Vegetarian", tracking=True)
    keyakinan_tidak_dirawat_kamar_tertentu = fields.Boolean(
        string="Tidak dirawat di kamar dengan nomor tertentu", tracking=True,
    )
    keyakinan_lainnya = fields.Boolean(string="Lainnya", tracking=True)
    keyakinan_lainnya_sebutkan = fields.Char(string="Sebutkan lainnya", tracking=True)

    # Hambatan - Emosional
    hambatan_emosional = fields.Selection(
        [
            ("depresi", "Depresi"),
            ("pemarah", "Pemarah"),
            ("lainnya", "Lainnya"),
        ],
        string="Hambatan - Emosional", tracking=True,
    )
    hambatan_emosional_lainnya_sebutkan = fields.Char(string="Sebutkan lainnya", tracking=True)

    # Hambatan - Bahasa
    hambatan_bahasa = fields.Selection(
        [
            ("tidak", "Tidak"),
            ("ya", "Ya"),
        ],
        string="Hambatan - Bahasa", tracking=True,
    )
    hambatan_bahasa_detail = fields.Char(string="Detail hambatan bahasa", tracking=True)

    # Hambatan - Keterbatasan Fisik
    hambatan_fisik_tidak_ada = fields.Boolean(string="Tidak ada", tracking=True)
    hambatan_fisik_visual = fields.Boolean(string="Visual", tracking=True)
    hambatan_fisik_pendengaran = fields.Boolean(string="Pendengaran", tracking=True)
    hambatan_fisik_gangguan_bicara = fields.Boolean(string="Gangguan bicara", tracking=True)
    hambatan_fisik_kognitif = fields.Boolean(string="Kognitif", tracking=True)

    # Motivasi
    motivasi = fields.Selection(
        [
            ("baik", "Baik"),
            ("kurang", "Kurang"),
        ],
        string="Motivasi", tracking=True,
    )

    # Ketersediaan menerima informasi / edukasi
    ketersediaan_edukasi = fields.Selection(
        [
            ("bersedia", "Bersedia"),
            ("tidak_bersedia", "Tidak bersedia"),
        ],
        string="Ketersediaan menerima informasi / edukasi", tracking=True,
    )

    # Kebutuhan edukasi di rumah sakit / di rumah
    kebutuhan_edukasi_obat = fields.Boolean(
        string="Penggunaan obat-obatan secara efektif dan aman", tracking=True,
    )
    kebutuhan_edukasi_penyakit = fields.Boolean(string="Penyakit", tracking=True)
    kebutuhan_edukasi_peralatan_medis = fields.Boolean(
        string="Penggunaan peralatan medis secara efektif dan aman", tracking=True,
    )
    kebutuhan_edukasi_diet_nutrisi = fields.Boolean(string="Diet dan Nutrisi", tracking=True)
    kebutuhan_edukasi_manajemen_nyeri = fields.Boolean(string="Manajemen nyeri", tracking=True)
    kebutuhan_edukasi_cuci_tangan = fields.Boolean(string="Cuci tangan", tracking=True)
    kebutuhan_edukasi_risiko_jatuh = fields.Boolean(string="Risiko jatuh", tracking=True)
    kebutuhan_edukasi_lainnya = fields.Boolean(string="Lainnya", tracking=True)
    kebutuhan_edukasi_lainnya_sebutkan = fields.Char(string="Sebutkan lainnya", tracking=True)
