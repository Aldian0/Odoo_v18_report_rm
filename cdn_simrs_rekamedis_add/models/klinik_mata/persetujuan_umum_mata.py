# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
import datetime

class ResCompany(models.Model):
    _inherit = 'res.company'
    @api.model
    def _get_pernyataan_persetujuan(self):
        template = """
<div>
    <p>Selaku Pasien / Wali hukum pasien dengan ini menyatakan memberikan persetujuan:</p>
    <ol>
        <li>Saya menyetujui untuk perawatan di {{company_name}} sebagai pasien {{type}}.</li>
        <li><strong>HAK DAN KEWAJIBAN SEBAGAI PASIEN.</strong> Saya mengakui bahwa pada proses pendaftaran untuk mendapatkan perawatan di {{company_name}}, saya telah mendapat informasi tentang hak-hak dan kewajiban saya sebagai pasien.</li>
        <li><strong>PERSETUJUAN PELAYANAN KESEHATAN.</strong> Saya menyetujui dan memberikan persetujuan untuk mendapat pelayanan kesehatan di {{company_name}} dan dengan ini saya meminta dan memberikan kuasa kepada klinik, dokter, perawat, dan tenaga kesehatan lainnya untuk memberikan asuhan perawatan, pemeriksaan fisik, prosedur diagnostik, terapi, dan tatalaksana sesuai pertimbangan dokter. Hal ini mencakup seluruh pemeriksaan, tindakan medis, penyuntikan, penggunaan produk farmasi, obat-obatan, serta pengambilan darah untuk pemeriksaan laboratorium atau patologi.</li>
        <li><strong>AKSES INFORMASI KESEHATAN.</strong> Saya memberi kuasa kepada tenaga kesehatan yang merawat saya untuk memeriksa dan/atau memberitahukan informasi kesehatan saya kepada tenaga kesehatan lain yang turut merawat saya selama di {{company_name}}.</li>
        <li><strong>RAHASIA MEDIS.</strong> Saya setuju bahwa {{company_name}} wajib menjaga kerahasiaan informasi medis saya, kecuali diungkapkan oleh saya atau oleh orang yang saya beri kuasa.</li>
        <li><strong>PRIVASI.</strong> Saya memberi kuasa kepada {{company_name}} untuk menjaga privasi dan kerahasiaan penyakit saya selama perawatan.</li>
        <li><strong>BARANG PRIBADI.</strong> Saya setuju bahwa apabila saya membawa barang di luar ketentuan, {{company_name}} tidak bertanggung jawab atas kehilangan, kerusakan, atau pencurian barang tersebut.</li>
        <li><strong>PENGAJUAN KELUHAN.</strong> Saya menyatakan bahwa saya telah menerima informasi mengenai tata cara pengajuan keluhan. Saya setuju mengikuti prosedur pengajuan keluhan sesuai ketentuan yang berlaku.</li>
        <li><strong>PELEPASAN INFORMASI.</strong> Saya memberi wewenang kepada {{company_name}} untuk memberikan informasi medis yang diperlukan untuk proses klaim BPJS, asuransi komersial, perusahaan, maupun lembaga pemerintah.</li>
        <li><strong>KEWAJIBAN PEMBAYARAN.</strong> Saya setuju bahwa saya wajib membayar seluruh biaya pelayanan sesuai ketentuan {{company_name}}. Saya memahami bahwa:
            <ol type="a">
                <li>Apabila saya tidak memberikan atau mencabut persetujuan terkait pelepasan rahasia kedokteran untuk keperluan klaim asuransi, maka saya pribadi bertanggung jawab atas seluruh biaya.</li>
                <li>Apabila {{company_name}} membutuhkan proses hukum untuk penagihan biaya, saya bertanggung jawab atas seluruh biaya yang timbul dari proses tersebut.</li>
            </ol>
        </li>
    </ol>
</div>
        """
        return template

    html_content_pernyataan_persetujuan = fields.Html(
        string="Pernyataan Persetujuan",
        default=_get_pernyataan_persetujuan
    )

    @api.model
    def _get_pernyataan_akhir(self):
        template = """
<div>
    Melalui dokumen ini, saya menegaskan kembali bahwa saya mempercayakan kepada seluruh tenaga kesehatan di {{company_name}} untuk memberikan perawatan, diagnostik, terapi, serta seluruh pemeriksaan penunjang yang diperlukan untuk pengobatan dan tindakan yang aman.
    SAYA TELAH MEMBACA DAN SEPENUHNYA SETUJU dengan seluruh pernyataan di atas, serta menandatangani dokumen ini tanpa paksaan dan dengan kesadaran penuh.
</div>
        """
        return template

    html_content_pernyataan_akhir = fields.Html(
        string="Pernyataan Akhir",
        default=_get_pernyataan_akhir
    )


