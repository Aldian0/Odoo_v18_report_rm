# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class SuratKeteranganKematian(models.Model):
    _name = 'cdn.surat.keterangan.kematian'
    _description = 'Surat Keterangan Kematian'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin'
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
    )

    # === HEADER ===
    no_surat = fields.Char(string='No. Surat')
    bulan_tahun_kematian = fields.Char(string='Bulan / Tahun Kematian')
    no_rekam_medis = fields.Char(string='No Rekam Medis')

    # === IDENTITAS JENAZAH ===
    # Field 1-8 dari form
    nama_lengkap_pasien = fields.Char(string='Nama lengkap pasien')
    nik = fields.Char(string='NIK')
    jenis_kelamin = fields.Selection([
        ('laki_laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Jenis kelamin')
    tempat_tanggal_lahir = fields.Char(string='Tempat / tanggal lahir')
    
    # Pendidikan
    pendidikan_tidak_sekolah = fields.Boolean(string='Tidak sekolah')
    pendidikan_sd = fields.Boolean(string='SD')
    pendidikan_sltp = fields.Boolean(string='SLTP')
    pendidikan_slta = fields.Boolean(string='SLTA')
    pendidikan_diploma = fields.Boolean(string='Diploma')
    pendidikan_sarjana = fields.Boolean(string='Sarjana')
    
    # Pekerjaan
    pekerjaan_tidak_belum_bekerja = fields.Boolean(string='Tidak/belum bekerja')
    pekerjaan_tni_polri = fields.Boolean(string='TNI/POLRI')
    pekerjaan_pns = fields.Boolean(string='PNS')
    pekerjaan_petani = fields.Boolean(string='Petani')
    pekerjaan_buruh = fields.Boolean(string='Buruh')
    pekerjaan_wiraswasta = fields.Boolean(string='Wiraswasta')
    pekerjaan_swasta = fields.Boolean(string='Swasta')
    pekerjaan_lainnya = fields.Char(string='Pekerjaan Lainnya')
    
    alamat_sesuai_ktp_kk = fields.Text(string='Alamat sesuai KTP/KK')
    
    # Status Kependudukan
    status_kependudukan_penduduk_tetap = fields.Boolean(string='Penduduk tetap')
    status_kependudukan_bukan_penduduk_tetap = fields.Boolean(string='Bukan Penduduk tetap')

    # === YANG BERSANGKUTAN DINYATAKAN TELAH MENINGGAL DUNIA ===
    # Field 9: Waktu meninggal
    waktu_meninggal_tanggal = fields.Date(string='Tanggal Meninggal')
    waktu_meninggal_jam = fields.Char(string='Pukul')
    
    # Field 10: Umur saat meninggal
    umur_saat_meninggal_hari = fields.Integer(string='Hari (< 29 hari)')
    umur_saat_meninggal_bulan = fields.Integer(string='Bulan (29 hari s/d ≤ 5tahun)')
    umur_saat_meninggal_tahun = fields.Integer(string='Tahun (≥5 tahun)')
    
    # Field 11: Tempat meninggal
    tempat_meninggal_rumah_sakit = fields.Boolean(string='Rumah Sakit')
    lama_dirawat = fields.Char(string='Lama dirawat')
    tempat_meninggal_rumah = fields.Boolean(string='Rumah')
    tempat_meninggal_doa = fields.Boolean(string='DoA (Dead on Arrival)')
    tempat_meninggal_lainnya = fields.Char(string='Tempat Meninggal Lainnya')
    
    # Field 12: Rencana pemulasaran
    rencana_pemulasaran_dikubur = fields.Date(string='Dikubur (Tgl/Bln/Thn)')
    rencana_pemulasaran_dikremasi = fields.Date(string='Dikremasi (Tgl/Bln/Thn)')
    rencana_pemulasaran_transportasi_keluar_kota = fields.Date(string='Transportasi keluar kota (Tgl/Bln/Thn)')
    rencana_pemulasaran_transportasi_keluar_negeri = fields.Date(string='Transportasi keluar negeri (Tgl/Bln/Thn)')

    # === PENERIMA JENAZAH ===
    penerima_nama_lengkap = fields.Char(string='Nama lengkap penerima')
    penerima_usia = fields.Char(string='Usia')
    penerima_jenis_kelamin = fields.Selection([
        ('laki_laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Jenis kelamin penerima')
    penerima_alamat = fields.Text(string='Alamat penerima')
    penerima_hubungan_dengan_almarhum = fields.Char(string='Hubungan dengan almarhum/ah')
    penerima_tanggal_serah_terima = fields.Date(string='Tanggal Serah Terima')
    penerima_kota = fields.Char(string='Kota', default='Surabaya')

    # === TANDA TANGAN ===
    ttd_penerima = fields.Binary(string='Tanda Tangan & Nama Jelas Penerima')
    ttd_dokter_pemeriksa = fields.Binary(string='Nama & Tanda Tangan Dokter Pemeriksa')

