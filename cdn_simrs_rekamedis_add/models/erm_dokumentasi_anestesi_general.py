# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class DokumentasiAnestesiGeneral(models.Model):
    _name = 'cdn.dokumentasi.anestesi.general'
    _description = 'Dokumentasi Pemberian Informasi dan Tindakan Anestesi General'
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

    # === IDENTITAS PASIEN ===
    nama_pasien = fields.Char(string='Nama Pasien')
    tanggal_lahir = fields.Date(string='Tanggal Lahir')
    no_rm = fields.Char(string='No RM')
    kode_4 = fields.Char(string='KODE 4')

    # === INFORMASI PERSONIL ===
    dokter_pelaksana_tindakan = fields.Char(string='Dokter pelaksana tindakan')
    pemberi_informasi = fields.Char(string='Pemberi Informasi')
    penerima_informasi_pemberi_persetujuan = fields.Char(string='Penerima informasi/ pemberi persetujuan/penolakan')

    # === INFORMASI ANESTESI GENERAL ===
    # Item 1: Tindakan Kedokteran
    informasi_tindakan_kedokteran = fields.Text(
        string='Tindakan Kedokteran',
        default='Anestesi general atau anestesi umum'
    )
    tanda_tindakan_kedokteran = fields.Boolean(string='Tanda (√) Tindakan Kedokteran')

    # Item 2: Indikasi Tindakan
    informasi_indikasi_tindakan = fields.Text(
        string='Indikasi Tindakan',
        default='Untuk semua jenis operasi'
    )
    tanda_indikasi_tindakan = fields.Boolean(string='Tanda (√) Indikasi Tindakan')

    # Item 3: Tata Cara
    informasi_tata_cara = fields.Text(
        string='Tata Cara',
        default='Penderita akan diberi penjelasan.\nObat-obatan anestesi akan dimasukkan lewat infuse\nPasien akan segera tertidur'
    )
    tanda_tata_cara = fields.Boolean(string='Tanda (√) Tata Cara')

    # Item 4: Tujuan
    informasi_tujuan = fields.Text(
        string='Tujuan',
        default='Kondisi atau prosedur ketika pasien menerima Obat untuk amnesia, analgesia, melumpuhkan otot, dan sedasi'
    )
    tanda_tujuan = fields.Boolean(string='Tanda (√) Tujuan')

    # Item 5: Risiko
    informasi_risiko = fields.Text(
        string='Risiko',
        default='Bila terdapat prediksi intubasi sulit, muntah'
    )
    tanda_risiko = fields.Boolean(string='Tanda (√) Risiko')

    # Item 6: Komplikasi
    informasi_komplikasi = fields.Text(
        string='Komplikasi',
        default='Mual, muntah pasca operasi'
    )
    tanda_komplikasi = fields.Boolean(string='Tanda (√) Komplikasi')

    # Item 7: Prognosis
    informasi_prognosis = fields.Text(
        string='Prognosis',
        default='Baik'
    )
    tanda_prognosis = fields.Boolean(string='Tanda (√) Prognosis')

    # Item 8: Alternatif
    informasi_alternatif = fields.Text(string='Alternatif')
    tanda_alternatif = fields.Boolean(string='Tanda (√) Alternatif')

    # Item 9: Lain-lain
    informasi_lain_lain = fields.Text(string='Lain-lain')
    tanda_lain_lain = fields.Boolean(string='Tanda (√) Lain-lain')

    # === PERNYATAAN DOKTER ===
    nama_dokter_dpjp = fields.Char(string='Nama Dokter DPJP')
    ttd_dpjp = fields.Binary(string='TTD DPJP')
    tgl_pkl_dpjp = fields.Datetime(string='Tgl/Pkl DPJP')

    # === PERNYATAAN PASIEN/KELUARGA ===
    nama_penerima_informasi = fields.Char(string='Nama Penerima Informasi')
    umur_penerima_informasi = fields.Integer(string='Umur Penerima Informasi')
    
    # Hubungan dengan pasien
    hubungan_pasien_sendiri = fields.Boolean(string='Pasien sendiri')
    hubungan_orang_tua = fields.Boolean(string='Orang tua')
    hubungan_anak = fields.Boolean(string='Anak')
    hubungan_istri = fields.Boolean(string='Istri')
    hubungan_suami = fields.Boolean(string='Suami')
    hubungan_saudara = fields.Boolean(string='Saudara')
    hubungan_pengantar = fields.Boolean(string='Pengantar')
    
    ttd_pasien_keluarga = fields.Binary(string='TTD Pasien/Keluarga')
    tgl_pkl_pasien_keluarga = fields.Datetime(string='Tgl/Pkl Pasien/Keluarga')
    
    ttd_saksi = fields.Binary(string='TTD Saksi')
    tgl_pkl_saksi = fields.Datetime(string='Tgl/Pkl Saksi')

    # === PERNYATAAN PERSETUJUAN/PENOLAKAN ===
    persetujuan_penolakan = fields.Selection([
        ('persetujuan', 'Persetujuan'),
        ('penolakan', 'Penolakan')
    ], string='Persetujuan/Penolakan')
    
    nama_pasien_persetujuan = fields.Char(string='Nama Pasien (untuk persetujuan)')
    umur_pasien_persetujuan = fields.Integer(string='Umur Pasien')
    jenis_kelamin_pasien = fields.Selection([
        ('laki_laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Jenis Kelamin Pasien')
    alamat_pasien_persetujuan = fields.Text(string='Alamat Pasien')

