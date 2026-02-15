from odoo import _, api, fields, models

class TessRm(models.Model):
    _name           = 'cdn.resiko.jatuh.morse'
    _description    = 'Resiko Jatuh Skala Morse'
    _inherits       = {
        'cdn.erm.base': 'rm_base_id',
        }
    _inherit        = [
        'mail.thread', 
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
        ]
    
    rm_base_id          = fields.Many2one(comodel_name='cdn.erm.base', string='RM', required=True, ondelete='cascade')

    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )
    line_ids            = fields.One2many(comodel_name='cdn.resiko.jatuh.morse.line', inverse_name='resiko_jatuh_id', string='Penilaian Resiko Jatuh Skala Morse')


class CdnReikoJatuhMorseLine(models.Model):
    _name                   = 'cdn.resiko.jatuh.morse.line'
    _description            = 'Cdn Resiko Jatuh Morse Line'

    # sequence                = fields.Integer(string='Sequence', default=0)

    tanggal                 = fields.Datetime(string='Tanggal', default=fields.Datetime.now)
    resiko_jatuh_id         = fields.Many2one(comodel_name='cdn.resiko.jatuh.morse', string='RM', required=True, ondelete='cascade')
    
    # Penilaian Resiko Jatuh Skala Morse
    morse_riwayat_jatuh     = fields.Selection(string='Riwayat Jatuh', selection=[('tidak', 'Tidak'), ('ya', 'Ya'),], default='tidak', tracking=True)
    morse_1                 = fields.Integer(string='Score Riwayat Jatuh')
    morse_diag_sekunder     = fields.Selection(string='Diagnosis Sekunder', selection=[('tidak', 'Tidak'), ('ya', 'Ya'),], default='tidak', tracking=True)
    morse_2                 = fields.Integer(string='Score Diagnosis Sekunder')
    morse_alat_bantu        = fields.Selection(string='Skala Alat Bantu', selection=[('tidak ada', 'Tidak Ada/Kursi Roda/Perawat/Tirah Baring'), ('tongkat', 'Tongkat/Alat Penopang'),('pegangan','Pegangan Perabot')], default='tidak ada', tracking=True)
    morse_3                 = fields.Integer(string='Score Alat Bantu')
    morse_pasang_infus      = fields.Selection(string='Terpasang Infus', selection=[('tidak', 'Tidak'), ('ya', 'Ya'),], default='tidak', tracking=True)
    morse_4                 = fields.Integer(string='Score Terpasang Infus')
    morse_gaya_jalan        = fields.Selection(string='Gaya Berjalan', selection=[('normal', 'Normal/Tirah Baring/Imobilisasi'), ('lemah', 'Lemah'),('terganggu','Terganggu')], default='normal', tracking=True)
    morse_5                 = fields.Integer(string='Score Gaya Berjalan')
    morse_status_mental     = fields.Selection(string='Status Mental', selection=[('sadar', 'Sadar Kemampuan Sendiri'), ('sering lupa', 'Sering Lupa Keterbatasan Diri'),], default='sadar', tracking=True)
    morse_6                 = fields.Integer(string='Score Status Mental')
    morse_skor              = fields.Integer(string='Skor Total Morse', compute='_compute_morse_skor', store=True)
    morse_tingkat_resiko    = fields.Selection(string='Tingkat Resiko', selection=[('rendah', 'Rendah, Skor 0-24 '), ('sedang', 'Sedang, Skor 25-45'),('tinggi','Tinggi, Skor > 45')], default='rendah', compute='_compute_morse_skor', store=True)
    
    @api.depends('morse_riwayat_jatuh', 'morse_diag_sekunder', 'morse_alat_bantu', 'morse_pasang_infus', 'morse_gaya_jalan', 'morse_status_mental')
    def _compute_morse_skor(self):
        for rec in self:
            morse_skor = 0
            if rec.morse_riwayat_jatuh == 'ya':
                rec.morse_1=25
                morse_skor += 25
            if rec.morse_diag_sekunder == 'ya':
                rec.morse_2=25
                morse_skor += 25
            if rec.morse_alat_bantu == 'tongkat':
                rec.morse_3=15
                rec.morse_skor += 15
            if rec.morse_alat_bantu == 'pegangan':
                rec.morse_3=30
                morse_skor += 30
            if rec.morse_pasang_infus == 'ya':
                rec.morse_4=20
                morse_skor += 20
            if rec.morse_gaya_jalan == 'lemah':
                rec.morse_5=10
                morse_skor += 10
            if rec.morse_gaya_jalan == 'terganggu':
                rec.morse_5=20
                morse_skor += 20
            if rec.morse_status_mental == 'sering lupa':
                rec.morse_6=15
                morse_skor += 15
            rec.morse_skor = morse_skor
            if morse_skor <= 24:
                rec.morse_tingkat_resiko = 'rendah'
            elif morse_skor <= 45:
                rec.morse_tingkat_resiko = 'sedang'
            else:
                rec.morse_tingkat_resiko = 'tinggi'



            # if rec.morse_tingkat_resiko:
            #     if rec.morse_tingkat_resiko == 'rendah':
            #         rec.intervensi_a = True
            #         rec.intervensi_b = False
            #         rec.intervensi_c = True
            #     elif rec.morse_tingkat_resiko == 'sedang':
            #         rec.intervensi_a = True
            #         rec.intervensi_b = True
            #         rec.intervensi_c = True
            #         rec.intervensi_d = True
            #         rec.intervensi_e = True
            #     elif rec.morse_tingkat_resiko == 'tinggi':
            #         rec.intervensi_a = True
            #         rec.intervensi_b = True
            #         rec.intervensi_c = True
            #         rec.intervensi_d = True
            #         rec.intervensi_e = True
            #         rec.intervensi_f = True
            #         rec.intervensi_g = True


    intervensi_a = fields.Boolean(
        string='Pastikan tempat tidur/brancart posisi rendah & roda terkunci'
    )

    intervensi_b = fields.Boolean(
        string='Pasang pagar tempat tidur/brancart'
    )

    intervensi_c = fields.Boolean(
        string='Orientasikan pasien/penunggu tentang lingkungan/ruangan'
    )

    intervensi_d = fields.Boolean(
        string='Edukasi keluarga tentang pencegahan jatuh'
    )

    intervensi_e = fields.Boolean(
        string='Pasang kancing kuning pada gelang identifikasi'
    )

    intervensi_f = fields.Boolean(
        string='Pasang tanda “Risiko Pasien Jatuh” di tempat tidur'
    )

    intervensi_g = fields.Boolean(
        string='Lakukan fiksasi fisik (dengan persetujuan keluarga)'
    )


