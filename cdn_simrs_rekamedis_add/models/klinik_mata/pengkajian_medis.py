# cdn_simrs_rekamedis_add/models/pengkajian_medis.py

from odoo import _, api, fields, models

from odoo.exceptions import UserError, ValidationError





class CdnErmCppt(models.Model):
    _inherit = 'cdn.erm.cppt'
    # def 
    refrensi_pengkajian_medis_id    = fields.Many2one('cdn.pengkajian.medis', string='Refrensi Pengkajian Medis', tracking=True)
    assesment_awal_id               = fields.Many2one('cdn.asesmen.awal.rawat.jalan', string='Refrensi Asesmen Awal Rawat Jalan', tracking=True)
    @api.onchange(
        'registrasi_id',
        'systolic_bp', 'diastolic_bp', 'hr', 'rr',
        'weight', 'height', 'spo2', 'temp',
        'kesadaran', 'gcs_score', 'tingkat_kesadaran',
    )
    def _onchange_soap(self):

        Pengkajian = self.env['cdn.pengkajian.medis'].sudo()
        Cppt = self.env['cdn.erm.cppt'].sudo()
        Assesment_awal = self.env['cdn.asesmen.awal.rawat.jalan'].sudo()

        for rec in self:
            soap_base = rec.soap or ''

            pengkajian = Pengkajian.search(
                [('pasien_id', '=', rec.pasien_id.id)],
                limit=1, order='id desc'
            )

            cppt = Cppt.search(
                [('registrasi_id', '=', rec.registrasi_id.id)],
                limit=1, order='id desc'
            )

            # =====================================
            # 1️⃣ TENTUKAN SOAP DASAR
            # =====================================
            assesment_awal = Assesment_awal.search(
                [('pasien_id', '=', rec.pasien_id.id)],
                limit=1, order='id desc'
            )

            if assesment_awal:
                self._set_if_empty('weight', assesment_awal.weight)
                self._set_if_empty('height', assesment_awal.height or assesment_awal.weight)

                self._set_if_empty('systolic_bp', assesment_awal.systolic_bp)
                self._set_if_empty('diastolic_bp', assesment_awal.diastolic_bp)
                self._set_if_empty('hr', assesment_awal.hr)
                self._set_if_empty('rr', assesment_awal.rr)
                self._set_if_empty('spo2', assesment_awal.spo2)
                self._set_if_empty('temp', assesment_awal.temp)

                self._set_if_empty('gcs_eye', assesment_awal.gcs_eye)
                self._set_if_empty('gcs_motor', assesment_awal.gcs_motor)
                self._set_if_empty('gcs_verbal', assesment_awal.gcs_verbal)

                self._set_if_empty('tingkat_kesadaran', assesment_awal.tingkat_kesadaran)
                self._set_if_empty('kesadaran', assesment_awal.kesadaran)
                self._set_if_empty('gcs_score', assesment_awal.gcs_score)



                self.assesment_awal_id = assesment_awal.id


            if pengkajian:
                rec.refrensi_pengkajian_medis_id = pengkajian.id

                soap_base = (
                    "S :\n..................\n\n"
                    "O :\n"
                    f"{pengkajian._get_data_objektive_for_cppt()}\n\n"
                    "A :\n..................\n\n"
                    "P :\n.................."
                )

            elif cppt:
                rec.refrensi_cppt_id = cppt.id
                soap_base = cppt.soap

            # =====================================
            # 2️⃣ LANJUTKAN LOGIC SOAP LAMA
            #    (TTV, dll)
            # =====================================
            rec.soap = soap_base

            # Panggil logic onchange SOAP sebelumnya
            super(CdnErmCppt, rec)._onchange_soap()

#     @api.onchange(
#         'registrasi_id',
#         'systolic_bp', 'diastolic_bp', 'hr', 'rr', 'weight', 'height',
#         'spo2', 'temp', 'kesadaran', 'gcs_score', 'tingkat_kesadaran',

#     )
#     def _onchange_soap(self):
#         pengkajian_medis_id = self.env['cdn.pengkajian.medis'].sudo().search([('pasien_id', '=', self.pasien_id.id)], limit=1, order='id desc')
#         cppt_id = self.env['cdn.erm.cppt'].sudo().search([('registrasi_id', '=', self.registrasi_id.id)], limit=1, order='id desc')
#         if pengkajian_medis_id:
#             # self.refrensi_cppt_id   = cppt_id.id
#             self.refrensi_pengkajian_medis_id = pengkajian_medis_id.id
#             # self.soap               = pengkajian_medis_id.soap
#             soap = f"""
# S : 
# .................
# O : 
# {pengkajian_medis_id._get_data_objektive_for_cppt()}
# A : 
# .................
# P : 
# .................
# """
#             self.soap = soap
#         elif cppt_id:
#             self.refrensi_cppt_id   = cppt_id.id
#             self.soap = cppt_id.soap
#         else:
#             super(CdnErmCppt, self)._onchange_soap()
        

    

