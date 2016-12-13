# -*- coding: utf-8 -*-
# Copyright 2016 KMEE - Luis Felipe Mileo <mileo@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields
# from openerp.addons.resource.tests import common
# from odoo.tests.common import SingleTransactionCase
import openerp.tests.common as test_common

# from pybrasil import feriado


class TestResourceCalendar(test_common.SingleTransactionCase):

    def setUp(self):
        super(TestResourceCalendar, self).setUp()

        self.resource_calendar = self.env['resource.calendar']
        self.resource_leaves = self.env['resource.calendar.leaves']

        self.nacional_calendar_id = self.resource_calendar.create({
            'name': 'Calendario Nacional',
            'country_id': self.env.ref("base.br").id,
        })
        self.leave_nacional_01 = self.resource_leaves.create({
            'name': 'Tiradentes',
            'date_from': fields.Datetime.from_string('2016-03-21 00:00:00'),
            'date_to': fields.Datetime.from_string('2016-03-21 23:59:59'),
            'calendar_id': self.nacional_calendar_id.id,
            'leave_type': 'F',
            'abrangencia': 'N',
        })
        self.estadual_calendar_id = self.resource_calendar.create({
            'name': 'Calendario Estadual',
            'parent_id': self.nacional_calendar_id.id,
        })
        self.leave_estadual_01 = self.resource_leaves.create({
            'name': 'Aniversario de SP',
            'date_from': fields.Datetime.from_string('2016-01-25 00:00:00'),
            'date_to': fields.Datetime.from_string('2016-01-25 23:59:59'),
            'calendar_id': self.estadual_calendar_id.id,
            'leave_type': 'F',
            'abrangencia': 'E',
        })
        self.municipal_calendar_id = self.resource_calendar.create({
            'name': 'Calendario Municipal',
            'parent_id': self.estadual_calendar_id.id,
        })
        self.leave_municipal_01 = self.resource_leaves.create({
            'name': 'Aniversario Chapeco',
            'date_from': fields.Datetime.from_string('2016-08-25 00:00:00'),
            'date_to': fields.Datetime.from_string('2016-08-25 23:59:59'),
            'calendar_id': self.municipal_calendar_id.id,
            'leave_type': 'F',
            'abrangencia': 'M',
        })

    def test_00_add_leave_nacional(self):
        """ Inclusao de um novo Feriado no calendario nacional """
        self.leave_nacional_02 = self.resource_leaves.create({
            'name': 'Natal',
            'date_from': fields.Datetime.from_string('2016-12-24 00:00:00'),
            'date_to': fields.Datetime.from_string('2016-12-24 23:59:59'),
            'calendar_id': self.nacional_calendar_id.id,
            'leave_type': 'F',
            'abrangencia': 'N',
        })
        self.assertEqual(self.leave_nacional_02.name, 'Natal')
        self.assertEqual(self.leave_nacional_02.calendar_id,
                         self.nacional_calendar_id)
        self.assertEqual(2, len(self.nacional_calendar_id.leave_ids))

    def test_01_add_leave_estadual(self):
        """ Inclusao de um novo Feriado no calendario Estadual """
        self.leave_estadual_02 = self.resource_leaves.create({
            'name': 'Aniversario MG',
            'date_from': fields.Datetime.from_string('2016-07-16 00:00:00'),
            'date_to': fields.Datetime.from_string('2016-07-16 23:59:59'),
            'calendar_id': self.estadual_calendar_id.id,
            'leave_type': 'F',
            'abrangencia': 'E',
        })
        self.assertEqual(self.leave_estadual_02.name, 'Aniversario MG')
        self.assertEqual(self.leave_estadual_02.calendar_id,
                         self.estadual_calendar_id)
        self.assertEqual(3, len(self.estadual_calendar_id.leave_ids))

    def test_02_add_leave_municipal(self):
        """ Inclusao de um novo Feriado no calendario municipal """
        self.leave_municipal_02 = self.resource_leaves.create({
            'name': 'Aniversario Itajuba',
            'date_from': fields.Datetime.from_string('2016-03-19 00:00:00'),
            'date_to': fields.Datetime.from_string('2016-03-19 23:59:59'),
            'calendar_id': self.municipal_calendar_id.id,
            'leave_type': 'F',
            'abrangencia': 'M',
        })
        self.assertEqual(self.leave_municipal_02.name, 'Aniversario Itajuba')
        self.assertEqual(self.leave_municipal_02.calendar_id,
                         self.municipal_calendar_id)
        self.assertEqual(4, len(self.municipal_calendar_id.leave_ids))

    def test_03_obter_feriados_no_periodo(self):
        self.holidays = self.resource_calendar.get_holidays_by_period(
            start_datetime=fields.Datetime.from_string('2016-03-01 00:00:00'),
            end_datetime=fields.Datetime.from_string('2016-03-31 00:00:00'),
            l10n_br_city_id=None,
            state_id=None,
            country_id=self.env.ref("base.br").id,
        )
        self.assertEqual(1, len(self.holidays))