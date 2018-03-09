def get_table(d):
    month = str(d.month) if d.month > 9 else '0' + str(d.month)
    table = "`fh-bigquery.reddit_comments." + str(d.year)
    if d.year > 2014:
        table += "_" + month
    table += "`"
    return table

def run_query(credentials, project, date):
    from google.cloud import bigquery
    from datetime import datetime
    d_start = datetime.fromtimestamp(date)
    d_end = datetime.fromtimestamp(date + 7*24*60*60 - 1)
    tables = []
    tables.append(get_table(d_start))
    if (d_start.month != d_end.month):
        tables.append(get_table(d_end))
    count = 0
    for table in tables:
        query = """
            SELECT count(*)
            FROM """ + table + """
            WHERE LOWER(body) like '%s&amp;p 500%' and created_utc >= """ + str(date) + """ and created_utc <  """ + str(date + 7*24*60*60)
        client = bigquery.Client(project=project, credentials=credentials)
        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = False
        query_job = client.query(query, job_config=job_config)

        # Expect only a single row.
        for row in query_job.result():
            count += row[0]
    return count

def authenticate(launch_browser=True):
    from google_auth_oauthlib import flow
    appflow = flow.InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/bigquery'])
    if launch_browser:
        appflow.run_local_server()
    else:
        appflow.run_console()
    return appflow

if __name__ == '__main__':
    project = "hip-field-159415"
    appflow = authenticate(True)
    # GMT: Sunday, February 17, 2013 12:00:00 AM
    date = 1361059200
    thefile = open('counts.csv', 'a')
    for i in range(1, 261):
        count = run_query(appflow.credentials, project, date)
        thefile.write("%d, %d\n" % (date, count))
        date += 7 * 24 * 60 * 60
    print('last date: %d' % date)
