from odoo import _, api, fields, models





class CdnHumptyDumpty(models.Model):
    _name           = 'cdn.humpty.dumpty'
    _description    = 'Humpty Dumpty'

    _inherits       = {
        'cdn.erm.base': 'rm_base_id',
        }
    _inherit        = [
        'mail.thread', 
        'mail.activity.mixin',
        'cdn.erm.mixin',
        'cdn.report.mailmerge'
        ]
    
    rm_base_id          = fields.Many2one(
        comodel_name    ='cdn.erm.base', string='RM', 
        required        =True, 
        ondelete        ='cascade'
    )

    erm_properties      = fields.Properties(
        definition      ="rm_id.erm_properties_definition",
        string          ="Properties",
    )

    line_ids            = fields.One2many(comodel_name='cdn.humpty.dumpty.line', inverse_name='humpty_dumpty_id', string='Penilaian Humpty Dumpty')



class CdnHumptyDumptyLine(models.Model):
    _name           = 'cdn.humpty.dumpty.line'
    _description    = 'Humpty Dumpty Line'

    tanggal = fields.Datetime('Tanggal', required=True, default=fields.Datetime.now)
    humpty_dumpty_id    = fields.Many2one(comodel_name='cdn.humpty.dumpty', string='Humpty Dumpty', required=True, ondelete='cascade')
    
    skor_umur               = fields.Selection(string='Umur', 
                                    selection=[('4', 'Kurang Dari 3 Tahun'), 
                                                ('3', '3 Tahun - 7 Tahun'), 
                                                ('2', '7 Tahun - 13 Tahun'),
                                                ('1', 'Lebih Dari 13 Tahun'),
                                                ], tracking=True, )
    skor_kelamin            = fields.Selection(string='Jenis Kelamin', 
                                    selection=[('2', 'Laki-Laki'), 
                                                ('1', 'Perempuan'),
                                                ], tracking=True, )
    skor_dianoksasi         = fields.Selection(string='Dianosisasi',
                                    selection=[('4', 'Neurologi'),
                                                ('3', 'Respratori, Dehidrasi, Anemis, Anorexia, syncope'),
                                                ('2', 'Perilaku'),
                                                ('1', 'Lainnya'),
                                                ], tracking=True, )
    skor_gangguan_kognitif  = fields.Selection(string='Ganggnuan Kognitif', 
                                    selection=[('3', 'Keterbatasan Daya Pikir'), 
                                                ('2', 'Pelupa'),
                                                ('1', 'Dapat Menggunakan Daya Pikir Tanpa Hambatan'),
                                                ], tracking=True, )
    skor_faktor_lingkungan  = fields.Selection(string='Faktor Lingkungan', 
                                    selection=[('4', 'Riwayat Jatuh atau Bayi/Balita yang di Tempatkan di tempat Tidur'),
                                                ('3', 'Pasien Menggunakan Alat Bantu/Bayi atau Balita yang di Tempatkan pada Ayunan'),
                                                ('2', 'Pasien di Tempat Tidur Standar'),
                                                ('1', 'Area Pasien Rawat Jalan'),
                                                ], tracking=True, )
    skor_respon             = fields.Selection(string='Respon Terhadap Pembedahan, Sendasi dan anestasi', 
                                    selection=[('3', 'Dalam 24 Jam'), 
                                                ('2', 'Dalam 48 Jam'),
                                                ('1', 'lebih Dari 48 Jam/Tidak ada Respon'),
                                                ], tracking=True, )
    skor_penggunaan_obat     = fields.Selection(string='Penggunaan Obat-Obatan',
                                    selection=[('3', 'Penggunaan Bersamaan Sedative, Barbiturate, Anti Despresan, Diuretik, Narkotik'),
                                                ('2', 'Salah Satu Obat Sedative, Barbiturate, Anti Despresan, Diuretik, Narkotik'),
                                                ('1', 'Obat-Obatan Lain/Tanpa Obat'),
                                                ], tracking=True, )
   

    total                   = fields.Integer(string='Total Skor', compute='_compute_total', store=True, )
    resiko                  = fields.Selection(string='Resiko',
                                        selection=[('rr', 'Resiko Rendah'), 
                                                    ('rt', 'Resiko Tinggi'),
                                                    ], store=True, tracking=True, )
    @api.depends(
        'skor_umur',
        'skor_kelamin',
        'skor_dianoksasi',
        'skor_gangguan_kognitif',
        'skor_faktor_lingkungan',
        'skor_respon',
        'skor_penggunaan_obat'
    )

    def _compute_total(self):
        for rec in self:
            skor_umur = 0
            skor_kelamin = 0
            skor_dianoksasi = 0
            skor_gangguan_kognitif = 0
            skor_faktor_lingkungan = 0
            skor_respon = 0
            skor_penggunaan_obat = 0
            total = 0
            if rec.skor_umur == False : 
                skor_umur = 0
            else:
                skor_umur = int(rec.skor_umur)
            if rec.skor_kelamin == False : 
                skor_kelamin = 0
            else:
                skor_kelamin = int(rec.skor_kelamin)
            if rec.skor_dianoksasi == False : 
                skor_dianoksasi = 0
            else:
                skor_dianoksasi = int(rec.skor_dianoksasi)
            if rec.skor_gangguan_kognitif == False : 
                skor_gangguan_kognitif = 0
            else:
                skor_gangguan_kognitif = int(rec.skor_gangguan_kognitif)
            if rec.skor_faktor_lingkungan == False : 
                skor_faktor_lingkungan = 0
            else:
                skor_faktor_lingkungan = int(rec.skor_faktor_lingkungan)
            if rec.skor_respon == False : 
                skor_respon = 0
            else:
                skor_respon = int(rec.skor_respon)
            if rec.skor_penggunaan_obat == False : 
                skor_penggunaan_obat = 0
            else:
                skor_penggunaan_obat = int(rec.skor_penggunaan_obat)
            total = skor_umur + skor_kelamin + skor_dianoksasi + skor_gangguan_kognitif + skor_faktor_lingkungan + skor_respon + skor_penggunaan_obat
            rec.total = total
            if total >= 12 :
                rec.resiko = 'rt'
            else:
                rec.resiko = 'rr'

    # Jika Resiko Tinggi
    rt_a  = fields.Selection(string='Memastikan tempat tidur/brankard dalam posisi roda terkunci', 
                                selection=[('sudah', 'Sudah Dilakukan'), 
                                            ('belum', 'Belum atau Tidak dilakukan'), 
                                            ('menolak', 'Pasien Menolak')], tracking=True, )
    rt_b  = fields.Selection(string='Pagar Sisi tempat tidur/brangkard dalam kondisi berdiri/terpasang', 
                                selection=[('sudah', 'Sudah Dilakukan'), 
                                            ('belum', 'Belum atau Tidak dilakukan'), 
                                            ('menolak', 'Pasien Menolak')], tracking=True, )  
    rt_c  = fields.Selection(string='Lingkungan bebas dari peralatan yang tidak digunakan', 
                                selection=[('sudah', 'Sudah Dilakukan'),
                                            ('belum', 'Belum atau Tidak dilakukan'), 
                                            ('menolak', 'Pasien Menolak')], tracking=True, )
    rt_d  = fields.Selection(string='Berikan penjelasan kepada orang tua tentang pencegahan jatuh', 
                                selection=[('sudah', 'Sudah Dilakukan'), 
                                            ('belum', 'Belum atau Tidak dilakukan'),
                                            ('menolak', 'Pasien Menolak')], tracking=True, )
    rt_e  = fields.Selection(string='Pastikan pasien memiliki stiker penanda risiko tinggi jatuh pada gelang identifikasi dan tanda kewaspadaan pada panel informasi pasien',
                                selection=[('sudah', 'Sudah Dilakukan'), 
                                            ('belum', 'Belum atau Tidak dilakukan'), 
                                            ('menolak', 'Pasien Menolak')], tracking=True, )
    
    # Jika Resiko Rendah
    rr_a  = fields.Selection(string='Memastikan tempat tidur/ brankard dalam posisi roda terkunci', 
                                selection=[('sudah', 'Sudah Dilakukan'), 
                                            ('belum', 'Belum atau Tidak dilakukan'), 
                                            ('menolak', 'Pasien Menolak')], tracking=True, )
    rr_b  = fields.Selection(string='Pagar sisi tempat tidur/ brankard dalam posisi berdiri/terpasang', 
                                selection=[('sudah', 'Sudah Dilakukan'), 
                                            ('belum', 'Belum atau Tidak dilakukan'), 
                                            ('menolak', 'Pasien Menolak')], tracking=True, )
    rr_c  = fields.Selection(string='Lingkungan bebas dari peralatan yang tidak digunakan', 
                                selection=[('sudah', 'Sudah Dilakukan'), 
                                            ('belum', 'Belum atau Tidak dilakukan'), 
                                            ('menolak', 'Pasien Menolak')], tracking=True, )
    rr_d  = fields.Selection(string='Berikan penjelasan kepada orang tua tentang pencegahan jatuh', 
                                selection=[('sudah', 'Sudah Dilakukan'), 
                                            ('belum', 'Belum atau Tidak dilakukan'), 
                                            ('menolak', 'Pasien Menolak')], tracking=True, )