from odoo import _, api, fields, models


class EdukasiPasien(models.Model):
    _name           = 'cdn.edukasi.pasien'
    _description    = 'Edukasi Pasien'

    _inherits       = {'cdn.erm.base': 'rm_base_id'}
    _inherit        = ['mail.thread', 'mail.activity.mixin', 'cdn.erm.mixin', 'cdn.report.mailmerge']

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade',
    )
    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )


    # asessment_kebutuhan_pendidikan
    pendidikan_id       = fields.Many2one('ref.pendidikan', string='Pendidikan', tracking=True)
    hambatan            = fields.Char(string='Hambatan', help="Hambatan yang dihadapi saat", tracking=True)
    bahasa_ids          = fields.Many2many('ref.bahasa', string='Bahasa', tracking=True)
    penterjemah         = fields.Selection(string='Penterjemah', selection=[('tidak_perlu', 'Tidak Perlu'), ('perlu', 'Perlu'),], default='tidak_perlu', tracking=True)
    ket_peneterjemah    = fields.Char(string='Keterangan', tracking=True)

    # kepercayaan budaya 
    budaya_ids          = fields.Many2many('ref.budaya', string='Pengaruh Pepercayaan Budaya', tracking=True)

    # rencana edukasi kebutuhan pembelajaran pasien
    hak_kewajiban       = fields.Boolean(string='Hak dan Kewajiban Pasien/Keluarga', tracking=True)
    dpjp                = fields.Boolean(string='Dokter Spesialis/DPJP', tracking=True)
    diet_pasien         = fields.Boolean(string='Diet dan Nutrisi', tracking=True)
    keperawatan         = fields.Boolean(string='Keperawatan', tracking=True)
    rehabilitasi        = fields.Boolean(string='Rehabilitasi Medis', tracking=True)
    nyeri               = fields.Boolean(string='Manangement Nyeri', tracking=True)
    farmasi             = fields.Boolean(string='Farmasi', tracking=True)
    case_manager        = fields.Boolean(string='Case Manager', tracking=True)
    lain_lain           = fields.Boolean(string='Lain-lain', tracking=True)

    # edukasi admisi
    edu_hak_kewajiban_ids      = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='hak_kewajiban_id', string='Edukasi Admisi', tracking=True )


    @api.onchange('hak_kewajiban')
    def _onchange_hak_kewajiban(self):
        if self.hak_kewajiban:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'hak_kewajiban')], limit=1)
            # print(template)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:
                    edukasi.create({
                        'name': t.name,
                        'hak_kewajiban_id': self.id,
                    })
        else:
            self.edu_hak_kewajiban_ids = False



    edu_dpjp_ids               = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='dpjp_id', string='Edukasi DPJP', tracking=True )
    @api.onchange('dpjp')
    def _onchange_dpjp(self):
        if self.dpjp:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'dpjp')], limit=1)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:
                # self.edu_admisi_ids = 
                    edukasi.create({
                        'name': t.name,
                        'dpjp_id': self.id,
                    })
        else:
            self.edu_dpjp_ids = False

    diet_pasien_ids           = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='diet_pasien_id', string='Edukasi Diet', tracking=True )
    
    @api.onchange('diet_pasien')
    def _onchange_diet_pasien(self):
        if self.diet_pasien:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'diet_pasien')], limit=1)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:
                # self.edu_admisi_ids =
                    edukasi.create({
                        'name': t.name,
                        'diet_pasien_id': self.id,
                    })
        else:
            self.diet_pasien_ids = False
    
    keperawatan_ids           = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='keperawatan_id', string='Edukasi Keperawatan', )
    
    @api.onchange('keperawatan')
    def _onchange_keperawatan(self):
        if self.keperawatan:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'keperawatan')], limit=1)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:
                    edukasi.create({
                        'name': t.name,
                        'keperawatan_id': self.id,
                    })
        else:
            self.keperawatan_ids = False

    rehabilitasi_ids           = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='rehabilitasi_id', string='Edukasi Rehabilitasi', tracking=True )
    @api.onchange('rehabilitasi')
    def _onchange_rehabilitasi(self):
        if self.rehabilitasi:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'rehabilitasi')], limit=1)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:

                    edukasi.create({
                        'name': t.name,
                        'rehabilitasi_id': self.id,
                    })
        else:
            self.rehabilitasi_ids = False


    nyeri_ids           = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='nyeri_id', string='Edukasi Nyeri', tracking=True )
    @api.onchange('nyeri')
    def _onchange_nyeri(self):
        if self.nyeri:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'nyeri')], limit=1)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:
                    edukasi.create({
                        'name': t.name,
                        'nyeri_id': self.id,     
                    })
        else:
            self.nyeri_ids = False
    farmasi_ids           = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='farmasi_id', string='Edukasi Farmasi', tracking=True )
    
    @api.onchange('farmasi')
    def _onchange_farmasi(self):
        if self.farmasi:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'farmasi')], limit=1)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:
                    edukasi.create({
                        'name': t.name,
                        'farmasi_id': self.id,
                    })
        else:
            self.farmasi_ids = False
    
    case_manager_ids           = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='case_manager_id', string='Edukasi Case Manager', tracking=True )
    
    @api.onchange('case_manager')
    def _onchange_case_manager(self):
        if self.case_manager:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'case_manager')], limit=1)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:
                    edukasi.create({
                        'name': t.name,
                        'case_manager_id': self.id,
                    })
        else:
            self.case_manager_ids = False

    lain_lain_ids           = fields.One2many(comodel_name='cdn.line.edukasi.pasien', inverse_name='lain_lain_id', string='Edukasi Lain Lain', tracking=True )
    
    @api.onchange('lain_lain')
    def _onchange_lain_lain(self):
        if self.lain_lain:
            template = self.env['cdn.line.edukasi.template'].sudo().search([('name', '=', 'lain_lain')], limit=1)
            edukasi = self.env['cdn.line.edukasi.pasien'].sudo()
            if template:
                for t in template.edu_name_ids:
                    edukasi.create({
                        'name': t.name,
                        'lain_lain_id': self.id,
                    })
        else:
            self.lain_lain_ids = False

