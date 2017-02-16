# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestFinancialMove(TransactionCase):

    def setUp(self):
        super(TestFinancialMove, self).setUp()
        self.main_company = self.env.ref('base.main_company')
        self.currency_euro = self.env.ref('base.EUR')
        self.financial_move = self.env['financial.move']

    def test_1(self):
        """ DADO a data de vencimento de 27/02/2017
        QUANDO criado um lançamento de contas a receber
        ENTÃO a data de vencimento útil deve ser de 01/03/2017
        """
        cr_1 = self.financial_move.create(dict(
            due_date='2017-02-27',
            company_id=self.main_company.id,
            currency_id=self.currency_euro.id,
            amount_document=100.00,
        ))
        self.assertEqual(cr_1.business_due_date, '2017-03-01')

    def test_2(self):
        """DADO a data de vencimento de 27/02/2017
        QUANDO criado um lançamento de contas a receber
        ENTÃO a data de vencimento útil deve ser de 01/03/2017
        """
        with self.assertRaises(ValidationError):
            cr_2 = self.financial_move.create(
                dict(due_date='2017-02-27',
                     company_id=self.main_company.id,
                     currency_id=self.currency_euro.id,
                     amount_document=0.00,
                     )
            )