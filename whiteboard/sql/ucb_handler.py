import subprocess as sp

def call_handler():
    for i in range(30):
        prefix = 'copy(select * from cache_2.get_patient_ucb_report((select array_agg(patient_id) from (select patient_id from core.patient where project_id = 466 order by patient_id offset '
        suffix = ' limit 10) as subq)::int[])) to stdout with csv header;'
        with open('tmp.sql', 'w') as sql:
            sql.write(prefix+str(i*5)+suffix)

        with open('ucb'+str(i)+'.csv', 'w') as out:
            process = sp.Popen('PGPASSWORD=G0Xh3Dy14cU psql -h live-db.sapientia.co.uk -U postgres sapientia -f tmp.sql', stdout = out, shell = True)
            process.wait()
            print(str(i) + ' out of 30 completed.')

call_handler()

'''


cp ucb0.csv head.csv
for file in $(ls ?.csv)
do
    tail -n +2 $file > $file.rebind.csv
done

cat head.csv *rebind.csv > ucb_final.csv 


'''
