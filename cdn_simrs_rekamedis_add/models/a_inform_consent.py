from odoo import _, api, fields, models




class CdnErmDaftariInformConsent(models.Model):
    _inherit                = 'cdn.erm.daftar'

    is_erm_inform_consent = fields.Boolean(
        string              = "Rekamedis Inform Consent", 
        default             = False
    )

    # selection_add
    jenis_rekamedis         = fields.Selection(string='Jenis Rekamedis', 
                                          selection_add=[('inform_consent', 'Inform Consent')])
    erm_inform_consent_template_id     = fields.Many2one(
        comodel_name        ='cdn.inform.consent.template', 
        string              ='Inform Consent'
    )


class CdnInformConsent(models.Model):
    _name           = 'cdn.inform.consent'
    _description    = 'Inform Consent'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin'
    ]

    rm_base_id          = fields.Many2one(
        comodel_name    ='cdn.erm.base', 
        string          ='RM', 
        required        =True, 
        ondelete        ='cascade'
    )
    erm_properties      = fields.Properties(
        definition      ="rm_id.erm_properties_definition",
        string          ="Properties",
    )

    template_id         = fields.Many2one(
        comodel_name    ='cdn.inform.consent.template', 
        string          ='Template', 
        related         ='rm_id.erm_inform_consent_template_id',
        store           =True
    )

    @api.onchange('template_id')
    def _onchange_template_id(self):
        line_data_ids       = [(5,0,0)]
        ket_line_data_ids   = [(5,0,0)]
        if self.template_id:
            for line_data_id in self.template_id.line_ids:
                line_data_ids.append((0,0,{'inform_consent_template_line_id':line_data_id.id}))
            for ket_line_data_id in self.template_id.ket_line_ids:
                ket_line_data_ids.append((0,0,{'inform_consent_template_line_id':ket_line_data_id.id}))

            self.line_ids       = line_data_ids
            self.ket_line_ids   = ket_line_data_ids
        
        for line in self.line_ids:
            line._onchange_inform_consent_template_line_id()
        for ket_line in self.ket_line_ids:
            ket_line._onchange_inform_consent_template_line_id()
    
    line_ids            = fields.One2many(comodel_name='cdn.inform.consent.line', 
                                          inverse_name='inform_consent_id', string='Inform Consent')
    
    ket_line_ids        = fields.One2many(comodel_name='cdn.inform.consent.line', 
                                          inverse_name='inforn_consent_ket_id', string='Inform Consent')
    # def tesss(self):
    #     self._onchange_template_id()
    nama_pj             = fields.Char(string='Nama Pj')
    tanggal_lahir_pj    = fields.Date(string='Tanggal Lahir Pj')
    hubungan_dengan_pasien = fields.Char(string='Hubungan Dengan Pasien')
    is_setuju           = fields.Boolean(string='Setuju')


