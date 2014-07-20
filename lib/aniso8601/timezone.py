# -*- coding: utf-8 -*-

#Copyright 2013 Brandon Nielsen
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime

def parse_timezone(tzstr):
    #tzstr can be ±hh:mm, ±hhmm, ±hh, the Z case is handled elsewhere

    tzstrlen = len(tzstr)

    if tzstrlen == 6:
        #±hh:mm
        tzhour = int(tzstr[1:3])
        tzminute = int(tzstr[4:6])

        if tzstr[0] == '+':
            return build_utcoffset(tzstr, datetime.timedelta(hours=tzhour, minutes=tzminute))
        else:
            if tzhour == 0 and tzminute == 0:
                raise ValueError('String is not a valid ISO8601 time offset.')
            else:
                return build_utcoffset(tzstr, -datetime.timedelta(hours=tzhour, minutes=tzminute))
    elif tzstrlen == 5:
        #±hhmm
        tzhour = int(tzstr[1:3])
        tzminute = int(tzstr[3:5])

        if tzstr[0] == '+':
            return build_utcoffset(tzstr, datetime.timedelta(hours=tzhour, minutes=tzminute))
        else:
            if tzhour == 0 and tzminute == 0:
                raise ValueError('String is not a valid ISO8601 time offset.')
            else:
                return build_utcoffset(tzstr, -datetime.timedelta(hours=tzhour, minutes=tzminute))
    elif tzstrlen == 3:
        #±hh
        tzhour = int(tzstr[1:3])

        if tzstr[0] == '+':
            return build_utcoffset(tzstr, datetime.timedelta(hours=tzhour))
        else:
            if tzhour == 0:
                raise ValueError('String is not a valid ISO8601 time offset.')
            else:
                return build_utcoffset(tzstr, -datetime.timedelta(hours=tzhour))
    else:
        raise ValueError('String is not a valid ISO8601 time offset.')

def build_utcoffset(name, utcdelta):
    #We build an offset in this manner since the
    #tzinfo class must have an init that can
    #"method that can be called with no arguments"

    returnoffset = UTCOffset()

    returnoffset.setname(name)
    returnoffset.setutcdelta(utcdelta)

    return returnoffset

class UTCOffset(datetime.tzinfo):
    def setname(self, name):
        self._name = name

    def setutcdelta(self, utcdelta):
        self._utcdelta = utcdelta

    def utcoffset(self, dt):
        return self._utcdelta

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        #ISO8601 specifies offsets should be different if DST is required,
        #instead of allowing for a DST to be specified
        return None
