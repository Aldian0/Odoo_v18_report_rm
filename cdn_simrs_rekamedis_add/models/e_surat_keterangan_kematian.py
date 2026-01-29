from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CdnErmSuratKeteranganKematian(models.Model):
    _name = 'cdn.erm.surat.keterangan.kematian'
    _description = 'Surat Keterangan Kematian'
    _inherits = {'cdn.erm.base': 'rm_base_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin', 'cdn.erm.mixin', 'cdn.report.mailmerge']

    rm_base_id = fields.Many2one(comodel_name='cdn.erm.base', string='RM', required=True, ondelete='cascade')

    # Properties untuk dynamic fields
    erm_properties = fields.Properties(definition="rm_id.erm_properties_definition", string="Properties")

    # DATA TAMBAHAN PASIEN
    pendidikan_pasien_id = fields.Many2one(string='Pendidikan Pasien', comodel_name='ref.pendidikan', tracking=True)
    pekerjaan_pasien = fields.Selection(string='Pekerjaan Pasien', selection=[('Tidak/belum bekerja', 'Tidak/belum bekerja'), ('TNI/POLRI', 'TNI/POLRI'), ('PNS', 'PNS'), ('Petani', 'Petani'), ('Wiraswasta', 'Wiraswasta'), ('Karyawan Swasta', 'Karyawan Swasta'), ('Buruh', 'Buruh,'), ('Lainnya', 'Lainnya')], tracking=True)    
    lainnya_pekerjaan_pasien = fields.Char(string='Lainnya Pekerjaan Pasien', tracking=True)
    status_kependudukan = fields.Selection(string='Status Kependudukan', selection=[('Penduduk Tetap', 'Penduduk Tetap'), ('Bukan Penduduk Tetap', 'Bukan Penduduk Tetap')],required=True, tracking=True)
    
    # Alamat lengkap
    alamat_pasien = fields.Char(string='Alamat Pasien', related='pasien_id.street')
    rt_pasien = fields.Char(string='RT Pasien', related='pasien_id.rt_ktp')
    rw_pasien = fields.Char(string='RW Pasien', related='pasien_id.rw_ktp')
    kota_pasien = fields.Char(string='Kota Pasien', related='pasien_id.kota_id_ktp.name')
    propinsi_pasien = fields.Char(string='Provinsi Pasien', related='pasien_id.propinsi_id_ktp.name')
    
    # DATA KEMATIAN
    tanggal_kematian = fields.Datetime(string='Tanggal Kematian', default=fields.Datetime.now, required=True, tracking=True)
    tempat_meninggal = fields.Selection(string='Tempat Meninggal', selection=[('rumah_sakit', 'Rumah Sakit'), ('rumah', 'Rumah'), ('doa', 'DoA'), ('lainnya', 'Lainnya')], required=True, tracking=True)
    lama_dirawat = fields.Char(string='Lama Dirawat', tracking=True)
    lainnya_dirawat = fields.Char(string='Lainnya', tracking=True)
    
    # UMUR SAAT MENINGGAL
    usm_skala_hari = fields.Integer(string='Umur Saat Meninggal (Hari)', help='Diisi jika usia kurang dari 29 hari', tracking=True)
    usm_skala_bulan = fields.Integer(string='Umur Saat Meninggal (Bulan)', help='Diisi jika usia 29 hari sampai 5 tahun', tracking=True)
    usm_skala_tahun = fields.Integer(string='Umur Saat Meninggal (Tahun)', help='Diisi jika usia di atas 5 tahun', tracking=True)

    # RENCANA PEMULASARAN
    rencana_pemulasaran = fields.Selection(string='Rencana Pemulasaran', selection=[('burial', 'Dikubur'), ('cremation', 'Dikremasi'), ('out_city', 'Transportasi Keluar Kota'), ('out_country', 'Transportasi Keluar Negeri')], required=True, tracking=True)
    tanggal_pemulasaran = fields.Date(string='Tanggal Pemulasaran', tracking=True)

    # DATA PENERIMA JENAZAH
    nama_penerima_jenazah = fields.Char(string='Nama Penerima Jenazah', required=True, tracking=True)
    usia_penerima_jenazah = fields.Integer(string='Usia Penerima', required=True, tracking=True)
    jenis_kelamin_penerima_jenazah = fields.Selection(string='Jenis Kelamin Penerima', selection=[('male', 'Laki-laki'), ('female', 'Perempuan')], required=True, tracking=True)
    alamat_penerima_jenazah = fields.Text(string='Alamat Penerima', required=True, tracking=True)
    hubungan_dengan_almarhum = fields.Char(string='Hubungan dengan Almarhum', required=True, tracking=True)
    
    # TANDA TANGAN
    signature_penerima = fields.Binary(string='Tanda Tangan Penerima Jenazah')

    # CONSTRAINTS
    @api.constrains('usm_skala_hari', 'usm_skala_bulan', 'usm_skala_tahun')
    def _check_age_only_one_filled(self):
        for rec in self:
            filled = sum([
                1 if rec.usm_skala_hari else 0,
                1 if rec.usm_skala_bulan else 0,
                1 if rec.usm_skala_tahun else 0,
            ])
            if filled > 1:
                raise ValidationError(
                    'Umur saat meninggal hanya boleh diisi salah satu: Hari, Bulan, atau Tahun.'
                )

    # ACTION PRINT
    def action_print(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/cdn_print_report_pdf/cdn.erm.surat.keterangan.kematian/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {
            'tanggal_kematian': self.tanggal_kematian.strftime('%d/%m/%Y %H:%M') if self.tanggal_kematian else '',
            'tempat_meninggal': self._get_selection_value(model='cdn.erm.surat.keterangan.kematian', field='tempat_meninggal', value=self.tempat_meninggal),
            'lama_dirawat': self.lama_dirawat or '',
            'usm_skala_hari': str(self.usm_skala_hari) if self.usm_skala_hari else '',
            'usm_skala_bulan': str(self.usm_skala_bulan) if self.usm_skala_bulan else '',
            'usm_skala_tahun': str(self.usm_skala_tahun) if self.usm_skala_tahun else '',
            'rencana_pemulasaran': self._get_selection_value(model='cdn.erm.surat.keterangan.kematian', field='rencana_pemulasaran', value=self.rencana_pemulasaran),
            'tanggal_pemulasaran': self.tanggal_pemulasaran.strftime('%d/%m/%Y') if self.tanggal_pemulasaran else '',
            'nama_penerima_jenazah': self.nama_penerima_jenazah or '',
            'usia_penerima_jenazah': str(self.usia_penerima_jenazah) if self.usia_penerima_jenazah else '',
            'jenis_kelamin_penerima_jenazah': self._get_selection_value(model='cdn.erm.surat.keterangan.kematian', field='jenis_kelamin_penerima_jenazah', value=self.jenis_kelamin_penerima_jenazah),
            'alamat_penerima_jenazah': self.alamat_penerima_jenazah or '',
            'hubungan_dengan_almarhum': self.hubungan_dengan_almarhum or '',
            # Data pasien dari rm_base_id
            'nama_pasien': self.pasien_id.name if self.pasien_id else '',
            'nik_pasien': self.nik or '',
            'jenis_kelamin_pasien': self.jenis_kelamin or '',
            'tempat_lahir_pasien': self.tempat_lahir or '',
            'tanggal_lahir_pasien': self.tanggal_lahir.strftime('%d/%m/%Y') if self.tanggal_lahir else '',
        }
        
        template = 'cdn_simrs_rekamedis_add/template/surat_keterangan_kematian.docx'
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
            'default_tipe_dokumen': 'Surat Keterangan Kematian',
            'default_perihal': 'Tanda tangan pada Surat Keterangan Kematian',
        }

        return self.rm_base_id.open_wizard_generate_qr_sign(data)

