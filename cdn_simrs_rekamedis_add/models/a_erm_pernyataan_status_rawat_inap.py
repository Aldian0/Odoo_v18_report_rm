# cdn_simrs_rekamedis_add/models/persetujuan_tindakan_medis.py

from odoo import _, api, fields, models

class SuratPernyataanStatusRawatInap(models.Model):
    _name = 'cdn.surat.pernyataan.status.rawat.inap'
    _description = 'Surat Pernyataan Status Pasien Rawat Inap'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin'  # jika ada; jika tidak, hapus baris ini
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

    # === DATA PENANDA TANGAN ===
    nama_penanda_tangan             = fields.Char(string='Nama')
    tanggal_lahir_penanda_tangan    = fields.Date(string='Tanggal Lahir')
    alamat_ktp_penanda_tangan       = fields.Text(string='Alamat sesuai KTP')
    alamat_tinggal_penanda_tangan   = fields.Text(string='Alamat Tinggal')
    no_telp_penanda_tangan          = fields.Char(string='No Telp')

    # Hubungan dengan pasien (Selection)
    hubungan_dengan_pasien = fields.Selection([
        ('diri_sendiri', 'Diri Sendiri'),
        ('suami', 'Suami'),
        ('istri', 'Istri'),
        ('anak', 'Anak'),
        ('orang_tua', 'Orang Tua'),
        ('lainnya', 'Lainnya'),
    ], string='Hubungan dengan Pasien')

    # === DATA PASIEN ===
    # Tidak perlu define ulang pasien_id, nama_pasien, dll → sudah diwarisi dari cdn.erm.base
    # Tapi jika butuh field tambahan:

    @api.onchange('pasien_id')
    def _onchange_pasien_id(self):
        if self.pasien_id:
            self.nama_pasien             = self.pasien_id.name
            self.tanggal_lahir_pasien    = self.pasien_id.tanggal_lahir
            self.alamat_ktp_pasien       = self.pasien_id.street
            self.alamat_tinggal_pasien   = self.pasien_id.street
            self.no_telp_pasien          = self.pasien_id.mobile

    nama_pasien             = fields.Char(string='Nama Pasien')
    tanggal_lahir_pasien    = fields.Date(string='Tanggal Lahir Pasien')
    alamat_ktp_pasien       = fields.Text(string='Alamat KTP Pasien')
    alamat_tinggal_pasien   = fields.Text(string='Alamat Tinggal Pasien')
    no_telp_pasien          = fields.Char(string='No Telp Pasien')

    # === STATUS PASIEN ===
    status_pasien = fields.Selection([
        ('umum', 'Pasien Umum'),
        ('jkn', 'Pasien JKN'),
        ('sktm', 'Pasien SKTM'),
        ('asuransi_lain', 'Pasien Asuransi Lain')
    ], string='Status Pasien', required=False)

    # detail pasien umum
    pasien_umum = fields.Selection(string='', selection=[
        ('tidak_punya', 'Pasien Umum, karena tidak mempunyai asuransi apapun'), 
        ('tidak_mau_pakai_asuransi', 'Pasien Umum, karena tidak mau menggunakan hak nya sebagai peserta JKN')])
    
    # Detail JKN (Selection)
    jkn_jenis = fields.Selection([
        ('askes_eks', 'Askes Eks'),
        ('jamsostek_tc', 'Jamsostek/TC'),
        ('jamkesmas_pbi', 'Jamkesmas/PBI'),
        ('tni_polri', 'TNI/POLRI'),
        ('bpjs_mandiri', 'BPJS Mandiri'),
    ], string='Jenis JKN')
    jkn_nomor               = fields.Char(string='Nomor Kartu JKN')

    sktm_surat_keterangan   = fields.Text(string='Surat Keterangan Tidak Mampu')
    asuransi_lain_nama      = fields.Char(string='Pasien Asuransi Lain (Sebutkan)')

    hak_kelas               = fields.Char(string='Hak Kelas')
    naik_kelas_perawatan    = fields.Char(string='Naik Kelas Perawatan')
    ruang_perawatan         = fields.Char(string='Ruang Perawatan')

    fornas                  = fields.Char(string='Fornas')


    # === TANDA TANGAN ===
    ttd_petugas_rumah_sakit = fields.Binary(string='Petugas Rumah Sakit')
    ttd_yang_membuat_pernyataan = fields.Binary(string='Yang Membuat Pernyataan')