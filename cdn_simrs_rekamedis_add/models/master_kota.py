# -*- coding: utf-8 -*-
from odoo import models, fields

class MasterKota(models.Model):
    _name = 'master.kota'
    _description = 'Master Data Kota'

    name = fields.Char(string='Nama Kota', required=True)
    kode = fields.Char(string='Kode Kota')
