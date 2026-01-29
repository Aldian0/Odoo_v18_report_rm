from odoo import _, api, fields, models


class CdnErmDaftarNursingCareplan(models.Model):
    _inherit                = 'cdn.erm.daftar'
    is_erm_nursing_careplan = fields.Boolean(
        string              = "Rekamedis Nursing Careplan", 
        default             = False
    )
    jenis_rekamedis    = fields.Selection(string='Jenis Rekamedis', 
                                          selection_add=[('nursing_careplan', 'Nursing Careplan')])
    erm_nursing_careplan_template_id     = fields.Many2one(
        comodel_name        ='cdn.nursing.careplan.template', 
        string              ='Nursing Careplan'
    )
    

class CdnNursingCareplan(models.Model):
    _name               = 'cdn.nursing.careplan'
    _description        = 'Nursing Careplan'
    
    _inherits           = {
        'cdn.erm.base': 'rm_base_id',
        }
    _inherit            = [
        'mail.thread', 
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
        
        ]
    
    rm_base_id          = fields.Many2one(
        comodel_name    ='cdn.erm.base', string='RM', 
        required        =True, 
        ondelete        ='cascade'
    )

    erm_properties      = fields.Properties(
        definition      ="rm_id.erm_properties_definition",
        string          ="Properties",
    )

    template_id         = fields.Many2one(
        comodel_name    ='cdn.nursing.careplan.template', 
        string          ='Template', 
        related         ='rm_id.erm_nursing_careplan_template_id',
    )

    @api.onchange('template_id')
    def _onchange_template_id(self):
        line_data_ids               = [(5,0,0)]
        line_diagnosa_ids           = [(5,0,0)]
        line_tujuan_ids             = [(5,0,0)]
        line_intervensi_ids         = [(5,0,0)]
        if self.template_id:
            for line_data_id in self.template_id.line_data_ids:
                line_data_ids.append((0,0,{'nursing_careplan_template_line_id':line_data_id.id,'name':line_data_id.name}))
            for line_diagnosa_id in self.template_id.line_diagnosa_ids:
                line_diagnosa_ids.append((0,0,{'nursing_careplan_template_line_id':line_diagnosa_id.id,'name':line_data_id.name}))
            for line_tujuan_id in self.template_id.line_tujuan_ids:
                line_tujuan_ids.append((0,0,{'nursing_careplan_template_line_id':line_tujuan_id.id,'name':line_data_id.name}))
            for line_intervensi_id in self.template_id.line_intervensi_ids:
                line_intervensi_ids.append((0,0,{'nursing_careplan_template_line_id':line_intervensi_id.id,'name':line_data_id.name}))
            self.line_data_ids       = line_data_ids
            self.line_diagnosa_ids   = line_diagnosa_ids
            self.line_tujuan_ids     = line_tujuan_ids
            self.line_intervensi_ids = line_intervensi_ids
            

    line_data_ids       = fields.One2many(
        comodel_name    ='cdn.nursing.careplan.line', 
        inverse_name    ='nursing_careplan_data_id', 
        string          ='Penilaian Nursing Careplan Template'
    )
    line_diagnosa_ids   = fields.One2many(
        comodel_name    ='cdn.nursing.careplan.line', 
        inverse_name    ='nursing_careplan_diagnosa_id', 
        string          ='Diagnosa'
    )
    line_tujuan_ids     = fields.One2many(
        comodel_name    ='cdn.nursing.careplan.line', 
        inverse_name    ='nursing_careplan_tujuan_id', 
        string          ='Tujuan'
    )
    line_intervensi_ids = fields.One2many(
        comodel_name    ='cdn.nursing.careplan.line', 
        inverse_name    ='nursing_careplan_intervensi_id', 
        string          ='Penilaian'
    )


