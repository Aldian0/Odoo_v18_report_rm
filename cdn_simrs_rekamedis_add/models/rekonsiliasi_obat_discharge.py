# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class RekonsiliasiObatDischarge(models.Model):
    _name = "cdn.rekonsiliasi.obat.discharge"
    _description = "Rekonsiliasi Obat Saat Discharge"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nama pasien", required=True, tracking=True)
    nama_pasien = fields.Char(string="Nama pasien")
    tanggal_lahir = fields.Date(string="Tanggal lahir")
    no_rm = fields.Char(string="No. RM")

    tanggal_jam = fields.Datetime(
        string="Tanggal/Jam", default=fields.Datetime.now, tracking=True
    )
    apoteker_nama = fields.Char(string="Apoteker Yang Melakukan Rekonsiliasi Obat")

    line_ids = fields.One2many(
        comodel_name="cdn.rekonsiliasi.obat.discharge.line",
        inverse_name="discharge_id",
        string="Daftar Obat",
        copy=True,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Selesai"),
            ("cancelled", "Dibatalkan"),
        ],
        default="draft",
        tracking=True,
    )

    @api.depends("name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.name or _("Rekonsiliasi Obat Discharge")

    def action_done(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError(
                    _("Tambahkan setidaknya satu baris obat sebelum menyelesaikan.")
                )
            rec.state = "done"
        return True

    def action_draft(self):
        self.write({"state": "draft"})
        return True

    def action_cancel(self):
        self.write({"state": "cancelled"})
        return True


class RekonsiliasiObatDischargeLine(models.Model):
    _name = "cdn.rekonsiliasi.obat.discharge.line"
    _description = "Baris Rekonsiliasi Obat Saat Discharge"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    discharge_id = fields.Many2one(
        comodel_name="cdn.rekonsiliasi.obat.discharge",
        string="Dokumen",
        required=True,
        ondelete="cascade",
    )

    nama_obat = fields.Char(string="Nama Obat", required=True)
    dosis = fields.Char(string="Dosis")
    frekuensi = fields.Char(string="Frekuensi")
    cara_pemberian = fields.Char(string="Cara Pemberian")

    tindak_lanjut = fields.Selection(
        [
            ("lanjut_sama", "Lanjut aturan pakai sama"),
            ("lanjut_berubah", "Lanjut aturan pakai berubah"),
            ("stop", "Stop"),
            ("obat_baru", "Obat Baru"),
        ],
        string="Tindak Lanjut Oleh DPJP",
    )
    perubahan_aturan_pakai = fields.Char(string="Perubahan Aturan Pakai")
