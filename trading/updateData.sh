#!/bin/bash

curl http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/rvxdailyprices.csv --output data/rvx.csv

curl http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv --output data/vix.csv

curl http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/gvzhistory.csv --output data/gvx.csv