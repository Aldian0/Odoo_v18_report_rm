# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StatusAnestesiSedasi(models.Model):
    _name = 'cdn.status.anestesi.sedasi'
    _description = 'Status Anestesi dan Sedasi'
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

    # Header
    nama_lengkap = fields.Char(string='Nama Lengkap', related='pasien_id.name', store=True)
    jenis_kelamin = fields.Selection([('L','L'),('P','P')], string='L/P', related='pasien_id.jenis_kelamin', store=True)
    poli_ruangan = fields.Char(string='Poli / Ruangan')
    umur = fields.Char(string='Umur')
    no_rm = fields.Char(string='No. RM', related='pasien_id.no_rm', store=True)

    # Diagnosa / Rencana
    diagnosa = fields.Text(string='Diagnosa')
    rencana_tindakan = fields.Text(string='Rencana Tindakan')
    tanggal = fields.Date(string='Tanggal')
    ruang_operasi = fields.Char(string='Ruang Operasi')

    # Tim Operasi / Anestesi
    spesialis_bedah = fields.Char(string='Spesialis Bedah')
    residen_bedah = fields.Char(string='Residen Bedah')
    asisten_bedah = fields.Char(string='Asisten Bedah')
    spesialis_anestesi = fields.Char(string='Spesialis Anestesi')
    residen_anestesi = fields.Char(string='Residen Anestesi')
    penata_anestesi = fields.Char(string='Penata Anestesi')

    # Anamnesa
    keadaan_pra_bedah = fields.Selection([
        ('sadar', 'Sadar'),
        ('menangis', 'Menangis'),
        ('gelisah', 'Gelisah'),
        ('koma', 'Koma')
    ], string='Keadaan Pra - Bedah')
    anamnesa_dari = fields.Char(string='Anamnesa dari')
    riwayat_anestesi = fields.Text(string='Riwayat Anestesi')
    obat_sedang_dikonsumsi = fields.Text(string='Obat - obat yang sedang dikonsumsi')
    riwayat_alergi = fields.Text(string='Riwayat Alergi')
    riwayat_asma = fields.Text(string='Riwayat Asma')

    # Anthropometri & Vital
    bb_kg = fields.Float(string='BB (kg)')
    tb_cm = fields.Float(string='TB (cm)')
    bmi = fields.Float(string='BMI')

    td = fields.Char(string='TD (mmHg)')
    rr = fields.Char(string='RR (x/mnt)')
    n_x_mnt = fields.Char(string='N (x/mnt)')
    temp_c = fields.Char(string='Temp (C)')

    # Fungsi sistem organ (free text per row)
    fungsi_pernafasan = fields.Text(string='Pernafasan')
    fungsi_kardiovaskular = fields.Text(string='Kardiovaskular')
    fungsi_neuro = fields.Text(string='Neuro/muskuloskeletal')
    fungsi_renal = fields.Text(string='Renal/endokrin')
    fungsi_hepato = fields.Text(string='Hepato/gastrointestinal')
    fungsi_lainnya = fields.Text(string='Lain - lain')

    # Catatan ringkas (merokok, alcohol, obat penggunaan)
    catatan_merokok = fields.Selection([('ya', 'Ya'), ('tidak', 'Tidak')], string='Merokok')
    catatan_merokok_jumlah = fields.Char(string='Jumlah / hari')
    catatan_alkoholic = fields.Selection([('ya', 'Ya'), ('tidak', 'Tidak')], string='Alkohol')
    catatan_alkoholic_jumlah = fields.Char(string='Jumlah')

    # Pemeriksaan laboratorium
    lab_hb = fields.Char(string='HB')
    lab_hct = fields.Char(string='HCT')
    lab_leukosit = fields.Char(string='Leukosit')
    lab_trombosit = fields.Char(string='Trombosit')
    lab_bt_ct = fields.Char(string='BT / CT')
    lab_ppt_aptt = fields.Char(string='PPT / APTT')
    lab_sgot_sgpt = fields.Char(string='SGOT / SGPT')
    lab_bun_sk = fields.Char(string='BUN / SK')
    lab_na_k = fields.Char(string='Na / K')
    lab_cl_ca = fields.Char(string='Cl / Ca')
    lab_albumin = fields.Char(string='Albumin')
    lab_gol_darah = fields.Char(string='Gol. Darah')
    lab_hbsag = fields.Char(string='HbsAg')
    lab_anti_hcv = fields.Char(string='Anti HCV')
    lab_anti_hiv = fields.Char(string='Anti HIV')

    # Pemeriksaan penunjang
    penunjang_ecg = fields.Char(string='ECG')
    penunjang_echo = fields.Char(string='Echo')
    penunjang_rothorax = fields.Char(string='Ro Thorax')
    penunjang_paal_paru = fields.Char(string='Paal Paru')
    penunjang_lain = fields.Text(string='Lain - lain')

    # Evaluasi Jalan Napas
    evaluasi_bebas = fields.Char(string='Bebas')
    evaluasi_alat_bantu = fields.Char(string='Alat bantu napas')
    evaluasi_protrusi = fields.Char(string='Protrusi mandibula')
    evaluasi_buka_mulut = fields.Char(string='Buka mulut')
    evaluasi_jarak_mentohyoid = fields.Char(string='Jarak mentohyoid')
    evaluasi_jarak_hyoidroid = fields.Char(string='Jarak hyoidroid')
    evaluasi_leher = fields.Char(string='Leher/gerak leher')
    evaluasi_malampaty = fields.Char(string='Malampaty')
    evaluasi_massa = fields.Char(string='Massa')
    evaluasi_gigi_geligi = fields.Char(string='Gigi geligi')
    evaluasi_sulit_ventilasi = fields.Char(string='Sulit ventilasi')

    # Simpulan Evaluasi Pra Anestesi
    simpulan_ps_asa = fields.Char(string='PS ASA')
    simpulan_emergency = fields.Boolean(string='Emergency')
    simpulan_cardiac_risk = fields.Char(string='CARDIAC RISK INDEKS')
    simpulan_penyulit = fields.Text(string='Penyulit')
    simpulan_komplikasi = fields.Text(string='Komplikasi')

    # Pemeriksa dan tanda tangan
    diperiksa_oleh = fields.Char(string='Diperiksa Oleh')
    diperiksa_tanggal_jam = fields.Datetime(string='Tanggal/Jam')

