# # -*- coding: utf-8 -*-

# from odoo import _, api, fields, models

# class TransferPasienAntarUnit(models.Model):
#     _name = 'cdn.transfer.pasien.antar.unit'
#     _description = 'Transfer Pasien Antar Unit Pelayanan'
#     _inherits = {
#         'cdn.erm.base': 'rm_base_id',
#     }
#     _inherit = [
#         'mail.thread',
#         'mail.activity.mixin',
#         'cdn.erm.mixin'
#     ]

#     rm_base_id = fields.Many2one(
#         comodel_name='cdn.erm.base',
#         string='RM',
#         required=True,
#         ondelete='cascade'
#     )

#     # === TRANSFER DETAILS ===
#     ruangan_asal = fields.Char(string='Ruangan Asal')
#     ruangan_tujuan = fields.Char(string='Ruangan Tujuan')
#     tanggal_transfer = fields.Date(string='Tanggal', default=fields.Date.context_today)
#     jam_transfer = fields.Char(string='Jam')

#     # === IDENTITAS PASIEN ===
#     nama_pasien = fields.Char(string='Nama Pasien')
#     tanggal_lahir = fields.Date(string='Tanggal Lahir')
#     no_rm = fields.Char(string='No. RM')
#     dpjp = fields.Char(string='DPJP')

#     # === KELUHAN DAN RIWAYAT ===
#     keluhan = fields.Text(string='Keluhan')
#     riwayat_penyakit_dahulu = fields.Text(string='Riwayat Penyakit Dahulu')
    
#     # Riwayat Alergi
#     riwayat_alergi = fields.Selection([
#         ('ada', 'Ada'),
#         ('tidak_ada', 'Tidak Ada'),
#         ('tidak_diketahui', 'Tidak Diketahui')
#     ], string='Riwayat Alergi')
    
#     pemeriksaan_fisik = fields.Text(string='Pemeriksaan Fisik')
    
#     # Pemeriksaan Penunjang
#     pemeriksaan_laboratorium = fields.Boolean(string='Laboratorium')
#     pemeriksaan_ekg = fields.Boolean(string='EKG')
#     pemeriksaan_radiologi = fields.Boolean(string='Radiologi')
#     pemeriksaan_usg = fields.Boolean(string='USG')
#     pemeriksaan_lainnya = fields.Char(string='Pemeriksaan Penunjang Lainnya')
    
#     diagnosa_masuk = fields.Text(string='Diagnosa Masuk')
#     indikasi_mrs = fields.Text(string='Indikasi MRS')

#     # === TERAPI DAN TINDAKAN ===
#     terapi_yang_diberikan = fields.Text(string='Terapi yang Diberikan')
#     tindakan_prosedur_yang_dilakukan = fields.Text(string='Tindakan/Prosedur yang Dilakukan')

#     # === KEADAAN PASIEN SAAT DIPINDAH ===
#     kesadaran = fields.Char(string='Kesadaran')
    
#     # TTV (Tanda Tanda Vital)
#     td = fields.Char(string='TD (Blood Pressure)')
#     rr = fields.Char(string='RR (Respiratory Rate)')
#     nadi = fields.Char(string='Nadi (Pulse)')
#     t_ax = fields.Char(string='T.ax (Axillary Temperature)')
    
#     saturasi_oksigen = fields.Char(string='Saturasi Oksigen')
    
#     # Bantuan Oksigen
#     bantuan_oksigen = fields.Selection([
#         ('tidak', 'Tidak'),
#         ('ya', 'Ya')
#     ], string='Bantuan Oksigen')
#     bantuan_oksigen_sebutkan = fields.Char(string='Bantuan Oksigen - Sebutkan')
#     kecepatan_aliran_oksigen = fields.Char(string='Kecepatan Aliran O₂ (lpm)')
    
#     # Resiko Jatuh
#     resiko_jatuh = fields.Selection([
#         ('tidak', 'Tidak'),
#         ('resiko_rendah', 'Resiko Rendah'),
#         ('resiko_tinggi', 'Resiko Tinggi')
#     ], string='Resiko Jatuh')

#     # === RENCANA PEMERIKSAAN / TINDAKAN ===
#     rencana_pemeriksaan_tindakan = fields.Text(string='Rencana Pemeriksaan / Tindakan di Ruangan')

#     # === TANDA TANGAN ===
#     ttd_dokter_memindah = fields.Binary(string='Tanda Tangan Dokter yang Memindah')
#     nama_dokter_memindah = fields.Char(string='Nama Dokter yang Memindah')
    
#     ttd_perawat_menyerahkan = fields.Binary(string='Tanda Tangan Perawat yang Menyerahkan')
#     nama_perawat_menyerahkan = fields.Char(string='Nama Perawat yang Menyerahkan')
    
#     ttd_perawat_penerima = fields.Binary(string='Tanda Tangan Perawat Penerima')
#     nama_perawat_penerima = fields.Char(string='Nama Perawat Penerima')

