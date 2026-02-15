# cdn_simrs_rekamedis_add/models/asesmen_awal_medis.py

from odoo import _, api, fields, models

class AsesmenAwalMedisRawatJalan(models.Model):
    _name = 'cdn.asesmen.awal.medis.rawat.jalan'
    _description = 'Asesmen Awal Medis Rawat Jalan'
    _inherits       = {'cdn.erm.base': 'rm_base_id'}
    _inherit        = ['mail.thread', 'mail.activity.mixin', 'cdn.erm.mixin', 'cdn.report.mailmerge']
    
    rm_base_id      = fields.Many2one(comodel_name='cdn.erm.base', string='RM', ondelete='cascade')
  
    # Properties untuk dynamic fields
    erm_properties = fields.Properties(definition="rm_id.erm_properties_definition", string="Properties")



    # === I. ANAMNESA ===
    an_keluhan_utama = fields.Text(string='Keluhan Utama', tracking=True)
    an_riwayat_penyakit_sekarang = fields.Text(string='Riwayat Penyakit Sekarang', tracking=True)
    an_riwayat_penyakit_dahulu = fields.Text(string='Riwayat Penyakit Dahulu', tracking=True)
    an_riwayat_penyakit_keluarga = fields.Text(string='Riwayat Penyakit Keluarga', tracking=True)

    # === II. PEMERIKSAAN FISIK ===
    pemeriksaan_fisik_img = fields.Binary(string='Gambar Pemeriksaan Fisik') 
    pf_keadaan_umum = fields.Text(string='Keadaan Umum', tracking=True)
    pf_gcs = fields.Char(string='GCS', tracking=True)
    pf_bb = fields.Float(string='BB (kg)', tracking=True)
    pf_tb = fields.Float(string='TB (cm)', tracking=True)
    pf_td = fields.Char(string='TD (mmHg)', tracking=True)
    pf_nadi = fields.Integer(string='N (x/menit)', tracking=True)
    pf_suhu = fields.Float(string='S (°C)', tracking=True)
    pf_rr = fields.Integer(string='RR (x/menit)', tracking=True)

    # Kepala
    pf_mata = fields.Char(string='Mata')
    pf_telinga = fields.Char(string='Telinga')    
    pf_hidung = fields.Char(string='Hidung')
    pf_gigi_mulut = fields.Char(string='Gigi / Mulut')
    pf_tenggorokan = fields.Char(string='Tenggorokan')
    pf_leher = fields.Char(string='Leher')

    # Thorax
    pf_dinding_dada = fields.Char(string='Dinding dada')
    pf_jantung = fields.Char(string='Jantung')
    pf_paru_paru = fields.Char(string='Paru – paru')

    # Abdomen
    pf_punggung = fields.Char(string='Punggung')
    pf_dinding_perut = fields.Char(string='Dinding perut')
    pf_liver = fields.Char(string='Liver')
    pf_lien = fields.Char(string='Lien')
    pf_usus_dll = fields.Char(string='Usus, dll')

    pf_neurologis = fields.Char(string='Neurologis')
    pf_genital = fields.Char(string='Genital')
    pf_ekstremitas = fields.Char(string='Ekstremitas')

    # === III. PEMERIKSAAN PENUNJANG ===
    pemeriksaan_penunjang = fields.Text(string='Pemeriksaan Penunjang', tracking=True)

    # === IV. DIAGNOSA ===
    diagnosa = fields.Text(string='Diagnosa', tracking=True)

    # === V. RENCANA ===
    rencana = fields.Text(string='Rencana', tracking=True)
    is_dirujuk_ke = fields.Boolean(string='Dirujuk ke', default=False, tracking=True)
    poli_specialis = fields.Char(string='Poli / Specialis', tracking=True)
    mrs = fields.Char(string='MRS', tracking=True)
    is_lainnya = fields.Boolean(string='Lainnya', default=False, tracking=True)
    lainnya = fields.Char(string='Lainnya', tracking=True)

    # === TANDA TANGAN ===
    signature_dokter = fields.Binary(string='TTD Dokter')


    # SIGNATURE GENERATE
    def signature_generate(self):
        login = False
        if self.env.user.login:
            login = self.env.user.login

        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_username': login,
            'default_field_name': self.env.context.get('field_name'),
            'default_model_id': model_id.id,
            'default_data_id': self.id,
            'default_tipe': self.env.context.get('tipe_nakes'),
            'default_tipe_dokumen': 'Asesmen Awal Medis Rawat Jalan',
            'default_perihal': 'Tanda tangan pada Asesmen Awal Medis Rawat Jalan',
        }

        return self.rm_base_id.open_wizard_generate_qr_sign(data)

    # ACTION PRINT
    def action_print(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/cdn_print_report_pdf/cdn.asesmen.awal.medis.rawat.jalan/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {
            'nama_pasien': self.pasien_id.name if self.pasien_id else '',
        }
        
        template = 'cdn_simrs_rekamedis_add/template/asesmen_awal_medis_rawat_jalan.docx'
        return self._mail_merge_to_pdf(
            path=template,
            data_info=data_field,
            image_info=[],
            list_info=[]
        )


    @api.model
    def _get_default_penandaan_fisik_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.pemeriksaan_fisik')
    
    penandaan_fisik_bg_img        = fields.Binary(string='Penandaan Fisik BG', default=_get_default_penandaan_fisik_bg_img)
    penandaan_fisik_json_img      = fields.Text(string='Penandaan Fisik JSON')
    penandaan_fisik_out_img       = fields.Image(string='Penandaan Fisik OUT')
    deskripsi_fisik               = fields.Text(string='Deskripsi Fisik')

     # PENANDAAN 
    def action_penandaan_fisik(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_fisik_bg_img',
            'default_bg_json_name'        : 'penandaan_fisik_json_img',
            'default_bg_out_name'         : 'penandaan_fisik_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_fisik_bg_img,
            'default_penandaan_json_img'  : self.penandaan_fisik_json_img,
            'default_penandaan_out_img'   : self.penandaan_fisik_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)