class PengkajianMedis(models.Model):
    _name = 'cdn.pengkajian.medis'
    _description = 'Pengkajian Medis'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
    )
    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )
    def _get_data_objektive_for_cppt(self):
        def val(v):
            return v if v not in (False, None, "") else None

        lines = []

        def add_title(title):
            if lines:
                lines.append(title)
            else:
                lines.append(title)

        def add_line(text):
            lines.append(text)

        # ================= PD =================
        if val(self.txt_pd):
            add_line(f"PD : {self.txt_pd}")

        # ================= REFRAKSI =================
        refraksi = []
        if any(val(x) for x in [
            self.s_refraksi_od, self.c_refraksi_od, self.a_refraksi_od, self.v_refraksi_od
        ]):
            refraksi.append(
                f"    OD : S:{val(self.s_refraksi_od) or '-'} "
                f"C:{val(self.c_refraksi_od) or '-'} "
                f"A:{val(self.a_refraksi_od) or '-'} "
                f"Visus:{val(self.v_refraksi_od) or '-'}"
            )

        if any(val(x) for x in [
            self.s_refraksi_os, self.c_refraksi_os, self.a_refraksi_os, self.v_refraksi_os
        ]):
            refraksi.append(
                f"    OS : S:{val(self.s_refraksi_os) or '-'} "
                f"C:{val(self.c_refraksi_os) or '-'} "
                f"A:{val(self.a_refraksi_os) or '-'} "
                f"Visus:{val(self.v_refraksi_os) or '-'}"
            )

        if refraksi:
            add_title("Refraksi")
            lines.extend(refraksi)

        # ================= RIWAYAT KACAMATA =================
        riwayat = []
        if any(val(x) for x in [
            self.s_riwayat_mata_od, self.c_riwayat_mata_od,
            self.a_riwayat_mata_od, self.v_riwayat_mata_od
        ]):
            riwayat.append(
                f"    OD : S:{val(self.s_riwayat_mata_od) or '-'} "
                f"C:{val(self.c_riwayat_mata_od) or '-'} "
                f"A:{val(self.a_riwayat_mata_od) or '-'} "
                f"Visus:{val(self.v_riwayat_mata_od) or '-'}"
            )

        if any(val(x) for x in [
            self.s_riwayat_mata_os, self.c_riwayat_mata_os,
            self.a_riwayat_mata_os, self.v_riwayat_mata_os
        ]):
            riwayat.append(
                f"    OS : S:{val(self.s_riwayat_mata_os) or '-'} "
                f"C:{val(self.c_riwayat_mata_os) or '-'} "
                f"A:{val(self.a_riwayat_mata_os) or '-'} "
                f"Visus:{val(self.v_riwayat_mata_os) or '-'}"
            )

        if riwayat:
            add_title("Riwayat Kacamata")
            lines.extend(riwayat)

        # ================= ADDITIONAL =================
        if val(self.additional_mata_od) or val(self.additional_mata_os):
            add_title("Additional")
            if val(self.additional_mata_od):
                add_line(f"    OD : {self.additional_mata_od}")
            if val(self.additional_mata_os):
                add_line(f"    OS : {self.additional_mata_os}")

        # ================= PEMERIKSAAN UMUM =================
        def add_pair(title, od, os):
            if val(od) or val(os):
                add_title(title)
                if val(od):
                    add_line(f"    OD : {od}")
                if val(os):
                    add_line(f"    OS : {os}")

        add_pair("Visus Naturalis", self.visus_naturalis_od, self.visus_naturalis_os)
        add_pair("Visus dengan koreksi", self.visus_jauh_od, self.visus_jauh_os)
        add_pair("Jauh", self.jauh_od, self.jauh_os)
        add_pair("Dekat", self.dekat_od, self.dekat_os)
        add_pair("TIO", self.tio_od, self.tio_os)
        add_pair("Posisi bola mata", self.posisi_bola_mata_od, self.posisi_bola_mata_os)
        add_pair("Palpebra", self.palpebra_od, self.palpebra_os)
        add_pair("Conjunctiva", self.conjunctiva_od, self.conjunctiva_os)
        add_pair("Cornea", self.cornea_od, self.cornea_os)
        add_pair("COA", self.coa_od, self.coa_os)
        add_pair("Iris", self.iris_od, self.iris_os)
        add_pair("Pupil", self.pupil_od, self.pupil_os)

        # ================= OPHTHALMOSCOPY =================
        add_pair("Vitreus", self.vitreus_od, self.vitreus_os)
        add_pair("PN II", self.pn_ii_od, self.pn_ii_os)
        add_pair("Vasa", self.vasa_od, self.vasa_os)
        add_pair("Retina", self.retina_od, self.retina_os)
        add_pair("Macula", self.macula_od, self.macula_os)
        data = "\n".join(lines)
        return data + "\n"