class RefBudaya(models.Model):
    _name = 'ref.budaya'
    _description = 'Ref Budaya'

    name = fields.Char(string='Name')

class CdnLineEdukasiPasien(models.Model):
    _name = 'cdn.line.edukasi.pasien'
    _description = 'Cdn Line Edukasi Pasien'

    name                = fields.Char(string='Name')
    tanggal             = fields.Datetime(string='Tanggal', default=fields.Datetime.now)
    metode              = fields.Selection(string='Metode', default='diskusi', selection=[('diskusi', 'Diskusi'), ('ceramah', 'Ceramah'),('praktek', 'Praktek'),('demo', 'Demo')])
    evaluasi            = fields.Selection(string='Evaluasi', default='mengerti', selection=[('mengerti', 'Mengerti'), ('kurang_mengerti', 'Kurang Mengerti'),('tidak_mengerti', 'Tidak Mengerti')])

    sasaran             = fields.Selection(string='Sasaran', default='keluarga', selection=[('pasien', 'Pasien'), ('keluarga', 'Keluarga'),])

    alat_edukasi        = fields.Selection(string='Alat Edukasi', default='model', selection=[('leafleat', 'Leafleat/Banner'), ('model', 'Model/Peraga')])
    hak_kewajiban_id    = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    dpjp_id             = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    diet_pasien_id      = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    keperawatan_id      = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    rehabilitasi_id     = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    nyeri_id            = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    farmasi_id          = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    case_manager_id     = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    lain_lain_id        = fields.Many2one(comodel_name='cdn.edukasi.pasien', string='Edukasi')
    
    

# access_manager_cdn_line_edukasi_template,access_cdn_line_edukasi_template,model_cdn_line_edukasi_template,base.group_user,1,1,1,1
# access_cdn_line_edukasi_template,access_cdn_line_edukasi_template,model_cdn_line_edukasi_template,cdn_simrs_base.group_simrs_manager,1,1,1,0

class RefEdukasiPasien(models.Model):
    _name = 'cdn.ref.edukasi.pasien'
    _description = 'Ref Edukasi Pasien'

    name                = fields.Char(string='Name')
    template_id         = fields.Many2one(comodel_name='cdn.line.edukasi.template', string='Template')
class CdnLineEdukasiTemplate(models.Model):
    _name = 'cdn.line.edukasi.template'
    _description = 'Cdn Line Edukasi Template'
    name                = fields.Selection(string='name', 
                            selection=[('hak_kewajiban', 'Hak dan Kewajiban Pasien/Keluarga'), 
                                        ('dpjp', 'Dokter Spesialis/DPJP'),
                                        ('diet_pasien', 'Diet dan Nutrisi'),
                                        ('keperawatan', 'Keperawatan'),
                                        ('rehabilitasi', 'Rehabilitasi Medis'),
                                        ('nyeri', 'Manangement Nyeri'),
                                        ('farmasi', 'Farmasi'),
                                        ('case_manager', 'Case Manager'),
                                        ('lain_lain', 'Lain-Lain'),
                                        ])

    edu_name_ids        = fields.One2many(comodel_name='cdn.ref.edukasi.pasien', inverse_name='template_id', string='Edukasi Template')

