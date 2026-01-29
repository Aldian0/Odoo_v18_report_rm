# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

# SURGICAL SAFETY CHECKLIST
# surgikal_safety_checklist
class SkorMonitoringAnastesiLokal(models.Model):
    _name = 'cdn.skor.monitoring.anastesi.lokal'
    _description = 'Skor Monitoring Anastesi Lokal'
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
    
    # Header Information
    nama_pasien = fields.Char(string='Nama', tracking=True)
    tanggal_lahir = fields.Date(string='Tanggal lahir', tracking=True)
    jenis_kelamin = fields.Selection([('laki', 'Laki-laki'), ('perempuan', 'Perempuan')], string='Jenis Kelamin', tracking=True)
    no_rm = fields.Char(string='No. RM', tracking=True)
    tanggal_anetesi = fields.Date(string='Tanggal', tracking=True)
    jam_mulai_anastesi = fields.Char(string='Jam Mulai Anestesi', tracking=True)
    jam_selesai_operasi = fields.Char(string='Jam Selesai Operasi', tracking=True)
    teknik_anastesi = fields.Text(string='Teknik Anestesi', tracking=True)

    # Obat Anastesi
    obat_anatesi_ids = fields.One2many (
        comodel_name='cdn.skor.monitoring.anastesi.lokal.line',
        inverse_name='obat_anetesi_id',
        string='Obat Anastesi', tracking=True
    )

    # Monitoring Data - Line Items
    monitoring_line_ids = fields.One2many(
        comodel_name='cdn.skor.monitoring.anastesi.lokal.line',
        inverse_name='monitoring_id',
        string='Data Monitoring', tracking=True
    )

    jam_ke = fields.Integer(string='Menit Ke', default='5', tracking=True)
    menit_ke = fields.Selection(string='Menit Ke', selection=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55'), ('60', '60')], default='5', tracking=True)
    heart_rate = fields.Float(string='Heart Rate', tracking=True)
    respiration_rate = fields.Float(string='Respiration Rate', tracking=True)
    blood_pressure = fields.Char(string='Blood Pressure', tracking=True)
    saturasi = fields.Float(string='Saturasi', tracking=True)
    kesadaran = fields.Char(string='Kesadaran', tracking=True)

    def rekam(self):
        for rec in self:
            self.env['cdn.skor.monitoring.anastesi.lokal.line'].sudo().create({
                'monitoring_id'     : rec.id,
                'jam_ke'            : rec.jam_ke,
                'heart_rate'        : rec.heart_rate,
                'respiration_rate'  : rec.respiration_rate,
                'blood_pressure'    : rec.blood_pressure,
                'saturasi'          : rec.saturasi,
                'kesadaran'         : rec.kesadaran,
            })

            rec.jam_ke += 5
            if rec.jam_ke == 60:
                self.jam_ke             = False
                # self.invisible_button   = True
                self.heart_rate         = 0.0
                self.respiration_rate   = 0.0
                self.blood_pressure     = "0"  
    
    # Satuan
    satuan                  = fields.Text(string='Satuan', tracking=True)

    # Kesadaran
    kesadaran               = fields.Text(string='Kesadaran', tracking=True)

    # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.skor.monitoring.anastesi.lokal/{self.id}/_generate_print_report',
            'target': 'new',
        }
    def _generate_print_report(self):
        # ===========================
        # BASIC DATA FIELD
        # ===========================
        data_field = {
            'nama_pasien'           : self.pasien_id.name or '',
            'tanggal_lahir'         : self.pasien_id.tanggal_lahir.strftime('%d/%m/%Y') if self.pasien_id.tanggal_lahir else '',
            'jenis_kelamin'         : str(self._get_selection_value(
                model='cdn.pasien',
                field='jenis_kelamin',
                value=self.pasien_id.jenis_kelamin
            ) or ''),
            'no_rm'                 : str(self.pasien_id.no_rm or ''),
            'tanggal_anetesi'       : self.tanggal_anetesi.strftime('%d/%m/%Y') if self.tanggal_anetesi else '',
            'jam_mulai_anastesi'    : str(self.jam_mulai_anastesi or ''),
            'jam_selesai_operasi'   : str(self.jam_selesai_operasi or ''),
            'teknik_anastesi'       : str(self.teknik_anastesi or ''),
            'satuan'                : str(self.satuan or ''),
            'kesadaran'             : str(self.kesadaran or ''),
            'perawat_nama_lengkap'  : str(self.perawat_nama_lengkap or ''),
            'dokter_nama_lengkap'   : str(self.dokter_nama_lengkap or ''),
        }

        # ===========================
        # MONITORING PER MINUTE (5,10,...60)
        # ===========================
        minutes = ['5','10','15','20','25','30','35','40','45','50','55','60']

        # Default kosong
        for m in minutes:
            data_field[f'heart_rate_{m}']       = ''
            data_field[f'respiration_rate_{m}'] = ''
            data_field[f'blood_pressure_{m}']   = ''
            data_field[f'saturasi_{m}']         = ''
            data_field[f'kesadaran_{m}']        = ''

        # Isi berdasarkan line
        for line in self.monitoring_line_ids:
            if line.jam_ke:
                minute = str(line.jam_ke)
                if minute in minutes:
                    data_field[f'heart_rate_{minute}']          = str(line.heart_rate or '-')
                    data_field[f'respiration_rate_{minute}']    = str(line.respiration_rate or '-')
                    data_field[f'blood_pressure_{minute}']      = str(line.blood_pressure or '-')
                    data_field[f'saturasi_{minute}']            = str(line.saturasi or '-')
                    data_field[f'kesadaran_{minute}']           = str(line.kesadaran or '-')

        # ===========================
        # OBAT — MULTILINE FIELD
        # ===========================
        obat_nama_list  = []
        obat_dosis_list = []

        for line in self.obat_anatesi_ids:
            obat_nama_list.append(str(line.nama_obat or ''))
            obat_dosis_list.append(str(line.dosis or ''))

        data_field['obat_nama']  = '\n'.join(obat_nama_list).strip() or '-'
        data_field['obat_dosis'] = '\n'.join(obat_dosis_list).strip() or '-'

        # ===========================
        # GENERATE PDF VIA MAIL MERGE
        # ===========================
        template        = 'cdn_simrs_rekamedis_add/template/klinik_mata/skor_monitoring_anastesi_lokal.docx'

        return self._mail_merge_to_pdf(
            path        = template,
            data_info   = data_field,
            image_info  = [
                {
                    'key'   : '{{logo}}',
                    'value' : self.company_id.logo,
                    'inches': 1
                    }
            ],
            list_info   = []
        )

    # Signature Fields
    perawat_nama_lengkap    = fields.Char(string='Nama Lengkap')
    perawat_tanda_tangan    = fields.Image(string='Tanda Tangan Perawat', max_width=256, max_height=128)
    dokter_nama_lengkap     = fields.Char(string='Nama Lengkap')
    dokter_tanda_tangan     = fields.Image(string='Tanda Tangan Dokter', max_width=256, max_height=128)


