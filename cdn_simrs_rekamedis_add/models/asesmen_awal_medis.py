# cdn_simrs_rekamedis_add/models/asesmen_awal_medis.py

from odoo import _, api, fields, models

class AsesmenAwalMedisRawatInap(models.Model):
    _name = 'cdn.asesmen.awal.medis.rawat.inap'
    _description = 'Asesmen Awal Medis Rawat Inap'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin'
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
    )

    # === I. ANAMNESA ===
    anamnesa_keluhan_utama = fields.Text(string='Keluhan Utama', tracking=True)
    anamnesa_riwayat_penyakit_sekarang = fields.Html(string='Riwayat Penyakit Sekarang', tracking=True)
    anamnesa_riwayat_penyakit_dahulu = fields.Html(string='Riwayat Penyakit Dahulu', tracking=True)
    anamnesa_riwayat_penyakit_keluarga = fields.Html(string='Riwayat Penyakit Keluarga', tracking=True)

    # Pemeriksaan Sistematis
    pemeriksaan_fisik_kepala_mata = fields.Char(string='Mata', tracking=True)
    pemeriksaan_fisik_kepala_telinga = fields.Char(string='Telinga', tracking=True)
    pemeriksaan_fisik_kepala_hidung = fields.Char(string='Hidung', tracking=True)
    pemeriksaan_fisik_kepala_gigi_mulut = fields.Char(string='Gigi / Mulut', tracking=True)
    pemeriksaan_fisik_kepala_tenggorokan = fields.Char(string='Tenggorokan', tracking=True)
    pemeriksaan_fisik_leher = fields.Char(string='Leher', tracking=True)
    pemeriksaan_fisik_thorax_dinding_dada = fields.Char(string='Dinding dada', tracking=True)
    pemeriksaan_fisik_thorax_jantung = fields.Char(string='Jantung', tracking=True)
    pemeriksaan_fisik_thorax_paru_paru = fields.Char(string='Paru – paru', tracking=True)
    pemeriksaan_fisik_punggung = fields.Char(string='Punggung', tracking=True)
    pemeriksaan_fisik_abdomen_dinding_perut = fields.Char(string='Dinding perut', tracking=True)
    pemeriksaan_fisik_abdomen_liver = fields.Char(string='Liver', tracking=True)
    pemeriksaan_fisik_abdomen_lien = fields.Char(string='Lien', tracking=True)
    pemeriksaan_fisik_abdomen_usus_dll = fields.Char(string='Usus, dll', tracking=True)
    pemeriksaan_fisik_ekstremitas = fields.Char(string='Ekstremitas', tracking=True)
    pemeriksaan_fisik_genital = fields.Char(string='Genital', tracking=True)
    pemeriksaan_fisik_neurologis = fields.Char(string='Neurologis', tracking=True)

    # === III. PEMERIKSAAN PENUNJANG ===
    pemeriksaan_penunjang = fields.Html(string='Pemeriksaan Penunjang', tracking=True)

    # === IV. DIAGNOSA ===
    diagnosa = fields.Html(string='Diagnosa', tracking=True)

    # === V. PENATALAKSANAAN ===
    penatalaksanaan = fields.Html(string='Penatalaksanaan', tracking=True)




    @api.model
    def _get_default_penandaan_asesmen_awal_medis_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.asesmen_awal_medis')
    
    penandaan_asesmen_awal_medis_bg_img        = fields.Binary(string='Penandaan AWM BG', default=_get_default_penandaan_asesmen_awal_medis_bg_img)
    penandaan_asesmen_awal_medis_json_img      = fields.Text(string='Penandaan AWM JSON')
    penandaan_asesmen_awal_medis_out_img       = fields.Image(string='Penandaan AWM OUT')
    deskripsi_asesmen_awal_medis               = fields.Text(string='Deskripsi AWM')

    # PENANDAAN 
    def action_penandaan(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_asesmen_awal_medis_bg_img',
            'default_bg_json_name'        : 'penandaan_asesmen_awal_medis_json_img',
            'default_bg_out_name'         : 'penandaan_asesmen_awal_medis_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_asesmen_awal_medis_bg_img,
            'default_penandaan_json_img'  : self.penandaan_asesmen_awal_medis_json_img,
            'default_penandaan_out_img'   : self.penandaan_asesmen_awal_medis_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)