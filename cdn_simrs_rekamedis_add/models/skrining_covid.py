# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CdnSkriningCovid19(models.Model):
    _name = 'cdn.skrining.covid19'
    _description = 'Formulir Skrining COVID-19'
    _inherits = {
        'cdn.erm.base': 'rm_base_id',
    }
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'cdn.erm.mixin',
    ]

    rm_base_id = fields.Many2one(
        comodel_name='cdn.erm.base',
        string='RM',
        required=True,
        ondelete='cascade'
    )

    # =====================================================
    # A. GEJALA
    # =====================================================
    gejala_demam = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Demam / Riwayat Demam < 2 Minggu',
        tracking=True
    )

    gejala_batuk = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Batuk / Pilek / Nyeri Tenggorokan < 2 Minggu',
        tracking=True
    )

    gejala_sesak = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Sesak Nafas',
        tracking=True
    )

    # =====================================================
    # B. FAKTOR RISIKO
    # =====================================================
    perjalanan_14_hari = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Riwayat perjalanan 14 hari terakhir',
        tracking=True
    )

    kontak_erat_covid = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Kontak erat dengan kasus COVID-19',
        tracking=True
    )

    bekerja_faskes = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Bekerja / mengunjungi fasilitas kesehatan',
        tracking=True
    )

    kontak_hewan = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Kontak dengan hewan penular',
        tracking=True
    )

    demam_tinggi = fields.Selection(
        [('ya', 'Ya'), ('tidak', 'Tidak')],
        string='Demam > 38°C',
        tracking=True
    )

    # =====================================================
    # C. KOTA TERDAMPAK (SELECTION SENDIRI, BUKAN MASTER)
    # =====================================================
    kota_jakarta = fields.Boolean(string='Jakarta')
    kota_bandung = fields.Boolean(string='Bandung')
    kota_yogyakarta = fields.Boolean(string='Yogyakarta')
    kota_depok = fields.Boolean(string='Depok')
    kota_tangerang = fields.Boolean(string='Tangerang')
    kota_bogor = fields.Boolean(string='Bogor')
    kota_manado = fields.Boolean(string='Manado')
    kota_pontianak = fields.Boolean(string='Pontianak')
    kota_solo = fields.Boolean(string='Solo')
    kota_denpasar = fields.Boolean(string='Denpasar')
    kota_lainnya = fields.Boolean(string='Kota Lainnya')
    kota_lainnya_nama = fields.Char(string='Nama Kota Lainnya')

    # =====================================================
    # D. KESIMPULAN
    # =====================================================
    kesimpulan = fields.Selection(
        [
            ('pdp', 'Pasien Dalam Pengawasan (PDP)'),
            ('odp', 'Orang Dalam Pemantauan (ODP)'),
            ('bukan', 'Bukan Keduanya'),
        ],
        string='Kesimpulan',
        compute='_compute_kesimpulan',
        store=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ], default='draft', string='Status', tracking=True)

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancelled'

    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('rm_base_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.rm_base_id.display_name or ''} - Skrining COVID-19"

    # =====================================================
    # LOGIKA PENILAIAN (SESUAI FORM KERTAS)
    # =====================================================
    @api.depends(
        'gejala_demam',
        'gejala_batuk',
        'gejala_sesak',
        'perjalanan_14_hari',
        'kontak_erat_covid',
        'bekerja_faskes',
        'kontak_hewan',
        'demam_tinggi'
    )
    def _compute_kesimpulan(self):
        for rec in self:
            gejala = [
                rec.gejala_demam == 'ya',
                rec.gejala_batuk == 'ya',
                rec.gejala_sesak == 'ya',
            ]

            faktor_risiko = [
                rec.perjalanan_14_hari == 'ya',
                rec.kontak_erat_covid == 'ya',
                rec.bekerja_faskes == 'ya',
                rec.kontak_hewan == 'ya',
                rec.demam_tinggi == 'ya',
            ]

            jumlah_gejala = sum(gejala)
            ada_faktor = any(faktor_risiko)

            # PDP
            if jumlah_gejala >= 2 and ada_faktor:
                rec.kesimpulan = 'pdp'

            # ODP
            elif jumlah_gejala >= 1 and ada_faktor:
                rec.kesimpulan = 'odp'

            # Bukan keduanya
            else:
                rec.kesimpulan = 'bukan'
