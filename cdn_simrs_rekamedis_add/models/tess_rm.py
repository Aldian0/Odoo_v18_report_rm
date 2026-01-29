from odoo import _, api, fields, models

class TessRm(models.Model):
    _name           = 'cdn.tess.rm'
    _description    = 'Tess Rm'
    _inherits       = {
        'cdn.erm.base': 'rm_base_id',
        }
    _inherit        = [
        'mail.thread', 
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
        ]
    
    rm_base_id      = fields.Many2one(comodel_name='cdn.erm.base', string='RM', required=True, ondelete='cascade')

    tess            = fields.Char(string='Tess')
    tes_selection   = fields.Selection(string='Selection', selection=[('1', 'Satu'), ('2', 'Dua'),])
    gambar_tess     = fields.Binary(string='Gambar Tess')
    tes_list_ids    = fields.Many2many('res.partner', string='Tes List')   

    # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.tess.rm/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {   
            'tess'           : self.tess or '',
            'selection_tess' : self._get_selection_value(model='cdn.tess.rm', field='tes_selection', value=self.tes_selection),
        }
        data_image = [
            {
                'key'       : '{{gambar}}',
                'value'     : self.gambar_tess,
                'inches'    : 2,
            }
        ]
        tes_list = []
        for tes in self.tes_list_ids:
            tes_list.append({
                'partner_name'  : tes.name or '',
                'phone'         : tes.phone or '',
                'email'         : tes.email or '',
            })
        data_list = [
            {
                'key'   : 'partner_name',
                'value' : tes_list,
            }
        ]
        template = 'cdn_simrs_rekamedis_add/template/tesss.docx'
        return self._mail_merge_to_pdf(
            path        = template, 
            data_info   = data_field, 
            image_info  = data_image, 
            list_info   = data_list
        )

    @api.model
    def _get_default_penandaan_tess_bg_img(self):
        return self.env['cdn.erm.daftar.line'].sudo()._get_image_code('cdn_simrs_rekamedis_add.tesssting')
    
    penandaan_tess_bg_img        = fields.Binary(string='Penandaan Tess BG', default=_get_default_penandaan_tess_bg_img)
    penandaan_tess_json_img      = fields.Text(string='Penandaan Tess JSON')
    penandaan_tess_out_img       = fields.Image(string='Penandaan Tess OUT')
    deskripsi_tess               = fields.Text(string='Deskripsi Tess')

    # PENANDAAN 
    def action_penandaan(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_bg_name'             : 'penandaan_tess_bg_img',
            'default_bg_json_name'        : 'penandaan_tess_json_img',
            'default_bg_out_name'         : 'penandaan_tess_out_img',
            'default_model_id'            : model_id.id,
            'default_data_id'             : self.id,
            'default_penandaan_bg_img'    : self.penandaan_tess_bg_img,
            'default_penandaan_json_img'  : self.penandaan_tess_json_img,
            'default_penandaan_out_img'   : self.penandaan_tess_out_img,
            'default_height'              : '100', #px
            'default_width'               : '100', #px
        }

        return self.rm_base_id.open_wizard_canvas(data)