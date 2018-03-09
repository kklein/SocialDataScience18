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
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    d_start = datetime.fromtimestamp(date)
    d_end = datetime.fromtimestamp(date + 7*24*60*60 - 1)
    tables = []
    tables.append(get_table(d_start))
    if (d_start.month != d_end.month):
        tables.append(get_table(d_end))
    sid = SentimentIntensityAnalyzer()
    pos_sentiment = 0
    neg_sentiment = 0
    compound_sentiment = 0
    count = 0
    for table in tables:
        query = """
            SELECT body
            FROM """ + table + """
            WHERE LOWER(body) like '%s&amp;p 500%' and created_utc >= """ + str(date) + """ and created_utc <  """ + str(date + 7*24*60*60)
        client = bigquery.Client(project=project, credentials=credentials)
        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = False
        query_job = client.query(query, job_config=job_config)

        for row in query_job.result():
            pos_sentiment += sid.polarity_scores(row[0])['pos']
            neg_sentiment += sid.polarity_scores(row[0])['neg']
            compound_sentiment += sid.polarity_scores(row[0])['compound']
            count += 1

    return (pos_sentiment/count, neg_sentiment/count, compound_sentiment/count)

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
    thefile = open('sentiments.csv', 'a')
    for i in range(1, 261):
        sentiment = run_query(appflow.credentials, project, date)
        thefile.write("%d, %f, %f, %f\n" % (date, sentiment[0], sentiment[1], sentiment[2]))
        date += 7 * 24 * 60 * 60
    print('last date: %d' % date)
