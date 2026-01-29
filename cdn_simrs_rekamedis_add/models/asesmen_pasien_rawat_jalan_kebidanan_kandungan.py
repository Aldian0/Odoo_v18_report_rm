from odoo import _, api, fields, models



class AsesmenPasienRawatJalanKebidananKandungan(models.Model):
    _name = 'cdn.asesmen.pasien.rawat.jalan.kebidanan.kandungan'
    _description = 'Asesmen Pasien Rawat Jalan Kebidanan Kandungan'
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
    
    # ===== DATA PASIEN =====
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

    rujukan = fields.Selection([
        ('rs_pemerintah', 'RS Pemerintah'),
        ('rs_swasta', 'RS Swasta'),
        ('rb', 'RB'),
        ('pkm', 'PKM'),
        ('dps', 'DPS'),
        ('bpm', 'BPM'),
        ('lainnya', 'Lainnya'),
    ], string='Tempat Rujukan')
    rujukan_lainnya_sebutkan = fields.Char(string='Sebutkan tempat rujukan lainnya')

    # WAKTU
    waktu_tanggal_jam_datang = fields.Datetime(string='Tanggal / Jam Datang')
    waktu_tanggal_jam_mulai_tindakan = fields.Datetime(string='Tanggal / Jam Mulai Tindakan')
    waktu_tanggal_jam_selesai_tindakan = fields.Datetime(string='Tanggal / Jam Selesai Tindakan')



    # ===== ASESMEN KEBIDANAN =====
    pendarahan_hamil = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Pendarahan Saat Hamil')
    jelaskan_pendarahan = fields.Char(string='Jelaskan Pendarahan Saat Hamil Jika Ya')

    status_imunisasi = fields.Selection([
        ('tt1', 'TT1'),
        ('tt2', 'TT2'),
        ('tt3', 'TT3'),
        ('tt4', 'TT4'),
        ('tt5', 'TT5'),
    ], string='Status Imunisasi')
    
    # Kebiasaan Ibu
    kebiasaan_merokok = fields.Boolean(string="Kebiasaan Merokok", default=False)
    kebiasaan_minum_alkohol = fields.Boolean(string="Kebiasaan Minum Alkohol", default=False)
    kebiasaan_obat_obatan = fields.Boolean(string="Kebiasaan Obat Obatan", default=False)
    kebiasaan_jamu = fields.Boolean(string="Kebiasaan Jamu", default=False)
    
    # Riwayat Penyakit Ibu
    riwayat_ht = fields.Boolean(string="Hipertensi", default=False) 
    riwayat_dm = fields.Boolean(string="Diabetes Melitus", default=False)
    riwayat_jantung = fields.Boolean(string="Kelainan Jantung", default=False)
    riwayat_per = fields.Boolean(string="PER", default=False)
    riwayat_peb = fields.Boolean(string="PEB", default=False)
    riwayat_eklampsia = fields.Boolean(string="Eklampsia", default=False)
    riwayat_prematuritas = fields.Boolean(string="Prematuritas", default=False)
    riwayat_toxoplasmosis = fields.Boolean(string="Toxoplasmosis", default=False)
    riwayat_penyakit_lain = fields.Char(string="Riwayat Penyakit Lain", default=False)

    # Riwayat Penyakit Keluarga
    keluarga_preeklampsia = fields.Boolean(string="Keluarga Preeklamsia", default=False)
    keluarga_ht = fields.Boolean(string="Hipertensi", default=False)
    keluarga_dm = fields.Boolean(string="Diabetes Melitus", default=False)
    keluarga_gemelli = fields.Boolean(string="Kembar", default=False)
    keluarga_lainnya = fields.Char(string="Keluarga Lainnya")

    # Riwayat ANC(Pemeriksaan Kehamilan)
    pernah_anc = fields.Boolean(string="Pernah ANC", default=True)
    lokasi_anc = fields.Char(string="Bidan/RB/DPS/PKM/RS", default=False)
    alasan_tidak_anc = fields.Text(string="Alasan Tidak ANC", blank=True)
    frekuensi_anc = fields.Integer(string="Frekuensi ANC", default=0)

    # DATA PELENGKAP
    pemberian_tablet_fe = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Pemberian Tablet Fe')

    senam_bumil = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Senam Ibu Hamil')

    temu_wicara = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Temu Wicara')

    reduksi_urin = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Pemeriksaan Reduksi Urin')
    hasil_pemeriksaan_urin = fields.Text(string='Hasil Pemeriksaan Reduksi Urin')

    terapi_malaria = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Pemberian Terapi Malaria')
    hasil_pemeriksaan_malaria = fields.Text(string='Hasil Pemeriksaan Terapi Malaria')

    vdrl = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Pemeriksaan VDRL')

    perawatan_payudara = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Perawatan Payudara')

    terapi_iodium = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Terapi Kapsul Iodiumm')

    protein_urin = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Pemeriksaan Protein Urin')
    hasil_protein_urin = fields.Text(string="Hasil Periksa Protein Urin", default='')

    # PEMERIKSAAN PENUNJANG
    plano_test = fields.Selection([
        ('+', '(+)'),
        ('-', '(-)')
    ], string="Keterangan Plano Test")
    sebutkan_plano = fields.Char(string='Sebutkan Plano')

    hb_level = fields.Float(string="Kadar Hb", digits=(4, 1), help="Input kadar Hemoglobin pasien dalam satuan g/dL")
    alergi = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string='Alergi')
    jenis_alergi = fields.Char(string='Jenis Alergi')

    riwayat_kehamilan_ids = fields.One2many(
        comodel_name='cdn.riwayat.kehamilan.pasien', 
        inverse_name='asesmen_id', 
        string='Riwayat Kehamilan & Persalinan Yang Lalu'
    )

    # REPORT PDF
    def action_print_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/cdn_print_report_pdf/{self._name}/{self.id}/print_report',
            'target': 'new',
        }

    def _get_boolean_checkbox(self, field_name):
        value = self[field_name]
        field_info = self.fields_get([field_name])
        label = field_info[field_name].get('string', field_name)
        if value:
            return f"☑ {label}"
        else:
            return f"☐ {label}"

    def _get_selection_checkbox(self, field_name):
        value = self[field_name]
        field_info = self.fields_get([field_name])
        selections = field_info[field_name].get('selection', [])
        result = []
        for key, label in selections:
            if key == value:
                result.append(f"☑ {label}")
            else:
                result.append(f"☐ {label}")
        return "    ".join(result)
    
    def print_report(self):
        riwayat_kehamilan_list = []
        for riwayat in self.riwayat_kehamilan_ids:
            riwayat_kehamilan_list.append({
                'kehamilan'   : str(riwayat.kehamilan_ke or ''),
                'suami'       : str(riwayat.suami_ke or ''),
                'cara_pers'   : dict(riwayat._fields['cara_pers'].selection).get(riwayat.cara_pers, '') if riwayat.cara_pers else '',
                'tmp_pers'    : riwayat.tempat_pers or '',
                'masa_nifas'  : dict(riwayat._fields['masa_nifas'].selection).get(riwayat.masa_nifas, '') if riwayat.masa_nifas else '',
                'laktasi'     : dict(riwayat._fields['laktasi'].selection).get(riwayat.laktasi, '') if riwayat.laktasi else '',
                'lp'          : dict(riwayat._fields['jenis_kelamin'].selection).get(riwayat.jenis_kelamin, '') if riwayat.jenis_kelamin else '',
                'bb_tb'       : str(riwayat.bb_bayi or ''), 
                'kb_dipakai'  : riwayat.kb_dipakai or '',
                'usia_anak'   : riwayat.usia_anak or '',  
            })
        data_list = [
                {
                    'key'   : 'kehamilan',
                    'value' : riwayat_kehamilan_list,
                }
            ]

        data_info = {   
            'nama'                          : self.pasien_id.name or '',
            'tgl_lahir'                     : self.pasien_id.tanggal_lahir.strftime('%d/%m/%Y') if self.pasien_id.tanggal_lahir else '',
            'no_rm'                         : self.pasien_id.no_rm or '',
            'alamat'                        : self.alamat or '', 
            'nik'                           : self.pasien_id.nik or '',
            'no_telp'                       : self.pasien_id.mobile or '',
            'suku'                          : dict(self._fields['suku'].selection).get(self.suku, '') if self.suku else '',
            'bahasa'                        : dict(self._fields['bahasa'].selection).get(self.bahasa, '') if self.bahasa else '',
            'pendidikan'                    : dict(self._fields['pendidikan'].selection).get(self.pendidikan, '') if self.pendidikan else '',            
            'status_perkawinan'             : dict(self._fields['status_perkawinan'].selection).get(self.status_perkawinan, '') if self.status_perkawinan else '',
            'agama'                         : dict(self._fields['agama'].selection).get(self.agama, '') if self.agama else '',    
            'pekerjaan'                     : self.pekerjaan or '',     
            'rujukan'                       : self.rujukan or '', 
            'datang'                        : self.waktu_tanggal_jam_datang.strftime('%d/%m/%Y %H:%M') if self.waktu_tanggal_jam_datang else '',
            'mulai_periksa'                 : self.waktu_tanggal_jam_mulai_tindakan.strftime('%H:%M') if self.waktu_tanggal_jam_mulai_tindakan else '',
            'selesai_periksa'               : self.waktu_tanggal_jam_selesai_tindakan.strftime('%H:%M') if self.waktu_tanggal_jam_selesai_tindakan else '',
            'status_imunisasi'              : dict(self._fields['status_imunisasi'].selection).get(self.status_imunisasi, '') if self.status_imunisasi else '',
            'pendarahan_ya'                 : '☑ Ya' if self.pendarahan_hamil == 'ya' else '☐ Ya',
            'pendarahan_tidak'              : '☑ Tidak' if self.pendarahan_hamil == 'tidak' else '☐ Tidak',
            'pendarahan_hamil_jelaskan'     : self.jelaskan_pendarahan if self.pendarahan_hamil == 'ya' else '....................',
    
            'merokok'                       : self._get_boolean_checkbox('kebiasaan_merokok'),
            'alkohol'                       : self._get_boolean_checkbox('kebiasaan_minum_alkohol'),
            'obat'                          : self._get_boolean_checkbox('kebiasaan_obat_obatan'),
            'jamu'                          : self._get_boolean_checkbox('kebiasaan_jamu'),


            'ht'                            : self._get_boolean_checkbox('riwayat_ht'),
            'dm'                            : self._get_boolean_checkbox('riwayat_dm'),
            'jantung'                       : self._get_boolean_checkbox('riwayat_jantung'),
            'per'                           : self._get_boolean_checkbox('riwayat_per'),
            'peb'                           : self._get_boolean_checkbox('riwayat_peb'),
            'eklam'                         : self._get_boolean_checkbox('riwayat_eklampsia'),
            'premat'                        : self._get_boolean_checkbox('riwayat_prematuritas'),
            'toxop'                         : self._get_boolean_checkbox('riwayat_toxoplasmosis'),
            'r_ya'                          : self._get_boolean_checkbox('riwayat_penyakit_lain'),
            'r_lain'                        : self.riwayat_penyakit_lain or '....................',

            'kel_eklam'                     : self._get_boolean_checkbox('keluarga_preeklampsia'),
            'kel_ht'                        : self._get_boolean_checkbox('keluarga_ht'),
            'ke_dm'                         : self._get_boolean_checkbox('keluarga_dm'),
            'kel_gemeli'                    : self._get_boolean_checkbox('keluarga_gemelli'),
            'lainnya'                       : self._get_boolean_checkbox('keluarga_lainnya'),
            'penyakit_lain'                 : self.keluarga_lainnya or '....................',

            'prn_anc'                       : self._get_boolean_checkbox('pernah_anc'),
            'als_anc'                       : self.alasan_tidak_anc or '....................',
            'lks_anc'                       : self.lokasi_anc or '....................',

            'frek_anc'                      : str(self.frekuensi_anc) if self.frekuensi_anc else '', 
            'f_1'                           : '☑ 1x' if self.frekuensi_anc == 1 else '☐ 1x',
            'f_2'                           : '☑ 2x' if self.frekuensi_anc == 2 else '☐ 2x',
            'f_3'                           : '☑ 3x' if self.frekuensi_anc == 3 else '☐ 3x',
            'f_4'                           : '☑ 4x' if self.frekuensi_anc == 4 else '☐ 4x',
            'f_5'                           : '☑ >5x' if self.frekuensi_anc >= 5 else '☐ >5x',

            'tablet_fe'                     : self._get_selection_checkbox('pemberian_tablet_fe'),

            'senam_bumil'                   : self._get_selection_checkbox('senam_bumil'),

            'temu_wicara'                   : self._get_selection_checkbox('temu_wicara'),

            'reduksi_urin'                  : self._get_selection_checkbox('reduksi_urin'),
            'hasil_urin'                    : self._get_selection_checkbox('hasil_pemeriksaan_urin'),
            'u_ket'                         : self.hasil_pemeriksaan_urin or '....................',

            'm_ya'                          : '☑ Ya' if self.terapi_malaria == 'ya' else '☐ Ya',
            'm_tdk'                         : '☑ Tidak' if self.terapi_malaria == 'tidak' else '☐ Tidak', 
            'm_kpn'                         : 'Hasil :' if self.hasil_pemeriksaan_malaria else '',
            'm_lain'                        : self.hasil_pemeriksaan_malaria or '....................',

            'vdrl_ya'                       : '☑ Ya' if self.vdrl == 'ya' else '☐ Ya',
            'vdrl_tdk'                      : '☑ Tidak' if self.vdrl == 'tidak' else '☐ Tidak',

            'p_ya'                          : '☑ Ya' if self.perawatan_payudara == 'ya' else '☐ Ya',
            'p_tdk'                         : '☑ Tidak' if self.perawatan_payudara == 'tidak' else '☐ Tidak',

            'pr_y'                          : '☑ Ya' if self.protein_urin == 'ya' else '☐ Ya',
            'pr_td'                         : '☑ Tidak' if self.protein_urin == 'tidak' else '☐ Tidak', 
            'pr_hs'                         : 'Hasil :' if self.hasil_protein_urin else '',
            'pr_ket'                        : self.hasil_protein_urin or '....................',

            'plano_tes'                     : self._get_selection_checkbox('plano_test'),
            'pl_hs'                         : self._get_selection_checkbox('sebutkan_plano'),
            'pl_ket'                        : self.sebutkan_plano or '....................',

            'alergi'                        : self._get_selection_checkbox('alergi'),
            'a_hs'                          : ', Jenis :' if self.jenis_alergi else 'Jenis :',
            'a_ket'                         : self.jenis_alergi or '....................',

            'hb'                            : str(self.hb_level) if self.hb_level else '',

            'terapi_kapsul'                 : self._get_selection_checkbox('terapi_iodium'),


        } 
            
            
        
        image_info = [
                # {
                #     'key'       : '{{gambar}}',
                #     'value'     : self.gambar_tess,
                #     'inches'    : 2,
                # }
            ]

        
        template_file = 'cdn_simrs_rekamedis_add/template/asesmen_pasien_rawat_jalan_kebidanan_kandungan.docx'
        return self.rm_base_id._mail_merge_to_pdf(
            path=template_file, 
            data_info=data_info, 
            list_info=data_list, 
            image_info=image_info)