class PersetujuanUmum(models.Model):
    _name = "cdn.persetujuan.umum"
    _description = "Persetujuan Umum / General Consent"
    _inherits = {
        "cdn.erm.base": "rm_base_id",
    }
    _inherit = ["mail.thread", "mail.activity.mixin", "cdn.erm.mixin", "cdn.report.mailmerge", 'cdn.simrs.library']

    rm_base_id = fields.Many2one(
        comodel_name="cdn.erm.base", string="RM", required=True, ondelete="cascade"
    )

    erm_properties      = fields.Properties(
        definition="rm_id.erm_properties_definition",
        string="Properties",
    )
    ttd_pasien_penanggung_jawab = fields.Binary(
        string="Ttd"
    )
    nama_pasien_penanggung_jawab = fields.Char(
        string="Nama", tracking=True
    )
    def action_print(self):
        return {
            'type'  : 'ir.actions.act_url',
            'url'   : f'/cdn_print_report_pdf/cdn.persetujuan.umum/{self.id}/_generate_print_report',
            'target': 'new',
        }

    def _generate_print_report(self):
        today = datetime.datetime.now()
        data_field = {
            'alamat'                             : self.pasien_id.city or '',
            'pasien_name'                        : self.pasien_id.name or '',
            'tanggal_lahir'                      : self.pasien_id.tanggal_lahir.strftime('%d/%m/%Y') if self.pasien_id.tanggal_lahir else '',
            'nama_pemberi_informasi'             : self.qr_ttd_informan_partner_id.name or '.................................',
            'nama_pasien_penanggung_jawab'       : self.nama_pasien_penanggung_jawab or '...............................',
            'tanggal_ttd'                        : self._tanggal_indonesia(self._to_wib(today)),
        }
        data_image = [
            {'key': '{{logo}}', 'value': self.company_id.logo, 'inches': 0.7},
            {'key': '{{ttd_pemberi_informasi}}', 'value': self.qr_ttd_informan_code, 'inches': 1},
            {'key': '{{ttd_pasien_penanggung_jawab}}', 'value': self.ttd_pasien_penanggung_jawab, 'inches': 2},
        ]
        template = 'cdn_simrs_rekamedis_add/template/klinik_mata/persetujuan_umum_general_consent_mata.docx'
        return self._mail_merge_to_pdf(
            path        = template,
            data_info   = data_field,
            image_info  = data_image
        )
    
    @api.model
    def _get_pernyataan_persetujuan(self):
        template = self.env.user.company_id.html_content_pernyataan_persetujuan if self.env.user.company_id.html_content_pernyataan_persetujuan else """
<div>
    <p>Selaku Pasien / Wali hukum pasien dengan ini menyatakan memberikan persetujuan:</p>
    <ol>
        <li>Saya menyetujui untuk perawatan di {{company_name}} sebagai pasien {{type}}.</li>
        <li><strong>HAK DAN KEWAJIBAN SEBAGAI PASIEN.</strong> Saya mengakui bahwa pada proses pendaftaran untuk mendapatkan perawatan di {{company_name}}, saya telah mendapat informasi tentang hak-hak dan kewajiban saya sebagai pasien.</li>
        <li><strong>PERSETUJUAN PELAYANAN KESEHATAN.</strong> Saya menyetujui dan memberikan persetujuan untuk mendapat pelayanan kesehatan di {{company_name}} dan dengan ini saya meminta dan memberikan kuasa kepada klinik, dokter, perawat, dan tenaga kesehatan lainnya untuk memberikan asuhan perawatan, pemeriksaan fisik, prosedur diagnostik, terapi, dan tatalaksana sesuai pertimbangan dokter. Hal ini mencakup seluruh pemeriksaan, tindakan medis, penyuntikan, penggunaan produk farmasi, obat-obatan, serta pengambilan darah untuk pemeriksaan laboratorium atau patologi.</li>
        <li><strong>AKSES INFORMASI KESEHATAN.</strong> Saya memberi kuasa kepada tenaga kesehatan yang merawat saya untuk memeriksa dan/atau memberitahukan informasi kesehatan saya kepada tenaga kesehatan lain yang turut merawat saya selama di {{company_name}}.</li>
        <li><strong>RAHASIA MEDIS.</strong> Saya setuju bahwa {{company_name}} wajib menjaga kerahasiaan informasi medis saya, kecuali diungkapkan oleh saya atau oleh orang yang saya beri kuasa.</li>
        <li><strong>PRIVASI.</strong> Saya memberi kuasa kepada {{company_name}} untuk menjaga privasi dan kerahasiaan penyakit saya selama perawatan.</li>
        <li><strong>BARANG PRIBADI.</strong> Saya setuju bahwa apabila saya membawa barang di luar ketentuan, {{company_name}} tidak bertanggung jawab atas kehilangan, kerusakan, atau pencurian barang tersebut.</li>
        <li><strong>PENGAJUAN KELUHAN.</strong> Saya menyatakan bahwa saya telah menerima informasi mengenai tata cara pengajuan keluhan. Saya setuju mengikuti prosedur pengajuan keluhan sesuai ketentuan yang berlaku.</li>
        <li><strong>PELEPASAN INFORMASI.</strong> Saya memberi wewenang kepada {{company_name}} untuk memberikan informasi medis yang diperlukan untuk proses klaim BPJS, asuransi komersial, perusahaan, maupun lembaga pemerintah.</li>
        <li><strong>KEWAJIBAN PEMBAYARAN.</strong> Saya setuju bahwa saya wajib membayar seluruh biaya pelayanan sesuai ketentuan {{company_name}}. Saya memahami bahwa:
            <ol type="a">
                <li>Apabila saya tidak memberikan atau mencabut persetujuan terkait pelepasan rahasia kedokteran untuk keperluan klaim asuransi, maka saya pribadi bertanggung jawab atas seluruh biaya.</li>
                <li>Apabila {{company_name}} membutuhkan proses hukum untuk penagihan biaya, saya bertanggung jawab atas seluruh biaya yang timbul dari proses tersebut.</li>
            </ol>
        </li>
    </ol>
</div>
        """
        data = {
            "company_name"  : self.env.user.company_id.name,
            "type"          : self.registrasi_id.jenis_registrasi or "Rawat Jalan",
        }
        return self._replace_value(template, data)

    html_content_pernyataan_persetujuan = fields.Html(
        string="Pernyataan Persetujuan",
        default=_get_pernyataan_persetujuan
    )

    @api.model
    def _get_pernyataan_akhir(self):
        template = str(self.env.user.company_id.html_content_pernyataan_akhir) if self.env.user.company_id.html_content_pernyataan_akhir else """
<div>
    Melalui dokumen ini, saya menegaskan kembali bahwa saya mempercayakan kepada seluruh tenaga kesehatan di {{company_name}} untuk memberikan perawatan, diagnostik, terapi, serta seluruh pemeriksaan penunjang yang diperlukan untuk pengobatan dan tindakan yang aman.
    SAYA TELAH MEMBACA DAN SEPENUHNYA SETUJU dengan seluruh pernyataan di atas, serta menandatangani dokumen ini tanpa paksaan dan dengan kesadaran penuh.
</div>
        """
        data = {
            "company_name": self.company_id.name,
        }
        return self._replace_value(template, data)

    html_content_pernyataan_akhir = fields.Html(
        string="Pernyataan Akhir",
        default=_get_pernyataan_akhir
    )