class CdnInformConsentLine(models.Model):
    _name               = 'cdn.inform.consent.line'
    _description        = 'Inform Consent'

    _inherit = [
        'cdn.simrs.library',
        'cdn.signature.library',
    ]

    inform_consent_id   = fields.Many2one(comodel_name='cdn.inform.consent', string='Inform Consent')
    inforn_consent_ket_id   = fields.Many2one(comodel_name='cdn.inform.consent', string='Inform Consent')
    name                = fields.Char(string='Nama')
    sequence            = fields.Integer(string='Sequence', related='inform_consent_template_line_id.sequence')
    inform_consent_template_line_id = fields.Many2one(comodel_name='cdn.inform.consent.template.line', string='Template')
    
    
    jns_informasi       = fields.Char(string='Jenis Informasi')
    isi_informasi       = fields.Text(string='Isi Informasi')
    keterangan          = fields.Html(string='Konfirmasi')

    centang             = fields.Boolean(string='Tanda (√)')

    is_tdd_dpjp         = fields.Boolean(string='TTD DPJP', help='Dibutuhkan TTD DPJP', related='inform_consent_template_line_id.is_tdd_dpjp')
    is_tdd_pihak_pasien = fields.Boolean(string='TTD Pihak Pasien', help='Dibutuhkan TTD Pihak Pasien', related='inform_consent_template_line_id.is_tdd_pihak_pasien')
    is_ttd_saksi        = fields.Boolean(string='TTD Saksi', help='Dibutuhkan TTD Saksi', related='inform_consent_template_line_id.is_ttd_saksi') 
    

    # ========= TTD PERAWAT ==========
    # qr_ttd_perawat_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    # qr_ttd_perawat_date         = fields.Date('Date', related='qr_ttd_perawat_id.tanggal_tdd')
    # qr_ttd_perawat_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_id.qr_code')
    # qr_ttd_perawat_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_id.partner_id', string='Partner')

    # ========= TTD DOKTER ==========
    qr_ttd_dokter_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_dokter_date         = fields.Date('Date', related='qr_ttd_dokter_id.tanggal_tdd')
    qr_ttd_dokter_code         = fields.Binary(string='QR Code', related='qr_ttd_dokter_id.qr_code')
    qr_ttd_dokter_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_dokter_id.partner_id', string='Partner')

    def signature_generate(self):
        login = False
        if self.env.user.login:
            login = self.env.user.login or ''

        model_id = self.env['ir.model'].sudo().search([('model', '=', self._name)])
        data = {
            'default_username'      : login,
            'default_field_name'    : self.env.context.get('field_name'),
            'default_model_id'      : model_id.id,
            'default_data_id'       : self.id,
            'default_tipe'          : self.env.context.get('tipe_nakes') or '',
            'default_tipe_dokumen'  : self.env.context.get('tipe_dokumen') or '',
            'default_perihal'       : self.env.context.get('perihal') or '',
        }

        return self.open_wizard_generate_qr_sign(data)

    waktu_ttd_pasien    = fields.Datetime(string='Waktu TTD Pasien')
    ttd_pasien_img      = fields.Binary(string='TTD Pasien')
    nama_ttd_pasien     = fields.Char(string='Nama TTD')
    

    waktu_ttd_saksi     = fields.Datetime(string='Waktu TTD Saksi')
    tdd_saksi_img       = fields.Binary(string='TTD Saksi')
    nama_ttd_saksi      = fields.Char(string='Nama TTD Saksi')




    @api.onchange('inform_consent_template_line_id')
    def _onchange_inform_consent_template_line_id(self):

        if self.inform_consent_template_line_id:
            isi_informasi, jns_informasi, keterangan = ( False, False, False)

            ic   = self.inforn_consent_ket_id or self.inform_consent_id or False
            data = {
                "nama_dokter"               : ic.dokter_id.name if ic else "..........................",
                "nama_pasien"               : ic.pasien_id.name if ic else "..........................",
                "umur_pasien"               : ic.pasien_id.usia if ic else "..........................",
                "nama_pj"                   : ic.nama_pj if ic.nama_pj else "..........................",
                "tanggal_lahir_pj"          : self._tanggal_indonesia(tanggal=ic.tanggal_lahir) if ic.tanggal_lahir else "..........................",
                "tgl_lahir_pasien"          : self._tanggal_indonesia(tanggal=ic.tanggal_lahir) if ic.tanggal_lahir else "..........................",
                "alamat_pasien"             : ic.pasien_id.usia if ic else "..........................",
                "hubungan_dengan_pasien"    : ic.hubungan_dengan_pasien if ic.hubungan_dengan_pasien else "..........................",
                # "is_setuju"                 : "Setuju" if ic.is_setuju else "Tidak Setuju",
                "jenis_kel"                 : ic.jenis_kelamin if ic.jenis_kelamin else "..........................",
                "isian"                     : "..........................",
            }

            print(data)
            if self.inform_consent_template_line_id.jns_informasi:
                jns_informasi       = self._replace_value((self.inform_consent_template_line_id.jns_informasi or ''), data)
            if self.inform_consent_template_line_id.isi_informasi:
                isi_informasi       = self._replace_value((self.inform_consent_template_line_id.isi_informasi or ''), data)
            if self.inform_consent_template_line_id.keterangan:
                keterangan          = self._replace_value((self.inform_consent_template_line_id.keterangan or ''), data)

            self.jns_informasi  = jns_informasi
            self.isi_informasi  = isi_informasi
            self.keterangan     = keterangan

            


class CdnInformConsentTemplate(models.Model):
    _name           = 'cdn.inform.consent.template'
    _description    = 'Inform Consent'

    name            = fields.Char(string='Name')
    code            = fields.Char(string='Code')
    
    line_ids        = fields.One2many(comodel_name='cdn.inform.consent.template.line', 
                                    inverse_name='inform_consent_template_id', string='Inform Consent Template')
    
    ket_line_ids    = fields.One2many(comodel_name='cdn.inform.consent.template.line', 
                                    inverse_name='inform_consent_ket_template_id', string='Inform Consent Template')


class CdnInformConsentTemplateLine(models.Model):
    _name                           = 'cdn.inform.consent.template.line'
    _description                    = 'Inform Consent'

    sequence                        = fields.Integer(string='Sequence')
    inform_consent_template_id      = fields.Many2one(comodel_name='cdn.inform.consent.template', string='Template')
    inform_consent_ket_template_id  = fields.Many2one(comodel_name='cdn.inform.consent.template', string='Template')
    jns_informasi                   = fields.Char(string='Jenis Informasi')
    isi_informasi                   = fields.Text(string='Isi Informasi')
    keterangan                      = fields.Html(string='Keterangan')

    # type                            = fields.Selection(string='Type', selection=[('dicentang', 'Dicentang'), ('informasi', 'Hanya Informasi')], default='dicentang')

    is_tdd_dpjp                     = fields.Boolean(string='TTD DPJP', help='Dibutuhkan TTD DPJP')
    is_tdd_pihak_pasien             = fields.Boolean(string='TTD Pihak Pasien', help='Dibutuhkan TTD Pihak Pasien')
    is_ttd_saksi                    = fields.Boolean(string='TTD Saksi', help='Dibutuhkan TTD Saksi') 
