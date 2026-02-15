from odoo import _, api, fields, models

class FormulirPerencanaanPasienPulang(models.Model):
    _name           = 'cdn.formulir.perencanaan.pasien.pulang'
    _description    = 'Formulir Perencanaan Pasien Pulang'
    _inherit        = [
        'mail.thread', 
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
        ]
    _inherits       = {
        'cdn.erm.base': 'rm_base_id',
        'cdn.pasien': 'tanggal_daftar',
        'cdn.kamar.inap': 'nama_kamar'
        }

    rm_base_id      = fields.Many2one(comodel_name='cdn.erm.base', string='RM', required=True, ondelete='cascade')
    
    # ========== HEADER INFORMATION ==========
    tanggal_daftar = fields.Many2one(string='Tanggal Masuk RS', comodel_name='cdn.pasien', store=True)
    
    tanggal_keluar_rs = fields.Datetime(
        string='Tanggal Keluar RS',
        tracking=True
    )
    
    nama_kamar = fields.Many2one(
        comodel_name='cdn.kamar.inap',
        string='Ruangan',
        tracking=True,
        ondelete='cascade'
    )
    
    # ========== SECTION A: KONDISI ==========
    waktu_kondisi = fields.Datetime(
        string='Waktu',
        tracking=True
    )
    
    tempat_kondisi = fields.Char(
        string='Tempat',
        tracking=True
    )
    
    dpjp_id = fields.Many2one(
        comodel_name='res.partner',
        string='DPJP',
        domain=[('is_company', '=', False)],
        tracking=True
    )
    
    # ========== KEADAAN SAAT PULANG ==========
    keadaan_sembuh = fields.Boolean(string='Sembuh', tracking=True)
    keadaan_pindah_rs = fields.Boolean(string='Pindah Rumah Sakit', tracking=True)
    keadaan_rujuk_rs = fields.Boolean(string='Rujuk Ke Rumah Sakit', tracking=True)
    keadaan_pulang_paksa = fields.Boolean(string='Pulang Paksa', tracking=True)
    keadaan_meninggal = fields.Boolean(string='Meninggal', tracking=True)
    
    alasan_pulang_paksa = fields.Text(
        string='Alasan Pulang Paksa',
        tracking=True
    )
    
    # ========== SECTION A: LANJUTAN PERAWATAN DI RUMAH ==========
    # Checkbox fields untuk lanjutan perawatan
    perawatan_luka_operasi = fields.Boolean(string='Perawatan luka operasi', tracking=True)
    perawatan_diri_hifiene_perseorangan = fields.Boolean(string='Perawatan diri/hifiene perseorangan', tracking=True)
    pencegahan_decubitus = fields.Boolean(string='Pencegahan Decubitus', tracking=True)
    perawatan_imobilisasi_sendi = fields.Boolean(string='Perawatan Imobilisasi Sendi (ROM)', tracking=True)
    perawatan_kateter = fields.Boolean(string='Perawatan Kateter', tracking=True)
    rendaman_duduk = fields.Boolean(string='Rendaman Duduk', tracking=True)
    pemberian_makan_melalui_ngt = fields.Boolean(string='Pemberian makan melalui NGT', tracking=True)
    penyuntikan_insulin = fields.Boolean(string='Penyuntikan Insulin', tracking=True)
    perawatan_payudara = fields.Boolean(string='Perawatan Payudara', tracking=True)
    vulva_hygiene = fields.Boolean(string='Vulva Hygiene', tracking=True)
    perawatan_tali_pusat = fields.Boolean(string='Perawatan tali pusat', tracking=True)
    imunisasi_lanjutan = fields.Boolean(string='Imunisasi Lanjutan', tracking=True)
    
    # ========== SECTION B: PENGATURAN DIET NUTRISI ==========
    pendidikan_gizi = fields.Char(string='Pendidikan Gizi', tracking=True)
    ya_diet = fields.Boolean(string='Ya, Diet', tracking=True)
    tidak_diet = fields.Boolean(string='Tidak Diet', tracking=True)

    alasan_tidak_diet = fields.Text(string='Alasan Tidak Diet', tracking=True)
    alasan_ya_diet = fields.Text(string='Alasan Ya Diet', tracking=True)
    
    # ========== SECTION C: KEBUTUHAN ALAT BANTU ==========
    # Alat Pemesangan
    is_tgl_pemesangan = fields.Boolean(string='Tgl Pemesangan', tracking=True)
    is_tgl_ganti_alat = fields.Boolean(string='Tgl Ganti Alat', tracking=True)

    isi_tgl_pemesangan = fields.Date(string='Alasan Tgl Pemesangan', tracking=True)
    isi_tgl_ganti_alat = fields.Date(string='Alasan Tgl Ganti Alat', tracking=True)
    
    # Perawatan NGT / Kateter
    perawatan_ngt_kateter = fields.Boolean(string='Perawatan NGT / Kateter', tracking=True)
    no_ngt_no_kateter = fields.Boolean(string='No. NGT/No. Kateter', tracking=True)

    keterangan_perawatan_ngt_kateter = fields.Text(string='Keterangan Perawatan NGT / Kateter', tracking=True)
    isi_no_ngt_no_kateter = fields.Char(string='No. NGT/No. Kateter', tracking=True)
    
    # ========== SECTION D: OBAT-OBATAN YANG DIBAWA PULANG ==========
    obat_1 = fields.Text(string='Obat 1', tracking=True)
    obat_2 = fields.Text(string='Obat 2', tracking=True)
    obat_3 = fields.Text(string='Obat 3', tracking=True)
    obat_4 = fields.Text(string='Obat 4', tracking=True)
    obat_5 = fields.Text(string='Obat 5', tracking=True)
    obat_6 = fields.Text(string='Obat 6', tracking=True)
    
    # ========== SECTION E: AKTIVITAS DAN ISTIRAHAT ==========
    # Alat bantu yang digunakan pasien untuk perawatan di rumah
    walker_treepod = fields.Boolean(string='Walker / Treepod', tracking=True)
    crutch = fields.Boolean(string='Crutch', tracking=True)
    kursi_roda = fields.Boolean(string='Kursi Roda', tracking=True)
    tempat_tidur_khusus = fields.Boolean(string='Tempat tidur khusus', tracking=True)
    bruce = fields.Boolean(string='Bruce', tracking=True)
    oksigen = fields.Boolean(string='Oksigen', tracking=True)
    nebulizer = fields.Boolean(string='Nebulizer', tracking=True)
    alat_pemantau = fields.Boolean(string='Alat Pemantau', tracking=True)
    alat_penghisap_lender_slym_suction = fields.Boolean(string='Alat Penghisap Lender/Slym Suction', tracking=True)
    
    # ========== SECTION F: PELAYANAN KESEHATAN ==========
    # Pelayanan kesehatan yang digunakan setelah perawatan
    pelayanan_kesehatan_di_rumah = fields.Boolean(string='Pelayanan Kesehatan Di Rumah', tracking=True)
    puskesmas = fields.Boolean(string='Puskesmas', tracking=True)
    praktek_mandiri_perawat_luka = fields.Boolean(string='Praktek mandiri perawat luka', tracking=True)
    dokter_keluarga = fields.Boolean(string='Dokter Keluarga', tracking=True)
    fisioterapi = fields.Boolean(string='Fisioterapi', tracking=True)
    speech_terapi = fields.Boolean(string='Speech terapi', tracking=True)
    pekerja_sosial = fields.Boolean(string='Pekerja Sosial', tracking=True)
    
    # ========== SECTION G: ORANG YANG MENEMANI ==========
    # Orang yang membantu pasien saat perawatan di rumah
    suami_istri = fields.Boolean(string='Suami / Istri', tracking=True)
    orang_tua = fields.Boolean(string='Orang Tua', tracking=True)
    anak = fields.Boolean(string='Anak', tracking=True)
    kakak_adik = fields.Boolean(string='Kakak / Adik', tracking=True)
    pos = fields.Boolean(string='POS', tracking=True)
    perawat = fields.Boolean(string='Perawat', tracking=True)
    saudara = fields.Boolean(string='Saudara', tracking=True)
    lain_lain = fields.Boolean(string='Lain-lain (Pembantu)', tracking=True)

    alasan_lain_lain = fields.Text(string='Alasan Lain-lain', tracking=True)
    
    # ========== SECTION H: HASIL PEMERIKSAAN DIAGNOSTIK ==========
    # Hasil pemeriksaan diagnostik yang diperlukan saat pulang
    laboratorium = fields.Boolean(string='Laboratorium', tracking=True)
    patologi_anatomi = fields.Boolean(string='Patologi Anatomi', tracking=True)
    ekg = fields.Boolean(string='E K G', tracking=True)
    foto_rontgen = fields.Boolean(string='Foto Rontgen', tracking=True)
    pemeriksaan_usg = fields.Boolean(string='Pemeriksaan USG', tracking=True)
    pemeriksaan_echo = fields.Boolean(string='Pemeriksaan ECHO', tracking=True)
    pemeriksaan_mri = fields.Boolean(string='Pemeriksaan MRI', tracking=True)
    lain_lain_pemeriksaan = fields.Boolean(string='Lain-lain', tracking=True)

    alasan_lain_lain_pemeriksaan = fields.Text(string='Alasan Lain-lain', tracking=True)
    
    # ========== SECTION I: PASIEN KHUSUS PERAWAT ==========
    # Pasien khusus Perawat
    cek_gula_darah_sehari_sebelum_control = fields.Boolean(string='Cek Gula Darah Sehari Sebelum Control', tracking=True)
    foto_rontgen_ekg_hasil = fields.Boolean(string='Foto Rontgen, EKG, hasil pemeriksaan laboratorium harus dibawa pada saat control', tracking=True)
    bila_ada_keluhan = fields.Boolean(string='Bila ada keluhan segera control ke rumah sakit atau ke unit pelaksana terdekat', tracking=True)
    lain_lain_pasien_khusus = fields.Boolean(string='Lain-lain', tracking=True)

    alasan_lain_lain_pasien_khusus = fields.Text(string='Alasan Lain-lain', tracking=True)
    
    # TTD Manual untuk Pasien/Keluarga (Non-Karyawan RS)
    signature_pasien = fields.Binary(string='Tanda Tangan Pasien/Keluarga')
    
    # NOTE: TTD fields sudah tersedia dari cdn.erm.mixin inherit:
    # - qr_ttd_dokter_id, qr_ttd_dokter_date, qr_ttd_dokter_code, qr_ttd_dokter_partner_id
    # - qr_ttd_perawat_id, qr_ttd_perawat_date, qr_ttd_perawat_code, qr_ttd_perawat_partner_id
    # - qr_ttd_bidan_id, qr_ttd_bidan_date, qr_ttd_bidan_code, qr_ttd_bidan_partner_id
    # - dan lainnya untuk Pasien/Keluarga
    
    # ========== REPORT PDF ==========
    def action_print(self):
        """Action untuk print formulir ke PDF"""
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.formulir.perencanaan.pasien.pulang/{self.id}/_generate_print_report',
            'target': 'new',
        }
    
    def _generate_print_report(self):
        """Generate PDF report dari template docx dengan mail merge"""
        
        # Helper function untuk checkbox value
        def checkbox_value(field_value):
            return '[X]' if field_value else '[  ]'
        
        # Data fields untuk mail merge
        data_field = {
            # Header Information
            'tanggal_masuk_rs'      : self.tanggal_masuk_rs.strftime('%d-%m-%Y %H:%M') if self.tanggal_masuk_rs else '',
            'tanggal_keluar_rs'     : self.tanggal_keluar_rs.strftime('%d-%m-%Y %H:%M') if self.tanggal_keluar_rs else '',
            'ruangan'               : self.ruangan_id or '',
            'no_rm'                 : self.no_rm or '',
            
            # Section A: Kondisi
            'waktu_kondisi'         : self.waktu_kondisi.strftime('%d-%m-%Y %H:%M') if self.waktu_kondisi else '',
            'tempat_kondisi'        : self.tempat_kondisi or '',
            'dpjp'                  : self.dpjp_id.name if self.dpjp_id else '',
            
            # Keadaan Saat Pulang (Updated to Boolean)
            'cb_keadaan_sembuh'     : checkbox_value(self.keadaan_sembuh),
            'cb_keadaan_pindah_rs'  : checkbox_value(self.keadaan_pindah_rs),
            'cb_keadaan_rujuk_rs'   : checkbox_value(self.keadaan_rujuk_rs),
            'cb_keadaan_pulang_paksa': checkbox_value(self.keadaan_pulang_paksa),
            'cb_keadaan_meninggal'  : checkbox_value(self.keadaan_meninggal),
            'alasan_pulang_paksa'   : self.alasan_pulang_paksa or '',
            
            # Section A: Lanjutan Perawatan (Checkboxes)
            'cb_perawatan_luka_operasi'         : checkbox_value(self.perawatan_luka_operasi),
            'cb_perawatan_diarifikasn'          : checkbox_value(self.perawatan_diarifikasn_pencegahan),
            'cb_pencegahan_decubitus'           : checkbox_value(self.pencegahan_decubitus),
            'cb_perawatan_imobilisasi'          : checkbox_value(self.perawatan_imobilisasi_sendi),
            'cb_perawatan_kanker'               : checkbox_value(self.perawatan_kanker),
            'cb_rawalan_dialek'                 : checkbox_value(self.rawalan_dialek),
            'cb_pemberian_makan_ngt'            : checkbox_value(self.pemberian_makan_melalui_ngt),
            'cb_penyuntikan_insulin'            : checkbox_value(self.penyuntikan_insulin),
            'cb_perawatan_pleurodesis'          : checkbox_value(self.perawatan_pleurodesis),
            'cb_rehabilitasi_medis'             : checkbox_value(self.rehabilitasi_medis),
            'cb_perawatan_tali_pusat'           : checkbox_value(self.perawatan_tali_pusat),
            'cb_imunisasi_lanjutan'             : checkbox_value(self.imunisasi_lanjutan),
            
            # Section B: Diet Nutrisi
            'cb_pendidikan_gizi'                : checkbox_value(self.pendidikan_gizi),
            'cb_tingkat_aktifitas'              : checkbox_value(self.tingkat_aktifitas),
            'cb_tidak_alergi'                   : checkbox_value(self.tidak_alergi),
            
            # Section C: Alat Bantu
            'tgl_pemesangan'                    : self.isi_tgl_pemesangan.strftime('%d-%m-%Y') if self.isi_tgl_pemesangan else '',
            'cb_td_ganti_alat'                  : checkbox_value(self.is_tgl_ganti_alat),
            'cb_perawatan_ngt_kateter'          : checkbox_value(self.perawatan_ngt_kateter),
            'no_ngt_no_kateter'                 : self.no_ngt_no_kateter or '',
            
            # Section D: Obat-obatan
            'obat_1'                            : self.obat_1 or '',
            'obat_2'                            : self.obat_2 or '',
            'obat_3'                            : self.obat_3 or '',
            'obat_4'                            : self.obat_4 or '',
            'obat_5'                            : self.obat_5 or '',
            'obat_6'                            : self.obat_6 or '',
            
            # Section E: Aktivitas dan Istirahat
            'cb_walker_treepod'                 : checkbox_value(self.walker_treepod),
            'cb_crutch'                         : checkbox_value(self.crutch),
            'cb_kursi_roda'                     : checkbox_value(self.kursi_roda),
            'cb_tempat_tidur_khusus'            : checkbox_value(self.tempat_tidur_khusus),
            'cb_brace'                          : checkbox_value(self.brace),
            'cb_oksigen'                        : checkbox_value(self.oksigen),
            'cb_nebulizer'                      : checkbox_value(self.nebulizer),
            'cb_alat_pernapasan'                : checkbox_value(self.alat_pernapasan),
            'cb_alat_penghalang_ladder'         : checkbox_value(self.alat_penghalang_ladder),
            
            # Section F: Pelayanan Kesehatan
            'cb_homecare'                       : checkbox_value(self.homecare_home_visit),
            'cb_puskesmas'                      : checkbox_value(self.puskesmas),
            'cb_praktek_mandiri'                : checkbox_value(self.praktek_mandiri_perawat_luka),
            'cb_speech_terapi'                  : checkbox_value(self.speech_terapi),
            'cb_dokter_sosial'                  : checkbox_value(self.dokter_sosial),
            
            # Section G: Orang yang Menemani
            'cb_suami_istri'                    : checkbox_value(self.suami_istri),
            'cb_orang_tua'                      : checkbox_value(self.orang_tua),
            'cb_anak'                           : checkbox_value(self.anak),
            'cb_kakak_adik'                     : checkbox_value(self.kakak_adik),
            'cb_pos'                            : checkbox_value(self.pos),
            'cb_saudara'                        : checkbox_value(self.saudara),
            'cb_lain_lain_pemberi'              : checkbox_value(self.lain_lain_pemberi),
            
            # Section H: Hasil Pemeriksaan Diagnostik
            'cb_lab_darah_lengkap'              : checkbox_value(self.lab_darah_lengkap),
            'cb_patologi_anatomi'               : checkbox_value(self.patologi_anatomi),
            'cb_ekg'                            : checkbox_value(self.ekg),
            'cb_foto_rontgen'                   : checkbox_value(self.foto_rontgen),
            'cb_screening_usg'                  : checkbox_value(self.screening_usg),
            'cb_pemeriksaan_echo'               : checkbox_value(self.pemeriksaan_echo),
            'cb_pemeriksaan_ct_scan'            : checkbox_value(self.pemeriksaan_ct_scan),
            'lainlain_pemeriksaan'              : self.lainlain_pemeriksaan or '',
            
            # Section I: Pasien Khusus Perawat
            'cb_pastikan_pasien_kontrol'        : checkbox_value(self.pastikan_pasien_kontrol),
            'cb_foto_rontgen_ekg_hasil'         : checkbox_value(self.foto_rontgen_ekg_hasil),
            'cb_bila_ada_keluhan'               : checkbox_value(self.bila_ada_keluhan),
            'lainlain_pasien_khusus'            : self.lainlain_pasien_khusus or '',
        }
        
        # Data image untuk QR code TTD dan Signature Pasien
        data_image = []
        
        # TTD Pasien (Manual Signature)
        if self.signature_pasien:
            data_image.append({
                'key'       : '{{ttd_pasien}}',
                'value'     : self.signature_pasien,
                'inches'    : 1.5,
            })
            
        # TTD Perawat (QR Code)
        if self.qr_ttd_perawat_code:
            data_image.append({
                'key'       : '{{ttd_perawat}}',
                'value'     : self.qr_ttd_perawat_code,
                'inches'    : 1.5,
            })
        
        # Template path
        template = 'cdn_simrs_rekamedis_add/template/formulir_perencanaan_pasien_pulang.docx'
        
        # Generate PDF
        return self._mail_merge_to_pdf(
            path        = template, 
            data_info   = data_field, 
            image_info  = data_image if data_image else None,
        )