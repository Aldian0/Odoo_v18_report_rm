# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import timedelta

class RujukanAntarInstansi(models.Model):
    _name = 'cdn.rujukan.antar.instansi'
    _description = 'Rujukan Antar Instansi'
    
    _inherits       = {'cdn.erm.base': 'rm_base_id'}
    _inherit        = ['mail.thread', 'mail.activity.mixin', 'cdn.erm.mixin', 'cdn.report.mailmerge']
    
    rm_base_id      = fields.Many2one(comodel_name='cdn.erm.base', string='RM', ondelete='cascade')
  
    # Properties untuk dynamic fields
    erm_properties = fields.Properties(definition="rm_id.erm_properties_definition", string="Properties")


    # Dirujuk oleh
    dokter_perujuk = fields.Char("Nama", tracking=True)
    jabatan_perujuk = fields.Char("Jabatan", tracking=True)
    perawat_perujuk = fields.Char("Perawat", tracking=True)

    # Fasilitas asal
    faskes_asal = fields.Selection([
        ('igd', 'IGD'),
        ('rawat_inap', 'Rawat Inap'),
        ('rawat_jalan', 'Rawat Jalan'),
    ], string="Fasilitas Asal", tracking=True)
    tanggal_merujuk = fields.Date(string="Tanggal Merujuk", default=fields.Datetime.now, tracking=True)

    # Komunikasi telepon
    is_komunikasi_telepon = fields.Boolean(string="Komunikasi Telepon", default=False, help="Tandai jika ada komunikasi telepon/fax", tracking=True)
    no_telepon = fields.Char(string="No. Telp", tracking=True)
    no_fax = fields.Char(string="No. Fax", tracking=True)

    # Penerima
    faskes_dituju = fields.Char("Fasilitas kesehatan yang dituju", tracking=True)
    dokter_penerima = fields.Char("Dokter/Perawat/Bidan yang menerima", tracking=True)
    perawat_penerima = fields.Char("Perawat Penerima", tracking=True)

    anamnesis = fields.Text("Anamnesis", tracking=True)

    # Pemeriksaan fisik
    is_gcs = fields.Boolean(string="GCS", default=False)
    gcs = fields.Char("GCS", tracking=True)
    
    is_td = fields.Boolean(string="TD", default=False)
    td = fields.Char("TD", tracking=True)
    
    is_rr = fields.Boolean(string="RR", default=False)
    rr = fields.Char("RR", tracking=True)
    
    is_temperature = fields.Boolean(string="Temp", default=False)
    temp = fields.Char("Temp", tracking=True)
    
    is_vas = fields.Boolean(string="VAS", default=False)
    vas = fields.Char("VAS", tracking=True)


    diagnosa = fields.Text(string="Diagnosa", tracking=True)
    terapi_diberikan = fields.Text(string="Terapi diberikan", tracking=True)
    alasan_merujuk = fields.Text(string="Alasan Merujuk", tracking=True)
    dokumen_disertakan = fields.Char(string="Dokumen yang disertakan", tracking=True)

    # Tanda tangan
    signature_dokter_perujuk = fields.Binary(string='TTD Dokter Perujuk')
    signature_perawat_perujuk = fields.Binary(string='TTD Perawat Perujuk')

    signature_dokter_penerima = fields.Binary(string='TTD Dokter Penerima')
    signature_perawat_penerima = fields.Binary(string='TTD Perawat Penerima')

    tanggal_jam_dirujuk = fields.Datetime(string="Tanggal / Jam Dirujuk", default=fields.Datetime.now, tracking=True)
    tanggal_jam_diterima = fields.Datetime(string="Tanggal / Jam Diterima", default=fields.Datetime.now, tracking=True)


    # ACTION PRINT
    def action_print(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/cdn_print_report_pdf/cdn.rujukan.antar.instansi/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {
            'nama_pasien': self.pasien_id.name if self.pasien_id else '',
        }
        
        template = 'cdn_simrs_rekamedis_add/template/rujukan_antar_instansi.docx'
        return self._mail_merge_to_pdf(
            path=template,
            data_info=data_field,
            image_info=[],
            list_info=[]
        )

    # SIGNATURE GENERATE
    def signature_generate(self):
        login = False
        if self.env.user.login:
            login = self.env.user.login

        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_username': login,
            'default_field_name': self.env.context.get('field_name'),
            'default_model_id': model_id.id,
            'default_data_id': self.id,
            'default_tipe': self.env.context.get('tipe_nakes'),
            'default_tipe_dokumen': 'Rujukan Antar Instansi',
            'default_perihal': 'Tanda tangan pada Rujukan Antar Instansi',
        }

        return self.rm_base_id.open_wizard_generate_qr_sign(data)

