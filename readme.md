# Web Vitals Reports
This is a simple Python script for extracting Web Vitals event data out of Google Analytics using the Reporting API. It outputs distribution and percentile values that you can pipe/paste into charting tools.

Using GA segments you can visualize things like [anonymous vs logged-in users](https://twitter.com/robflaherty/status/1273730608410353665) or comparing [converting vs non-converting sessions](https://twitter.com/robflaherty/status/1275449153288458241).

### Set-up
1. Set up Web Vitals tracking in Google Analytics as described in the `web-vitals` library [usage docs](https://github.com/GoogleChrome/web-vitals/#send-the-results-to-google-analytics)

2. Follow steps in the [Analytics Reporting API v4 quick start](https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py) to get the python client and credentials set up

3. Edit `vitals.py` to include the path to your JSON credentials and GA profile ID

4. Edit the `fetch_data()` function with the filters or segments you want to use

### Functions

#### `get_good_avg_poor()`
Returns 3 buckets using the Good, Needs Improvement, and Poor thresholds defined by the Web Vitals project. Supports LCP, FID, CLS, FCP, and TTFB.

#### `get_percentile()`
Returns an overall value for a given percentile.

#### `get_percentile_timeseries()`
Returns a timeseries for a given percentile. Adjust the time delta for daily/weekly/monthly intervals.
