# cdn_simrs_rekamedis_add/models/asesmen_awal_keperawatan_rawat_inap_detail.py

from odoo import _, api, fields, models

class AsesmenAwalKeperawatanRawatInapDetail(models.Model):
    _name = 'cdn.asesmen.awal.keperawatan.rawat.inap.detail'
    _description = 'Asesmen Awal Keperawatan Rawat Inap - Detail Fisik'
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

    # === HIDUNG ===
    hidung_bentuk_normal = fields.Boolean(string='Normal')
    hidung_bentuk_tidak = fields.Boolean(string='Tidak, jelaskan')
    hidung_bentuk_tidak_jelaskan = fields.Text(string='Jelaskan bentuk hidung')
    hidung_perdarahan_ada = fields.Boolean(string='Ada')
    hidung_perdarahan_tidak = fields.Boolean(string='Tidak')
    hidung_gangguan_penciuman_ada = fields.Boolean(string='Ada')
    hidung_gangguan_penciuman_tidak = fields.Boolean(string='Tidak')
    hidung_lainnya = fields.Char(string='Lain-lain hidung')
    hidung_catatan_masalah = fields.Text(string='Catatan / Masalah (Hidung)')

    # === MULUT ===
    mulut_bentuk_normal = fields.Boolean(string='Normal')
    mulut_bentuk_simetris = fields.Boolean(string='Simetris')
    mulut_bentuk_asimetris = fields.Boolean(string='Asimetris')
    mulut_bentuk_kelainan_congenital = fields.Boolean(string='Kelainan Congenital')
    mulut_bentuk_lainnya = fields.Boolean(string='Lain-lain')
    mulut_bentuk_lainnya_sebutkan = fields.Char(string='Sebutkan bentuk mulut lainnya')
    mulut_gigi_normal = fields.Boolean(string='Normal')
    mulut_gigi_karies = fields.Boolean(string='Karies')
    mulut_gigi_palsu = fields.Boolean(string='Gigi Palsu')
    mulut_gigi_lainnya = fields.Boolean(string='Lain-lain')
    mulut_gigi_lainnya_sebutkan = fields.Char(string='Sebutkan gigi lainnya')
    mulut_lidah_normal = fields.Boolean(string='Normal')
    mulut_lidah_kotor = fields.Boolean(string='Kotor')
    mulut_lidah_mukosa_kering = fields.Boolean(string='Mukosa Kering')
    mulut_lidah_asimetris = fields.Boolean(string='Asimetris')
    mulut_lidah_lainnya = fields.Boolean(string='Lain-lain')
    mulut_lidah_lainnya_sebutkan = fields.Char(string='Sebutkan lidah lainnya')
    mulut_lainnya = fields.Char(string='Lain-lain mulut')
    mulut_catatan_masalah = fields.Text(string='Catatan / Masalah (Mulut)')

    # === LEHER & TENGGOROKAN ===
    leher_normal = fields.Boolean(string='Normal')
    leher_pembesaran_tiroid = fields.Boolean(string='Pembesaran Tiroid')
    leher_pembesaran_vena_jugularis = fields.Boolean(string='Pembesaran Vena Jugularis')
    leher_kaku_kuduk = fields.Boolean(string='Kaku kuduk')
    leher_keterbatasan_gerak = fields.Boolean(string='Keterbatasan Gerak')
    leher_lainnya = fields.Boolean(string='Lain-lain')
    leher_lainnya_sebutkan = fields.Char(string='Sebutkan leher lainnya')
    tenggorokan_normal = fields.Boolean(string='Normal')
    tenggorokan_faring_merah = fields.Boolean(string='Faring merah')
    tenggorokan_tonsil_membesar = fields.Boolean(string='Tonsil membesar')
    tenggorokan_lainnya = fields.Boolean(string='Lain-lain')
    tenggorokan_lainnya_sebutkan = fields.Char(string='Sebutkan tenggorokan lainnya')
    leher_tenggorokan_catatan_masalah = fields.Text(string='Catatan / Masalah (Leher & Tenggorokan)')

    # === DADA - PERNAFASAN ===
    pernafasan_simetris = fields.Boolean(string='Simetris')
    pernafasan_asimetris = fields.Boolean(string='Asimetris')
    pernafasan_nyeri = fields.Boolean(string='Nyeri')
    pernafasan_batuk = fields.Boolean(string='Batuk')
    pernafasan_dyspnea = fields.Boolean(string='Dyspnea')
    pernafasan_ronchi = fields.Boolean(string='Ronchi')
    pernafasan_wheezing = fields.Boolean(string='Wheezing')
    pernafasan_rales = fields.Boolean(string='Rales')
    pernafasan_hemoptoe = fields.Boolean(string='Hemoptoe')
    pernafasan_bradipnea = fields.Boolean(string='Bradipnea')
    pernafasan_takipnea = fields.Boolean(string='Takipnea')
    pernafasan_apnea = fields.Boolean(string='Apnea')
    pernafasan_lainnya = fields.Boolean(string='Lain-lain')
    pernafasan_lainnya_sebutkan = fields.Char(string='Sebutkan pernafasan lainnya')
    pernafasan_alat_bantu = fields.Char(string='Alat bantu yang digunakan (Pernafasan)')

    # === DADA - JANTUNG ===
    jantung_bunyi_normal = fields.Boolean(string='Bunyi jantung normal')
    jantung_murmur = fields.Boolean(string='Murmur')
    jantung_gallop = fields.Boolean(string='Gallop')
    jantung_nyeri_dada = fields.Boolean(string='Nyeri dada')
    jantung_bradikardi = fields.Boolean(string='Bradikardi')
    jantung_takikardi = fields.Boolean(string='Takikardi')
    jantung_palpitasi = fields.Boolean(string='Palpitasi')
    jantung_aritmia = fields.Boolean(string='Aritmia')
    jantung_lainnya = fields.Boolean(string='Lain-lain')
    jantung_lainnya_sebutkan = fields.Char(string='Sebutkan jantung lainnya')
    jantung_alat_bantu = fields.Char(string='Alat bantu yang digunakan (Jantung)')
    dada_catatan_masalah = fields.Text(string='Catatan / Masalah (Dada)')

    # === ABDOMEN & NUTRISI ===
    abdomen_normal = fields.Boolean(string='Normal')
    abdomen_distensi = fields.Boolean(string='Distensi')
    abdomen_lainnya = fields.Boolean(string='Lain-lain')
    abdomen_lainnya_sebutkan = fields.Char(string='Sebutkan abdomen lainnya')
    nutrisi_anoreksia = fields.Boolean(string='Anoreksia')
    nutrisi_kesulitan_menelan = fields.Boolean(string='Kesulitan Menelan')
    nutrisi_mual = fields.Boolean(string='Mual')
    nutrisi_muntah = fields.Boolean(string='Muntah')
    nutrisi_lainnya = fields.Boolean(string='Lain-lain')
    nutrisi_lainnya_sebutkan = fields.Char(string='Sebutkan nutrisi lainnya')
    benjolan_massa_tidak = fields.Boolean(string='Tidak')
    benjolan_massa_ada = fields.Boolean(string='Ada, lokasi')
    benjolan_massa_lokasi = fields.Char(string='Lokasi benjolan/massa')
    abdomen_alat_bantu = fields.Char(string='Alat bantu yang digunakan (Abdomen)')
    makanan_pantang = fields.Text(string='Makanan Pantang')
    diet = fields.Char(string='Diet')
    abdomen_nutrisi_catatan_masalah = fields.Text(string='Catatan / Masalah (Abdomen & Nutrisi)')

    # === INTEGUMEN & EKSTREMITAS ===
    integumen_normal = fields.Boolean(string='Normal')
    integumen_turgor = fields.Boolean(string='Turgor')
    integumen_turgor_detail = fields.Char(string='Detail Turgor')
    integumen_dingin = fields.Boolean(string='Dingin')
    integumen_bula = fields.Boolean(string='Bula')
    integumen_luka_tekan = fields.Boolean(string='Luka Tekan')
    integumen_rl_positif = fields.Boolean(string='RL Positif')
    integumen_kemerahan = fields.Boolean(string='Kemerahan')
    integumen_lesi = fields.Boolean(string='Lesi')
    integumen_luka = fields.Boolean(string='Luka')
    integumen_memar = fields.Boolean(string='Memar')
    integumen_lainnya = fields.Boolean(string='Lain-lain')
    integumen_lainnya_sebutkan = fields.Char(string='Sebutkan integumen lainnya')
    ekstremitas_normal = fields.Boolean(string='Normal')
    ekstremitas_parese = fields.Boolean(string='Parese')
    ekstremitas_plegi = fields.Boolean(string='Plegi')
    ekstremitas_paralisis = fields.Boolean(string='Paralisis')
    ekstremitas_oedema = fields.Boolean(string='Oedema')
    ekstremitas_rasa_tebal = fields.Boolean(string='Rasa Tebal')
    ekstremitas_tremor = fields.Boolean(string='Tremor')
    ekstremitas_kelainan_kongenital = fields.Boolean(string='Kelainan Kongenital')
    ekstremitas_deformitas = fields.Boolean(string='Deformitas')
    ekstremitas_kontraktur = fields.Boolean(string='Kontraktur')
    ekstremitas_lainnya = fields.Boolean(string='Lain-lain')
    ekstremitas_lainnya_sebutkan = fields.Char(string='Sebutkan ekstremitas lainnya')
    luka_tidak = fields.Boolean(string='Tidak')
    luka_ya = fields.Boolean(string='Ya, di area')
    luka_area = fields.Char(string='Area luka')
    luka_tekan_tidak = fields.Boolean(string='Tidak')
    luka_tekan_ya = fields.Boolean(string='Ya, di area')
    luka_tekan_area = fields.Char(string='Area luka tekan')
    integumen_ekstremitas_catatan_masalah = fields.Text(string='Catatan / Masalah (Integumen & Ekstremitas)')

