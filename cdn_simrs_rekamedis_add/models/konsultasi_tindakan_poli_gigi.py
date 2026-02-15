# cdn_simrs_rekamedis_add/models/konsultasi_tindakan_poli_gigi.py

from odoo import _, api, fields, models

class KonsultasiTindakanPoliGigi(models.Model):
    _name = 'cdn.konsultasi.tindakan.poli.gigi'
    _description = 'Lembar Konsultasi dan Tindakan Poli Gigi'
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

    # Informasi Pasien
    ket = fields.Selection([
        ('umum', 'UMUM'),
        ('bpjs', 'BPJS'),
        ('jkk', 'JKK'),
        ('piutang', 'PIUTANG')
    ], string='KET', default='umum')

    # Konsultasi & Pemeriksaan
    tindakan_konsultasi_periksa = fields.Selection([
        ('dr_gigi_spesialis', 'Konsul / Pemeriksaan Dr. Gigi Spesialis'),
        ('konsultasi_gigi_px_umum', 'Konsultasi Gigi Px Umum'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Konsultasi & Pemeriksaan', default='none')

    # Pengobatan & Pencabutan
    tindakan_pengobatan_pencabutan = fields.Selection([
        ('pengobatan_peradangan', 'Pengobatan Peradangan'),
        ('incisi_abces_intra_oral', 'Incisi Abces Intra Oral'),
        ('pencabutan_gigi_anak_chlorethyl', 'Pencabutan Gigi Anak Dengan Chlorethyl'),
        ('pencabutan_gigi_dewasa_biasa', 'Pencabutan Gigi Dewasa Biasa'),
        ('pencabutan_dengan_komplikasi', 'Pencabutan Dengan Komplikasi'),
        ('operasi_gigi_tertanam_miring', 'Operasi Gigi (Tertanam) Miring'),
        ('cabut_gigi_sulung', 'Cabut Gigi Sulung (Sp. GIGI)'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Pengobatan & Pencabutan', default='none')

    # Scaling & Operasi
    tindakan_scaling_operasi = fields.Selection([
        ('scalling_sebagian_rahang_per_regio', 'Scalling Sebagian Rahang Per Regio'),
        ('scalling_penuh', 'Scalling Penuh'),
        ('uperculectomy_alveolectomy', 'Uperculectomy / Alveolectomy'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Scaling & Operasi', default='none')

    # Tumpatan (bagian 1)
    tindakan_tumpatan_1 = fields.Selection([
        ('sementara', 'Tumpatan Sementara'),
        ('ionomer', 'Tumpatan Ionomer'),
        ('amalgam_1_bidang', 'Tumpatan Amalgam 1 Bidang'),
        ('amalgam_2_bidang_lebih', 'Tumpatan Amalgam 2 Bidang / Lebih'),
        ('composit', 'Tumpatan Composit'),
        ('composit_dgn_sinar', 'Tumpatan Composit Dgn Sinar'),
        ('inlay_tanpa_logam_mulia', 'Tumpatan Inlay Tanpa Logam Mulia'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Tumpatan (1)', default='none')

    # Perawatan Saluran Akar (bagian 1)
    tindakan_saluran_akar_1 = fields.Selection([
        ('per_visit', 'Perawatan Saluran Akar Per Visit'),
        ('rawat_saluran_ak_ganda_kunj_isi', 'Rawatan Saluran Ak. Ganda/Kunjungan+Isi'),
        ('rawat_saluran_ak_tunggal_kunj_isi', 'Rawatan Saluran Ak. Tunggal/Kunjungan+Isi'),
        ('preparasi_tunggal_sterilisasi', 'Preparasi Saluran Ak. Tunggal + Sterilisasi'),
        ('preparasi_ganda_sterilisasi', 'Preparasi Saluran Akar Ganda + Sterilisasi'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Perawatan Saluran Akar (1)', default='none')

    # Tumpatan (bagian 2)
    tindakan_tumpatan_2 = fields.Selection([
        ('komposit_besar', 'Tumpatan Komposit Besar (Sp. GIGI)'),
        ('komposit_kecil', 'Tumpatan Komposit Kecil (Sp. GIGI)'),
        ('komposit_sedang', 'Tumpatan Komposit Sedang (Sp. GIGI)'),
        ('gic', 'Tumpatan GIC'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Tumpatan (2)', default='none')

    # Perawatan Saluran Akar (bagian 2)
    tindakan_saluran_akar_2 = fields.Selection([
        ('isi_tunggal', 'Pengisian Saluran Akar Tunggal'),
        ('isi_ganda', 'Pengisian Saluran Akar Ganda'),
        ('isi_tunggal_komposit', 'Pengisian Saluran Akar Tunggal + Komposit'),
        ('isi_ganda_komposit', 'Pengisian Saluran Akar Ganda + Komposit'),
        ('emergency_endodontic', 'Emergency Endodontic'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Perawatan Saluran Akar (2)', default='none')

    # Gigi Tiruan (bagian 1)
    tindakan_gigi_tiruan_1 = fields.Selection([
        ('atas_bawah_acrilic', 'Gigi Tiruan Atas Bawah Acrilic'),
        ('acrilic_sebagian_1_gigi', 'Gigi Tiruan Acrilic Sebagian + 1 Gigi'),
        ('tambahan_acrilic_per_gigi', 'Tambahan Gigi Tiruan Acrilic Per Gigi'),
        ('full_denture_ra_rb', 'Full Denture RA & RB (Sp. GIGI)'),
        ('metal_frame', 'Gigi Tiruan Metal Frame (Sp. GIGI)'),
        ('metal_frame_tambahan_gigi', 'Gigi Tiruan Metal Frame Tambahan/Gigi'),
        ('metal_kombinasi_valplast', 'Gigi Tiruan Metal Kombinasi Valplast'),
        ('metal_kom_valplast_tambahan', 'Gigi Tiruan Metal Komb. Valplast +/Gigi'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Gigi Tiruan (1)', default='none')

    # Gigi Tiruan (bagian 2)
    tindakan_gigi_tiruan_2 = fields.Selection([
        ('sebagian_lepas_akrilik', 'Gigi Tiruan Sebagian Lepasan Akrilik'),
        ('sebagian_lepas_akrilik_tambahan', 'Gigi Tiruan Sebagian Lep. Akrilik +/Gigi'),
        ('valplast', 'Gigi Tiruan Valplast (Sp. GIGI)'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Gigi Tiruan (2)', default='none')

    # Kawat & Pasak (bagian 1)
    tindakan_kawat_pasak_1 = fields.Selection([
        ('cabut_gigi_anak_anest_local', 'Pencabutan Gigi Anak Dg Anastesi Local'),
        ('pasang_baru_kawat_per_rahang', 'Pasang Baru Kawat Per Rahang'),
        ('pasang_kawat_baru_atas_bawah', 'Pasang Kawat Baru Rahang Atas & Bawah'),
        ('ganti_kawat_per_rahang', 'Ganti Kawat Per Rahang'),
        ('pembuatan_gigi', 'Pembuatan Gigi'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Kawat & Pasak (1)', default='none')

    # Kawat & Pasak (bagian 2)
    tindakan_kawat_pasak_2 = fields.Selection([
        ('pasak_unimetric_crown_porcelain', 'Pasak Unimetric + Crown Porcelain'),
        ('pasak_unimet_akar_ganda_core_build_up', 'Pasang Pasak Unimet Akar Ganda Core B.UP'),
        ('pasak_unimet_akar_tunggal_cr_build_up', 'Pasang Pasak Unimet Akar Tunggal CR B.UP'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Kawat & Pasak (2)', default='none')

    # Kurretase & Mahkota
    tindakan_kurretase_mahkota = fields.Selection([
        ('kurretase_per_gigi', 'Kurretase Per Gigi'),
        ('mahkota_jembatan_pfm', 'Mahkota Jembatan Porcelain Fused 2 Metal'),
        ('mahkota_selubung_pfm', 'Mahkota Selubung Porcelain Fused 2 Metal'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Kurretase & Mahkota', default='none')

    # Paket Endodontik
    tindakan_paket_endodontik = fields.Selection([
        ('paket_endodon_pasak_unimetic_crown_por', 'Paket Endodon + Pasak Unimetic + Crown Por.'),
        ('paket_endo_psk_unimetic_crown_por_metal', 'Paket Endo. + Psk Unimetic + Crown Por-Metal'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Paket Endodontik', default='none')

    # Pembersihan & Perawatan
    tindakan_pembersihan_perawatan = fields.Selection([
        ('pembersihan_karang_gigi', 'Pembersihan Karang Gigi'),
        ('pulp_capping', 'Pulp Capping (Sp. GIGI)'),
        ('rooth_planning', 'Rooth Planning (Sp. GIGI)'),
        ('sterilisasi', 'Sterilisasi (Sp. GIGI)'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Pembersihan & Perawatan', default='none')

    # Inlay & Veneer
    tindakan_inlay_veneer = fields.Selection([
        ('inlay_logam', 'Inlay Logam (Sp. GIGI)'),
        ('inlay_porcelain', 'Inlay Porcelain (Sp. GIGI)'),
        ('veneer_all_porcelain', 'Veneer All Porcelain (Sp. GIGI)'),
        ('veneer_komposit', 'Veneer Komposit'),
        ('dental_whitening', 'Dental Whitening (Sp. GIGI)'),
        ('lainnya', 'Lainnya'),
        ('none', '-')
    ], string='Inlay & Veneer', default='none')

    # Lainnya detail
    tindakan_lainnya_detail = fields.Text(string='Detail Lainnya')
