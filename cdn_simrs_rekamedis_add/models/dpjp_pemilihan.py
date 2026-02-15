# # from odoo import fields, models, api


# # class DPJPPemilihan(models.Model):
# #     _name = "cdn.dpjp.pemilihan"
# #     _description = "Formulir Keinginan Pasien Memilih DPJP"

# #     _inherits = {
# #         "cdn.erm.base": "rm_base_id",
# #     }

# #     _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

# #     rm_base_id = fields.Many2one(
# #         comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
# #     )

# #     nama_penanda_tangan = fields.Char(string="Nama Penanda Tangan")
# #     hubungan_dengan_pasien = fields.Selection(
# #         [
# #             ("diri_sendiri", "Diri Sendiri"),
# #             ("suami", "Suami"),
# #             ("istri", "Istri"),
# #             ("ayah", "Ayah"),
# #             ("ibu", "Ibu"),
# #             ("anak", "Anak"),
# #             ("kakak", "Kakak"),
# #             ("adik", "Adik"),
# #             ("teman", "Teman"),
# #             ("kerabat", "Kerabat"),
# #         ],
# #         string="Hubungan dengan Pasien",
# #         required=True,
# #     )

# #     nama_pasien = fields.Char(string="Nama Pasien")

# #     nama_dpjp_dipilih = fields.Char(string="Nama DPJP yang Dipilih", required=True)

# #     state = fields.Selection(
# #         [
# #             ("draft", "Draft"),
# #             ("confirmed", "Dikonfirmasi"),
# #             ("signed", "Ditandatangani"),
# #             ("cancelled", "Dibatalkan"),
# #         ],
# #         string="Status",
# #         default="draft",
# #         tracking=True,
# #     )

# #     display_name = fields.Char(compute="_compute_display_name", store=True)

# #     @api.depends("nama_penanda_tangan", "rm_base_id")
# #     def _compute_display_name(self):
# #         for rec in self:
# #             base_name = rec.rm_base_id.display_name or "RM"
# #             rec.display_name = f"{rec.nama_penanda_tangan} - {base_name}"

# #     def action_confirm(self):
# #         self.write({"state": "confirmed"})

# #     def action_sign(self):
# #         self.write({"state": "signed"})

# #     def action_cancel(self):
# #         self.write({"state": "cancelled"})

# #     def action_draft(self):
# #         self.write({"state": "draft"})

# #     @api.model
# #     def create(self, vals):
# #         if vals.get("name", "New") == "New":
# #             vals["name"] = (
# #                 self.env["ir.sequence"].next_by_code("cdn.dpjp.pemilihan") or "New"
# #             )
# #         return super().create(vals)
# from odoo import fields, models, api


# class DPJPPemilihan(models.Model):
#     _name = "cdn.dpjp.pemilihan"
#     _description = "Formulir Keinginan Pasien Memilih DPJP"

#     _inherits = {
#         "cdn.erm.base": "rm_base_id",
#     }

#     _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

#     rm_base_id = fields.Many2one(
#         comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
#     )

#     nama_penanda_tangan = fields.Char(string="Nama Penanda Tangan")
#     hubungan_dengan_pasien = fields.Selection(
#         [
#             ("diri_sendiri", "Diri Sendiri"),
#             ("suami", "Suami"),
#             ("istri", "Istri"),
#             ("ayah", "Ayah"),
#             ("ibu", "Ibu"),
#             ("anak", "Anak"),
#             ("kakak", "Kakak"),
#             ("adik", "Adik"),
#             ("teman", "Teman"),
#             ("kerabat", "Kerabat"),
#         ],
#         string="Hubungan dengan Pasien",
#         required=True,
#     )

#     nama_pasien = fields.Char(string="Nama Pasien")

#     nama_dpjp_dipilih = fields.Char(string="Nama DPJP yang Dipilih", required=True)

#     state = fields.Selection(
#         [
#             ("draft", "Draft"),
#             ("confirmed", "Dikonfirmasi"),
#             ("signed", "Ditandatangani"),
#             ("cancelled", "Dibatalkan"),
#         ],
#         string="Status",
#         default="draft",
#         tracking=True,
#     )

#     display_name = fields.Char(compute="_compute_display_name", store=True)

#     @api.depends("nama_penanda_tangan", "rm_base_id")
#     def _compute_display_name(self):
#         for rec in self:
#             base_name = rec.rm_base_id.display_name or "RM"
#             rec.display_name = f"{rec.nama_penanda_tangan} - {base_name}"

#     def action_confirm(self):
#         self.write({"state": "confirmed"})

#     def action_sign(self):
#         self.write({"state": "signed"})

#     def action_cancel(self):
#         self.write({"state": "cancelled"})

#     def action_draft(self):
#         self.write({"state": "draft"})

#     @api.model
#     def create(self, vals):
#         if vals.get("name", "New") == "New":
#             vals["name"] = (
#                 self.env["ir.sequence"].next_by_code("cdn.dpjp.pemilihan") or "New"
#             )
#         return super().create(vals)