class CdnNursingCareplanLine(models.Model):
    _name                       = 'cdn.nursing.careplan.line'
    _description                = 'Nursing Careplan Line'

    nursing_careplan_template_line_id = fields.Many2one(
        comodel_name            ='cdn.nursing.careplan.template.line', string='Template', 
    )
    sequence                    = fields.Integer(
        string                  ='Sequence',
        related                 ='nursing_careplan_template_line_id.sequence',
        store                   =True
    )
    tempate_type                = fields.Selection(
        related                 ='nursing_careplan_template_line_id.tempate_type',
    )
    cheklist                    = fields.Boolean(string='Cheklist')
    name                        = fields.Char(string='Name')
    nursing_careplan_data_id    = fields.Many2one(
        comodel_name            ='cdn.nursing.careplan', string='Nursing Careplan', 
        ondelete                ='cascade'
    )
    nursing_careplan_diagnosa_id = fields.Many2one(
        comodel_name            ='cdn.nursing.careplan', string='Nursing Careplan', 
        ondelete                ='cascade'
    )
    nursing_careplan_tujuan_id  = fields.Many2one(
        comodel_name            ='cdn.nursing.careplan', string='Nursing Careplan', 
        ondelete                ='cascade'
    )
    nursing_careplan_intervensi_id = fields.Many2one(
        comodel_name            ='cdn.nursing.careplan', string='Nursing Careplan', 
        ondelete                ='cascade'
    )

    @api.onchange('nursing_careplan_template_line_id')
    def _onchange_nursing_careplan_template_line_id(self):
        if self.nursing_careplan_template_line_id:
            self.name = self.nursing_careplan_template_line_id.name
    

class CdnNursingCareplanTemplate(models.Model):
    _name               = 'cdn.nursing.careplan.template'
    _description        = 'Nursing Careplan Template'

    name                = fields.Char(string='Name')
    code                = fields.Char(string='Code')
    line_data_ids       = fields.One2many(
        comodel_name    ='cdn.nursing.careplan.template.line', 
        inverse_name    ='nursing_careplan_data_template_id', 
        string          ='Penilaian Nursing Careplan Template'
    )
    line_diagnosa_ids   = fields.One2many(
        comodel_name    ='cdn.nursing.careplan.template.line', 
        inverse_name    ='nursing_careplan_diagnosa_template_id', 
        string          ='Diagnosa'
    )
    line_tujuan_ids     = fields.One2many(
        comodel_name    ='cdn.nursing.careplan.template.line', 
        inverse_name    ='nursing_careplan_tujuan_template_id', 
        string          ='Tujuan'
    )
    line_intervensi_ids = fields.One2many(
        comodel_name    ='cdn.nursing.careplan.template.line', 
        inverse_name    ='nursing_careplan_intervensi_template_id', 
        string          ='Penilaian'
    )

class CdnNursingCareplanTemplateLine(models.Model):
    _name               = 'cdn.nursing.careplan.template.line'
    _description        = 'Nursing Careplan Template Line'

    sequence            = fields.Integer(string='Sequence', default=10)

    name                = fields.Char(string='Name')
    TEMPLATE_TYPE       = [('dicentang', 'Dicentang'), ('informasi', 'Hanya Informasi')]
    tempate_type        = fields.Selection(string='Template', 
        selection       = TEMPLATE_TYPE, default='dicentang')
    
    nursing_careplan_data_template_id = fields.Many2one(
        comodel_name    ='cdn.nursing.careplan.template', 
        string          ='Nursing Careplan Template', 
        ondelete        ='cascade'
    )
    nursing_careplan_diagnosa_template_id = fields.Many2one(
        comodel_name    ='cdn.nursing.careplan.template', 
        string          ='Nursing Careplan Template', 
        ondelete        ='cascade'
    )
    nursing_careplan_tujuan_template_id = fields.Many2one(
        comodel_name    ='cdn.nursing.careplan.template', 
        string          ='Nursing Careplan Template', 
        ondelete        ='cascade'
    )
    nursing_careplan_intervensi_template_id = fields.Many2one(
        comodel_name    ='cdn.nursing.careplan.template', 
        string          ='Nursing Careplan Template', 
        ondelete        ='cascade'
    )