class RiwayatKehamilanPasien(models.Model):
    _name = 'cdn.riwayat.kehamilan.pasien'
    _description = 'Riwayat Kehamilan dan Persalinan Pasien'

    asesmen_id    = fields.Many2one(
        comodel_name='cdn.asesmen.pasien.rawat.jalan.kebidanan.kandungan', 
        string='Asesmen Terkait', 
        ondelete='cascade'
    )
    

    kehamilan_ke  = fields.Integer(string='Kehamilan')
    suami_ke      = fields.Integer(string='Suami ke-')
    cara_pers     = fields.Selection([
        ('normal', 'Normal/Spontan'),
        ('sc', 'Sectio Caesarea (SC)'),
        ('vakum', 'Vakum Ekstraksi'),
        ('forcep', 'Forcep'),
        ('induksi', 'Induksi'),
        ('abortus', 'Abortus/Keguguran')
    ], string='Cara Persalinan')

    tempat_pers   = fields.Char(string='Tempat & Penolong', help="Contoh: RS Ganesha / dr. Agus, Sp.OG")
    masa_nifas    = fields.Selection([
        ('normal', 'Normal'),
        ('infeksi', 'Infeksi/Sepsis'),
        ('perdarahan', 'Perdarahan Postpartum'),
        ('eklampsia', 'Eklampsia Postpartum'),
        ('lainnya', 'Lain-lain')
    ], string='Masa Nifas', default='normal')

    laktasi = fields.Selection([
        ('ya', 'Ya'), 
        ('tidak', 'Tidak')
    ], string='Laktasi')

    jenis_kelamin = fields.Selection([
        ('l', 'L'), 
        ('p', 'P')
    ], string='L/P')
    bb_bayi       = fields.Integer(string='BB (Gram)', help="Berat Badan Bayi dalam Gram")
    pb_bayi       = fields.Float(string='PB (cm)', help="Panjang Badan Bayi dalam CM")
    kb_dipakai    = fields.Char(string='Kontrasepsi (KB)', help="Metode KB yang digunakan setelah persalinan ini")
    usia_anak     = fields.Char(string='Kondisi/Usia Anak Saat Ini', help="Contoh: 5 Tahun atau Meninggal")

