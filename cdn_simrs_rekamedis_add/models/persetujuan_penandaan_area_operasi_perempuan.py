from odoo import _, api, fields, models

class PenandaanAreaOperasiPerempuan(models.Model):
    _name = 'cdn.penandaan.area.operasi.perempuan'
    _description = 'Penandaan Area Operasi Perempuan'
    _inherits = {'cdn.erm.base': 'rm_base_id'}
    _inherit = [
        'mail.thread', 
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
        ]

    rm_base_id      = fields.Many2one(comodel_name='cdn.erm.base', string='RM', required=True, ondelete='cascade')

    diagnosa = fields.Char(string='Diagnosa')

        # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.penandaan.area.operasi.perempuan/{self.id}/_generate_print_report',
            'target': 'new',
        }



    def _generate_print_report(self):
        data_field = {   
            'nama' : self.pasien_id.name or '',
            'tgl_lahir' : self.pasien_id.tanggal_lahir or '',
            'no_rm' : self.pasien_id.no_rm or '',
            'tgl_jam' : self.rm_base_id.tanggal or '', 
            'diagnosa' : self.diagnosa or '',
        }
        data_image = [
            {
                'key'       : '{{penandaan_badan}}',
                'value'     : self.penandaan_badan_bg_img,
                'inches'    : 2,
            },
            {
                'key'       : '{{kepala_samping}}',
                'value'     : self.penandaan_kepala_samping_bg_img,
                'inches'    : 2,
            },
            {
                'key'       : '{{kepala_depan}}',
                'value'     : self.penandaan_kepala_depan_bg_img,
                'inches'    : 2,
            },
            {
                'key'       : '{{punggung_tangan}}',
                'value'     : self.penandaan_punggung_tangan_bg_img,
                'inches'    : 2,
            },
            {
                'key'       : '{{telapak_tangan}}',
                'value'     : self.penandaan_telapak_tangan_bg_img,
                'inches'    : 2,
            },
            {
                'key'       : '{{penandaan_kaki}}',
                'value'     : self.penandaan_kaki_bg_img,
                'inches'    : 2,
            },
        ]
        template = 'cdn_simrs_rekamedis_add/template/penandaan_area_operasi_perempuan.docx'
        return self._mail_merge_to_pdf(
            path        = template, 
            data_info   = data_field, 
            image_info  = data_image, 
        )

    @api.model
    def _get_default_penandaan_badan_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.badan')
    
    penandaan_badan_bg_img        = fields.Binary(string='Penandaan Badan BG', default=_get_default_penandaan_badan_bg_img)
    penandaan_badan_json_img      = fields.Text(string='Penandaan Badan JSON')
    penandaan_badan_out_img       = fields.Image(string='Penandaan Badan OUT')
    deskripsi_badan               = fields.Text(string='Deskripsi Badan')

    @api.model
    def _get_default_penandaan_kepala_samping_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.kepala_samping')
    
    penandaan_kepala_samping_bg_img        = fields.Binary(string='Penandaan Kepala Samping BG', default=_get_default_penandaan_kepala_samping_bg_img)
    penandaan_kepala_samping_json_img      = fields.Text(string='Penandaan Kepala Samping JSON')
    penandaan_kepala_samping_out_img       = fields.Image(string='Penandaan Kepala Samping OUT')
    deskripsi_kepala_samping               = fields.Text(string='Deskripsi Kepala Samping')

    @api.model
    def _get_default_penandaan_kepala_depan_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.kepala_depan')
    
    penandaan_kepala_depan_bg_img        = fields.Binary(string='Penandaan Kepala Depan BG', default=_get_default_penandaan_kepala_depan_bg_img)
    penandaan_kepala_depan_json_img      = fields.Text(string='Penandaan Kepala Depan JSON')
    penandaan_kepala_depan_out_img       = fields.Image(string='Penandaan Kepala Depan OUT')
    deskripsi_kepala_depan               = fields.Text(string='Deskripsi Kepala Depan')

    @api.model
    def _get_default_penandaan_punggung_tangan_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.punggung_tangan')
    
    penandaan_punggung_tangan_bg_img        = fields.Binary(string='Penandaan Punggung Tangan BG', default=_get_default_penandaan_punggung_tangan_bg_img)
    penandaan_punggung_tangan_json_img      = fields.Text(string='Penandaan Punggung Tangan JSON')
    penandaan_punggung_tangan_out_img       = fields.Image(string='Penandaan Punggung Tangan OUT')
    deskripsi_punggung_tangan               = fields.Text(string='Deskripsi Punggung Tangan')

    @api.model
    def _get_default_penandaan_telapak_tangan_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.telapak_tangan')
    
    penandaan_telapak_tangan_bg_img        = fields.Binary(string='Penandaan telapak Tangan BG', default=_get_default_penandaan_telapak_tangan_bg_img)
    penandaan_telapak_tangan_json_img      = fields.Text(string='Penandaan telapak Tangan JSON')
    penandaan_telapak_tangan_out_img       = fields.Image(string='Penandaan telapak Tangan OUT')
    deskripsi_telapak_tangan               = fields.Text(string='Deskripsi telapak Tangan')

    @api.model
    def _get_default_penandaan_kaki_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.kaki')
    
    penandaan_kaki_bg_img        = fields.Binary(string='Penandaan Kaki BG', default=_get_default_penandaan_kaki_bg_img)
    penandaan_kaki_json_img      = fields.Text(string='Penandaan Kaki JSON')
    penandaan_kaki_out_img       = fields.Image(string='Penandaan Kaki OUT')
    deskripsi_kaki               = fields.Text(string='Deskripsi Kaki')

    # PENANDAAN 
    def action_penandaan_badan(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_badan_bg_img',
            'default_bg_json_name'        : 'penandaan_badan_json_img',
            'default_bg_out_name'         : 'penandaan_badan_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_badan_bg_img,
            'default_penandaan_json_img'  : self.penandaan_badan_json_img,
            'default_penandaan_out_img'   : self.penandaan_badan_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)

    def action_penandaan_kepala_samping(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_kepala_samping_bg_img',
            'default_bg_json_name'        : 'penandaan_kepala_samping_json_img',
            'default_bg_out_name'         : 'penandaan_kepala_samping_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_kepala_samping_bg_img,
            'default_penandaan_json_img'  : self.penandaan_kepala_samping_json_img,
            'default_penandaan_out_img'   : self.penandaan_kepala_samping_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)

    def action_penandaan_kepala_depan(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_kepala_depan_bg_img',
            'default_bg_json_name'        : 'penandaan_kepala_depan_json_img',
            'default_bg_out_name'         : 'penandaan_kepala_depan_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_kepala_depan_bg_img,
            'default_penandaan_json_img'  : self.penandaan_kepala_depan_json_img,
            'default_penandaan_out_img'   : self.penandaan_kepala_depan_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)

    def action_penandaan_punggung_tangan(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_punggung_tangan_bg_img',
            'default_bg_json_name'        : 'penandaan_punggung_tangan_json_img',
            'default_bg_out_name'         : 'penandaan_punggung_tangan_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_punggung_tangan_bg_img,
            'default_penandaan_json_img'  : self.penandaan_punggung_tangan_json_img,
            'default_penandaan_out_img'   : self.penandaan_punggung_tangan_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)

    def action_penandaan_telapak_tangan(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_telapak_tangan_bg_img',
            'default_bg_json_name'        : 'penandaan_telapak_tangan_json_img',
            'default_bg_out_name'         : 'penandaan_telapak_tangan_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_telapak_tangan_bg_img,
            'default_penandaan_json_img'  : self.penandaan_telapak_tangan_json_img,
            'default_penandaan_out_img'   : self.penandaan_telapak_tangan_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)

    def action_penandaan_kaki(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_kaki_bg_img',
            'default_bg_json_name'        : 'penandaan_kaki_json_img',
            'default_bg_out_name'         : 'penandaan_kaki_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_kaki_bg_img,
            'default_penandaan_json_img'  : self.penandaan_kaki_json_img,
            'default_penandaan_out_img'   : self.penandaan_kaki_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)

    signature_pasien     = fields.Binary(string='Tanda Tangan Pasien', tracking=True)
    