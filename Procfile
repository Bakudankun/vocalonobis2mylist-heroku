daily: python vocalonobis2mylist.py $MID_DAILY daily
weekly: if [ `TZ=Asia/Tokyo date +%w` = 1 ]; then python vocalonobis2mylist.py $MID_WEEKLY weekly ; fi
monthly: if [ `TZ=Asia/Tokyo date +%-d` = 1 ]; then python vocalonobis2mylist.py $MID_MONTHLY monthly ; fi
