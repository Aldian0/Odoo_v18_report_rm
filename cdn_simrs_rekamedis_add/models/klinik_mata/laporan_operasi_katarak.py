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
    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )

    # Header informasi umum
    dpjp_id     =  fields.Many2one('hr.employee', string='DPJP', domain=[('hr_simcendana_type','=','dokter')], tracking=True)
    asisten_id  = fields.Many2one('hr.employee', string='Asisten', domain=[('hr_simcendana_type','in',['dokter', 'perawat', 'nakes_lain', 'bidan'])], tracking=True)
    asisten     = fields.Char(string='Asisten', tracking=True)
    sirkuler    = fields.Char(string='Sirkuler', tracking=True)
    op_room     = fields.Char(string='Op. Room', tracking=True)

    tgl_operasi = fields.Date(string='Tanggal Operasi', tracking=True)
    operasi_mulai_jam = fields.Datetime(string='Operasi mulai jam', tracking=True)
    operasi_selesai_jam = fields.Datetime(string='Operasi selesai jam', tracking=True)
    lama_operasi = fields.Char(string='Lama operasi', tracking=True)

    anestesi_mulai_jam = fields.Datetime(string='Anestesi mulai jam', tracking=True)
    anestesi_selesai_jam = fields.Datetime(string='Anestesi selesai jam', tracking=True)
    lama_anestesi = fields.Char(string='Lama anestesi', tracking=True)

    # Mata yang dioperasi
    mata_operasi = fields.Selection(
        [('od', 'OD (Mata Kanan)'), ('os', 'OS (Mata Kiri)')],
        string='Mata Operasi', tracking=True
    )
    terapi_catatan = fields.Text(string='Terapi / Catatan', tracking=True)
    catatan_image = fields.Binary('Lampiran Catatan', tracking=True)
    operasi_ke = fields.Char(string='Operasi Ke', tracking=True)
    diagnosa_pra_bedah = fields.Char(string='Diagnosa Pra Bedah', tracking=True)
    diagnosa_pasca_bedah = fields.Char(string='Diagnosa Pasca Bedah', tracking=True)

    # Data biometri singkat
    retinometri = fields.Char(string='Retinometri', tracking=True)
    visus_bcva = fields.Char(string='Visus BCVA', tracking=True)
    k1 = fields.Char(string='K1', tracking=True)
    k2 = fields.Char(string='K2', tracking=True)
    axl = fields.Char(string='AXL', tracking=True)
    acd = fields.Char(string='ACD', tracking=True)
    iol_power = fields.Char(string='IOL power (Target Emmetropia)', tracking=True)
    formula_iol = fields.Char(string='Formula IOL', tracking=True)

    # Jenis operasi
    jenis_operasi = fields.Selection([
        ('phaco', 'Fakoemulsifikasi'),
        ('sics', 'SICS'),
        ('ecce', 'ECCE'),
        ('icce', 'ICCE'),
        ('lainnya', 'Lainnya'),
    ], string='Jenis Operasi', tracking=True)
    jenis_operasi_lainnya = fields.Char(string='Jenis Operasi Lainnya', tracking=True)

    # Disinfeksi & persiapan lapangan operasi
    disinfeksi_betadine = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Disinfeksi lapangan operasi dengan betadine', tracking=True
    )
    pasang_eye_drape_steril = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Pasang eye drape steril', tracking=True
    )
    pasang_blepharospat = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Pasang blepharospat', tracking=True
    )

    # Anestesi
    jenis_anestesi = fields.Selection([
        ('topikal', 'Topikal'),
        ('subkon_tenon', 'Sub-kon/tenon'),
        ('blok', 'Blok'),
        ('umum', 'Umum'),
    ], string='Anestesi', tracking=True)

    # Approach
    approach = fields.Selection([
        ('temporal', 'Temporal'),
        ('superior', 'Superior'),
        ('skleral_tunnel', 'Skleral tunnel'),
        ('limbal', 'Limbal'),
        ('kornea', 'Kornea'),
    ], string='Approach', tracking=True)

    # Insisi
    jenis_insisi = fields.Selection([
        ('sklera', 'Sklera'),
        ('limbal', 'Limbal'),
        ('kornea', 'Kornea'),
    ], string='Insisi', tracking=True)

    # Kapsulotomi CCC
    kapsulotomi_ccc = fields.Selection([
        ('komplit', 'Komplit'),
        ('tidak_komplit', 'Tidak Komplit'),
        ('can_opener', 'Can Opener'),
    ], string='Kapsulotomi (CCC)', tracking=True)

    hidrodiseksi = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Hidrodisection', tracking=True
    )

    manajemen_nukleus = fields.Selection([
        ('vectis', 'Vectis'),
        ('ekspresi', 'Ekspresi'),
        ('fako', 'Fako'),
    ], string='Manajemen Nukleus', tracking=True)

    teknik_fako = fields.Selection([
        ('stop_chop', 'Stop & Chop'),
        ('horizontal_chop', 'Horizontal Chop'),
        ('vertical_chop', 'Vertical Chop'),
        ('dnc', 'D&C'),
    ], string='Teknik Fako', tracking=True)

    ia_kortex = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='I/A Kortex', tracking=True
    )

    iol_implan = fields.Selection([
        ('bag', 'Bag'),
        ('sulkus', 'Sulkus'),
        ('afakia', 'Afakia'),
        ('iris_claw', 'Iris Claw Anterior/Posterior'),
        ('fiksasi_sklera', 'Fiksasi Sklera'),
    ], string='IOL Implan', tracking=True)

    iol_tipe = fields.Selection([
        ('iris_claw', 'Iris Claw Anterior/Posterior'),
        ('fiksasi_sklera', 'Fiksasi Sklera'),
    ], string='Tipe IOL', tracking=True)

    jahitan = fields.Selection([
        ('tidak', 'Tidak'),
        ('ya', 'Ya'),
        ('final_incision', 'Final Incision'),
    ], string='Jahitan', tracking=True)

    isi_jahitan = fields.Integer(string='Jumlah Jahitan')
    

    vitrektomi_anterior = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Vitrektomi Anterior', tracking=True
    )
    kapsulotomi_posterior = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Kapsulotomi Posterior', tracking=True
    )
    miotikum = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Miotikum', tracking=True
    )

    injeksi_antibiotika = fields.Selection([
        ('intra_kameral', 'Intra kameral'),
        ('sub_konjungtiva', 'Sub Konjungtiva'),
        ('peribulbar', 'Peribulbar'),
    ], string='Injeksi Antibiotika', tracking=True)

    tetes_mata = fields.Selection([
        ('salep_antibiotik', 'Salep Antibiotik'),
        ('ya', 'Tetes mata - Ya'),
        ('tidak', 'Tetes mata - Tidak'),
    ], string='Tetes mata', tracking=True)

    bebat_mata = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Bebat mata', tracking=True
    )

    mesin_fako = fields.Char(string='Mesin Fako', tracking=True)
    cairan_irigasi = fields.Char(string='Cairan Irigasi', tracking=True)
    phaco_time = fields.Char(string='Phaco Time', tracking=True)
    ept_cde = fields.Char(string='EPT / CDE', tracking=True)

    # Komplikasi
    komplikasi = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Komplikasi', tracking=True
    )
    komplikasi_rk_posterior = fields.Boolean(string='Ruptur Kapsul Posterior', tracking=True)
    komplikasi_vitreous_prolaps = fields.Boolean(string='Vitreous Prolaps', tracking=True)
    komplikasi_sisa_material_lensa = fields.Boolean(string='Sisa Material Lensa', tracking=True)
    komplikasi_sisa_kortex = fields.Boolean(string='Sisa Kortex', tracking=True)
    terapi_catatan = fields.Text(string='Terapi / Catatan', tracking=True)
    dpjp_tanda_tangan = fields.Many2one('res.users', string='DPJP (Tanda tangan dan nama terang)', tracking=True)

    # REPORT PDF
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.laporan.operasi.katarak/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        data_field = {
            'dpjp'                  : self.dpjp_id.name or '',
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
            'jumlah_jahitan'        : str(self.isi_jahitan or ''),
            'phaco_time'            : self.phaco_time or '',
            'ept_cde'               : self.ept_cde or '',
            'komplikasi'            : self._get_selection_value(model='cdn.laporan.operasi.katarak', field='komplikasi', value=self.komplikasi),
            'komplikasi_rk_posterior' : '☑' if self.komplikasi_rk_posterior else '☐',
            'komplikasi_vitreous_prolaps' : '☑' if self.komplikasi_vitreous_prolaps else '☐',
            'komplikasi_sisa_material_lensa' : '☑' if self.komplikasi_sisa_material_lensa else '☐',
            'komplikasi_sisa_kortex': '☑' if self.komplikasi_sisa_kortex else '☐',
            'terapi_catatan'        : self.terapi_catatan or '',
            'nama_pasien': self.pasien_id.name or '',
            'tanggal_lahir': self.pasien_id.tanggal_lahir.strftime('%d/%m/%Y') if self.pasien_id.tanggal_lahir else '',
            # 'jenis_kelamin': str(self._get_selection_value(
            #     model='cdn.pasien',
            #     field='jenis_kelamin',
            #     value=self.pasien_id.jenis_kelamin
            # ) or ''),
            'no_rm': str(self.pasien_id.no_rm or ''),
            'ttd_dpjp': self.qr_ttd_dokter_partner_id.name or '................................................',
        }
        template = 'cdn_simrs_rekamedis_add/template/klinik_mata/Laporan_Operasi_Katarak.docx'
        return self._mail_merge_to_pdf(
            path        = template,
            data_info   = data_field,
            image_info  = [ 
                {'key'       : '{{gambar}}','value'     : self.qr_ttd_dokter_code,   'inches'    : 1,},
                {'key'       : '{{catatan_image}}','value'     : self.catatan_image or False,   'inches'    : 1,},
                {'key'       : '{{logo}}','value'     : self.company_id.logo,       'inches'    : 0.7,},
            ],
            list_info   = []
        )



