from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PersetujuanTindakanMedis(models.Model):
    _name = "cdn.persetujuan.tindakan.medis"
    _description = "Persetujuan Tindakan Medis"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin"]

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    nama_penanda_tangan = fields.Char(string="Nama")
    jenis_kelamin_penanda_tangan = fields.Selection(
        [("L", "Laki-laki"), ("P", "Perempuan")], string="L/P", required=True
    )
    tanggal_lahir_penanda_tangan = fields.Date(string="Tanggal Lahir")
    umur_penanda_tangan = fields.Integer(
        string="Umur", compute="_compute_umur_penanda_tangan", store=True
    )
    alamat_ktp_penanda_tangan = fields.Text(string="Alamat sesuai KTP")
    alamat_tinggal_penanda_tangan = fields.Text(string="Alamat Tinggal")
    no_telepon_penanda_tangan = fields.Char(string="No. Telepon")

    hubungan_dengan_pasien = fields.Selection(
        [
            ("diri_sendiri", "Diri Sendiri"),
            ("istri", "Istri"),
            ("suami", "Suami"),
            ("anak", "Anak"),
            ("ayah", "Ayah"),
            ("ibu", "Ibu"),
            ("lainnya", "Lainnya"),
        ],
        string="Hubungan dengan Pasien",
        required=True,
    )

    alamat_tinggal_pasien = fields.Text(string="Alamat Tinggal Pasien")
    no_telepon_pasien = fields.Char(string="No. Telepon Pasien")

    status_pasien = fields.Selection(
        [
            ("umum", "Pasien Umum"),
            ("jkn", "Pasien JKN"),
            ("sktm", "Pasien SKTM"),
            ("asuransi_lain", "Pasien Asuransi Lain"),
        ],
        string="Status Pasien",
        required=False,
    )

    jkn_jenis = fields.Selection(
        [
            ("askes_eks", "Askes Eks"),
            ("jamsostek_tc", "Jamsostek/TC"),
            ("jamkesmas_pbi", "Jamkesmas/PBI"),
            ("tni_polri", "TNI/POLRI"),
            ("bpjs_mandiri", "BPJS Mandiri"),
        ],
        string="Jenis JKN",
    )
    jkn_nomor = fields.Char(string="Nomor JKN")

    sktm_surat_keterangan = fields.Text(string="Surat Keterangan Tidak Mampu")
    asuransi_lain_nama = fields.Char(string="Nama Asuransi Lain")

    ttd_petugas_rumah_sakit = fields.Binary(string="Tanda Tangan Petugas Rumah Sakit")
    ttd_penanda_tangan = fields.Binary(string="Tanda Tangan Penanda Tangan")

    state = fields.Selection(
        [("draft", "Draft"), ("signed", "Ditandatangani"), ("cancelled", "Dibatalkan")],
        string="Status",
        default="draft",
        tracking=True,
    )

    display_name = fields.Char(compute="_compute_display_name", store=True)

    @api.depends("tanggal_lahir_penanda_tangan")
    def _compute_umur_penanda_tangan(self):
        for rec in self:
            if rec.tanggal_lahir_penanda_tangan:
                from datetime import date

                today = date.today()
                birth_date = rec.tanggal_lahir_penanda_tangan
                age = (
                    today.year
                    - birth_date.year
                    - ((today.month, today.day) < (birth_date.month, birth_date.day))
                )
                rec.umur_penanda_tangan = age
            else:
                rec.umur_penanda_tangan = 0

    @api.depends("nama_penanda_tangan", "rm_base_id")
    def _compute_display_name(self):
        for rec in self:

            rec.display_name = (
                f"{rec.nama_penanda_tangan or ''} - {rec.rm_base_id.display_name or ''}"
            )

    @api.constrains(
        "status_pasien",
        "jkn_jenis",
        "jkn_nomor",
        "sktm_surat_keterangan",
        "asuransi_lain_nama",
    )
    def _check_status_pasien_consistency(self):
        for record in self:
            if record.status_pasien == "jkn":
                if not record.jkn_jenis:
                    raise ValidationError(
                        _("Jika status pasien adalah JKN, pilih jenis JKN.")
                    )
                if not record.jkn_nomor:
                    raise ValidationError(
                        _("Nomor JKN wajib diisi jika status pasien adalah JKN.")
                    )
            elif record.status_pasien == "sktm":
                if not record.sktm_surat_keterangan:
                    raise ValidationError(
                        _(
                            "Surat Keterangan Tidak Mampu wajib diisi jika status pasien adalah SKTM."
                        )
                    )
            elif record.status_pasien == "asuransi_lain":
                if not record.asuransi_lain_nama:
                    raise ValidationError(
                        _(
                            "Nama asuransi lain wajib diisi jika status pasien adalah Asuransi Lain."
                        )
                    )
