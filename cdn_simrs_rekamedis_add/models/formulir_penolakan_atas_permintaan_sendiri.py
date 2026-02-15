from odoo import _, api, fields, models

class FormulirPenolakanAtasPermintaanSendiri(models.Model):
    _name = 'cdn.formulir.penolakan.atas.permintaan.sendiri'
    _description = 'Formulir Penolakan Atas Permintaan Sendiri'
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
    
    nama_pengisi = fields.Char(string='Nama')
    tgl_lahir_pengisi = fields.Date(string='Tanggal Lahir')
    nik_pengisi = fields.Char(string='NIK')
    alamat_pengisi = fields.Text(string='Alamat')
    no_hp_pengisi = fields.Char(string='No HP')

    nama = fields.Char(string='Nama')
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    nik = fields.Char(string='NIK')
    alamat = fields.Text(string='Alamat')
    no_hp = fields.Char(string='No HP')
    nomor_rm_pasien = fields.Char(string='No RM Pasien', related='pasien_id.no_rm', readonly=True)
    nama_pasien = fields.Char(string='Terhadap Pasien', related='pasien_id.name', readonly=True)
    hubungan = fields.Selection([
        ('diri_sendiri', 'Diri Sendiri'),
        ('ortu', 'Orang Tua'),
        ('anak', 'Anak'),
        ('wali', 'Wali'),
        ('lainnya', 'Lainnya'),
    ], string='Hubungan Dengan Pasien')
    hubungan_lainnya = fields.Char(string='Hubungan Lainnya')

    # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.tess.rm/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {   
            'nama'           : self.nama_pengisi or '',
            'tgl_lahir'      : self.tgl_lahir_pengisi or '',
            'nik'            : self.nik_pengisi or '',
            'alamat'         : self.alamat_pengisi or '',
            'no_hp'          : self.no_hp_pengisi or '',
            'nomor_rm_pasien': self.nomor_rm_pasien or '',


        }
        template = 'cdn_simrs_rekamedis_add/template/formulir_penolakan_atas_permintaan_sendiri.docx'
        return self._mail_merge_to_pdf(
            path        = template, 
            data_info   = data_field, 
        )

    signature_saksi     = fields.Binary(string='Tanda Tangan Pasien') 
    signature_pasien     = fields.Binary(string='Tanda Tangan Pasien')   
    

    