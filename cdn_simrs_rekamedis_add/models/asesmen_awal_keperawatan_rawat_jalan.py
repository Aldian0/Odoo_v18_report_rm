
from odoo import _, api, fields, models

class AsesmenAwalKeperawatanRawatJalan(models.Model):
    _name = 'cdn.asesmen.awal.keperawatan.rawat.jalan'
    _description = 'Asesmen Awal Keperawatan Rawat Jalan'
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

    alamat = fields.Text(string='Alamat')
    nik = fields.Char(string='NIK')
    no_telepon_hp = fields.Char(string='No. Telepon / HP')

    pendidikan = fields.Selection([
        ('tdk_sekolah', 'Tidak Sekolah'),
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('diploma', 'Diploma'),
        ('pt', 'Perguruan Tinggi'),
    ], string='Pendidikan')

    status_perkawinan = fields.Selection([
        ('kawin', 'Kawin'),
        ('belum_kawin', 'Belum Kawin'),
        ('janda_duda', 'Janda / Duda'),
    ], string='Status Perkawinan')

    agama = fields.Selection([
        ('islam', 'Islam'),
        ('kristen', 'Kristen'),
        ('katolik', 'Katolik'),
        ('hindu', 'Hindu'),
        ('budha', 'Budha'),
        ('lainnya', 'Lainnya'),
    ], string='Agama')
    agama_lainnya_sebutkan = fields.Char(string='Sebutkan agama lainnya')

    suku = fields.Selection([
        ('jawa', 'Jawa'),
        ('tionghoa', 'Tionghoa'),
        ('madura', 'Madura'),
        ('lainnya', 'Lainnya'),
    ], string='Suku')
    suku_lainnya_sebutkan = fields.Char(string='Sebutkan suku lainnya')

    bahasa = fields.Selection([
        ('indonesia', 'Indonesia'),
        ('jawa', 'Jawa'),
        ('madura', 'Madura'),
        ('mandarin', 'Mandarin'),
        ('lainnya', 'Lainnya'),
    ], string='Bahasa')
    bahasa_lainnya_sebutkan = fields.Char(string='Sebutkan bahasa lainnya')

    pekerjaan = fields.Selection([
        ('swasta', 'Swasta'),
        ('pns', 'PNS'),
        ('bumn_bumd', 'BUMN/BUMD'),
        ('wiraswasta', 'Wiraswasta'),
        ('lainnya', 'Lainnya'),
    ], string='Pekerjaan')
    pekerjaan_lainnya_sebutkan = fields.Char(string='Sebutkan pekerjaan lainnya')

    status_pembiayaan = fields.Selection([
        ('umum', 'Umum'),
        ('bpjs_kesehatan', 'BPJS Kesehatan'),
        ('bpjs_ketenagakerjaan', 'BPJS Ketenagakerjaan'),
        ('asuransi', 'Asuransi'),
        ('perusahaan_piutang', 'Perusahaan / Piutang'),
        ('lainnya', 'Lainnya'),
    ], string='Status Pembiayaan')
    status_pembiayaan_lainnya_sebutkan = fields.Char(string='Sebutkan status pembiayaan lainnya')

    klinik_dituju = fields.Selection([
        ('umum', 'Umum'),
        ('penyakit_dalam', 'Penyakit Dalam'),
        ('anak', 'Anak'),
        ('bedah', 'Bedah'),
        ('orthopedi', 'Orthopedi'),
        ('syaraf', 'Syaraf'),
        ('kebidanan_kandungan', 'Kebidanan / Kandungan'),
        ('mata', 'Mata'),
        ('gigi', 'Gigi'),
        ('tht', 'THT'),
        ('lainnya', 'Lainnya'),
    ], string='Klinik yang dituju')

    klinik_lainnya_sebutkan = fields.Char(string='Sebutkan klinik lainnya')

    # === WAKTU ===
    waktu_tanggal_jam_datang = fields.Datetime(string='Tanggal / Jam Datang')
    waktu_tanggal_jam_mulai_tindakan = fields.Datetime(string='Tanggal / Jam Mulai Tindakan')
    waktu_tanggal_jam_selesai_tindakan = fields.Datetime(string='Tanggal / Jam Selesai Tindakan')

    # === ALERGI / REAKSI ===

    alergi_status = fields.Selection([
        ('tidak', 'Tidak'),
        ('ya', 'Ya'),
    ], string='Alergi')
    alergi_jenis = fields.Char(string='Jenis Alergi')
    alergi_obat_sebutkan = fields.Char(string='Alergi Obat, Sebutkan')
    alergi_obat_reaksi = fields.Char(string='Reaksi Alergi Obat')
    alergi_makanan_sebutkan = fields.Char(string='Alergi Makanan, Sebutkan')
    alergi_makanan_reaksi = fields.Char(string='Reaksi Alergi Makanan')

    alergi_lainnya_sebutkan = fields.Char(string='Alergi Lainnya, Sebutkan')
    alergi_lainnya_reaksi = fields.Char(string='Reaksi Alergi Lainnya')

    # === SKRINING GIZI BERDASARKAN MST ===

    mst_penurunan_bb = fields.Selection([
        ('tidak_ada', 'Tidak ada'),
        ('tidak_yakin', 'Tidak yakin'),
        ('ya', 'Ya, ada penurunan berat badan'),
    ], string='Penurunan BB')
    mst_penurunan_bb_jumlah = fields.Selection([
        ('1_5', '1-5 kg'),
        ('6_10', '6-10 kg'),
        ('11_15', '11-15 kg'),
        ('lebih_15', '> 15 kg'),
    ], string='Jumlah Penurunan BB')
    mst_skor_penurunan_bb = fields.Integer(string='Skor Penurunan BB', compute='_compute_mst_total_skor', store=True, default=0)

    mst_asupan_makanan = fields.Selection([
        ('tidak', 'Tidak'),
        ('ya', 'Ya'),
    ], string='Asupan Makanan Berkurang')
    mst_skor_asupan_makanan = fields.Integer(string='Skor Asupan Makanan', compute='_compute_mst_total_skor', store=True, default=0)

    mst_total_skor = fields.Integer(string='Total Skor', compute='_compute_mst_total_skor', store=True)

    mst_diagnosa_khusus_status = fields.Selection([
        ('tidak', 'Tidak'),
        ('ya', 'Ya, Lapor DPJP untuk konsultasi gizi'),
    ], string='Diagnosa Khusus')
    mst_diagnosa_khusus = fields.Selection([
        ('dm', 'DM'),
        ('ginjal', 'Ginjal'),
        ('hati', 'Hati'),
        ('jantung', 'Jantung'),
        ('kanker', 'Kanker'),
        ('stroke', 'Stroke'),
        ('paru', 'Paru'),
        ('geriatri', 'Geriatri'),
        ('penurunan_imunitas', 'Penurunan Imunitas'),
        ('lainnya', 'Lainnya'),
    ], string='Jenis Diagnosa Khusus')
    mst_diagnosa_khusus_lainnya_sebutkan = fields.Char(string='Sebutkan diagnosa khusus lainnya')

    # === STATUS FUNGSIONAL ===
    status_fungsional = fields.Selection([
        ('mandiri', 'Mandiri'),
        ('ketergantungan_total', 'Ketergantungan Total'),
        ('perlu_bantuan', 'Perlu bantuan'),
    ], string='Status Fungsional')
    status_fungsional_ketergantungan_total_dilaporkan_ke_dokter = fields.Datetime(string='Dilaporkan ke dokter (WIB)')
    status_fungsional_perlu_bantuan_sebutkan = fields.Text(string='Sebutkan bantuan yang diperlukan')

    # === PSIKOSOSIAL ===
    psikososial_status_psikologis = fields.Selection([
        ('tenang', 'Tenang'),
        ('cemas', 'Cemas'),
        ('takut', 'Takut'),
        ('marah', 'Marah'),
        ('sedih', 'Sedih'),
        ('kecenderungan_bunuh_diri', 'Kecenderungan bunuh diri'),
    ], string='Status Psikologis')

    psikososial_status_mental = fields.Selection([
        ('sadar_orientasi_baik', 'Sadar dan orientasi baik'),
        ('lainnya', 'Lainnya'),
    ], string='Status Mental')

    psikososial_ada_masalah_perilaku = fields.Selection([
        ('tidak', 'Tidak'),
        ('ya', 'Ada masalah perilaku'),
    ], string='Masalah Perilaku')
    psikososial_masalah_perilaku_sebutkan = fields.Text(string='Sebutkan masalah perilaku')
    psikososial_perilaku_kekerasan_sebelumnya = fields.Text(string='Perilaku kekerasan yang dialami pasien sebelumnya')

    psikososial_kebutuhan_kerohanian = fields.Selection([
        ('tidak', 'Tidak'),
        ('ya', 'Ya'),
    ], string='Kebutuhan Pelayanan Kerohanian')

    # === ASESMEN RISIKO JATUH TIME UP GO TEST (TUG) ===
    tug_a = fields.Selection([
        ('ya', 'Ya (Tidak seimbang)'),
        ('tidak', 'Tidak (Seimbang)'),
    ], string='TUG A')
    tug_b = fields.Selection([
        ('ya', 'Ya (Memegang penopang)'),
        ('tidak', 'Tidak (Tidak memegang)'),
    ], string='TUG B')
    tug_hasil = fields.Selection([
        ('tidak_beresiko', 'Tidak beresiko (tidak ditemukan a dan b)'),
        ('resiko_rendah', 'Resiko Rendah (tidak ditemukan salah satu a dan b)'),
        ('resiko_tinggi', 'Resiko Tinggi (ditemukan a dan b)'),
    ], string='Hasil')

    # === ASESMEN NYERI ===
    nyeri_kualitas = fields.Selection([
        ('terbakar', 'Terbakar'),
        ('tajam', 'Tajam'),
        ('tertekan', 'Tertekan'),
        ('tumpul', 'Tumpul'),
        ('lain', 'Lain-lain'),
    ], string='Kualitas Nyeri')
    nyeri_kualitas_lainnya_sebutkan = fields.Char(string='Sebutkan kualitas nyeri lainnya')


    nyeri_wong_baker_scale = fields.Selection([
        ('0', '0 - Tidak Nyeri'),
        ('1', '1 - Nyeri Ringan'),
        ('2', '2 - Nyeri Ringan'),
        ('3', '3 - Nyeri Ringan'),
        ('4', '4 - Nyeri Sedang'),
        ('5', '5 - Nyeri Sedang'),
        ('6', '6 - Nyeri Sedang'),
        ('7', '7 - Nyeri Berat'),
        ('8', '8 - Nyeri Berat'),
        ('9', '9 - Nyeri Berat'),
        ('10', '10 - Nyeri Berat'),
    ], string='Wong Baker Face Scale (0-10)', default='0')

    nyeri_waktu = fields.Selection([
        ('hilang_timbul', 'Hilang Timbul'),
        ('terus_menerus', 'Terus Menerus'),
    ], string='Waktu Nyeri')

    nyeri_lama_menit = fields.Integer(string='Lama Nyeri (menit)')
    nyeri_lokasi = fields.Text(string='Lokasi Nyeri')
    nyeri_diperberat_oleh = fields.Text(string='Diperberat oleh')

    # === FLACC PAIN SCALE ===
    flacc_face = fields.Selection([
        ('0', '0 - Tidak ada ekspresi'),
        ('1', '1 - Menyeringai'),
        ('2', '2 - Dagu gemetar dan rahang dikatup erat'),
    ], string='Face (Wajah)')
    flacc_skor_face = fields.Integer(string='Skor Face', compute='_compute_flacc_total_skor', store=True, default=0)

    flacc_leg = fields.Selection([
        ('0', '0 - Normal'),
        ('1', '1 - Gelisah, tegang'),
        ('2', '2 - Menendang / melawan'),
    ], string='Leg (Kaki)')
    flacc_skor_leg = fields.Integer(string='Skor Leg', compute='_compute_flacc_total_skor', store=True, default=0)

    flacc_activity = fields.Selection([
        ('0', '0 - Terbaring tenang'),
        ('1', '1 - Menggeliat, tegang'),
        ('2', '2 - Kaku atau kejang'),
    ], string='Activity (Aktivitas)')
    flacc_skor_activity = fields.Integer(string='Skor Activity', compute='_compute_flacc_total_skor', store=True, default=0)

    flacc_cry = fields.Selection([
        ('0', '0 - Tidak menangis'),
        ('1', '1 - Merintih, merengek'),
        ('2', '2 - Terus menangis, menjerit'),
    ], string='Cry (Menangis)')
    flacc_skor_cry = fields.Integer(string='Skor Cry', compute='_compute_flacc_total_skor', store=True, default=0)

    flacc_consolability = fields.Selection([
        ('0', '0 - Santai'),
        ('1', '1 - Dapat ditenangkan dengan sentuhan, pelukan, bujukan'),
        ('2', '2 - Sulit dibujuk'),
    ], string='Consolability (Konsabilitas)')
    flacc_skor_consolability = fields.Integer(string='Skor Consolability', compute='_compute_flacc_total_skor', store=True, default=0)

    flacc_total_skor = fields.Integer(string='Total Skor FLACC', compute='_compute_flacc_total_skor', store=True)

    # === EDUKASI ===
    edukasi_topik = fields.Selection([
        ('penggunaan_obat', 'Penggunaan obat - obat secara efektif dan aman'),
        ('manajemen_nyeri', 'Penyakit Manajemen Nyeri'),
        ('peralatan_medis', 'Penggunaan peralatan medis secara efektif dan aman'),
        ('risiko_jatuh', 'Risiko Jatuh'),
        ('cuci_tangan', 'Cuci Tangan'),
        ('diet_nutrisi', 'Diet dan Nutrisi'),
        ('lainnya', 'Lainnya'),
    ], string='Kebutuhan edukasi')

    edukasi_lainnya_sebutkan = fields.Char(string='Sebutkan edukasi lainnya')
    edukasi_masalah_keperawatan = fields.Text(string='Masalah Keperawatan')

    # === RENCANA DAN TINDAKAN KEPERAWATAN ===
    rencana_tindakan_keperawatan = fields.Text(string='Rencana dan Tindakan Keperawatan')

    # === EVALUASI (SOAP) ===
    evaluasi_soap = fields.Text(string='Evaluasi (SOAP)')

    # === TANDA TANGAN ===

    perawat_tanda_tangan = fields.Many2one('res.users', string='Tanda Tangan & Nama Perawat')

    @api.depends('mst_penurunan_bb', 'mst_penurunan_bb_jumlah', 'mst_asupan_makanan')
    def _compute_mst_total_skor(self):
        for record in self:
            skor_bb = 0
            if record.mst_penurunan_bb == 'tidak_ada':
                skor_bb = 0
            elif record.mst_penurunan_bb == 'tidak_yakin':
                skor_bb = 2
            elif record.mst_penurunan_bb == 'ya':
                if record.mst_penurunan_bb_jumlah == '1_5':
                    skor_bb = 1
                elif record.mst_penurunan_bb_jumlah == '6_10':
                    skor_bb = 2
                elif record.mst_penurunan_bb_jumlah == '11_15':
                    skor_bb = 3
                elif record.mst_penurunan_bb_jumlah == 'lebih_15':
                    skor_bb = 4
            record.mst_skor_penurunan_bb = skor_bb

            skor_asupan = 1 if record.mst_asupan_makanan == 'ya' else 0
            record.mst_skor_asupan_makanan = skor_asupan

            record.mst_total_skor = skor_bb + skor_asupan

    @api.depends('flacc_face', 'flacc_leg', 'flacc_activity', 'flacc_cry', 'flacc_consolability')
    def _compute_flacc_total_skor(self):
        for record in self:
            try:
                skor_face = int(record.flacc_face or 0)
                skor_leg = int(record.flacc_leg or 0)
                skor_activity = int(record.flacc_activity or 0)
                skor_cry = int(record.flacc_cry or 0)
                skor_consolability = int(record.flacc_consolability or 0)
            except ValueError:
                skor_face = skor_leg = skor_activity = skor_cry = skor_consolability = 0
            record.flacc_skor_face = skor_face
            record.flacc_skor_leg = skor_leg
            record.flacc_skor_activity = skor_activity
            record.flacc_skor_cry = skor_cry
            record.flacc_skor_consolability = skor_consolability
            record.flacc_total_skor = skor_face + skor_leg + skor_activity + skor_cry + skor_consolability
