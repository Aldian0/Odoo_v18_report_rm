# cdn_simrs_rekamedis_add/models/asesmen_awal_keperawatan_rawat_inap.py

from odoo import _, api, fields, models

class AsesmenAwalKeperawatanRawatInap(models.Model):
    _name = 'cdn.asesmen.awal.keperawatan.rawat.inap'
    _description = 'Asesmen Awal Keperawatan Rawat Inap'
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

    # === ALERGI / REAKSI ===
    alergi_tidak_ada = fields.Boolean(string='Tidak ada alergi')
    alergi_obat = fields.Boolean(string='Alergi obat')
    alergi_obat_sebutkan = fields.Char(string='Sebutkan alergi obat')
    alergi_obat_reaksi = fields.Char(string='Reaksi alergi obat')
    alergi_makanan = fields.Boolean(string='Alergi makanan')
    alergi_makanan_sebutkan = fields.Char(string='Sebutkan alergi makanan')
    alergi_makanan_reaksi = fields.Char(string='Reaksi alergi makanan')
    alergi_lainnya = fields.Boolean(string='Alergi lainnya')
    alergi_lainnya_sebutkan = fields.Char(string='Sebutkan alergi lainnya')
    alergi_lainnya_reaksi = fields.Char(string='Reaksi alergi lainnya')
    gelang_tanda_alergi_dipasang = fields.Boolean(string='Gelang tanda alergi dipasang (warna merah)')
    alergi_tidak_diketahui = fields.Boolean(string='Tidak diketahui')
    diberitahukan_ke_dokter = fields.Boolean(string='Diberitahukan ke dokter / farmasi (apoteker) / dietisien')
    diberitahukan_ke_dokter_tidak = fields.Boolean(string='Tidak')
    diberitahukan_ke_dokter_ya = fields.Boolean(string='Ya')
    diberitahukan_ke_dokter_jam = fields.Char(string='Jam pemberitahuan')

    # === TANGGAL MASUK & PENGKAJIAN ===
    tanggal_masuk_perawatan = fields.Datetime(string='Tanggal masuk perawatan')
    tanggal_pengkajian = fields.Datetime(string='Tanggal pengkajian')
    diagnosa_dokter_saat_masuk = fields.Text(string='Diagnosa dokter saat masuk')

    # === RIWAYAT PENYAKIT ===
    riwayat_penyakit_sekarang = fields.Text(string='Riwayat Penyakit Sekarang')
    riwayat_penyakit_dahulu = fields.Text(string='Riwayat Penyakit Dahulu')
    riwayat_pengobatan_lalu = fields.Text(string='Riwayat Pengobatan Lalu')

    # === RIWAYAT PENYAKIT KELUARGA ===
    riwayat_penyakit_keluarga_tidak_ada = fields.Boolean(string='Tidak ada')
    riwayat_penyakit_keluarga_diabetes = fields.Boolean(string='Diabetes')
    riwayat_penyakit_keluarga_hipertensi = fields.Boolean(string='Hipertensi')
    riwayat_penyakit_keluarga_tuberkulosis = fields.Boolean(string='Tuberkulosis')
    riwayat_penyakit_keluarga_lainnya = fields.Boolean(string='Lain-lain')
    riwayat_penyakit_keluarga_lainnya_sebutkan = fields.Char(string='Sebutkan lainnya')

    # === DATA SUMBER ===
    data_didapat_dari = fields.Char(string='Data didapat dari')
    hubungan_dengan_pasien = fields.Char(string='Hubungan dengan pasien')
    asal_masuk_igd = fields.Boolean(string='IGD')
    asal_masuk_irjal = fields.Boolean(string='IRJAL')
    asal_masuk_lainnya = fields.Boolean(string='Lainnya')
    asal_masuk_lainnya_sebutkan = fields.Char(string='Sebutkan lainnya')

    # === ASESMEN FISIK - KESADARAN ===
    kesadaran_composmentis = fields.Boolean(string='Composmentis')
    kesadaran_apatis = fields.Boolean(string='Apatis')
    kesadaran_somnolent = fields.Boolean(string='Somnolent')
    kesadaran_soporcoma = fields.Boolean(string='Soporcoma')
    kesadaran_koma = fields.Boolean(string='Koma')
    gcs_e = fields.Char(string='GCS E (Eye)')
    gcs_v = fields.Char(string='GCS V (Verbal)')
    gcs_m = fields.Char(string='GCS M (Motor)')

    # === ASESMEN FISIK - VITAL SIGN ===
    td = fields.Char(string='TD (mmHg)')
    nadi = fields.Char(string='N (x/menit)')
    suhu = fields.Float(string='S (°C)')
    rr = fields.Char(string='RR (x/menit)')
    tb = fields.Float(string='TB (cm)')
    bb = fields.Float(string='BB (kg)')

    # === ASESMEN FISIK - KEPALA ===
    kepala_rambut_tidak_ada_masalah = fields.Boolean(string='Tidak ada masalah')
    kepala_rambut_kelainan = fields.Boolean(string='Kelainan')
    kepala_rambut_lainnya = fields.Boolean(string='Lain-lain')
    kepala_rambut_lainnya_sebutkan = fields.Char(string='Sebutkan lainnya')
    kepala_wajah_normal = fields.Boolean(string='Normal')
    kepala_wajah_asimetris = fields.Boolean(string='Asimetris')
    kepala_wajah_bells_palsy = fields.Boolean(string='Bells Palsy')
    kepala_wajah_tic_facial = fields.Boolean(string='Tic Facial')
    kepala_wajah_lainnya = fields.Boolean(string='Lain-lain')
    kepala_wajah_lainnya_sebutkan = fields.Char(string='Sebutkan lainnya')

    # === ASESMEN FISIK - MATA, TELINGA, HIDUNG & MULUT ===
    # MATA - Palpebra
    mata_palpebra_oedema = fields.Boolean(string='Oedema')
    mata_palpebra_hematom = fields.Boolean(string='Hematom')
    mata_palpebra_luka_robek = fields.Boolean(string='Luka Robek')
    mata_palpebra_lainnya = fields.Boolean(string='Lain-lain')
    mata_palpebra_lainnya_sebutkan = fields.Char(string='Sebutkan lainnya')
    # MATA - Konjungtiva
    mata_konjungtiva_normal = fields.Boolean(string='Normal')
    mata_konjungtiva_anemis = fields.Boolean(string='Anemis')
    # MATA - Pupil
    mata_pupil_isokor = fields.Boolean(string='Isokor')
    mata_pupil_anisokor = fields.Boolean(string='Anisokor')
    mata_pupil_miosis = fields.Boolean(string='Miosis')
    mata_pupil_midriasis = fields.Boolean(string='Midriasis')
    # MATA - Selera (Sclera)
    mata_selera_normal = fields.Boolean(string='Normal')
    mata_selera_icterik = fields.Boolean(string='Icteric')
    # Alat bantu penglihatan
    alat_bantu_penglihatan = fields.Char(string='Alat bantu penglihatan')
    alat_bantu_penglihatan_lainnya = fields.Char(string='Lain-lain alat bantu penglihatan')

    # TELINGA
    telinga_gangguan_pendengaran_ada = fields.Boolean(string='Ada')
    telinga_gangguan_pendengaran_tidak = fields.Boolean(string='Tidak')
    telinga_perdarahan_ada = fields.Boolean(string='Ada')
    telinga_perdarahan_tidak = fields.Boolean(string='Tidak')
    telinga_lainnya = fields.Char(string='Lain-lain telinga')

    # HIDUNG
    hidung_lainnya = fields.Char(string='Lain-lain hidung')

    # MULUT
    mulut_lainnya = fields.Char(string='Lain-lain mulut')