#     def _get_data_objektive_for_cppt(self):
#         data = f"""
# PD : {self.txt_pd or "-"}
# Refraksi
#     OD :
#         S:{self.s_refraksi_od or "-"}	C:{self.c_refraksi_od or "-"}	A: {self.a_refraksi_od or "-" }	Visus: {self.v_refraksi_od or "-"}
#     OS :
#         S:{self.s_refraksi_os or "-"}	C:{self.c_refraksi_os or "-"}	A: {self.a_refraksi_os or "-"}	Visus: {self.v_refraksi_os or "-"}

# Riwayat Kacamata
#     OD :
#         S:{self.s_riwayat_mata_od or "-"}	C:{self.c_riwayat_mata_od or "-"}	A: {self.a_riwayat_mata_od or "-" }	Visus: {self.v_riwayat_mata_od or "-"}
#     OS :
#         S:{self.s_riwayat_mata_os or "-"}	C:{self.c_riwayat_mata_os or "-"}	A: {self.a_riwayat_mata_os or "-"}	Visus: {self.v_riwayat_mata_os or "-"}

# Additional
#     OD :
#     {self.additional_mata_os or "-"}
#     OS :
#     {self.additional_mata_od or "-"}

# Ophthalmologis:
# Visus Naturalis
#     OD : {self.visus_naturalis_od or "-"}
#     OS : {self.visus_naturalis_os or "-"}
# Visus dengan koreksi
#     OD : {self.visus_jauh_od or "-"}
#     OS : {self.visus_jauh_os or "-"}
# Jauh
#     OD : {self.jauh_od or "-"}
#     OS : {self.jauh_os or "-"}
# Dekat
#     OD : {self.dekat_od or "-"}
#     OS : {self.dekat_os or "-"}
# TIO
#     OD : {self.tio_od or "-"}
#     OS : {self.tio_os or "-"}
# Posisi bola mata
#     OD : {self.posisi_bola_mata_od or "-"}
#     OS : {self.posisi_bola_mata_os or "-"}
# Palpebra
#     OD : {self.palpebra_od or "-"}
#     OS : {self.palpebra_os or "-"}
# Conjunctiva
#     OD : {self.conjunctiva_od or "-"}
#     OS : {self.conjunctiva_os or "-"}
# Cornea
#     OD : {self.cornea_od or "-"}
#     OS : {self.cornea_os or "-"}
# COA
#     OD : {self.coa_od or "-"}
#     OS : {self.coa_os or "-"}
# Iris
#     OD : {self.iris_od or "-"}
#     OS : {self.iris_os or "-"}
# Pupil
#     OD : {self.pupil_od or "-"}
#     OS : {self.pupil_os or "-"}

