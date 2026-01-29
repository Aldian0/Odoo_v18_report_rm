# cdn_simrs_rekamedis_add/models/rekonsiliasi_obat_transfer.py

from odoo import _, api, fields, models


class RekonsiliasiObatTransfer(models.Model):
    _name = "cdn.rekonsiliasi.obat.transfer"
    _description = "Formulir Rekonsiliasi Obat Saat Transfer"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    state = fields.Selection(
        [("draft", "Draft"), ("done", "Selesai"), ("cancelled", "Dibatalkan")],
        string="Status",
        default="draft",
        tracking=True,
    )

    nama_pasien = fields.Char(string="Nama Pasien", required=True)
    tanggal_lahir = fields.Date(string="Tanggal Lahir")
    no_rm = fields.Char(string="No. RM")

    obat_lines = fields.One2many(
        "cdn.rekonsiliasi.obat.transfer.line",
        "rekonsiliasi_id",
        string="Obat yang Sedang Digunakan",
    )

    tanggal_jam = fields.Datetime(string="Tanggal/Jam", default=fields.Datetime.now)
    apoteker_nama = fields.Char(string="Apoteker Yang Melakukan Rekonsiliasi Obat")

    def action_draft(self):
        self.write({"state": "draft"})

    def action_done(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancelled"})


class RekonsiliasiObatTransferLine(models.Model):
    _name = "cdn.rekonsiliasi.obat.transfer.line"
    _description = "Baris Obat dalam Rekonsiliasi Obat"
    _order = "sequence"

    rekonsiliasi_id = fields.Many2one(
        "cdn.rekonsiliasi.obat.transfer", required=True, ondelete="cascade"
    )
    sequence = fields.Integer(string="Urutan", default=10)

    nama_obat = fields.Char("Nama Obat", required=True)
    dosis = fields.Char("Dosis")
    frekuensi = fields.Char("Frekuensi")
    cara_pemberian = fields.Char("Cara Pemberian")
    tindak_lanjut = fields.Selection(
        [
            ("lanjut_sama", "Lanjut aturan pakai sama"),
            ("lanjut_berubah", "Lanjut aturan pakai berubah"),
            ("stop", "Stop"),
        ],
        string="Tindak Lanjut",
    )
    perubahan_aturan_pakai = fields.Text("Perubahan Aturan Pakai")
