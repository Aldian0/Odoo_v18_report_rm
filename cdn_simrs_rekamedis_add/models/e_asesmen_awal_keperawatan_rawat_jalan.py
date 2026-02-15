from odoo import models, fields, api
from datetime import datetime

class CdnErmAsesmenAwalKeperawatanRawatJalan(models.Model):
    _name = 'cdn.erm.asesmen.awal.keperawatan.rawat.jalan'
    _description = 'Asesmen Awal Keperawatan Rawat Jalan'
    _inherits = {'cdn.erm.base': 'rm_base_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin', 'cdn.erm.mixin', 'cdn.report.mailmerge']

    rm_base_id = fields.Many2one(comodel_name='cdn.erm.base', string='RM', required=True, ondelete='cascade')

    # Properties untuk dynamic fields
    erm_properties = fields.Properties(definition="rm_id.erm_properties_definition", string="Properties")

    # Data Tambahan Pasien
    mobile_pasien = fields.Char(string='No. Telp Pasien', related='pasien_id.mobile', tracking=True)
    pendidikan_pasien_id = fields.Many2one(string='Pendidikan Pasien', comodel_name='ref.pendidikan', tracking=True)
    status_perkawinan = fields.Selection(string='Status Perkawinan',related='pasien_id.status_kawin', store=True,tracking=True)
    agama_pasien = fields.Selection(string='Agama Pasien',related='pasien_id.agama', tracking=True)
    suku_pasien = fields.Many2one(string='Suku Pasien', comodel_name='ref.suku', tracking=True)
    bahasa_pasien = fields.Many2many(string='Bahasa Pasien', comodel_name='ref.bahasa', tracking=True)
    pekerjaan_pasien = fields.Selection(string='Pekerjaan Pasien', selection=[('Tidak/belum bekerja', 'Tidak/belum bekerja'), ('TNI/POLRI', 'TNI/POLRI'), ('PNS', 'PNS'), ('Petani', 'Petani'), ('Wiraswasta', 'Wiraswasta'), ('Karyawan Swasta', 'Karyawan Swasta'), ('Buruh', 'Buruh'), ('Lainnya', 'Lainnya')], tracking=True)
    lainnya_pekerjaan_pasien = fields.Char(string='Lainnya Pekerjaan Pasien', tracking=True)
    status_pembiayaan = fields.Selection(string='Status Pembiayaan', selection=[('umum', 'Umum'), ('BPJS', 'BPJS'), ('Asuransi', 'Asuransi'), ('Perusahaan/Piutang', 'Perusahaan/Piutang'), ('Lainnya', 'Lainnya')], tracking=True)
    lainnya_pembiayaan = fields.Char(string='Lainnya Pembiayaan', tracking=True)
    klinik_tujuan_pasien = fields.Selection(string='Klinik Tujuan Pasien', selection=[('Umum', 'Umum'), ('Penyakit Dalam', 'Penyakit Dalam'), ('Anak', 'Anak'), ('Bedah', 'Bedah'), ('Orthopedi', 'Orthopedi'), ('Syaraf', 'Syaraf'), ('Kebidanan/Kandungan', 'Kebidanan/Kandungan'), ('Mata', 'Mata'), ('THT', 'THT'), ('Gigi', 'Gigi'), ('Lainnya', 'Lainnya')], tracking=True)
    lainnya_klinik_tujuan_pasien = fields.Char(string='Lainnya Klinik Tujuan Pasien', tracking=True)

    line_ids = fields.One2many(string='Data Asesmen', inverse_name='asesmen_awal_keperawatan_rawat_jalan_id', comodel_name='cdn.erm.asesmen.awal.keperawatan.rawat.jalan.line', tracking=True)

    # Alamat lengkap
    alamat_pasien = fields.Char(string='Alamat Pasien', related='pasien_id.street')
    rt_pasien = fields.Char(string='RT Pasien', related='pasien_id.rt_ktp')
    rw_pasien = fields.Char(string='RW Pasien', related='pasien_id.rw_ktp')
    kota_pasien = fields.Char(string='Kota Pasien', related='pasien_id.kota_id_ktp.name')
    propinsi_pasien = fields.Char(string='Provinsi Pasien', related='pasien_id.propinsi_id_ktp.name')

    # Alergi / Reaksi
    alergi = fields.Selection(string='Alergi', selection=[('Tidak', 'Tidak'), ('Ya', 'Ya')], tracking=True)
    ya_alergi = fields.Text(string='Ya Alergi', tracking=True)
    alergi_obat = fields.Char(string='Alergi Obat', tracking=True)
    alergi_makanan = fields.Char(string='Alergi Makanan', tracking=True)
    alergi_lainnya = fields.Char(string='Alergi Lainnya', tracking=True)
    reaksi = fields.Selection(string='Reaksi', selection=[('Tidak', 'Tidak'), ('Ya', 'Ya')], tracking=True)
    ya_reaksi = fields.Text(string='Ya Reaksi', tracking=True)
    reaksi_obat = fields.Char(string='Reaksi Obat', tracking=True)
    reaksi_makanan = fields.Char(string='Reaksi Makanan', tracking=True)
    reaksi_lainnya = fields.Char(string='Reaksi Lainnya', tracking=True)

    # penurunan Berat Badan
    penurunan_bb = fields.Selection(string='Penurunan Berat Badan (6 Bulan Terakhir)', selection=[('tidak', 'Tidak ada'), ('tidak yakin', 'Tidak yakin'), ('1_5', '1 – 5 kg'), ('6_10', '6 – 10 kg'), ('11_15', '11 – 15 kg'), ('lebih_15', '> 15 kg')], tracking=True)
    skor_penurunan_bb = fields.Integer(string='Skor Penurunan BB', compute='_compute_skor', store=True)
    # Asupan Makanan
    asupan_berkurang = fields.Selection(string='Asupan Makanan', selection=[('tidak', 'Tidak'), ('ya', 'Ya')], tracking=True)
    skor_asupan = fields.Integer(string='Skor Asupan', compute='_compute_skor', store=True)
    # Total Skor
    total_skor = fields.Integer(string='Total Skor', compute='_compute_skor', store=True)

    #Diagnosa Khusus
    pasien_diagnosa = fields.Selection(string='Pasien dengan Diagnosa Khusus', selection=[('tidak', 'Tidak'), ('ya', 'Ya')], tracking=True)
    ya_diagnosa = fields.Selection(string='Ya, Lapor DPJP Untuk Konsultasi Gizi', selection=[('DM', 'DM'), ('Ginjal', 'Ginjal'), ('Hati', 'Hati'), ('Jantung', 'Jantung'), ('Kanker', 'Kanker'), ('Stroke', 'Stroke'), ('Paru', 'Paru'), ('Geriatri', 'Geriatri'), ('Penurunan Imunitas', 'Penurunan Imunitas'), ('Lainnya', 'Lainnya')], tracking=True)
    lainnya_diagnosa = fields.Char(string='Lainnya Diagnosa', tracking=True)

    #status fungsional
    status_fungsional_mandiri = fields.Boolean(string='Mandiri', tracking=True)
    status_fungsional_dilaporkan = fields.Boolean(string='Ketergantungan Total, di laporkan ke dokter pukul', tracking=True)
    date_dilaporkan = fields.Datetime(string='Tanggal Dilaporkan', tracking=True)
    status_fungsional_bantuan = fields.Boolean(string='Perlu Bantuan, Sebutkan', tracking=True)
    bantuan = fields.Char(string='Bantuan', tracking=True)

    #Psikolog
    status_psikolog = fields.Selection(string='Status Psikolog', selection=[('tenang', 'Tenang'), ('takut', 'Takut'), ('marah', 'Marah'), ('sedih', 'Sedih'), ('cemas', 'Cemas'), ('kecenderungan bunuh diri', 'Kecenderungan bunuh diri')], tracking=True)
    status_mental = fields.Selection(string='Status Mental', selection=[('sadar dan orientasi baik', 'Sadar dan orientasi baik'), ('tidak sadar dan orientasi kurang baik', 'Tidak sadar dan orientasi kurang baik')], tracking=True)
    masalah_prilaku = fields.Char(string='Ada Masalah Prilaku, Sebutkan', tracking=True)
    prilaku_kekerasan = fields.Char(string='Prilaku Kekerasan Yang Di Alami Pasien Sebelumnya', tracking=True)
    kebutuhan_pelayanan = fields.Selection(string='Kebutuhan Pelayanan Kerohanian', selection=[('tidak', 'Tidak'), ('ya', 'Ya')], tracking=True)
    ya_kebutuhan_pelayanan = fields.Char(string='Ya Kebutuhan Pelayanan Kerohanian', tracking=True)

    # Logika Skor
    @api.depends('penurunan_bb', 'asupan_berkurang')    
    def _compute_skor(self):
        for record in self:
            skor_bb = 0
            if record.penurunan_bb == 'tidak':
                skor_bb = 0
            elif record.penurunan_bb == 'tidak yakin':
                skor_bb = 2
            elif record.penurunan_bb == '1_5':
                skor_bb = 1
            elif record.penurunan_bb == '6_10':
                skor_bb = 2
            elif record.penurunan_bb == '11_15':
                skor_bb = 3
            elif record.penurunan_bb == 'lebih_15':
                skor_bb = 4
            
            # Asupan
            skor_asupan_val = 1 if record.asupan_berkurang == 'ya' else 0

            record.skor_penurunan_bb = skor_bb
            record.skor_asupan = skor_asupan_val
            record.total_skor = skor_bb + skor_asupan_val

    def action_print(self):
        return self.action_print_docx()

class CdnErmAsesmenAwalKeperawatanRawatJalanLine(models.Model):
    _name = 'cdn.erm.asesmen.awal.keperawatan.rawat.jalan.line'
    _description = 'Asesmen Awal Keperawatan Rawat Jalan Line'

    asesmen_awal_keperawatan_rawat_jalan_id = fields.Many2one(string='Asesmen Awal Keperawatan Rawat Jalan', comodel_name='cdn.erm.asesmen.awal.keperawatan.rawat.jalan', required=True)

    waktu_asesmen = fields.Datetime(string='Waktu Asesmen', default=fields.Datetime.now, tracking=True)
    kondisi_datang_pasien = fields.Char(string='Datang', tracking=True)
    mulai_tindakan_pasien = fields.Char(string='Mulai Tindakan', tracking=True)
    selesai_tindakan_pasien = fields.Char(string='Selesai Tindakan', tracking=True)


    