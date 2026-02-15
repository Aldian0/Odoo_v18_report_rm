from odoo import _, api, fields, models

class AsuhangGizi(models.Model):
    _name = 'cdn.asuhan.gizi'
    _description = 'Asuhan Gizi'
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

    diagnosis_gizi = fields.Char(string= "Diagnosis Gizi")
    intervensi_gizi_c = fields.Char(string= "Intervensi Gizi")
    kebutuhan_gizi_pasien = fields.Selection([
        ('energi', 'Energi'),
        ('protein', 'Protein'),
        ('lemak', 'Lemak'),
        ('karbohidrat', 'Karbohidrat'),
    ], string='Kebutuhan Gizi Pasien')
    energi = fields.Char(string= "Energi")
    protein = fields.Char(string= "Protein")
    lemak = fields.Char(string= "Lemak")
    karbohidrat = fields.Char(string= "Karbohidrat")
    intervensi_gizi = fields.Selection([
        ('terapi', 'Terapi Diet'),
        ('batuk', 'Batuk Makanan'),
        ('diet', 'Cara Pemberian Diet'),
    ], string='Intervensi Gizi')
    terapi = fields.Char(string= "Terapi Diet")
    batuk = fields.Char(string= "Batuk Makanan")
    diet = fields.Char(string= "Cara Pemberian Diet")

    # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.penandaan.area.operasi.perempuan/{self.id}/_generate_print_report',
            'target': 'new',
        }



    def _generate_print_report(self):
        data_field = {   
            
        }
        template = 'cdn_simrs_rekamedis_add/template/penandaan_area_operasi_perempuan.docx'
        return self._mail_merge_to_pdf(
            path        = template, 
            data_info   = data_field, 
        )

    