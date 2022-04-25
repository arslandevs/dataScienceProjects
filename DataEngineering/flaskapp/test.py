import unittest
from tests import mysqlRowcount, postgresRowcount


class rowCount(unittest.TestCase):
    def test_line_rowCount(self):

        self.assertEqual(mysqlRowcount("line"), postgresRowcount("line"))

    def test_module_rowCount(self):

        self.assertEqual(mysqlRowcount("module"), postgresRowcount("module"))

    def test_userpermission_rowCount(self):

        self.assertEqual(mysqlRowcount("userpermission"),
                         postgresRowcount("userpermission"))

    def test_worker_rowCount(self):

        self.assertEqual(mysqlRowcount("worker"), postgresRowcount("worker"))

    def test_machine_type_rowCount(self):

        self.assertEqual(mysqlRowcount("machine_type"),
                         postgresRowcount("machine_type"))

    def test_machine_rowCount(self):

        self.assertEqual(mysqlRowcount("machine"), postgresRowcount("machine"))

    def test_sale_order_rowCount(self):

        self.assertEqual(mysqlRowcount("sale_order"),
                         postgresRowcount("sale_order"))

    def test_section_rowCount(self):

        self.assertEqual(mysqlRowcount("section"), postgresRowcount("section"))

    def test_user_rowCount(self):

        self.assertEqual(mysqlRowcount("user"), postgresRowcount("user"))

    def test_operation_rowCount(self):

        self.assertEqual(mysqlRowcount("operation"),
                         postgresRowcount("operation"))

    def test_worker_scan_rowCount(self):

        self.assertEqual(mysqlRowcount("worker_scan"),
                         postgresRowcount("worker_scan"))

    def test_style_template_rowCount(self):

        self.assertEqual(mysqlRowcount("style_template"),
                         postgresRowcount("style_template"))

    def test_style_bulletin_rowCount(self):

        self.assertEqual(mysqlRowcount("style_bulletin"),
                         postgresRowcount("style_bulletin"))

    def test_production_order_rowCount(self):

        self.assertEqual(mysqlRowcount("production_order"),
                         postgresRowcount("production_order"))

    def test_marker_rowCount(self):

        self.assertEqual(mysqlRowcount("marker"), postgresRowcount("marker"))

    def test_cut_job_rowCount(self):

        self.assertEqual(mysqlRowcount("cut_job"), postgresRowcount("cut_job"))

    def test_cut_report_rowCount(self):

        self.assertEqual(mysqlRowcount("cut_report"),
                         postgresRowcount("cut_report"))

    def test_tag_rowCount(self):

        self.assertEqual(mysqlRowcount("tag"), postgresRowcount("tag"))

    def test_scan_rowCount(self):

        self.assertEqual(mysqlRowcount("scan"), postgresRowcount("scan"))

    def test_piece_wise_scan_rowCount(self):

        self.assertEqual(mysqlRowcount("piece_wise_scan"),
                         postgresRowcount("piece_wise_scan"))

    def test_piece_wise_cut_report_rowCount(self):

        self.assertEqual(mysqlRowcount("piece_wise_cut_report"),
                         postgresRowcount("piece_wise_cut_report"))


if __name__ == '__main__':
    unittest.main()