class SkorMonitoringAnastesiLokalLine(models.Model):
    _name               = 'cdn.skor.monitoring.anastesi.lokal.line'
    _description        = 'Skor Monitoring Anastesi Lokal - Detail'
    _inherit            = ['mail.thread', 'mail.activity.mixin']
    _order              = "menit_ke asc"

    monitoring_id       = fields.Many2one(
        comodel_name    = 'cdn.skor.monitoring.anastesi.lokal',
        string          = 'Monitoring',
        required        = False,
        ondelete        = 'cascade'
    )
    obat_anetesi_id     = fields.Many2one(
        comodel_name    = 'cdn.skor.monitoring.anastesi.lokal',
        string          = 'Obat Anestesi',
        required        = False,
        ondelete        = 'cascade'
    )
    menit_ke            = fields.Selection(string='Menit Ke', selection=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55'), ('60', '60')], tracking=True)
    jam_ke              = fields.Integer(string='Menit Ke', tracking=True)
    heart_rate          = fields.Float(string='Heart Rate', tracking=True)
    respiration_rate    = fields.Float(string='Respiration Rate', tracking=True)
    blood_pressure      = fields.Char(string='Blood Pressure', tracking=True)
    saturasi            = fields.Float(string='Saturasi', tracking=True)
    kesadaran           = fields.Text(string='kesadaran', tracking=True)





    no          = fields.Integer(string='No.', tracking=True)
    nama_obat   = fields.Char(string='Nama obat yang diberikan', tracking=True)
    dosis       = fields.Char(string='Dosis', tracking=True)
    
