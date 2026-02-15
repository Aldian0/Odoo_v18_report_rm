from odoo import _, api, fields, models

class SurgicalSafetyChecklist(models.Model):
    _name           = 'cdn.surgical.safety.checklist'

    _description    = 'Surgikal Safety Checklist'

    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
    )
    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )


    # ==================================================
    # WAKTU & TAHAP
    # ==================================================
    sign_in_time = fields.Datetime(string='SIGN IN (Jam WIB)', tracking=True)
    time_out_time = fields.Datetime(string='TIME OUT (Jam WIB)', tracking=True)
    sign_out_time = fields.Datetime(string='SIGN OUT (Jam WIB)', tracking=True)

    prosedure_tindakan  = fields.Char(string='Prosedur Tindakan', tracking=True)
    ruang_rawat         = fields.Char(string='Ruang Rawat', tracking=True)
    tanggal_operasi     = fields.Date(string='Tanggal', tracking=True)

    # ==================================================
    # VERIFIKASI
    # ==================================================
    verif_identitas_gelang = fields.Boolean(
        string='Identitas dan Gelang Pasien', tracking=True
    )
    verif_informed_consent = fields.Boolean(
        string='Informed Consent', tracking=True
    )

    dokter_bedah_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Dokter Bedah', tracking=True
    )
    dokter_anestesi_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Dokter Anestesi', tracking=True
    )

    nama_tindakan = fields.Char(string='Nama Tindakan', tracking=True)

    tanda_lokasi_operasi = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak dapat dilakukan')
    ], string='Pemberian Tanda di Lokasi Operasi', tracking=True)

    diagnosa_pasien = fields.Text(string='Diagnosa Pasien', tracking=True)

    # ==================================================
    # KELENGKAPAN PASIEN
    # ==================================================
    mesin_anestesi = fields.Boolean(string='Mesin Anestesi', tracking=True)
    iv_line = fields.Boolean(string='IV Line', tracking=True)
    obat_obatan = fields.Boolean(string='Obat-obatan', tracking=True)
    laboratorium = fields.Boolean(string='Laboratorium', tracking=True)
    selang_o2 = fields.Boolean(string='Penggunaan Selang O2', tracking=True)

    # ==================================================
    # PEMERIKSAAN TANDA VITAL
    # ==================================================
    kesadaran = fields.Char(string='Kesadaran', tracking=True)
    tekanan_darah = fields.Char(string='Tekanan Darah', tracking=True)
    nadi = fields.Char(string='Nadi', tracking=True)
    saturasi_oksigen = fields.Char(string='Saturasi Oksigen', tracking=True)
    suhu = fields.Char(string='Suhu', tracking=True)
    skala_nyeri = fields.Char(string='Skala Nyeri', tracking=True)

    # ==================================================
    # RIWAYAT ALERGI
    # ==================================================
    riwayat_alergi = fields.Selection([
        ('ada', 'Ada'),
        ('tidak', 'Tidak Ada')
    ], string='Riwayat Alergi', tracking=True)

    alergi_keterangan = fields.Char(string='Sebutkan Alergi', tracking=True)

    # ==================================================
    # RISIKO
    # ==================================================
    risiko_aspirasi = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')],
        string='Risiko Aspirasi / Gangguan Pernapasan', tracking=True

    )

    risiko_perdarahan = fields.Selection([
        ('ya', 'Ya (>100 ml)'),
        ('tidak', 'Tidak')
    ], string='Risiko Perdarahan', tracking=True)

    risiko_perdarahan_catatan = fields.Char(
        string='Catatan (IV Line / CVP)', tracking=True
    )

    # ==================================================
    # LENSA TANAM (KATARAK)
    # ==================================================
    lensa_tanam_status = fields.Selection([
        ('sesuai', 'Sesuai'),
        ('ganti', 'Ganti Ukuran IOL')
    ], string='Ukuran Lensa Tanam', tracking=True)

    ukuran_iol = fields.Char(string='Ukuran IOL', tracking=True)

    # ==================================================
    # RENCANA ANESTESI
    # ==================================================
    anestesi_umum = fields.Boolean(string='Umum', tracking=True)
    anestesi_lokal = fields.Boolean(string='Lokal', tracking=True)
    anestesi_topikal = fields.Boolean(string='Topikal', tracking=True)
    anestesi_spinal = fields.Boolean(string='Spinal', tracking=True)
    anestesi_epidural = fields.Boolean(string='Epidural', tracking=True)
    anestesi_blok = fields.Boolean(string='Blok', tracking=True)

    # ==================================================
    # BACA SECARA VERBAL (TIME OUT)
    # ==================================================
    verbal_tanggal = fields.Boolean(string='Tanggal Tindakan', tracking=True)
    verbal_nama_tindakan = fields.Boolean(string='Nama Tindakan', tracking=True)
    verbal_lokasi = fields.Boolean(string='Lokasi Tindakan', tracking=True)
    verbal_identitas = fields.Boolean(string='Identitas Pasien', tracking=True)
    verbal_prosedur = fields.Boolean(string='Nama Tindakan', tracking=True)
    verbal_informed_consent = fields.Boolean(string='Informed Consent', tracking=True)
    verbal_konfirmasi_tim = fields.Boolean(
        string='Konfirmasi Seluruh Anggota Tim', tracking=True
    )

    # ==================================================
    # TIM & FASILITAS OPERASI
    # ==================================================
    tim_fasilitas_lengkap = fields.Selection([
        ('lengkap', 'Lengkap'),
        ('tidak', 'Tidak Lengkap')
    ], string='Tim dan Fasilitas Operasi', tracking=True)

    # ==================================================
    # ANTIBIOTIK PROFILAKSIS
    # ==================================================
    antibiotik_diberikan = fields.Selection([
            ('ya', 'Ya'),
            ('tidak', 'Tidak')
        ],
        string='Antibiotik < 60 Menit', tracking=True
    )
    antibiotik_nama = fields.Char(string='Nama Obat', tracking=True)

    antibiotik_jam  = fields.Datetime(string='Jam', tracking=True)
    antibiotik_dosis = fields.Char(string='Dosis', tracking=True)

    # ==================================================
    # ANTISIPASI KEJADIAN KRITIS
    # ==================================================
    antisipasi_bedah = fields.Text(
        string='Antisipasi Kejadian Kritis (Bedah)',
        help='Bagian Bedah : Langkah apa yangdilakukan bila kondisi kritis ataukejadian yang tidak diharapkan,pemanjangan lamanya operasi danantisipasi kehilangan darah ?', tracking=True
    )
    antisipasi_anestesi = fields.Text(
        string='Antisipasi Kejadian Kritis (Anestesi)',
        help='Bagian Anestesi : Apakah ada hal khusus yang perlu diperhatikan pada pasien ?', tracking=True
    )

    indikator_sterilisasi = fields.Selection([
            ('ya', 'Ya'),
            ('tidak', 'Tidak')
        ],
        string='Indikator Sterilisasi Alat', tracking=True
    )
    instrumen_lengkap = fields.Selection([
            ('ya', 'Ya'),
            ('tidak', 'Tidak')
        ],
        string='Instrumen Lengkap', tracking=True
    )

    kondisi_khusus_pasien = fields.Selection([
            ('ya', 'Ya'),
            ('tidak', 'Tidak')
        ],
        string='Kondisi Khusus Pasien', tracking=True
    )
    kondisi_khusus_catatan = fields.Text(
        string='Keterangan Kondisi Khusus', tracking=True
    )

    hasil_usg = fields.Selection([
        ('sudah', 'Sudah'),
        ('belum', 'Belum')
    ], string='Hasil USG / Informasi Khusus Operasi', tracking=True)

    hasil_usg_catatan = fields.Text(
        string='Keterangan Hasil USG / Informasi Khusus Operasi', tracking=True
    )

    # # ==================================================
    # # SIGN OUT – SEBELUM LUKA DITUTUP
    # # ==================================================


    # ==================================================
    # BACA SECARA VERBAL
    # ==================================================
    nama_tindakan = fields.Char(
        string='Nama Tindakan', tracking=True
    )

    # ==================================================
    # SIGN OUT – SEBELUM LUKA DITUTUP
    # ==================================================
    cek_instrumen = fields.Boolean(string='Instrumen', tracking=True)
    cek_spon = fields.Boolean(string='Spon', tracking=True)
    cek_kassa = fields.Boolean(string='Kassa', tracking=True)
    cek_depper = fields.Boolean(string='Depper', tracking=True)
    cek_jarum = fields.Boolean(string='Jarum', tracking=True)
    cek_lainnya = fields.Char(string='Lainnya', tracking=True)

    # ==================================================
    # BAHAN PEMERIKSAAN
    # ==================================================
    preparat_ada = fields.Selection([
            ('ya', 'Ya'),
            ('tidak', 'Tidak')
        ],string='Preparat Ada', tracking=True)

    preparat_jenis = fields.Selection([
        ('pa', 'P.A'),
        ('kultur', 'Kultur'),
        ('sitologi', 'Sitologi'),
        ('lainnya', 'Lainnya'),
        ('tidak_ada', 'Tidak Ada'),
    ], string='Jenis Preparat', tracking=True)

    formulir_ada = fields.Selection([
            ('ya', 'Ya'),
            ('tidak', 'Tidak')
        ],
        string='Formulir Ada', tracking=True
    )

    identitas_lengkap = fields.Selection([
            ('ya', 'Ya'),
            ('tidak', 'Tidak')
        ],
        string='Identitas Pasien Lengkap', tracking=True
    )

    # ==================================================
    # PERHATIAN KHUSUS UNTUK PASIEN
    # ==================================================
    perhatian_operator = fields.Text(
        string='Perhatian dari Operator', tracking=True
    )

    perhatian_anestesi = fields.Text(
        string='Perhatian dari Dokter Anestesi', tracking=True
    )

    perhatian_perawat = fields.Text(
        string='Perhatian dari Perawat Bedah', tracking=True
    )

    # ==================================================
    # PASCA OPERASI
    # ==================================================
    pindah_recovery = fields.Selection([
            ('ya', 'Ya'),
            ('tidak', 'Tidak')
        ],
        string='Pasien Bisa Pindah ke Ruang Pemulihan', tracking=True
    )

    kondisi_luka = fields.Selection([
        ('rembesan', 'Ada Rembesan'),
        ('tidak', 'Tidak Ada Rembesan')
    ], string='Kondisi Luka Operasi', tracking=True)

    instruksi_khusus = fields.Text(
        string='Instruksi Khusus Pasca Operasi', tracking=True
    )

    # ==================================================
    # PETUGAS & TANDA TANGAN
    # ==================================================
    dokter_operator_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Dokter Operator', tracking=True
    )

    dokter_anestesi_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Dokter Anestesi', tracking=True
    )

    perawat_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Perawat Bedah', tracking=True
    )


    def _get_check_bool(self, field_name):
        return '☑' if field_name else '☐'

    def _generate_print_report(self):

        template        = 'cdn_simrs_rekamedis_add/template/klinik_mata/surgikal_safety_checklist.docx'
        data_field      = {
            'no_rm'          : self.pasien_id.no_rm or '',
            'nama_pasien'    : self.pasien_id.name or '',
            'tgl_lahir'      : str(self.tanggal_lahir) if self.tanggal_lahir else '',

            'prosedure_tindakan'    : self.prosedure_tindakan or '',
            'ruang_rawat'           : self.ruang_rawat or '',
            'tanggal'               : str(self.tanggal_operasi) if self.tanggal_operasi else '',

            'jam_sign_in'  : self.rm_base_id._tanggal_indonesia(self.rm_base_id._to_wib(self.sign_in_time), True, True) if self.sign_in_time else '',
            'jam_time_out' : self.rm_base_id._tanggal_indonesia(self.rm_base_id._to_wib(self.time_out_time), True, True) if self.time_out_time else '',
            'jam_sign_out' : self.rm_base_id._tanggal_indonesia(self.rm_base_id._to_wib(self.sign_out_time), True, True) if self.sign_out_time else '',

            # SIGN IN
            'verif_identitas_gelang'    : self._get_check_bool(self.verif_identitas_gelang),
            'verif_informed_consent'    : self._get_check_bool(self.verif_informed_consent),
            'verif_dokter_bedah'        : self._get_check_bool(self.dokter_bedah_id),
            'dokter_bedah_name'         : self.dokter_bedah_id.name or '',
            'verif_dokter_anestesi'     : self._get_check_bool(self.dokter_anestesi_id),
            'dokter_anestesi_name'      : self.dokter_anestesi_id.name or '',
            'verif_tindakan'            : self._get_check_bool(self.nama_tindakan),
            'tindakan_name'             : self.nama_tindakan or '',
            
            'verif_pemberian_tanda_lokasi'       : self._get_check_bool(self.tanda_lokasi_operasi),
            'verif_pemberian_tanda_lokasi_ya'    : self._get_check_bool(True if self.tanda_lokasi_operasi == 'ya' else False),
            'verif_pemberian_tanda_lokasi_tidak' : self._get_check_bool(True if self.tanda_lokasi_operasi == 'tidak' else False),

            'diagnosa_pasien' : self.diagnosa_pasien or '',

            'verif_mesin_anestesi'      : self._get_check_bool(self.mesin_anestesi),
            'verif_iv_line'             : self._get_check_bool(self.iv_line),
            'verif_obat_obatan'         : self._get_check_bool(self.obat_obatan),
            'verif_lab'                 : self._get_check_bool(self.laboratorium),
            'verif_penggunakan_selang'  : self._get_check_bool(self.selang_o2),
            
            'kesadaran'     : self.kesadaran or '',
            'tekanan_darah' : str(self.systolic_bp or '')+' / '+str(self.diastolic_bp or ''),
            'nadi'          : str(self.hr or ''),
            'spo'           : str(self.spo2 or ''),
            'suhu'          : str(self.temp or ''),
            'skala_nyeri'   : self.skala_nyeri or '',

            'verif_riwayat_alergi_ada'    : self._get_check_bool(True if self.riwayat_alergi == 'ada' else False),
            'riwayat_alergi'              : self.alergi_keterangan,
            'verif_riwayat_alergi_tidak'  : self._get_check_bool(True if self.riwayat_alergi == 'tidak' else False),

            'verif_gangguan_napas_ya'     : self._get_check_bool(True if self.risiko_aspirasi == 'ya' else False),
            'verif_gangguan_napas_tidak'  : self._get_check_bool(True if self.risiko_aspirasi == 'tidak' else False),

            'verif_resiko_pendarahan_ya'     : self._get_check_bool(True if self.risiko_perdarahan == 'ya' else False),
            'verif_resiko_pendarahan_tidak'  : self._get_check_bool(True if self.risiko_perdarahan == 'tidak' else False),

            'verif_ukuran_lensa_ya'     : self._get_check_bool(True if self.lensa_tanam_status == 'sesuai' else False),
            'verif_ukuran_lensa_tidak'  : self._get_check_bool(True if self.lensa_tanam_status == 'ganti' else False),
            'ganti_ukuran_lensa'        : self.ukuran_iol or '..............',

            # TIME OUT
            'verif_tanggal_tindakan'        : self._get_check_bool(self.verbal_tanggal),
            'verif_nama_tindakan'           : self._get_check_bool(self.verbal_nama_tindakan),
            'verif_lokasi_tindakan'         : self._get_check_bool(self.verbal_lokasi),
            'verif_identitas_pasien'        : self._get_check_bool(self.verbal_identitas),
            'verif_prosedure_tindakan'      : self._get_check_bool(self.verbal_prosedur),
            'verif_inform_consent'          : self._get_check_bool(self.verbal_informed_consent),
            'verif_konfirmasi_seluruh_tim'  : self._get_check_bool(self.verbal_konfirmasi_tim),

            'verif_lengkap'         : self._get_check_bool(True if self.tim_fasilitas_lengkap == 'lengkap' else False),
            'verif_tidak_lengkap'   : self._get_check_bool(True if self.tim_fasilitas_lengkap == 'tidak' else False),

            'verif_umum'     : self._get_check_bool(self.anestesi_umum),
            'verif_lokal'    : self._get_check_bool(self.anestesi_lokal),
            'verif_topikal'  : self._get_check_bool(self.anestesi_topikal),
            'verif_spinal'   : self._get_check_bool(self.anestesi_spinal),
            'verif_epidural' : self._get_check_bool(self.anestesi_epidural),
            'verif_blok'     : self._get_check_bool(self.anestesi_blok),

            'verif_kurang_dari_60_tidak'  : self._get_check_bool(True if self.antibiotik_diberikan == 'tidak' else False),
            'verif_kurang_dari_60_ya'     : self._get_check_bool(True if self.antibiotik_diberikan == 'ya' else False),
            'nama_obat'    : self.antibiotik_nama or '',
            'jam_obat'     : self.rm_base_id._tanggal_indonesia(self.rm_base_id._to_wib(self.antibiotik_jam), True, True) if self.antibiotik_jam else '',
            'dosis_obat'   : self.antibiotik_dosis or '',

            'antisipasi_kehilangan_darah'            : self.antisipasi_bedah or '..........',
            'antisipasi_kehilangan_darah_anestesi'   : self.antisipasi_anestesi or '.........',

            'indikator_strelisasi_ya'    : self._get_check_bool(True if self.indikator_sterilisasi == 'ya' else False),
            'indikator_strelisasi_tidak' : self._get_check_bool(True if self.indikator_sterilisasi == 'tidak' else False),
            'tidak_instrument_ya'        : self._get_check_bool(True if self.instrumen_lengkap == 'ya' else False),
            'tidak_instrument_tidak'     : self._get_check_bool(True if self.instrumen_lengkap == 'tidak' else False),
            'kondisi_khusus_ya'          : self._get_check_bool(True if self.kondisi_khusus_pasien == 'ya' else False),
            'kondisi_khusus_tidak'       : self._get_check_bool(True if self.kondisi_khusus_pasien == 'tidak' else False),
            'kondisi_khusus_catatan'     : self.kondisi_khusus_catatan or '..........',
            'hasil_usg_ya'               : self._get_check_bool(True if self.hasil_usg == 'ya' else False),
            'hasil_usg_tidak'            : self._get_check_bool(True if self.hasil_usg == 'tidak' else False),
            'hasil_usg_catatan'          : self.hasil_usg_catatan or '...........',
            
            # SIGN OUT
            'verif_nama_tindakan_so'        : self._get_check_bool(self.nama_tindakan),
            'nama_tindakan_so'              : self.nama_tindakan or '...........................',

            'verif_instrumen'       : self._get_check_bool(self.cek_instrumen),
            'verif_kassa'           : self._get_check_bool(self.cek_kassa),
            'verif_jarum'           : self._get_check_bool(self.cek_jarum),
            'verif_spoon'           : self._get_check_bool(self.cek_spon),
            'verif_depper'          : self._get_check_bool(self.cek_depper),
            'verif_lainnya'         : self._get_check_bool(self.cek_lainnya),
            'name_lainnya'          : self.cek_lainnya or '',

            'verif_preparat_ya'     : self._get_check_bool(True if self.preparat_ada == 'ya' else False),
            'verif_preparat_tidak'  : self._get_check_bool(True if self.preparat_ada == 'tidak' else False),
            
            'verif_jenis_pa'        : self._get_check_bool(True if self.preparat_jenis == 'pa' else False),
            'verif_jenis_kultur'    : self._get_check_bool(True if self.preparat_jenis == 'kultur' else False),
            'verif_jenis_sitologi'  : self._get_check_bool(True if self.preparat_jenis == 'sitologi' else False),
            'verif_jenis_lainnya'   : self._get_check_bool(True if self.preparat_jenis == 'lainnya' else False),
            'verif_jenis_tidak_ada' : self._get_check_bool(True if self.preparat_jenis == 'tidak_ada' else False),

            'verif_formulir_ya'     : self._get_check_bool(True if self.formulir_ada == 'ya' else False),
            'verif_formulir_tidak'  : self._get_check_bool(True if self.formulir_ada == 'tidak' else False),

            'verif_ip_ya'     : self._get_check_bool(True if self.identitas_lengkap == 'ya' else False),
            'verif_ip_tidak'  : self._get_check_bool(True if self.identitas_lengkap == 'tidak' else False),

            'dari_operator'          : self.perhatian_operator or '......',
            'dari_dokter_anestesi'   : self.perhatian_anestesi or '......',
            'dari_perawat_bedah'     : self.perhatian_perawat or '......',

            'verif_pasien_pindah_pemulihan_ya'      : self._get_check_bool(True if self.pindah_recovery == 'ya' else False),
            'verif_pasien_pindah_pemulihan_tidak'   : self._get_check_bool(True if self.pindah_recovery == 'tidak' else False),

            'verif_ada_rembesan_ya'      : self._get_check_bool(True if self.kondisi_luka == 'rembesan' else False),
            'verif_ada_rembesan_tidak'   : self._get_check_bool(True if self.kondisi_luka == 'tidak' else False),

            'instruksi_khusus_pemulihan'     : self.instruksi_khusus or '..........',
            'ttd_dokter': self.qr_ttd_dokter_partner_id.name or '..................................',
            'ttd_perawat': self.qr_ttd_perawat_partner_id.name or '..................................',

        }
        return self._mail_merge_to_pdf(
            path        = template,
            data_info   = data_field,
            image_info  = [
                {'key'   : '{{logo}}', 'value' : self.company_id.logo, 'inches': 1},
                {'key'   : '{{ttd_perawat}}','value' : self.qr_ttd_perawat_code,'inches'    : 1,},
                {'key'   : '{{ttd_dokter}}','value' : self.qr_ttd_dokter_code,'inches'    : 1,},
            ],
            list_info   = []
        )
    
    def action_print(self):
        # print(self._get_boolean_checkbox('cek_instrumen'))

        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/{self._name}/{self.id}/_generate_print_report',
            'target': 'new',
        }





