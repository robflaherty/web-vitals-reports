from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, timedelta, datetime
import math
import numpy as np

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '<REPLACE_WITH_JSON_FILE>'

VIEW_ID = '<REPLACE_WITH_JSON_FILE>'

START_DATE = '2020-06-01'
END_DATE   = '2020-06-14'

def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
    KEY_FILE_LOCATION, SCOPES)

  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics

# Adjust the query details; comment out segments if not needed
def fetch_data(metric, start_date = START_DATE, end_date = END_DATE):

  return API.reports().batchGet(
    body={
      'reportRequests': [
      {
        'viewId': VIEW_ID,
        'pageSize': 100000,
        'samplingLevel':  'LARGE',
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [{'expression': 'ga:eventValue'}],
        # If using segments, need to add {'name': 'ga:segment'} to the dimensions
        'dimensions': [{'name': 'ga:eventAction'},{'name': 'ga:eventLabel'},{'name': 'ga:segment'}],
        'dimensionFilterClauses': [
          {'filters': [
            {
              'dimensionName': 'ga:eventAction',
              'operator': 'EXACT',
              'expressions': [ metric ]
            }
          ]}
        ],
        'segments':[
        {
          'dynamicSegment':
          {
            'name': 'Page path filter',
            'sessionSegment':
            {
              'segmentFilters':[
              {
                'simpleSegment':
                {
                  'orFiltersForSegment':
                  {
                    'segmentFilterClauses': [
                    {
                      'dimensionFilter':
                      {
                        'dimensionName':'ga:medium',
                        'operator':'EXACT',
                        'expressions':['organic']
                      }
                    }]
                  }
                }
              }]
            }
          }
        }]
      }]
    }
  ).execute().get('reports')[0].get('data').get('rows')

# Returns buckets for Good - Needs Improvement - Poor
def get_distribution(metric):
  good = 0
  avg = 0
  poor = 0

  # Web Vitals Good and Poor thresholds
  thresholds = {
    'LCP':  [2500,4000],
    'FID':  [100,300],
    'CLS':  [500,1500],
    'TTFB': [500,1500]
  }

  result = fetch_data(metric)

  for row in result:
    val = int(row.get('metrics')[0].get('values')[0])
    if val <= thresholds[metric][0]:
      good += 1
    elif val > thresholds[metric][1]:
      poor += 1
    else:
      avg += 1

  return [good, avg, poor]

# Returns timeseries for a given percentile
def get_percentile(metric):
  start_date = datetime.strptime(START_DATE, '%Y-%m-%d').date()
  end_date = datetime.strptime(END_DATE, '%Y-%m-%d').date()

  cache = []

  # Adjust this to change between daily, weekly, etc
  delta = timedelta(days=1)

  while start_date <= end_date:
    vals = []
    print (start_date.strftime('%Y-%m-%d'))
    result = fetch_data(metric, start_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))

    for row in result:
      vals.append(int(row.get('metrics')[0].get('values')[0]))

    a = np.array(vals)

    # Adjust for different percentiles
    p = np.percentile(a, 75)

    cache.append(math.floor(p))

    start_date += delta

  return cache

# Main
def main():
  global API
  API = initialize_analyticsreporting()

  #response = get_distribution('LCP')

  response = get_percentile('LCP')

  print(response)

if __name__ == '__main__':
  main()
