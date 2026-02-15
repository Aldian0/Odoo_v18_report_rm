# cdn_simrs_rekamedis_add/models/lembar_laporan_operasi_tindakan_medis.py

from odoo import _, api, fields, models


class LembarLaporanOperasiTindakanMedis(models.Model):
    _name = 'cdn.lembar.laporan.operasi.tindakan.medis'
    _description = 'Lembar Laporan Operasi/Tindakan Medis'
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
    # DIAGNOSA & TINDAKAN
    # =========================================
    diagnosa_pra_tindakan = fields.Text(
        string='Diagnosa Pra Tindakan',
        help='Diagnosa sebelum tindakan',
        tracking=True
    )
    diagnosa_pasca_tindakan = fields.Text(
        string='Diagnosa Pasca Tindakan',
        help='Diagnosa setelah tindakan',
        tracking=True
    )

    tindakan_operasi = fields.Text(
        string='Tindakan Operasi',
        help='Tindakan operasi yang dilakukan',
        tracking=True
    )
    

    # =========================================
    # 🗓 INFORMASI WAKTU OPERASI
    # =========================================
    tanggal_operasi = fields.Date(
        string='Tanggal Operasi',
        help='Tanggal pelaksanaan operasi',
        tracking=True
    )
    waktu_sign_in = fields.Datetime(
        string='Waktu Sign In',
        help='Waktu sign in operasi',
        tracking=True
    )
    waktu_time_out = fields.Datetime(
        string='Waktu Time Out',
        help='Waktu time out operasi',
        tracking=True
    )
    waktu_sign_out = fields.Datetime(
        string='Waktu Sign Out',
        help='Waktu sign out operasi',
        tracking=True
    )
    waktu_selesai_operasi = fields.Datetime(
        string='Waktu Selesai Operasi',
        help='Waktu selesai operasi',
        tracking=True
    )

    # =========================================
    # 👨‍⚕️ TENAGA MEDIS
    # =========================================
    operator = fields.Many2one(
        'hr.employee',
        string='Operator',
        help='Nama operator/dokter bedah',
        tracking=True
    )
    asisten = fields.Many2one(
        'hr.employee',
        string='Asisten',
        help='Nama asisten operasi',
        tracking=True
    )
    perawat_instrumen = fields.Many2one(
        'hr.employee',
        string='Perawat Instrumen',
        help='Nama perawat instrumen',
        tracking=True
    )
    sirkulator = fields.Many2one(
        'hr.employee',
        string='Sirkulator',
        help='Nama sirkulator',
        tracking=True
    )

    # =========================================
    # 💉 ANESTESI DAN PROSEDUR TERKAIT
    # =========================================
    jenis_anestesi = fields.Selection([
        ('umum', 'Umum'),
        ('regional', 'Regional'),
        ('lokal', 'Lokal'),
        ('sedasi', 'Sedasi'),
        ('lainnya', 'Lainnya'),
    ], string='Jenis Anestesi', tracking=True)
    jenis_anestesi_lainnya = fields.Char(
        string='Jenis Anestesi Lainnya',
        help='Jenis anestesi lainnya',
        tracking=True
    )
    premedikasi = fields.Text(
        string='Premedikasi',
        help='Premedikasi yang diberikan',
        tracking=True
    )
    jenis_tindakan_anestesi = fields.Char(
        string='Jenis Tindakan Anestesi',
        help='Jenis tindakan anestesi',
        tracking=True
    )
    bahan_anestesi = fields.Text(
        string='Bahan Anestesi',
        help='Bahan anestesi yang digunakan',
        tracking=True
    )
    induksi = fields.Text(
        string='Induksi',
        help='Proses induksi anestesi',
        tracking=True
    )
    extubasi = fields.Text(
        string='extubasi',
        help='Proses extubasi',
        tracking=True
    )
    anestesi_penata = fields.Many2one(
        'hr.employee',
        string='Anestesi Penata',
        help='Nama dokter anestesi penata',
        tracking=True
    )

    # =========================================
    # 🏥 KLASIFIKASI OPERASI
    # =========================================
    golongan_operasi = fields.Selection([
        ('kecil', 'Kecil'),
        ('sedang', 'Sedang'),
        ('besar', 'Besar'),
        ('canggih', 'Canggih'),
        ('khusus', 'Khusus'),
    ], string='Golongan Operasi', tracking=True)
    macam_tindakan = fields.Selection([
        ('bersih', 'Bersih'),
        ('bersih_kontaminasi', 'Bersih Kontaminasi'),
        ('kontaminasi', 'Kontaminasi'),
        ('kotor_infeksi', 'Kotor Infeksi'),
    ], string='Macam Tindakan', tracking=True)
    urgensi_tindakan = fields.Selection([
        ('darurat', 'Darurat'),
        ('urgent', 'Urgent'),
        ('elektif', 'Elektif'),
        ('lainnya', 'Lainnya'),
    ], string='Urgensi Tindakan', tracking=True)
    urgensi_tindakan_lainnya = fields.Char(
        string='Urgensi Tindakan Lainnya',
        help='Urgensi tindakan lainnya',
        tracking=True
    )
    kamar_operasi = fields.Char(
        string='Kamar Operasi',
        help='Nomor/lokasi kamar operasi',
        tracking=True
    )
    ronde = fields.Char(
        string='Ronde',
        help='Ronde operasi',
        tracking=True
    )
    instrumenator = fields.Char(
        string='Instrumenator',
        help='Nama instrumenator',
        tracking=True
    )

    # =========================================
    # 📝 CATATAN OPERATOR
    # =========================================
    catatan_operator_tindakan_medis = fields.Text(
        string='Catatan Operator Tindakan Medis',
        help='Catatan dari operator mengenai tindakan medis',
        tracking=True
    )

    # =========================================
    # 📋 TAHAPAN TINDAKAN OPERASI
    # =========================================
    persiapan_tindakan_medis = fields.Text(
        string='Persiapan Tindakan Medis',
        help='Persiapan sebelum tindakan medis',
        tracking=True
    )
    posisi_pasien = fields.Char(
        string='Posisi Pasien',
        help='Posisi pasien selama operasi',
        tracking=True
    )
    desinfeksi = fields.Text(
        string='Desinfeksi',
        help='Proses desinfeksi',
        tracking=True
    )
    insisi_kulit_pembukaan_lapangan_operasi = fields.Text(
        string='Insisi Kulit/Pembukaan Lapangan Operasi',
        help='Deskripsi insisi kulit dan pembukaan lapangan operasi',
        tracking=True
    )
    pendapatan_pada_eksplorasi = fields.Text(
        string='Pendapatan pada Eksplorasi',
        help='Temuan selama eksplorasi',
        tracking=True
    )
    deskripsi_uraian_tindakan_medis = fields.Text(
        string='Deskripsi/Uraian Tindakan Medis',
        help='Deskripsi detail tindakan medis yang dilakukan',
        tracking=True
    )
    nama_operasi = fields.Char(
        string='Nama Operasi',
        help='Nama operasi yang dilakukan',
        tracking=True
    )
    komplikasi = fields.Text(
        string='Komplikasi',
        help='Komplikasi yang terjadi selama operasi',
        tracking=True
    )
    penutupan_lapangan_operasi = fields.Text(
        string='Penutupan Lapangan Operasi',
        help='Proses penutupan lapangan operasi',
        tracking=True
    )
    hasil_operasi = fields.Text(
        string='Hasil Operasi',
        help='Hasil akhir operasi',
        tracking=True
    )
    pengiriman_jaringan_tindakan_medis = fields.Text(
        string='Pengiriman Jaringan Tindakan Medis',
        help='Pengiriman jaringan untuk pemeriksaan',
        tracking=True
    )
    catatan_post_tindakan_medis = fields.Text(
        string='Catatan Post Tindakan Medis',
        help='Catatan setelah tindakan medis',
        tracking=True
    )
    perdarahan_post_operasi = fields.Text(
        string='Perdarahan Post Operasi',
        help='Catatan perdarahan setelah operasi',
        tracking=True
    )

    # =========================================
    # 📆 TANDA TANGAN & LOKASI
    # =========================================
    # tempat_pelaksanaan = fields.Char(
    #     string='Tempat Pelaksanaan',
    #     help='Tempat pelaksanaan operasi',
    #     tracking=True
    # )
    # tanggal_pelaksanaan = fields.Date(
    #     string='Tanggal Pelaksanaan',
    #     help='Tanggal pelaksanaan operasi',
    #     tracking=True
    # )
    # nama_dokter_penanggung_jawab = fields.Char(
    #     string='Nama Dokter Penanggung Jawab',
    #     help='Nama dokter yang bertanggung jawab'
    # )

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
            'default_tipe_dokumen'  : 'RM Operasi Tindakan Medis',
            'default_perihal'       : 'Tanda tangan asesmen operasi tindakan medis',
        }

        return self.rm_base_id.open_wizard_generate_qr_sign(data)
    
    def action_print_report(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/{self._name}/{self.id}/print_report',
            'target': 'new',
        }
    def print_report(self):
        data_info ={
            'no_rm_doc'         : self.rm_id.no_rekam_medis or '',
            'no_rm'             : self.pasien_id.no_rm or '',
            'nama_pasien'       : self.pasien_id.name or '',
            'tgl_lahir_pasien'  : str(self.pasien_id.tanggal_lahir) if self.pasien_id.tanggal_lahir else '',

            'diagnosa_pra_tindakan' : self.diagnosa_pra_tindakan or '',
            'diagnosa_pasca_tindakan' : self.diagnosa_pasca_tindakan or '',
            'tindakan_operasi'  : self.tindakan_operasi or '',

            'tanggal_operasi'   : str(self.tanggal_operasi) if self.tanggal_operasi else '',
            'waktu_sign_in'     : str(self.waktu_sign_in) if self.waktu_sign_in else '',
            'waktu_time_out'    : str(self.waktu_time_out) if self.waktu_time_out else '',
            'waktu_selesai_operasi' : str(self.waktu_selesai_operasi) if self.waktu_selesai_operasi else '',
            'waktu_sign_out'    : str(self.waktu_sign_out) if self.waktu_sign_out else '',

            'operator'          : self.operator.name or '',
            'asisten'           : self.asisten.name or '',
            'perawat_instrumen' : self.perawat_instrumen.name or '',
            'sirkulator'        : self.sirkulator.name or '',

            'jenis_anestesi'    : dict(self._fields['jenis_anestesi'].selection).get(self.jenis_anestesi) or '',
            'premedikasi'       : self.premedikasi or '',
            'jenis_tindakan_anestesi' : self.jenis_tindakan_anestesi or '',
            'bahan_anestesi'    : self.bahan_anestesi or '',
            'induksi'           : self.induksi or '',
            'extubasi'          : self.extubasi or '',
            'anestesi_penata'   : self.anestesi_penata.name or '',

            'golongan_operasi'  : dict(self._fields['golongan_operasi'].selection).get(self.golongan_operasi) or '',
            'macam_tindakan'    : dict(self._fields['macam_tindakan'].selection).get(self.macam_tindakan) or '',
            'urgensi_tindakan'  : dict(self._fields['urgensi_tindakan'].selection).get(self.urgensi_tindakan) or '',
            'kamar_operasi'     : self.kamar_operasi or '',
            'ronde'             : self.ronde or '',
            'instrumenator'     : self.instrumenator or '',

            'catatan_operator_tindakan_medis' : self.catatan_operator_tindakan_medis or '',

            'persiapan_tindakan_medis' : self.persiapan_tindakan_medis or '',
            'posisi_pasien'     : self.posisi_pasien or '',
            'desinfeksi'        : self.desinfeksi or '',
            'insisi_kulit_pembukaan_lapangan_operasi' : self.insisi_kulit_pembukaan_lapangan_operasi or '',
            'pendapatan_pada_eksplorasi' : self.pendapatan_pada_eksplorasi or '',
            'deskripsi_uraian_tindakan_medis' : self.deskripsi_uraian_tindakan_medis or '',
            'nama_operasi'      : self.nama_operasi or '',
            'komplikasi'        : self.komplikasi or '',
            'penutupan_lapangan_operasi' : self.penutupan_lapangan_operasi or '',
            'hasil_operasi'     : self.hasil_operasi or '',
            'pengiriman_jaringan_tindakan_medis' : self.pengiriman_jaringan_tindakan_medis or '',
            'catatan_post_tindakan_medis' : self.catatan_post_tindakan_medis or '',
            'perdarahan_post_operasi' : self.perdarahan_post_operasi or '',

            'tempat_pelaksanaan' : self.env.company.city or '',
            'tanggal_pelaksanaan' : self.rm_base_id._tanggal_indonesia(self.write_date) if self.write_date else '',
            'nama_dokter_penanggung_jawab' : self.qr_ttd_dokter_partner_id.name or '.....................',
        }

        image_info      = [
            {'key': '{{logo_company}}', 'value': self.company_id.logo or False, 'inches': 1},
            {'key': '{{ttd_dokter}}', 'value': self.qr_ttd_dokter_id.qr_code or False, 'inches': 1},
        ]
        template_file = 'cdn_simrs_rekamedis_add/template/lembar_laporan_operasi/lembar_laporan_operasi_template.docx'
        return self.rm_base_id._mail_merge_to_pdf(path=template_file, data_info=data_info, image_info=image_info)