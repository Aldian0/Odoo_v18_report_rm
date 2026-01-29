# cdn_simrs_rekamedis_add/models/transfer_pasien_antar_unit.py

from odoo import _, api, fields, models

class TransferPasienAntarUnit(models.Model):
    _name = 'cdn.transfer.pasien.antar.unit'
    _description = 'Transfer Pasien Antar Unit Pelayanan (Perlu TTV, Keadaan Umum)'
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

    # === INFORMASI RUANGAN & WAKTU ===
    ruangan_asal = fields.Char(string='Ruangan Asal', tracking=True)
    ruangan_tujuan = fields.Char(string='Ruangan Tujuan', tracking=True)
    tanggal_transfer = fields.Datetime(string='Waktu Transfer', tracking=True)
    # jam_transfer = fields.Float(string='Jam Transfer', tracking=True)

    # === SECTION S: INFORMASI PASIEN ===
    # Note: nama_pasien, tanggal_lahir, no_rm sudah diwarisi dari cdn.erm.base
    dpjp = fields.Many2one('hr.employee', string='DPJP', help='Dokter Penanggung Jawab Pasien', tracking=True)

    # === SECTION B: RIWAYAT & PEMERIKSAAN ===
    keluhan = fields.Text(string='Keluhan', tracking=True)
    riwayat_penyakit_dahulu = fields.Text(string='Riwayat Penyakit Dahulu', tracking=True)
    
    # Riwayat Alergi
    # riwayat_alergi_ada = fields.Boolean(string='Ada')
    # riwayat_alergi_tidak_ada = fields.Boolean(string='Tidak Ada')
    # riwayat_alergi_tidak_diketahui = fields.Boolean(string='Tidak Diketahui')
    riwayat_alergi = fields.Selection([
        ('ada', 'Ada'),
        ('tidak_ada', 'Tidak Ada'),
        ('tidak_diketahui', 'Tidak Diketahui'),
    ], string='Riwayat Alergi', tracking=True)
    # riwayat_alergi_detail = fields.Text(string='Detail Alergi')
    
    pemeriksaan_fisik = fields.Text(string='Pemeriksaan Fisik',tracking=True)
    
    # Pemeriksaan Penunjang
    pemeriksaan_penunjang = fields.Selection([
        ('laboratorium', 'Laboratorium'),
        ('radiologi', 'Radiologi'),
        ('usg', 'USG'),
        ('ekg', 'EKG'),
        ('lainnya', 'Lainnya'),
    ], string='Pemeriksaan Penunjang', tracking=True)
    # pemeriksaan_penunjang_ekg = fields.Boolean(string='EKG')
    # pemeriksaan_penunjang_radiologi = fields.Boolean(string='Radiologi')
    # pemeriksaan_penunjang_usg = fields.Boolean(string='USG')
    # pemeriksaan_penunjang_lainnya = fields.Boolean(string='Lainnya')
    pemeriksaan_penunjang_detail = fields.Text(string='Detail Pemeriksaan Penunjang', tracking=True)
    
    diagnosa_masuk = fields.Text(string='Diagnosa Masuk', tracking=True)
    indikasi_mrs = fields.Text(string='Indikasi MRS (Masuk Rumah Sakit)', tracking=True)
    
    # Terapi dan Tindakan
    terapi_yang_diberikan = fields.Text(string='Terapi yang diberikan', tracking=True)
    tindakan_prosedur_yang_dilakukan = fields.Text(string='Tindakan/prosedur yang dilakukan', tracking=True)

    # === SECTION A: KEADAAN PASIEN SAAT DIPINDAH ===
    kesadaran = fields.Char(string='Kesadaran', tracking=True)
    
    # TTV (Tanda Tanda Vital)
    ttv_td = fields.Char(string='TD (Tensi Darah)', tracking=True)
    ttv_nadi = fields.Char(string='Nadi', tracking=True)
    ttv_rr = fields.Char(string='RR (Respiratory Rate)', tracking=True)
    ttv_t_ax = fields.Char(string='T.ax (Suhu Aksila)', tracking=True)
    ttv_ews = fields.Char(string='EWS (Early Warning Score)', tracking=True)
    
    saturasi_oksigen = fields.Char(string='Saturasi Oksigen (%)', tracking=True)
    
    # Bantuan Oksigen
    # bantuan_oksigen_tidak = fields.Boolean(string='Tidak')
    # bantuan_oksigen_ya = fields.Boolean(string='Ya')
    bantuan_oksigen = fields.Selection([
        ('tidak', 'Tidak'),
        ('ya', 'Ya'),
    ], string='Bantuan Oksigen', tracking=True)
    bantuan_oksigen_sebutkan = fields.Char(string='Sebutkan jenis bantuan oksigen', tracking=True)
    bantuan_oksigen_kecepatan = fields.Char(string='Kecepatan aliran O2 (lpm)', tracking=True)
    
    # Resiko Jatuh
    resiko_jatuh = fields.Selection([
        ('tidak', 'Tidak'),
        ('rendah', 'Resiko Rendah'),
        ('tinggi', 'Resiko Tinggi'),
    ], string='Resiko Jatuh', tracking=True)

    # === SECTION R: RENCANA PEMERIKSAAN / TINDAKAN ===
    rencana_pemeriksaan_tindakan = fields.Text(string='Rencana pemeriksaan / tindakan di ruangan', tracking=True)

    # # === TANDA TANGAN ===
    # dokter_yang_memindah = fields.Many2one('res.users', string='Dokter yang memindah', tracking=True)
    # perawat_yang_menyerahkan = fields.Many2one('res.users', string='Perawat yang menyerahkan', tracking=True)
    # perawat_penerima = fields.Many2one('res.users', string='Perawat penerima', tracking=True)

    # ========= TTD PERAWAT PENERIMA ==========
    qr_ttd_perawat_penerima_id           = fields.Many2one(comodel_name='cdn.signature', string='UID QR Code')
    qr_ttd_perawat_penerima_date         = fields.Date('Date', related='qr_ttd_perawat_penerima_id.tanggal_tdd')
    qr_ttd_perawat_penerima_code         = fields.Binary(string='QR Code', related='qr_ttd_perawat_penerima_id.qr_code')
    qr_ttd_perawat_penerima_partner_id   = fields.Many2one(comodel_name='res.partner',related='qr_ttd_perawat_penerima_id.partner_id', string='Partner')

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
            'default_tipe_dokumen'  : 'Transfer Pasien Antar Unit',
            'default_perihal'       : 'Tanda tangan transfer pasien antar unit',
        }

        return self.rm_base_id.open_wizard_generate_qr_sign(data)
    
    def action_print_report(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/{self._name}/{self.id}/print_report',
            'target': 'new',
        }
    def print_report(self):
        data_info = {
            'no_rm_doc'         : self.rm_id.no_rekam_medis or '',
            'no_rm'             : self.pasien_id.no_rm or '',
            'nama_pasien'       : self.pasien_id.name or '',
            'tgl_lahir_pasien'  : str(self.pasien_id.tanggal_lahir) if self.pasien_id.tanggal_lahir else '',
            'ruangan_asal'      : self.ruangan_asal or '',
            'ruangan_tujuan'    : self.ruangan_tujuan or '',
            'tanggal_transfer'  : fields.Datetime.context_timestamp(self, self.tanggal_transfer).strftime('%Y-%m-%d') if self.tanggal_transfer else '',
            'jam_transfer'      : fields.Datetime.context_timestamp(self, self.tanggal_transfer).strftime('%H:%M') if self.tanggal_transfer else '',
            'dpjp'              : self.dpjp.name or '',
            'keluhan'           : self.keluhan or '',
            'riwayat_penyakit'  : self.riwayat_penyakit_dahulu or '',
            'riwayat_alergi'    : dict(self._fields['riwayat_alergi'].selection).get(self.riwayat_alergi) or '',
            'pemeriksaan_fisik' : self.pemeriksaan_fisik or '',
            'pemeriksaan_penunjang' : dict(self._fields['pemeriksaan_penunjang'].selection).get(self.pemeriksaan_penunjang) or '',
            'diagnosa_masuk'    : self.diagnosa_masuk or '',
            'indikasi_mrs'      : self.indikasi_mrs or '',
            'terapi_yang_diberikan' : self.terapi_yang_diberikan or '',
            'tindakan_prosedur_yang_dilakukan' : self.tindakan_prosedur_yang_dilakukan or '',
            'kesadaran'         : self.kesadaran or '',
            'ttv_td'            : self.ttv_td or '',
            'ttv_nadi'          : self.ttv_nadi or '',
            'ttv_rr'            : self.ttv_rr or '',
            'ttv_t_ax'          : self.ttv_t_ax or '',
            'ttv_ews'           : self.ttv_ews or '',
            'saturasi_oksigen'  : self.saturasi_oksigen or '',
            'bantuan_oksigen'   : dict(self._fields['bantuan_oksigen'].selection).get(self.bantuan_oksigen) or '',
            'bantuan_oksigen_sebutkan' : self.bantuan_oksigen_sebutkan or '',
            'bantuan_oksigen_kecepatan' : self.bantuan_oksigen_kecepatan or '',
            'resiko_jatuh'      : dict(self._fields['resiko_jatuh'].selection).get(self.resiko_jatuh) or '',
            'rencana_pemeriksaan_tindakan' : self.rencana_pemeriksaan_tindakan or '',
            'nama_dokter'       : self.qr_ttd_dokter_partner_id.name or '.....................',
            'nama_perawat'      : self.qr_ttd_perawat_partner_id.name or '.....................',
            'nama_perawat_penerima' : self.qr_ttd_perawat_penerima_partner_id.name or '.....................',
        }
        image_info      = [
            {'key': '{{logo_company}}', 'value': self.company_id.logo or False, 'inches': 1},
            {'key': '{{ttd_dokter}}', 'value': self.qr_ttd_dokter_id.qr_code or False, 'inches': 1},
            {'key': '{{ttd_perawat}}', 'value': self.qr_ttd_perawat_id.qr_code or False, 'inches': 1},
            {'key': '{{ttd_perawat_penerima}}', 'value': self.qr_ttd_perawat_penerima_id.qr_code or False, 'inches': 1},
        ]
        template_file = 'cdn_simrs_rekamedis_add/template/transfer_pasien_antar_unit/transfer_pasien_antar_unit_pelayanan.docx'
        return self.rm_base_id._mail_merge_to_pdf(path=template_file, data_info=data_info, image_info=image_info)
