from odoo import api, fields, models, _


class SurgicalSafetyChecklist(models.Model):
    _name = 'cdn.surgical.safety.checklist'
    _description = 'Surgical Safety Checklist'
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

    # =========================================
    # IDENTITAS PASIEN
    # =========================================
    nama_pasien = fields.Char(
        string='Nama',
        help='Nama pasien'
    )
    tanggal_lahir = fields.Date(
        string='Tanggal Lahir',
        help='Tanggal lahir pasien'
    )
    no_rm = fields.Char(
        string='No. RM',
        help='Nomor rekam medis'
    )
    ruang = fields.Char(
        string='Ruang',
        help='Ruang/unit rawat pasien'
    )
    tanggal_masuk = fields.Date(
        string='Tgl MRS',
        help='Tanggal masuk rumah sakit'
    )

    # =========================================
    # SIGN IN - Sebelum Anestesi
    # =========================================
    sign_in_verifikasi_identitas = fields.Boolean(string='Verifikasi Identitas')
    sign_in_verifikasi_prosedur = fields.Boolean(string='Verifikasi Prosedur Operasi')
    sign_in_verifikasi_lokasi = fields.Boolean(string='Verifikasi Lokasi Operasi')
    sign_in_puasa = fields.Boolean(string='Status Puasa Dicek')
    sign_in_puasa_catatan = fields.Char(string='Catatan Puasa')
    sign_in_checklist_alat = fields.Text(string='Daftar Peralatan (Sign In)')
    sign_in_kelengkapan_dokumen = fields.Boolean(string='Dokumen Lengkap')
    sign_in_catatan = fields.Text(string='Catatan Sign In')

    sign_in_verifikasi_identitas_1 = fields.Selection([
        ('sudah', 'Sudah'),
        ('belum', 'Belum')
    ], string='Verifikasi Identitas')
    
    sign_in_tanda_operasi_1 = fields.Selection([
        ('sudah', 'Sudah'),
        ('tidak perlu', 'Tidak Perlu')
    ], string='Verifikasi Tanda Operasi')

    sign_in_alat_pulse_oksimetri = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Verifikasi Alat')

    sign_in_riwayat_penyakit = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Verifikasi Riwayat Penyakit')
    sign_in_sebutkan_riwayat_penyakit = fields.Char(string='Sebutkan Riwayat Penyakit')
    
    sign_in_jalan_nafas = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Verifikasi Kesulitan Bernafas')

    sign_in_kehilangan_darah = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Resiko Kehilangan Darah')

    # =========================================
    # TIME OUT - Sebelum Insisi
    # =========================================
    timeout_konfirmasi_tim = fields.Boolean(string='Konfirmasi Seluruh Tim')
    timeout_antibiotik_profilaksis = fields.Boolean(string='Antibiotik Profilaksis Diberikan')
    timeout_antibiotik_jam = fields.Datetime(string='Waktu Pemberian Antibiotik')
    timeout_resiko_komplikasi = fields.Text(string='Risiko Komplikasi Khusus')
    timeout_kesiapan_alat = fields.Boolean(string='Kesiapan Peralatan Utama')
    timeout_daftar_instrumen = fields.Text(string='Daftar Instrumen Operasi')
    timeout_lab_penting = fields.Boolean(string='Hasil Lab Penting Dicek')
    timeout_catatan = fields.Text(string='Catatan Time Out')

    timeout_konfirmasi_anggota_tim = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Konfirmasi Anggota Tim')

    timeout_konfirmasi_data_pasien = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Konfirmasi Data Pasien')

    timeout_pemberian_antibiotik = fields.Selection([
        ('sudah', 'Sudah'),
        ('belum diberikan', 'Belum Diberikan'),
        ('tidak perlu', 'Tidak Perlu')
    ], string='Pemberian Antibiotik Profilaksis')

    timeout_keadaan_krisis = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Keadaan Krisis Pasien')
    timeout_sebutkan_keadaan_krisis = fields.Char(string='Jelaskan Keadaan Krisis')
    
    timeout_kehilangan_darah = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Antisipasi Kehilangan Darah')
    timeout_sebutkan_kehilangan_darah = fields.Char(string='Jelaskan Kehilangan Darah')

    timeout_kondisi_khusus_pasien = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Kondisi Khusus Pasien')
    timeout_sebutkan_kondisi_khusus_pasien = fields.Char(string='Jelaskan Kondisi Khusus Pasien')

    timeout_peralatan_steril = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Verifikasi Peralatan Steril')
    timeout_sebutkan_peralatan_steril = fields.Char(string='Jelaskan Peralatan Steril')

    timeout_keadaan_alat = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Masalah Pada Peralatan')
    timeout_sebutkan_keadaan_alat = fields.Char(string='Jelaskan Masalah Peralatan')

    timeout_foto_pasien = fields.Selection([
        ('sudah', 'Sudah'),
        ('tidak perlu', 'Tidak Perlu')
    ], string='Menampilkan Foto Pasien')

    timeout_jml_kasa = fields.Char(string='Jumlah Kasa')
    

    # =========================================
    # SIGN OUT - Sebelum Keluar Ruang Operasi
    # =========================================
    signout_perhitungan_instrumen = fields.Boolean(string='Perhitungan Instrument Lengkap')
    signout_daftar_instrumen_kembali = fields.Text(string='Instrumen Kembali (Detail)')
    signout_spesimen_label = fields.Boolean(string='Label Spesimen Lengkap')
    signout_spesimen_ket = fields.Text(string='Keterangan Spesimen')
    signout_ada_masalah = fields.Boolean(string='Ada Masalah Teknis/Klinis?')
    signout_masalah_keterangan = fields.Text(string='Keterangan Masalah')
    signout_rencana_lanjutan = fields.Text(string='Rencana Pasca Operasi')
    signout_catatan = fields.Text(string='Catatan Sign Out')

    signout_nama_prosedur = fields.Char(string='Sebutkan Nama Prosedur')
    signout_perhitungan_instrumen_1 = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Perhitungan Instrument Lengkap')
    signout_jml_kasa = fields.Char(string='Jumlah Kasa Terpakai')

    signout_pemakaian_alat = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string='Pemakaian Alat Single use')

    signout_labeling_spesimen = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak'),
    ], string="Labeling Spesimen Sesuai", default='ya')

    signout_masalah_peralatan = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string="Masalah Peralatan", default='tidak')
    signout_sebutkan_masalah_peralatan = fields.Char(string="Jelaskan Masalah Peralatan")

    signout_anestesis_peralatan = fields.Selection([
        ('ya', 'Ya'),
        ('tidak', 'Tidak')
    ], string="Masalah Peralatan", default='tidak')
    signout_sebutkan_masalah_anestesi = fields.Char(string="Jelaskan Masalah Anestesi")

    signout_pakai_1 = fields.Boolean(string="1")
    signout_pakai_2 = fields.Boolean(string="2")
    signout_pakai_3 = fields.Boolean(string="3")
    signout_pakai_4 = fields.Boolean(string="4")
    

    # =========================================
    # PETUGAS & TANDA TANGAN
    # =========================================

    # ========= TTD DOKTER BEDAH ==========
    qr_ttd_dokter_bedah_id                        = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_dokter_bedah_date                      = fields.Date('Date', related='qr_ttd_dokter_bedah_id.tanggal_tdd')
    qr_ttd_dokter_bedah_code                      = fields.Binary(string='QR Code', related='qr_ttd_dokter_bedah_id.qr_code')
    qr_ttd_dokter_bedah_partner_id                = fields.Many2one(comodel_name='res.partner',related='qr_ttd_dokter_bedah_id.partner_id', string='Partner')
    
    # ========= TTD DOKTER ANESTESI ==========
    qr_ttd_dokter_anestesi_id                     = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_dokter_anestesi_date                   = fields.Date('Date', related='qr_ttd_dokter_anestesi_id.tanggal_tdd')
    qr_ttd_dokter_anestesi_code                   = fields.Binary(string='QR Code', related='qr_ttd_dokter_anestesi_id.qr_code')
    qr_ttd_dokter_anestesi_partner_id             = fields.Many2one(comodel_name='res.partner',related='qr_ttd_dokter_anestesi_id.partner_id', string='Partner')

    # ========= TTD PERAWAT SIRKULASI SIGN IN ==========
    qr_ttd_perawat_sirkulasi_sign_in_id               = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_sirkulasi_sign_in_date         = fields.Date('Date', related='qr_ttd_perawat_sirkulasi_sign_in_id.tanggal_tdd')
    qr_ttd_perawat_sirkulasi_sign_in_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_sirkulasi_sign_in_id.qr_code')
    qr_ttd_perawat_sirkulasi_sign_in_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_sirkulasi_sign_in_id.partner_id', string='Partner')

    # ========= TTD PERAWAT SIRKULASI TIME OUT ==========
    qr_ttd_perawat_sirkulasi_time_out_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_sirkulasi_time_out_date         = fields.Date('Date', related='qr_ttd_perawat_sirkulasi_time_out_id.tanggal_tdd')
    qr_ttd_perawat_sirkulasi_time_out_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_sirkulasi_time_out_id.qr_code')
    qr_ttd_perawat_sirkulasi_time_out_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_sirkulasi_time_out_id.partner_id', string='Partner')

    # ========= TTD PERAWAT SIRKULASI SIGN OUT ==========
    qr_ttd_perawat_sirkulasi_sign_out_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_sirkulasi_sign_out_date         = fields.Date('Date', related='qr_ttd_perawat_sirkulasi_sign_out_id.tanggal_tdd')
    qr_ttd_perawat_sirkulasi_sign_out_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_sirkulasi_sign_out_id.qr_code')
    qr_ttd_perawat_sirkulasi_sign_out_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_sirkulasi_sign_out_id.partner_id', string='Partner')

    # =========================================
    # LOG WAKTU
    # =========================================
    sign_in_time = fields.Datetime(string='Waktu Sign In')
    time_out_time = fields.Datetime(string='Waktu Time Out')
    sign_out_time = fields.Datetime(string='Waktu Sign Out')

    # =========================================
    # STATUS & TRACKING
    # =========================================
    status_checklist = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'Dalam Proses'),
        ('done', 'Selesai'),
    ], default='draft', string='Status', tracking=True, compute='_compute_check_complete', store=True)
    

    @api.depends('sign_in_verifikasi_identitas', 'timeout_konfirmasi_tim', 'signout_perhitungan_instrumen')
    def _compute_check_complete(self):
        """Logika untuk status otomatis berdasarkan checklist"""
        for rec in self:
            if rec.sign_in_verifikasi_identitas and rec.timeout_konfirmasi_tim and rec.signout_perhitungan_instrumen:
                rec.status_checklist = 'done'
            else:
                rec.status_checklist = 'in_progress'


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

    def signature_generate(self):
        login = False
        if self.env.user.login:
            login = self.env.user.login

        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        data = {
            'default_username'      : login,
            'default_field_name'    : self.env.context.get('field_name'),
            'default_model_id'      : model_id.id,
            'default_data_id'       : self.id,
            'default_tipe'          : self.env.context.get('tipe_nakes'),
            'default_tipe_dokumen'  : 'Surgical Safety Checklist',
            'default_perihal'       : 'Tanda tangan surgical safety checklist',
        }

        return self.rm_base_id.open_wizard_generate_qr_sign(data)
    


    def print_report(self):
        data_info = {   
            'nama'           : self.pasien_id.name or '',
            'tgl_lahir'      : self.pasien_id.tanggal_lahir.strftime('%d/%m/%Y') if self.pasien_id.tanggal_lahir else '',
            'no_rm'          : self.pasien_id.no_rm or '',
            'konfirmasi_nama' : self._get_selection_checkbox(field_name='sign_in_verifikasi_identitas_1'),
            'tanda_operasi' : self._get_selection_checkbox(field_name='sign_in_tanda_operasi_1'),
            'fungsi_alat' : self._get_selection_checkbox(field_name='sign_in_alat_pulse_oksimetri'),
            'riwayat_pasien' : self._get_selection_checkbox(field_name='sign_in_riwayat_penyakit'),
            'sbt_rp' : self.sign_in_sebutkan_riwayat_penyakit or '........................................',
            'resiko_aspirasi' : self._get_selection_checkbox(field_name='sign_in_jalan_nafas'),
            'resiko_kehilangan_darah' : self._get_selection_checkbox(field_name='sign_in_kehilangan_darah'),
            'pemberian_antibiotik' : self._get_selection_checkbox(field_name='timeout_pemberian_antibiotik'),
            'keadaan_krisis' : self._get_selection_checkbox(field_name='timeout_keadaan_krisis'),
            'sbt_ks' : self.timeout_sebutkan_keadaan_krisis or '........................................',
            'antisipasi_kehilangan_darah' : self._get_selection_checkbox(field_name='timeout_kehilangan_darah'),
            'sbt_kd' : self.timeout_sebutkan_kehilangan_darah or '........................................',
            'kondisi_khusus_pasien' : self._get_selection_checkbox(field_name='timeout_kondisi_khusus_pasien'),
            'sbt_kp' : self.timeout_sebutkan_kondisi_khusus_pasien or '........................................',
            'peralatan_steril' : self._get_selection_checkbox(field_name='timeout_peralatan_steril'),
            'sbt_ps' : self.timeout_sebutkan_peralatan_steril or '........................................',
            'masalah_peralatan' : self._get_selection_checkbox(field_name='timeout_keadaan_alat'),
            'sbt_mp' : self.timeout_sebutkan_keadaan_alat or '........................................',
            'menampilkan_foto_pasien' : self._get_selection_checkbox(field_name='timeout_foto_pasien'),
            'jml_kasa' : self.timeout_jml_kasa or '',
            'nama_prosedur' : self.signout_nama_prosedur or '........................................',
            'kelengkapan_alat' : self._get_selection_checkbox(field_name='signout_perhitungan_instrumen_1'),
            'jml_kasa_terpakai' : self.signout_jml_kasa or '........................................',
            'single_use_re_use' : self._get_selection_checkbox(field_name='signout_pemakaian_alat'),
            'labeling_spesimen' : self._get_selection_checkbox(field_name='signout_labeling_spesimen'),
            'tindak_masalah_alat' : self._get_selection_checkbox(field_name='signout_masalah_peralatan'),
            'sbt_ma' : self.signout_sebutkan_masalah_peralatan or '........................................',
            'hal_penting_untuk_pulih' : self._get_selection_checkbox(field_name='signout_anestesis_peralatan'),
            'sbt_up' : self.signout_sebutkan_masalah_anestesi or '........................................',
            'ttd_perawat_sirkulasi_1' : self.qr_ttd_perawat_sirkulasi_sign_in_partner_id.name or '........................................',
            'ttd_perawat_sirkulasi_2' : self.qr_ttd_perawat_sirkulasi_time_out_partner_id.name or '........................................',
            'ttd_perawat_sirkulasi_3' : self.qr_ttd_perawat_sirkulasi_sign_out_partner_id.name or '........................................',
            'ttd_dokter_anestesi' : self.qr_ttd_dokter_anestesi_partner_id.name or '........................................',
            'ttd_dokter_bedah' : self.qr_ttd_dokter_bedah_partner_id.name or '........................................',
        }   
        

        image_info = [
                    {'key': '{{ttd_perawat_sirkulasi_1}}', 'value': self.qr_ttd_perawat_sirkulasi_sign_in_id.qr_code or False, 'inches': 1},
                    {'key': '{{ttd_perawat_sirkulasi_2}}', 'value': self.qr_ttd_perawat_sirkulasi_time_out_id.qr_code or False, 'inches': 1},
                    {'key': '{{ttd_perawat_sirkulasi_3}}', 'value': self.qr_ttd_perawat_sirkulasi_sign_out_id.qr_code or False, 'inches': 1},
                    {'key': '{{ttd_dokter_bedah}}', 'value': self.qr_ttd_dokter_bedah_id.qr_code or False, 'inches': 1},
                    {'key': '{{ttd_dokter_anestesi}}', 'value': self.qr_ttd_dokter_anestesi_id.qr_code or False, 'inches': 1},
                    # {'key': '{{ttd_perawat}}', 'value': self.qr_ttd_perawat_id.qr_code or False, 'inches': 1},
                    # {'key': '{{ttd_perawat_penerima}}', 'value': self.qr_ttd_perawat_penerima_id.qr_code or False, 'inches': 1},
                ]

        template_file = 'cdn_simrs_rekamedis_add/template/surgical_safety.docx' 
        return self.rm_base_id._mail_merge_to_pdf(
            path=template_file, 
            data_info=data_info, 
            image_info=image_info)

