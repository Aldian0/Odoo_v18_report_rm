from odoo import _, api, fields, models


class PenjadwalanOperasi(models.Model):
    _name = "cdn.penjadwalan.operasi"
    _description = "Penjadwalan Operasi"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    tanggal_operasi = fields.Date(string="Tanggal Operasi")
    jam_operasi = fields.Char(string="Jam")
    diagnosis_prabedah = fields.Char(string="Diagnosis Prabedah")

    kategori_pembedahan = fields.Selection(
        [("kecil", "Kecil"), ("sedang", "Sedang"), ("besar", "Besar")],
        string="Kategori Pembedahan",
    )
    klasifikasi_pembedahan = fields.Selection(
        [
            ("bersih", "Bersih"),
            ("bersih_kontaminasi", "Bersih-Kontaminasi"),
            ("kontaminasi", "Kontaminasi"),
            ("infeksi", "Infeksi"),
        ],
        string="Klasifikasi Pembedahan",
    )
    jenis_pembedahan = fields.Selection(
        [("elektif", "Elektif"), ("darurat", "Darurat")],
        string="Jenis Pembedahan",
    )
    jenis_anestesi = fields.Selection(
        [("general", "General"), ("regional", "Regional"), ("lokal", "Lokal")],
        string="Jenis Anestesi",
    )
    rencana_tindakan = fields.Text(string="Rencana Tindakan Pembedahan")
    lain_lain = fields.Text(string="Lain-lain (penunjang)")

    # Tanda tangan dan nama
    perawat_poli_ttd = fields.Binary(string="TTD Perawat Poli/Ruangan")
    perawat_poli_nama = fields.Char(string="Nama Perawat Poli/Ruangan")

    dokter_operator_ttd = fields.Binary(string="TTD Dokter Operator")
    dokter_operator_nama = fields.Char(string="Nama Dokter Operator")

    perawat_ok_ttd = fields.Binary(string="TTD Perawat OK")
    perawat_ok_nama = fields.Char(string="Nama Perawat OK")

    pasien_ttd = fields.Binary(string="TTD Pasien")
    pasien_nama = fields.Char(string="Nama Pasien (Penanda Tangan)")

    state = fields.Selection(
        [("draft", "Draft"), ("scheduled", "Dijadwalkan"), ("cancelled", "Dibatalkan")],
        default="draft",
        tracking=True,
    )

    display_name = fields.Char(compute="_compute_display_name", store=True)

    @api.depends("rm_base_id", "tanggal_operasi", "jam_operasi")
    def _compute_display_name(self):
        for rec in self:
            base = rec.rm_base_id.display_name or _("RM")
            when = (rec.tanggal_operasi or "") and str(rec.tanggal_operasi)
            rec.display_name = f"{base} - Jadwal Operasi {when or ''}"


