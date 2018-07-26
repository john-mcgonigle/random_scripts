'''
If manually running this, run the following in the shell first:
export SAPIENTIA_DB_HOST=staging-db.sapientia.co.uk
export SAPIENTIA_DB_NAME=sapientia
export SAPIENTIA_DB_USER=postgres
export SAPIENTIA_DB_PASSWORD=Orange18a
'''

import psycopg2
import os

class Sapientia(object):
    def __init__(self):
        self.db = self.get_cursor()

    def get_cursor(self):
        connect_str = "host={SAPIENTIA_DB_HOST} dbname={SAPIENTIA_DB_NAME} user={SAPIENTIA_DB_USER} password={SAPIENTIA_DB_PASSWORD}".format(**os.environ)
        conn = psycopg2.connect(connect_str)
        cur = conn.cursor()

        return cur

    def _get_count(self, query):
        self.db.execute(query)
        entries = self.db.fetchall()

        return entries[0][0] if entries else 'N/A'

    @property
    def num_irs(self):
        return self._get_count("SELECT count(*) as num_irs FROM interpretation_request")

    @property
    def num_patients(self):
        return self._get_count("SELECT count(*) FROM patient WHERE project_id=431")

    @property
    def num_finished_patients(self):
        # patients go Files pending -> Processing -> Ready for review
        return self._get_count("SELECT count(*) FROM patient WHERE status='Ready for review'")

    @property
    def num_pending(self):
        return self._get_count("SELECT count(*) FROM patient WHERE status='Files pending'")

    @property
    def num_processing(self):
        return self._get_count("SELECT count(*) FROM patient WHERE status='Processing'")

sap = Sapientia()
class Patient(Sapientia):
    def __init__(self, patient_id):
        Sapientia.__init__(self)
        self.id = patient_id

    def _get_query_results(self, query):
        self.db.execute(query)
        entries = self.db.fetchall()
        return entries

    @property
    def get_files(self, file_type):
        return self._get_query_results("SELECT * FROM patient_file where patient_id = {id} "
                                       "and file_id = {file_type}".format(id=self.id, file_type = file_type))



patient = Patient(8061)
patient.get_files(2)
