# # cdn_simrs_rekamedis_add/models/persetujuan_tindakan_medis.py

# from odoo import _, api, fields, models

# class SuratPernyataanStatusRawatInap(models.Model):
#     _name = 'cdn.surat.pernyataan.status.rawat.inap'
#     _description = 'Surat Pernyataan Status Pasien Rawat Inap'
#     _inherits = {
#         'cdn.erm.base': 'rm_base_id',
#     }
#     _inherit = [
#         'mail.thread',
#         'mail.activity.mixin',
#         'cdn.erm.mixin'  # jika ada; jika tidak, hapus baris ini
#     ]

#     rm_base_id = fields.Many2one(
#         comodel_name='cdn.erm.base',
#         string='RM',
#         required=True,
#         ondelete='cascade'
#     )

#     # === DATA PENANDA TANGAN ===
#     nama_penanda_tangan = fields.Char(string='Nama')
#     tanggal_lahir_penanda_tangan = fields.Date(string='Tanggal Lahir')
#     alamat_ktp_penanda_tangan = fields.Text(string='Alamat sesuai KTP')
#     alamat_tinggal_penanda_tangan = fields.Text(string='Alamat Tinggal')
#     no_telp_penanda_tangan = fields.Char(string='No Telp')

#     # Hubungan dengan pasien (checkbox)
#     hubungan_dengan_pasien_diri_sendiri = fields.Boolean(string='Diri Sendiri')
#     hubungan_dengan_pasien_suami = fields.Boolean(string='Suami')
#     hubungan_dengan_pasien_istri = fields.Boolean(string='Istri')
#     hubungan_dengan_pasien_anak = fields.Boolean(string='Anak')
#     hubungan_dengan_pasien_orang_tua = fields.Boolean(string='Orang tua')
#     hubungan_dengan_pasien_lainnya = fields.Boolean(string='Lainnya')


    
#     # === DATA PASIEN ===
#     # Tidak perlu define ulang pasien_id, nama_pasien, dll → sudah diwarisi dari cdn.erm.base
#     # Tapi jika butuh field tambahan:
#     alamat_tinggal_pasien = fields.Text(string='Alamat Tinggal Pasien')
#     no_telp_pasien = fields.Char(string='No Telp Pasien')

#     # === STATUS PASIEN ===
#     status_pasien = fields.Selection([
#         ('umum', 'Pasien Umum'),
#         ('jkn', 'Pasien JKN'),
#         ('sktm', 'Pasien SKTM'),
#         ('asuransi_lain', 'Pasien Asuransi Lain')
#     ], string='Status Pasien', required=False)

#     # Detail JKN
#     jkn_jenis_askes_eks = fields.Boolean(string='Askes Eks')
#     jkn_jenis_jamsostek_tc = fields.Boolean(string='Jamsostek/TC')
#     jkn_jenis_jamkesmas_pbi = fields.Boolean(string='Jamkesmas/PBI')
#     jkn_jenis_tni_polri = fields.Boolean(string='TNI/POLRI')
#     jkn_jenis_bpjs_mandiri = fields.Boolean(string='BPJS Mandiri')
#     jkn_nomor = fields.Char(string='Dengan Nomor JKN')

#     sktm_surat_keterangan = fields.Text(string='Surat Keterangan Tidak Mampu')
#     asuransi_lain_nama = fields.Char(string='Pasien Asuransi Lain (Sebutkan)')

#     # === TANDA TANGAN ===
#     ttd_petugas_rumah_sakit = fields.Binary(string='Petugas Rumah Sakit')
#     ttd_yang_membuat_pernyataan = fields.Binary(string='Yang membuat pernyataan')