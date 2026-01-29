# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AsesmenPraBedah(models.Model):
    _name = "cdn.asesmen.pra.bedah"
    _description = "Asesmen Pra Bedah"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin", "cdn.report.mailmerge"]

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    # ===== DATA PASIEN =====
    nama_pasien = fields.Char(string="Nama", required=True)
    tanggal_lahir = fields.Date(string="Tanggal lahir")
    jenis_kelamin = fields.Selection(
        [("L", "Laki-laki"), ("P", "Perempuan")],
        string="L/P"
    )
    no_rm = fields.Char(string="No. RM")
    tanggal_asesmen = fields.Date(string="Tanggal Asesmen", default=fields.Date.today)
    jam_asesmen = fields.Char(string="Jam Asesmen")

    # ===== 1. ANAMNESIS =====
    anamnesis = fields.Text(string="1. Anamnesis")

    # ===== 2. PEMERIKSAAN FISIK =====
    pemeriksaan_fisik = fields.Text(string="2. Pemeriksaan Fisik")

    # ===== 3. PEMERIKSAAN PENUNJANG =====
    pemeriksaan_penunjang_laboratorium = fields.Text(
        string="3.a. Laboratorium"
    )
    pemeriksaan_penunjang_usg = fields.Text(
        string="3.b. USG"
    )
    pemeriksaan_penunjang_ct_scan = fields.Text(
        string="3.c. CT Scan/ MRI /MRCP/ Rontgen"
    )
    pemeriksaan_penunjang_lain_lain = fields.Text(
        string="3.d. Lain-lain"
    )

    # ===== 4. DIAGNOSIS PRA BEDAH =====
    diagnosis_pra_bedah = fields.Text(string="4. Diagnosis Pra Bedah", required=True)

    # ===== 5. RENCANA OPERASI =====
    rencana_operasi_tindakan_prosedur = fields.Text(
        string="5.a. Tindakan /Prosedur"
    )
    rencana_operasi_waktu_tempat = fields.Text(
        string="5.b. Waktu dan tempat"
    )

    # ===== 6. ALTERNATIF =====
    alternatif = fields.Text(string="6. Alternatif")

    # ===== 7. RISIKO DAN RENCANA PROSEDUR OPERASI =====
    risiko_rencana_prosedur = fields.Text(
        string="7. Risiko dan Rencana Prosedur Operasi"
    )

    # ===== 8. POTENSI KOMPLIKASI =====
    potensi_komplikasi = fields.Text(string="8. Potensi Komplikasi")

    # ===== 9. KEUNTUNGAN DARI PROSEDUR OPERASI INI =====
    keuntungan_prosedur = fields.Text(
        string="9. Keuntungan dari Prosedur Operasi ini"
    )

    # ===== 10. TRANSFUSI (OPTIONAL) =====
    transfusi = fields.Text(string="10. Transfusi (Optional)")

    # ===== 11. CATATAN =====
    catatan_telah_dijelaskan_kepada = fields.Selection(
        [("pasien", "Pasien"), ("wali_keluarga", "Wali/Keluarga"), ("keduanya", "Keduanya")],
        string="11.a. Telah dijelaskan kepada"
    )
    catatan_sebagai = fields.Selection(
        [("pasien", "Pasien"), ("wali", "Wali/Keluarga"), ("kuasa", "Kuasa")],
        string="11.b. Sebagai (Pasien/Wali/Kuasa)"
    )
    catatan_tentang_diagnosis = fields.Text(
        string="11.c. Tentang diagnosis, rencana operasi, risiko dan keuntungan prosedur operasi"
    )
    catatan_keuangan_prosedur = fields.Text(
        string="11.d. Tentang keuangan prosedur operasi"
    )

    # ===== TANDA TANGAN =====
    tanda_tangan_dokter_operasi = fields.Binary(string="Tanda Tangan Dokter Operasi")
    nama_dokter_operasi = fields.Char(string="Nama Dokter Operasi")

    # ===== STATUS =====
    state = fields.Selection(
        [("draft", "Draft"), ("signed", "Ditandatangani"), ("cancelled", "Dibatalkan")],
        string="Status",
        default="draft",
        tracking=True,
    )

    display_name = fields.Char(compute="_compute_display_name", store=True)

    # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.asesmen.pra.bedah/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {
            'nama_pasien'                           : self.nama_pasien or '',
            'tanggal_lahir'                         : self.tanggal_lahir.strftime('%d/%m/%Y') if self.tanggal_lahir else '',
            'jenis_kelamin'                         : self._get_selection_value(model='cdn.asesmen.pra.bedah', field='jenis_kelamin', value=self.jenis_kelamin),
            'no_rm'                                 : self.no_rm or '',
            'tanggal_asesmen'                       : self.tanggal_asesmen.strftime('%d/%m/%Y') if self.tanggal_asesmen else '',
            'jam_asesmen'                           : self.jam_asesmen or '',
            'anamnesis'                             : self.anamnesis or '',
            'pemeriksaan_fisik'                     : self.pemeriksaan_fisik or '',
            'pemeriksaan_penunjang_laboratorium'    : self.pemeriksaan_penunjang_laboratorium or '',
            'pemeriksaan_penunjang_usg'             : self.pemeriksaan_penunjang_usg or '',
            'pemeriksaan_penunjang_ct_scan'         : self.pemeriksaan_penunjang_ct_scan or '',
            'pemeriksaan_penunjang_lain_lain'       : self.pemeriksaan_penunjang_lain_lain or '',
            'diagnosis_pra_bedah'                   : self.diagnosis_pra_bedah or '',
            'rencana_operasi_tindakan_prosedur'     : self.rencana_operasi_tindakan_prosedur or '',
            'rencana_operasi_waktu_tempat'          : self.rencana_operasi_waktu_tempat or '',
            'alternatif'                            : self.alternatif or '',
            'risiko_rencana_prosedur'               : self.risiko_rencana_prosedur or '',
            'potensi_komplikasi'                    : self.potensi_komplikasi or '',
            'keuntungan_prosedur'                   : self.keuntungan_prosedur or '',
            'transfusi'                             : self.transfusi or '',
            'catatan_telah_dijelaskan_kepada'       : self._get_selection_value(model='cdn.asesmen.pra.bedah', field='catatan_telah_dijelaskan_kepada', value=self.catatan_telah_dijelaskan_kepada),
            'catatan_sebagai'                       : self._get_selection_value(model='cdn.asesmen.pra.bedah', field='catatan_sebagai', value=self.catatan_sebagai),
            'catatan_tentang_diagnosis'             : self.catatan_tentang_diagnosis or '',
            'catatan_keuangan_prosedur'             : self.catatan_keuangan_prosedur or '',
            'nama_dokter_operasi'                   : self.nama_dokter_operasi or '',
        }
        template = 'cdn_simrs_rekamedis_add/template/Asesmen_pra_bedah.docx'
        return self._mail_merge_to_pdf(
            path        = template,
            data_info   = data_field,
            image_info  = [],
            list_info   = []
        )

    @api.depends("nama_pasien", "rm_base_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nama_pasien or ''} - {rec.rm_base_id.display_name or ''}"
            )

    @api.constrains("tanggal_lahir")
    def _check_tanggal_lahir(self):
        for record in self:
            if record.tanggal_lahir:
                from datetime import date
                if record.tanggal_lahir > date.today():
                    raise ValidationError(
                        _("Tanggal lahir tidak boleh lebih besar dari hari ini.")
                    )

    @api.constrains("diagnosis_pra_bedah")
    def _check_diagnosis_pra_bedah(self):
        for record in self:
            if not record.diagnosis_pra_bedah:
                raise ValidationError(
                    _("Diagnosis Pra Bedah wajib diisi.")
                )
