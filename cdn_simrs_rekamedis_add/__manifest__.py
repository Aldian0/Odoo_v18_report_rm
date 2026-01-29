# -*- coding: utf-8 -*-
#
#  _  __                      _                           _____       _           _           _       
# | |/ /                     | |                         / ____|     | |         (_)         | |      
# | ' / __ _ _ __ _   _  __ _| |_ __ _ _ __ ___   __ _  | (___   ___ | |_   _ ___ _ _ __   __| | ___  
# |  < / _` | '__| | | |/ _` | __/ _` | '_ ` _ \ / _` |  \___ \ / _ \| | | | / __| | '_ \ / _` |/ _ \ 
# | . \ (_| | |  | |_| | (_| | || (_| | | | | | | (_| |  ____) | (_) | | |_| \__ \ | | | | (_| | (_) |
# |_|\_\__,_|_|   \__, |\__,_|\__\__,_|_| |_| |_|\__,_| |_____/ \___/|_|\__,_|___/_|_| |_|\__,_|\___/ 
#                  __/ |                                                                              
#                 |___/                                                                               
#

{
    'name': "Rekamedis SIMRS ADD",

    'summary': """
        Modul untuk Menambahkan SIMRS Rekamedis
    """,

    'description': """
        Modul untuk Menambahkan SIMRS Rekamedis
    """,

    'author'    : "Karyatama Solusindo",
    'website'   : "https://karyasolusi.id",
    'category'  : 'Services/SIMRS',
    'version'   : '0.1',
    'license'   : 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
        'cdn_simrs_erm',
    ],

    # always loaded
    'data': [

        'security/ir.model.access.csv',
        'security/base/ir.model.access.csv',
        'views/tess_rm.xml',

        'views/klinik_mata/persetujuan_umum_mata_views.xml',
        'views/klinik_mata/pengkajian_medis_views.xml',
        'views/klinik_mata/laporan_operasi_katarak.xml',
        'views/klinik_mata/skor_monitoring_anastesi_lokal.xml',
        'views/klinik_mata/assesmen_awal_rawat_jalan.xml',
        'views/klinik_mata/edukasi_pasien.xml',
        # 'views/klinik_mata/surgikal_safety_checklist.xml',

        # EM RS MUJI RAHAYU
        'views/a_erm_surat_permintaan_masuk_rs.xml',
        'views/a_erm_pernyataan_status_rawat_inap.xml',
        'views/a_rekonsiliasi_obat.xml',
        'views/a_rekonsiliasi_obat_transfer_views.xml',
        'views/a_rekonsiliasi_obat_discharge_views.xml',
        'views/a_skala_jatuh_morse.xml',
        'views/a_humpty_dumty.xml',
        'views/a_nursing_careplan.xml',
        'views/a_erm_implementasi_keperawatan.xml',
        'views/a_asesmen_ulang_nyeri.xml',
        'views/a_inform_consent.xml',


        'views/asesmen_awal_medis.xml',
        'views/asesmen_pasien_rawat_jalan_kebidanan_dan_kandungan.xml',
        'views/asesmen_awal_keperawatan_rawat_inap.xml',
        'views/asesmen_awal_keperawatan_rawat_inap_detail.xml',
        'views/asesmen_awal_keperawatan_rawat_inap_psikososial.xml',
        'views/transfer_pasien_antar_unit.xml',
        'views/konsultasi_tindakan_poli_gigi.xml',
        'views/asesmen_awal_keperawatan_rawat_jalan.xml',

        'views/asesmen_awal_keperawatan_rawat_jalan.xml',

        'views/erm_surat_keterangan_kematian.xml',
        'views/erm_dokumentasi_anestesi_general.xml',
        'views/status_anestesi_sedasi.xml',
        'views/erm_laporan_harian_rawat_inap.xml',
        'views/erm_form_dpjp.xml',
        # 'views/erm_transfer_pasien_antar_unit.xml',
        'views/general_consent_views.xml',
        
        # 'views/dpjp_pemilihan_views.xml',
        'views/identifikasi_bayi_views.xml',
        'views/asesmen_pra_bedah_views.xml',
        'views/skrining_mpp_views.xml',
        'views/penjadwalan_operasi_views.xml',
        'views/dokumentasi_inform_hecting_views.xml',
        'views/asuhan_gizi_views.xml',
        'views/lembar_laporan_operasi_tindakan_medis_views.xml',
        
        'views/ringkasan_kematian.xml',
        
        'views/surgical_safety_checklist_views.xml',

        'views/asesmen_awal_keperawatan_rawat_jalan.xml',        
        
        #'views/rujukan_antar_instansi.xml',
        'views/catatan_implementasi_mpp.xml',
        'views/skrining_covid_views.xml',
        'views/surveilans_infeksi_luka_views.xml',
        #'views/rujukan_antar_instansi.xml',
        'views/formulir_perencanaan_pasien_pulang_views.xml',

        'views/u_rujukan_antar_instansi.xml',
        'views/u_asesment_awal_rawat_jalan.xml',

        'views/e_surat_keterangan_kematian.xml',
        'views/e_asesmen_awal_keperawatan_rawat_jalan.xml',
        'views/persetujuan_penandaan_area_operasi_perempuan.xml',
        'views/formulir_penolakan_atas_permintaan_sendiri.xml',



    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
}
