from odoo import _, api, fields, models


class LaporanOperasiKatarak(models.Model):
    _name = 'cdn.laporan.operasi.katarak'
    _description = 'Laporan Operasi Katarak'
    _inherits = {'cdn.erm.base': 'rm_base_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin', 'cdn.erm.mixin', 'cdn.report.mailmerge']

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade',
    )

    # Header informasi umum
    dpjp = fields.Many2one('res.users', string='DPJP')
    asisten = fields.Char(string='Asisten')
    sirkuler = fields.Char(string='Sirkuler')
    op_room = fields.Char(string='Op. Room')

    tgl_operasi = fields.Date(string='Tanggal Operasi')
    operasi_mulai_jam = fields.Datetime(string='Operasi mulai jam')
    operasi_selesai_jam = fields.Datetime(string='Operasi selesai jam')
    lama_operasi = fields.Char(string='Lama operasi')

    anestesi_mulai_jam = fields.Datetime(string='Anestesi mulai jam')
    anestesi_selesai_jam = fields.Datetime(string='Anestesi selesai jam')
    lama_anestesi = fields.Char(string='Lama anestesi')

    # Mata yang dioperasi
    mata_operasi = fields.Selection(
        [('od', 'OD (Mata Kanan)'), ('os', 'OS (Mata Kiri)')],
        string='Mata Operasi',
    )
    terapi_catatan = fields.Text(string='Terapi / Catatan')
    operasi_ke = fields.Char(string='Operasi Ke')
    diagnosa_pra_bedah = fields.Char(string='Diagnosa Pra Bedah')
    diagnosa_pasca_bedah = fields.Char(string='Diagnosa Pasca Bedah')

    # Data biometri singkat
    retinometri = fields.Char(string='Retinometri')
    visus_bcva = fields.Char(string='Visus BCVA')
    k1 = fields.Char(string='K1')
    k2 = fields.Char(string='K2')
    axl = fields.Char(string='AXL')
    acd = fields.Char(string='ACD')
    iol_power = fields.Char(string='IOL power (Target Emmetropia)')
    formula_iol = fields.Char(string='Formula IOL')

    # Jenis operasi
    jenis_operasi = fields.Selection([
        ('phaco', 'Fakoemulsifikasi'),
        ('sics', 'SICS'),
        ('ecce', 'ECCE'),
        ('icce', 'ICCE'),
        ('lainnya', 'Lainnya'),
    ], string='Jenis Operasi')
    jenis_operasi_lainnya = fields.Char(string='Jenis Operasi Lainnya')

    # Disinfeksi & persiapan lapangan operasi
    disinfeksi_betadine = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Disinfeksi lapangan operasi dengan betadine',
    )
    pasang_eye_drape_steril = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Pasang eye drape steril',
    )
    pasang_blepharospat = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Pasang blepharospat',
    )

    # Anestesi
    jenis_anestesi = fields.Selection([
        ('topikal', 'Topikal'),
        ('subkon_tenon', 'Sub-kon/tenon'),
        ('blok', 'Blok'),
        ('umum', 'Umum'),
    ], string='Anestesi')

    # Approach
    approach = fields.Selection([
        ('temporal', 'Temporal'),
        ('superior', 'Superior'),
        ('skleral_tunnel', 'Skleral tunnel'),
        ('limbal', 'Limbal'),
        ('kornea', 'Kornea'),
    ], string='Approach')

    # Insisi
    jenis_insisi = fields.Selection([
        ('sklera', 'Sklera'),
        ('limbal', 'Limbal'),
        ('kornea', 'Kornea'),
    ], string='Insisi')

    # Kapsulotomi CCC
    kapsulotomi_ccc = fields.Selection([
        ('komplit', 'Komplit'),
        ('tidak_komplit', 'Tidak Komplit'),
        ('can_opener', 'Can Opener'),
    ], string='Kapsulotomi (CCC)')

    hidrodiseksi = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Hidrodisection',
    )

    manajemen_nukleus = fields.Selection([
        ('vectis', 'Vectis'),
        ('ekspresi', 'Ekspresi'),
        ('fako', 'Fako'),
    ], string='Manajemen Nukleus')

    teknik_fako = fields.Selection([
        ('stop_chop', 'Stop & Chop'),
        ('horizontal_chop', 'Horizontal Chop'),
        ('vertical_chop', 'Vertical Chop'),
        ('dnc', 'D&C'),
    ], string='Teknik Fako')

    ia_kortex = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='I/A Kortex',
    )

    iol_implan = fields.Selection([
        ('bag', 'Bag'),
        ('sulkus', 'Sulkus'),
        ('afakia', 'Afakia'),
    ], string='IOL Implan')

    iol_tipe = fields.Selection([
        ('iris_claw', 'Iris Claw Anterior/Posterior'),
        ('fiksasi_sklera', 'Fiksasi Sklera'),
    ], string='Tipe IOL')

    jahitan = fields.Selection([
        ('tidak', 'Tidak'),
        ('ya', 'Ya (1–2–3–4–5–6)'),
        ('final_incision', 'Final Incision'),
    ], string='Jahitan')

    vitrektomi_anterior = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Vitrektomi Anterior',
    )
    kapsulotomi_posterior = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Kapsulotomi Posterior',
    )
    miotikum = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Miotikum',
    )

    injeksi_antibiotika = fields.Selection([
        ('intra_kameral', 'Intra kameral'),
        ('sub_konjungtiva', 'Sub Konjungtiva'),
        ('peribulbar', 'Peribulbar'),
    ], string='Injeksi Antibiotika')

    tetes_mata = fields.Selection([
        ('salep_antibiotik', 'Salep Antibiotik'),
        ('ya', 'Tetes mata - Ya'),
        ('tidak', 'Tetes mata - Tidak'),
    ], string='Tetes mata')

    bebat_mata = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Bebat mata',
    )

    mesin_fako = fields.Char(string='Mesin Fako')
    cairan_irigasi = fields.Char(string='Cairan Irigasi')
    phaco_time = fields.Char(string='Phaco Time')
    ept_cde = fields.Char(string='EPT / CDE')

    # Komplikasi
    komplikasi = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Komplikasi',
    )
    komplikasi_rk_posterior = fields.Boolean(string='Ruptur Kapsul Posterior')
    komplikasi_vitreous_prolaps = fields.Boolean(string='Vitreous Prolaps')
    komplikasi_sisa_material_lensa = fields.Boolean(string='Sisa Material Lensa')
    komplikasi_sisa_kortex = fields.Boolean(string='Sisa Kortex')
    terapi_catatan = fields.Text(string='Terapi / Catatan')
    dpjp_tanda_tangan = fields.Many2one('res.users', string='DPJP (Tanda tangan dan nama terang)')

    # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.laporan.operasi.katarak/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {
            'dpjp'                  : self.dpjp.name or '',
            'asisten'               : self.asisten or '',
            'sirkuler'              : self.sirkuler or '',
            'op_room'               : self.op_room or '',
            'tgl_operasi'           : self.tgl_operasi.strftime('%d/%m/%Y') if self.tgl_operasi else '',
            'operasi_mulai_jam'     : self.operasi_mulai_jam.strftime('%H:%M') if self.operasi_mulai_jam else '',
            'operasi_selesai_jam'   : self.operasi_selesai_jam.strftime('%H:%M') if self.operasi_selesai_jam else '',
            'lama_operasi'          : self.lama_operasi or '',
            'anestesi_mulai_jam'    : self.anestesi_mulai_jam.strftime('%H:%M') if self.anestesi_mulai_jam else '',
            'anestesi_selesai_jam'  : self.anestesi_selesai_jam.strftime('%H:%M') if self.anestesi_selesai_jam else '',
            'lama_anestesi'         : self.lama_anestesi or '',
            'mata_operasi'          : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='mata_operasi', value=self.mata_operasi),
            'operasi_ke'            : self.operasi_ke or '',
            'diagnosa_pra_bedah'    : self.diagnosa_pra_bedah or '',
            'diagnosa_pasca_bedah'  : self.diagnosa_pasca_bedah or '',
            'retinometri'           : self.retinometri or '',
            'visus_bcva'            : self.visus_bcva or '',
            'k1'                    : self.k1 or '',
            'k2'                    : self.k2 or '',
            'axl'                   : self.axl or '',
            'acd'                   : self.acd or '',
            'iol_power'             : self.iol_power or '',
            'formula_iol'           : self.formula_iol or '',
            'jenis_operasi'         : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='jenis_operasi', value=self.jenis_operasi),
            'jenis_operasi_lainnya' : self.jenis_operasi_lainnya or '',
            'disinfeksi_betadine'   : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='disinfeksi_betadine', value=self.disinfeksi_betadine),
            'pasang_eye_drape_steril' : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='pasang_eye_drape_steril', value=self.pasang_eye_drape_steril),
            'pasang_blepharospat'   : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='pasang_blepharospat', value=self.pasang_blepharospat),
            'jenis_anestesi'        : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='jenis_anestesi', value=self.jenis_anestesi),
            'approach'              : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='approach', value=self.approach),
            'jenis_insisi'          : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='jenis_insisi', value=self.jenis_insisi),
            'kapsulotomi_ccc'       : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='kapsulotomi_ccc', value=self.kapsulotomi_ccc),
            'hidrodiseksi'          : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='hidrodiseksi', value=self.hidrodiseksi),
            'manajemen_nukleus'     : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='manajemen_nukleus', value=self.manajemen_nukleus),
            'teknik_fako'           : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='teknik_fako', value=self.teknik_fako),
            'ia_kortex'             : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='ia_kortex', value=self.ia_kortex),
            'iol_implan'            : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='iol_implan', value=self.iol_implan),
            'iol_tipe'              : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='iol_tipe', value=self.iol_tipe),
            'jahitan'               : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='jahitan', value=self.jahitan),
            'vitrektomi_anterior'   : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='vitrektomi_anterior', value=self.vitrektomi_anterior),
            'kapsulotomi_posterior' : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='kapsulotomi_posterior', value=self.kapsulotomi_posterior),
            'miotikum'              : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='miotikum', value=self.miotikum),
            'injeksi_antibiotika'   : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='injeksi_antibiotika', value=self.injeksi_antibiotika),
            'tetes_mata'            : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='tetes_mata', value=self.tetes_mata),
            'bebat_mata'            : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='bebat_mata', value=self.bebat_mata),
            'mesin_fako'            : self.mesin_fako or '',
            'cairan_irigasi'        : self.cairan_irigasi or '',
            'phaco_time'            : self.phaco_time or '',
            'ept_cde'               : self.ept_cde or '',
            'komplikasi'            : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='komplikasi', value=self.komplikasi),
            'komplikasi_rk_posterior' : 'Ya' if self.komplikasi_rk_posterior else 'Tidak',
            'komplikasi_vitreous_prolaps' : 'Ya' if self.komplikasi_vitreous_prolaps else 'Tidak',
            'komplikasi_sisa_material_lensa' : 'Ya' if self.komplikasi_sisa_material_lensa else 'Tidak',
            'komplikasi_sisa_kortex' : 'Ya' if self.komplikasi_sisa_kortex else 'Tidak',
            'terapi_catatan'        : self.terapi_catatan or '',
        }
        template = 'cdn_simrs_rekamedis_add/template/Laporan_Operasi_Katarak.docx'
        return self._mail_merge_to_pdf(
            path        = template,
            data_info   = data_field,
            image_info  = [ 
                {'key'       : '{{gambar}}','value'     : self.qr_ttd_bidan_code,'inches'    : 1,},
            ],
            list_info   = []
        )