# Opthalmoscopy:
# Vitreus
#     OD : {self.vitreus_od or "-"}
#     OS : {self.vitreus_os or "-"}
# PN II
#     OD : {self.pn_ii_od or "-"}
#     OS : {self.pn_ii_os or "-"}
# Vasa
#     OD : {self.vasa_od or "-"}
#     OS : {self.vasa_os or "-"}
# Retina
#     OD : {self.retina_od or "-"}
#     OS : {self.retina_os or "-"}
# Macula
#     OD : {self.macula_od or "-"}
#     OS : {self.macula_os or "-"}
# """
#         # print(data)
#         # raise UserError(data)
#         return data
    # =========================================
    # 1. JENIS ANAMNESIS
    # =========================================
    auto_anamnesis = fields.Boolean(
        string='Auto Anamnesis',
        help='Anamnesis langsung dari pasien', tracking=True
    )
    allo_anamnesis = fields.Boolean(
        string='Allo Anamnesis',
        help='Anamnesis dari orang lain', tracking=True
    )
    hubungan_keluarga = fields.Char(
        string='Hubungan Keluarga',
        help='Hubungan keluarga dengan pasien (jika Allo Anamnesis)', tracking=True
    )

    # =========================================
    # 2. KELUHAN UTAMA
    # =========================================

    # =========================================
    # 2. PEMERIKSAAN FISIK
    # =========================================
    @api.model
    def _default_gambar_pemeriksaan_mata(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.rm_pengkajian_medis_gambar_mata')

    gambar_pemeriksaan_mata                = fields.Binary(string='Gambar Pemeriksaan Mata', default=_default_gambar_pemeriksaan_mata)
    gambar_pemeriksaan_mata_out_img        = fields.Image(string='Gambar Pemeriksaan Mata Out')
    gambar_pemeriksaan_mata_json_img       = fields.Text(string='Gambar Pemeriksaan Mata JSON')

    def action_penandaan_gambar_pemeriksaan_mata(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'gambar_pemeriksaan_mata',
            'default_bg_json_name'        : 'gambar_pemeriksaan_mata_json_img',
            'default_bg_out_name'         : 'gambar_pemeriksaan_mata_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.gambar_pemeriksaan_mata,
            'default_penandaan_json_img'  : self.gambar_pemeriksaan_mata_json_img,
            'default_penandaan_out_img'   : self.gambar_pemeriksaan_mata_out_img,
            'height'                      : self.env.context.get('height'), #px
            'width'                       : self.env.context.get('width'), #px
        }

        return self.rm_base_id.open_wizard_canvas(data)

                        # <field name="txt_pd"/>

                        
    txt_pd              = fields.Char(string='PD', tracking=True)
    # MATA KIRI (OS)
    s_refraksi_os = fields.Char(string='S Refraksi OS', tracking=True)
    s_tonometri_os = fields.Char(string='S Tonometri OS', tracking=True)
    s_riwayat_mata_os = fields.Char(string='S Riwayat Mata OS', tracking=True)

    c_refraksi_os = fields.Char(string='C Refraksi OS', tracking=True)
    c_tonometri_os = fields.Char(string='C Tonometri OS', tracking=True)
    c_riwayat_mata_os = fields.Char(string='C Riwayat Mata OS', tracking=True)

    a_refraksi_os = fields.Char(string='A Refraksi OS', tracking=True)
    a_tonometri_os = fields.Char(string='A Tonometri OS', tracking=True)
    a_riwayat_mata_os = fields.Char(string='A Riwayat Mata OS', tracking=True)

    v_refraksi_os = fields.Char(string='V Refraksi OS', tracking=True)
    v_riwayat_mata_os = fields.Char(string='V Riwayat Mata OS', tracking=True)
    additional_mata_os = fields.Text(string='Additional ', tracking=True)
    

    # MATA KANAN (OD)
    s_refraksi_od = fields.Char(string='S Refraksi OD', tracking=True)
    s_tonometri_od = fields.Char(string='S Tonometri OD', tracking=True)
    s_riwayat_mata_od = fields.Char(string='S Riwayat Mata OD', tracking=True)

    c_refraksi_od = fields.Char(string='C Refraksi OD', tracking=True)
    c_tonometri_od = fields.Char(string='C Tonometri OD')
    c_riwayat_mata_od = fields.Char(string='C Riwayat Mata OD', tracking=True)

    a_refraksi_od = fields.Char(string='A Refraksi OD', tracking=True)
    a_tonometri_od = fields.Char(string='A Tonometri OD', tracking=True)
    a_riwayat_mata_od = fields.Char(string='A Riwayat Mata OD', tracking=True)
    
    v_refraksi_od = fields.Char(string='V Refraksi OD', tracking=True)
    v_riwayat_mata_od = fields.Char(string='V Riwayat Mata OD', tracking=True)
    additional_mata_od= fields.Text(string='Additional', tracking=True)
    

    # A. STATUS OPHTHALMOLOGIS
    # Mata Kanan (OD)

    # gambar_od = fields.Binary(string='Gambar OD')

    visus_naturalis_od = fields.Text(string='Visus Naturalis OD', tracking=True)
    visus_jauh_od = fields.Text(string='Visus Jauh (Koreksi) OD', tracking=True)
    visus_dekat_od = fields.Text(string='Visus Dekat (Koreksi) OD', tracking=True)
    jauh_od = fields.Text(string='Jauh OD', tracking=True)
    dekat_od = fields.Text(string='Dekat OD', tracking=True)
    tio_od = fields.Text(string='TIO OD', tracking=True)
    posisi_bola_mata_od = fields.Text(string='Posisi Bola Mata OD', tracking=True)
    palpebra_od = fields.Text(string='Palpebra OD', tracking=True)
    conjunctiva_od = fields.Text(string='Conjunctiva OD', tracking=True)
    cornea_od = fields.Text(string='Cornea OD', tracking=True)
    coa_od = fields.Text(string='COA OD', tracking=True)
    iris_od = fields.Text(string='Iris OD', tracking=True)
    pupil_od = fields.Text(string='Pupil OD', tracking=True)
    lensa_od = fields.Text(string='Lensa OD', tracking=True)

    # Mata Kiri (OS)

    # gambar_os = fields.Binary(string='Gambar OS')


    visus_naturalis_os = fields.Text(string='Visus Naturalis OS', tracking=True)
    visus_jauh_os = fields.Text(string='Visus Jauh (Koreksi) OS', tracking=True)
    visus_dekat_os = fields.Text(string='Visus Dekat (Koreksi) OS', tracking=True)
    jauh_os = fields.Text(string='Jauh OS', tracking=True)
    dekat_os = fields.Text(string='Dekat OS', tracking=True)
    tio_os = fields.Text(string='TIO OS', tracking=True)
    posisi_bola_mata_os = fields.Text(string='Posisi Bola Mata OS', tracking=True)
    palpebra_os = fields.Text(string='Palpebra OS', tracking=True)
    conjunctiva_os = fields.Text(string='Conjunctiva OS', tracking=True)
    cornea_os = fields.Text(string='Cornea OS', tracking=True)
    coa_os = fields.Text(string='COA OS', tracking=True)
    iris_os = fields.Text(string='Iris OS', tracking=True)
    pupil_os = fields.Text(string='Pupil OS', tracking=True)
    lensa_os = fields.Text(string='Lensa OS', tracking=True)

    # B. PEMERIKSAAN TAMBAHAN
    gerakan_bola_mata = fields.Text(
        string='Gerakan Bola Mata',
        help='Pemeriksaan gerakan bola mata', tracking=True
    )
    tes_ishihara = fields.Text(
        string='Tes Ishihara',
        help='Hasil tes Ishihara', tracking=True
    )
    pemeriksaan_tambahan_lainnya = fields.Text(
        string='Lain-lainnya',
        help='Pemeriksaan tambahan lainnya', tracking=True
    )

    hasil_pemeriksaan_penunjang_text = fields.Char(string='Hasil Pemeriksaan Penunjang', tracking=True)
    

    # C. PEMERIKSAAN OPTHALMOSCOPY
    # Mata Kanan
    @api.model
    def _get_icon_pemeriksaan_ophtalmoscopy_od(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.icon_pemeriksaan_ophtalmoscopy_od')
    
    icon_pemeriksaan_ophtalmoscopy_od = fields.Binary(string='Gambar Ophtalmoscopy OD', default=_get_icon_pemeriksaan_ophtalmoscopy_od)
    icon_pemeriksaan_ophtalmoscopy_od_out_img        = fields.Image(string='Gambar Ophtalmoscopy Out')
    icon_pemeriksaan_ophtalmoscopy_od_json_img       = fields.Text(string='Gambar Ophtalmoscopy JSON')


    def _get_icon_pemeriksaan_garis_garis_od(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.icon_garis_garis')
    icon_pemeriksaan_garis_garis_od = fields.Binary(string='Gambar Garis Garis OD', default=_get_icon_pemeriksaan_garis_garis_od)
    icon_pemeriksaan_garis_garis_od_out_img        = fields.Image(string='Gambar Garis Garis Out')
    icon_pemeriksaan_garis_garis_od_json_img       = fields.Text(string='Gambar Garis Garis JSON')


    def action_penandaan_icon_pemeriksaan_garis_garis_od(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'icon_pemeriksaan_garis_garis_od',
            'default_bg_json_name'        : 'icon_pemeriksaan_garis_garis_od_json_img',
            'default_bg_out_name'         : 'icon_pemeriksaan_garis_garis_od_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.icon_pemeriksaan_garis_garis_od,
            'default_penandaan_json_img'  : self.icon_pemeriksaan_garis_garis_od_json_img,
            'default_penandaan_out_img'   : self.icon_pemeriksaan_garis_garis_od_out_img,
            'height'                      : self.env.context.get('height'),
            'width'                       : self.env.context.get('width'),
        }
        return self.rm_base_id.open_wizard_canvas(data)
    
    def action_penandaan_icon_pemeriksaan_ophtalmoscopy_od(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'icon_pemeriksaan_ophtalmoscopy_od',
            'default_bg_json_name'        : 'icon_pemeriksaan_ophtalmoscopy_od_json_img',
            'default_bg_out_name'         : 'icon_pemeriksaan_ophtalmoscopy_od_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.icon_pemeriksaan_ophtalmoscopy_od,
            'default_penandaan_json_img'  : self.icon_pemeriksaan_ophtalmoscopy_od_json_img,
            'default_penandaan_out_img'   : self.icon_pemeriksaan_ophtalmoscopy_od_out_img,
            'height'                      : self.env.context.get('height'), #px
            'width'                       : self.env.context.get('width'), #px
        }

        return self.rm_base_id.open_wizard_canvas(data)


    reflex_fundus_od = fields.Text(string='Reflex Fundus OD', tracking=True)
    vitreus_od = fields.Text(string='Vitreus OD', tracking=True)
    pn_ii_od = fields.Text(string='PN II OD', tracking=True)
    vasa_od = fields.Text(string='Vasa OD', tracking=True)
    retina_od = fields.Text(string='Retina OD', tracking=True)
    macula_od = fields.Text(string='Macula OD', tracking=True)

    # Mata Kiri
    @api.model
    def _get_icon_pemeriksaan_ophtalmoscopy_os(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.icon_pemeriksaan_ophtalmoscopy_os')
    
    icon_pemeriksaan_ophtalmoscopy_os = fields.Binary(string='Gambar Ophtalmoscopy OS' , default=_get_icon_pemeriksaan_ophtalmoscopy_os)
    icon_pemeriksaan_ophtalmoscopy_os_out_img        = fields.Image(string='Gambar Ophtalmoscopy OS Out')
    icon_pemeriksaan_ophtalmoscopy_os_json_img       = fields.Text(string='Gambar Ophtalmoscopy OS JSON')


    def _get_icon_pemeriksaan_garis_garis_os(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.icon_garis_garis')
    icon_pemeriksaan_garis_garis_os                = fields.Binary(string='Gambar Garis Garis OS', default=_get_icon_pemeriksaan_garis_garis_os)
    icon_pemeriksaan_garis_garis_os_out_img        = fields.Image(string='Gambar Garis Garis Out')
    icon_pemeriksaan_garis_garis_os_json_img       = fields.Text(string='Gambar Garis Garis JSON')


    def action_penandaan_icon_pemeriksaan_garis_garis_os(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'icon_pemeriksaan_garis_garis_os',
            'default_bg_json_name'        : 'icon_pemeriksaan_garis_garis_os_json_img',
            'default_bg_out_name'         : 'icon_pemeriksaan_garis_garis_os_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.icon_pemeriksaan_garis_garis_os,
            'default_penandaan_json_img'  : self.icon_pemeriksaan_garis_garis_os_json_img,
            'default_penandaan_out_img'   : self.icon_pemeriksaan_garis_garis_os_out_img,
            'height'                      : self.env.context.get('height'),
            'width'                       : self.env.context.get('width'),
        }
        return self.rm_base_id.open_wizard_canvas(data)



    def action_penandaan_icon_pemeriksaan_ophtalmoscopy_os(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'icon_pemeriksaan_ophtalmoscopy_os',
            'default_bg_json_name'        : 'icon_pemeriksaan_ophtalmoscopy_os_json_img',
            'default_bg_out_name'         : 'icon_pemeriksaan_ophtalmoscopy_os_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.icon_pemeriksaan_ophtalmoscopy_os,
            'default_penandaan_json_img'  : self.icon_pemeriksaan_ophtalmoscopy_os_json_img,
            'default_penandaan_out_img'   : self.icon_pemeriksaan_ophtalmoscopy_os_out_img,
            'height'                      : self.env.context.get('height'), #px
            'width'                       : self.env.context.get('width'), #px
        }

        return self.rm_base_id.open_wizard_canvas(data)


    reflex_fundus_os = fields.Text(string='Reflex Fundus OS', tracking=True)
    vitreus_os = fields.Text(string='Vitreus OS', tracking=True)
    pn_ii_os = fields.Text(string='PN II OS', tracking=True)
    vasa_os = fields.Text(string='Vasa OS', tracking=True)
    retina_os = fields.Text(string='Retina OS', tracking=True)
    macula_os = fields.Text(string='Macula OS', tracking=True)

    # D. TEMUAN LAIN
    temuan_lain = fields.Text(
        string='Temuan Lain',
        help='Temuan lain dari pemeriksaan'
    )

    # =========================================
    # 3. PEMERIKSAAN PENUNJANG
    # =========================================
    tanggal_penunjang = fields.Date(
        string='Tanggal Pemeriksaan Penunjang',
        help='Tanggal pemeriksaan penunjang dilakukan', tracking=True
    )
    nama_pemeriksaan = fields.Char(
        string='Nama Pemeriksaan',
        help='Nama jenis pemeriksaan penunjang', tracking=True
    )
    kesan_hasil = fields.Text(
        string='Kesan Hasil',
        help='Kesan/interpretasi hasil pemeriksaan penunjang', tracking=True
    )

    # =========================================
    # 4. DIAGNOSA
    # =========================================
    diagnosa_utama = fields.Text(
        string='Diagnosa Utama',
        help='Diagnosa utama pasien', tracking=True
    )
    diagnosa_sekunder = fields.Text(
        string='Diagnosa Sekunder',
        help='Diagnosa sekunder/penyerta', tracking=True
    )

    # =========================================
    # 5. PENATALAKSANAAN / PERENCANAAN PELAYANAN
    # =========================================
    rencana_pelayanan = fields.Text(
        string='Rencana Pelayanan',
        help='Rencana penatalaksanaan dan pelayanan untuk pasien', tracking=True
    )

    # =========================================
    # 6. CATATAN PENTING (KONDISI SAAT INI)
    # =========================================

    # A. INSTRUKSI, SASARAN, EDUKASI (TINDAK LANJUT)
    tindak_lanjut_kontrol = fields.Boolean(
        string='Kontrol',
        help='Tindak lanjut kontrol', tracking=True
    )
    tanggal_kontrol = fields.Date(
        string='Tanggal Kontrol',
        help='Tanggal kontrol berikutnya', tracking=True
    )
    tindak_lanjut_rujuk = fields.Boolean(
        string='Rujuk',
        help='Tindak lanjut rujuk', tracking=True
    )
    rujuk_ke = fields.Char(
        string='Rujuk Ke',
        help='Tempat rujukan', tracking=True
    )

    # B. BERKAS YANG DIBAWA PULANG
    surat_keterangan_sehat = fields.Boolean(
        string='Surat Keterangan Sehat',
        help='Berkas surat keterangan sehat', tracking=True
    )
    surat_keterangan_sakit = fields.Boolean(
        string='Surat Keterangan Sakit',
        help='Berkas surat keterangan sakit', tracking=True
    )
    hasil_pemeriksaan_penunjang = fields.Boolean(
        string='Hasil Pemeriksaan Penunjang',
        help='Berkas hasil pemeriksaan penunjang', tracking=True
    )
    tambahan_catatan = fields.Text(
        string='Tambahan Catatan',
        help='Catatan tambahan untuk pasien', tracking=True
    )

    # =========================================
    # 7. PERNYATAAN PENJELASAN & PERSETUJUAN
    # =========================================
    tanda_tangan_pasien = fields.Binary(
        string='Tanda Tangan Pasien',
        help='Tanda tangan pasien'
    )
    tanda_tangan_dokter = fields.Binary(
        string='Tanda Tangan Dokter',
        help='Tanda tangan dokter'
    )

    tanggal_persetujuan = fields.Date(
        string='Tanggal Persetujuan',
        help='Tanggal persetujuan diberikan'
    )

    # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.pengkajian.medis/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {
            'no_rm'                         : self.pasien_id.no_rm or '',
            'nama_pasien'                   : self.pasien_id.name or '',
            'tgl_lahir'                         : self.pasien_id.tanggal_lahir.strftime('%d/%m/%Y') if self.pasien_id.tanggal_lahir else '',
            'au'                                : '☑' if self.auto_anamnesis else '☐',
            'al'                                : '☑' if self.allo_anamnesis else '☐',
            'hubungan_keluarga'             : self.hubungan_keluarga or '',
            'keluhan_utama'                 : self.keluhan_utama or '',
            
            'visus_naturalis_od'             : self.visus_naturalis_od or '',
            'visus_jauh_od'                  : self.visus_jauh_od or '',
            'visus_dekat_od'                 : self.visus_dekat_od or '',
            'jauh_od'                        : self.jauh_od or '',
            'dekat_od'                       : self.dekat_od or '',
            'tio_od'                         : self.tio_od or '',
            'posisi_bola_mata_od'            : self.posisi_bola_mata_od or '',
            'palpebra_od'                    : self.palpebra_od or '',
            'conjunctiva_od'                 : self.conjunctiva_od or '',
            'cornea_od'                      : self.cornea_od or '',
            'coa_od'                         : self.coa_od or '',
            'iris_od'                        : self.iris_od or '',
            'pupil_od'                       : self.pupil_od or '',
            'lensa_od'                       : self.lensa_od or '',
            
            'visus_naturalis_os'             : self.visus_naturalis_os or '',
            'visus_jauh_os'                  : self.visus_jauh_os or '',
            'visus_dekat_os'                 : self.visus_dekat_os or '',
            'jauh_os'                        : self.jauh_os or '',
            'dekat_os'                       : self.dekat_os or '',
            'tio_os'                         : self.tio_os or '',
            'posisi_bola_mata_os'            : self.posisi_bola_mata_os or '',
            'palpebra_os'                    : self.palpebra_os or '',
            'conjunctiva_os'                 : self.conjunctiva_os or '',
            'cornea_os'                      : self.cornea_os or '',
            'coa_os'                         : self.coa_os or '',
            'iris_os'                        : self.iris_os or '',
            'pupil_os'                       : self.pupil_os or '',
            'lensa_os'                       : self.lensa_os or '',
            
            'gerakan_bola_mata'              : self.gerakan_bola_mata or '.....................',
            'tes_ishihara'                   : self.tes_ishihara or '.....................',
            'pemeriksaan_tambahan_lainnya'   : self.pemeriksaan_tambahan_lainnya or '.....................',
            
            'reflex_fundus_od'               : self.reflex_fundus_od,
            'vitreus_od'                     : self.vitreus_od,
            'pn_ii_od'                       : self.pn_ii_od,
            'vasa_od'                        : self.vasa_od,
            'retina_od'                      : self.retina_od,
            'macula_od'                      : self.macula_od,
            
            'reflex_fundus_os'               : self.reflex_fundus_os,
            'vitreus_os'                     : self.vitreus_os,
            'pn_ii_os'                       : self.pn_ii_os,
            'vasa_os'                        : self.vasa_os,
            'retina_os'                      : self.retina_os,
            'macula_os'                      : self.macula_os,
            
            'temuan_lain'                    : self.temuan_lain or '',
            'tanggal_penunjang'              : self.tanggal_penunjang or '',
            'nama_pemeriksaan'               : self.nama_pemeriksaan or '',
            'kesan_hasil'                    : self.kesan_hasil or '',
            'diagnosa_utama'                 : self.diagnosa_utama or '',
            'diagnosa_sekunder'              : self.diagnosa_sekunder or '',
            'rencana_pelayanan'              : self.rencana_pelayanan or '',
            'ko'                             : '☑' if self.tindak_lanjut_kontrol else '☐',
            'tanggal_kontrol'                : self.tanggal_kontrol or '....................',
            'hasil_pemeriksaan_penunjang'    : self.hasil_pemeriksaan_penunjang_text or '....................',
            'ru'                             : '☑' if self.tindak_lanjut_rujuk else '☐',
            'rujuk_ke'                       : self.rujuk_ke or '....................',
            'sk'                             : '☑' if self.surat_keterangan_sehat else '☐',
            'ss'                             : '☑' if self.surat_keterangan_sakit else '☐',
            'hpp'                            : '☑' if self.hasil_pemeriksaan_penunjang else '☐',
            'temuan_lain'                    : self.temuan_lain or '',
            'tambahan_catatan'               : self.tambahan_catatan or '',
            'tanggal_persetujuan'            : self.tanggal_persetujuan or '',
            'qr_ttd_dokter_partner_id'       : self.qr_ttd_dokter_partner_id.name or '...............................',

            # MATA KIRI (OS)
            's_refraksi_os'     : self.s_refraksi_os,
            's_tonometri_os'    : self.s_tonometri_os,  
            's_riwayat_mata_os' : self.s_riwayat_mata_os,

            'c_refraksi_os'     : self.c_refraksi_os,
            'c_tonometri_os'    : self.c_tonometri_os,
            'c_riwayat_mata_os' : self.c_riwayat_mata_os,

            'a_refraksi_os'     : self.a_refraksi_os,
            'a_tonometri_os'    : self.a_tonometri_os,  
            'a_riwayat_mata_os' : self.a_riwayat_mata_os,

            'v_refraksi_os'     : self.v_refraksi_os,
            'v_riwayat_mata_os' : self.v_riwayat_mata_os,

            # MATA KANAN (
            's_refraksi_od'     : self.s_refraksi_od,
            's_tonometri_od'    : self.s_tonometri_od,  
            's_riwayat_mata_od' : self.s_riwayat_mata_od,

            'c_refraksi_od'     : self.c_refraksi_od, 
            'c_tonometri_od'    : self.c_tonometri_od,  
            'c_riwayat_mata_od' : self.c_riwayat_mata_od,

            'a_refraksi_od'     : self.a_refraksi_od,
            'a_tonometri_od'    : self.a_tonometri_od,  
            'a_riwayat_mata_od' : self.a_riwayat_mata_od,

            'v_refraksi_od'     : self.v_refraksi_od,
            'v_riwayat_mata_od' : self.v_riwayat_mata_od,
        }

        gambar_penandaan_mata_os_od = self.gambar_pemeriksaan_mata_out_img
        if not gambar_penandaan_mata_os_od:
            gambar_penandaan_mata_os_od = self.gambar_pemeriksaan_mata
        
        icon_ophtalmoscopy_os = self.icon_pemeriksaan_ophtalmoscopy_os_out_img
        if not icon_ophtalmoscopy_os:
            icon_ophtalmoscopy_os = self.icon_pemeriksaan_ophtalmoscopy_os

        icon_ophtalmoscopy_od = self.icon_pemeriksaan_ophtalmoscopy_od_out_img
        if not icon_ophtalmoscopy_od:
            icon_ophtalmoscopy_od = self.icon_pemeriksaan_ophtalmoscopy_od

        data_image = [
            {'key': '{{ttd_pasien}}', 'value': self.tanda_tangan_pasien, 'inches': 1},
            {'key': '{{tanda_tangan_dokter}}', 'value': self.qr_ttd_dokter_code, 'inches': 1},
            {'key': '{{logo}}', 'value': self.company_id.logo, 'inches': 0.7},
            {'key': '{{gambar_penandaan_mata_os_od}}', 'value': gambar_penandaan_mata_os_od or False, 'inches': 3},
            {'key': '{{icon_ophtalmoscopy_os}}', 'value': icon_ophtalmoscopy_os or False, 'inches': 1},
            {'key': '{{icon_ophtalmoscopy_od}}', 'value': icon_ophtalmoscopy_od or False, 'inches': 1},
            # {'key': '{{ophtalmoscopy_od}}', 'value': self.icon_pemeriksaan_ophtalmoscopy_od, 'inches': 1},
            # {'key': '{{ophtalmoscopy_os}}', 'value': self.icon_pemeriksaan_ophtalmoscopy_os, 'inches': 1},
        ]

        template = 'cdn_simrs_rekamedis_add/template/klinik_mata/pengkajian_medis.docx'
        return self._mail_merge_to_pdf(
            path        = template,
            data_info   = data_field,
            image_info  = data_image
        )