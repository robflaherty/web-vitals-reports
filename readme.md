# Web Vitals Reports
This is a simple Python script for extracting Web Vitals event data out of Google Analytics using the Reporting API. It outputs distributions and percentiles.

### Set-up
1. Set up Web Vitals tracking in Google Analytics as described in the `web-vitals` library [usage docs](https://github.com/GoogleChrome/web-vitals/#send-the-results-to-google-analytics)

2. Follow steps in the [Analytics Reporting API v4 quick start](https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py) to get the python client and credentials set up

3. Edit `run.py` to include the path to your JSON credentials and GA profile ID

4. Edit the `fetch_data()` function with the dimensions, metrics, filters, and segments you want to query

### Functions

#### `get_distribution()`
Returns 3 buckets using the Good, Needs Improvement, and Poor thresholds defined by the Web Vitals project. Supports LCP, FID, CLS, FCP, and TTFB.

#### `get_percentile()`
Returns a timeseries for a given percentile. Adjust the time delta for daily/weekly/monthly intervals.
