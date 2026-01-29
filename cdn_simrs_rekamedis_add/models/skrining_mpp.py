from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SkriningMPP(models.Model):
    _name = "cdn.skrining.mpp"
    _description = "Checklist Skrining Pasien untuk Kebutuhan MPP"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    # Kriteria Skrining (Ya/Tidak)
    krt_usia_65 = fields.Boolean(string="Usia ≥ 65 tahun")
    krt_fungsi_kognitif_rendah = fields.Boolean(string="Fungsi kognitif rendah")
    krt_resiko_tinggi = fields.Boolean(string="Resiko tinggi")
    krt_potensi_komplain_tinggi = fields.Boolean(string="Potensi komplain tinggi")
    krt_penyakit_kronis_terminal = fields.Boolean(
        string="Penyakit kronis/katastropik/terminal"
    )
    krt_status_fungsional_adl_tinggi = fields.Boolean(
        string="Status fungsional rendah, kebutuhan ADL tinggi"
    )
    krt_riwayat_gangguan_mental_isu_sosial = fields.Boolean(
        string="Riwayat gangguan mental/isu sosial"
    )
    krt_sering_masuk_igd = fields.Boolean(string="Sering masuk IGD (re-admisi)")
    krt_perkiraan_biaya_asuhan_tinggi = fields.Boolean(
        string="Perkiraan biaya asuhan tinggi"
    )
    krt_lama_rawat_melebihi_rerata = fields.Boolean(
        string="Kasus melebihi rata-rata lama dirawat"
    )
    krt_masalah_pembiayaan = fields.Boolean(
        string="Kemungkinan masalah pembiayaan/kompleks"
    )

    ada_kriteria = fields.Boolean(
        string="Memenuhi Kriteria",
        compute="_compute_ada_kriteria",
        store=True,
    )

    # Pernyataan & TTD PPA
    ppa_nama = fields.Char(string="Nama PPA")
    ppa_ttd = fields.Binary(string="TTD PPA")
    ppa_waktu = fields.Datetime(string="Tgl / Pukul PPA")

    # Keputusan MPP
    keputusan_mpp = fields.Selection(
        [
            ("butuh", "Memerlukan pendampingan MPP"),
            ("tidak", "Tidak memerlukan pendampingan MPP"),
        ],
        string="Keputusan MPP",
        tracking=True,
    )
    mpp_nama = fields.Char(string="Nama MPP")
    mpp_ttd = fields.Binary(string="TTD MPP")
    mpp_waktu = fields.Datetime(string="Tgl / Pukul MPP")

    catatan = fields.Text(string="Catatan")

    display_name = fields.Char(compute="_compute_display_name", store=True)
    state = fields.Selection(
        [("draft", "Draft"), ("done", "Selesai"), ("cancelled", "Dibatalkan")],
        default="draft",
        tracking=True,
    )

    @api.depends(
        "krt_usia_65",
        "krt_fungsi_kognitif_rendah",
        "krt_resiko_tinggi",
        "krt_potensi_komplain_tinggi",
        "krt_penyakit_kronis_terminal",
        "krt_status_fungsional_adl_tinggi",
        "krt_riwayat_gangguan_mental_isu_sosial",
        "krt_sering_masuk_igd",
        "krt_perkiraan_biaya_asuhan_tinggi",
        "krt_lama_rawat_melebihi_rerata",
        "krt_masalah_pembiayaan",
    )
    def _compute_ada_kriteria(self):
        for rec in self:
            rec.ada_kriteria = any(
                [
                    rec.krt_usia_65,
                    rec.krt_fungsi_kognitif_rendah,
                    rec.krt_resiko_tinggi,
                    rec.krt_potensi_komplain_tinggi,
                    rec.krt_penyakit_kronis_terminal,
                    rec.krt_status_fungsional_adl_tinggi,
                    rec.krt_riwayat_gangguan_mental_isu_sosial,
                    rec.krt_sering_masuk_igd,
                    rec.krt_perkiraan_biaya_asuhan_tinggi,
                    rec.krt_lama_rawat_melebihi_rerata,
                    rec.krt_masalah_pembiayaan,
                ]
            )

    @api.depends("rm_base_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.rm_base_id.display_name or _("Skrining MPP")


