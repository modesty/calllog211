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

from date import parse_date
from time import parse_time

def parse_duration(isodurationstr):
    #Given a string representing an ISO 8601 duration, return a
    #datetime.timedelta that matches the given duration. Valid formts are:
    #
    #PnYnMnDTnHnMnS (or any reduced precision equivalent)
    #P<date>T<time>

    if isodurationstr[0] != 'P':
        raise ValueError('String is not a valid ISO8601 duration.')

    #If Y, M, D, H, or S are in the string, assume it is a specified duration
    if isodurationstr.find('Y') != -1 or isodurationstr.find('M') != -1 or isodurationstr.find('W') != -1 or isodurationstr.find('D') != -1 or isodurationstr.find('H') != -1 or isodurationstr.find('S') != -1:
        return parse_duration_prescribed(isodurationstr)
    else:
        return parse_duration_combined(isodurationstr)

def parse_duration_prescribed(durationstr):
    #durationstr can be of the form PnYnMnDTnHnMnS

    #Make sure only the lowest order element has decimal precision
    if durationstr.count('.') > 1:
        raise ValueError('String is not a valid ISO8601 duration.')
    elif durationstr.count('.') == 1:
        #There should only ever be 1 letter after a decimal if there is more
        #then one, the string is invalid
        lettercount = 0;

        for character in durationstr.split('.')[1]:
            if character.isalpha() == True:
                lettercount += 1

            if lettercount > 1:
                raise ValueError('String is not a valid ISO8601 duration.')

    #Parse the elements of the duration
    if durationstr.find('T') == -1:
        if durationstr.find('Y') != -1:
            years = _parse_duration_element(durationstr, 'Y')
        else:
            years = 0

        if durationstr.find('M') != -1:
            months = _parse_duration_element(durationstr, 'M')
        else:
            months = 0

        if durationstr.find('W') != -1:
            weeks = _parse_duration_element(durationstr, 'W')
        else:
            weeks = 0

        if durationstr.find('D') != -1:
            days = _parse_duration_element(durationstr, 'D')
        else:
            days = 0

        #No hours, minutes or seconds
        hours = 0
        minutes = 0
        seconds = 0
    else:
        firsthalf = durationstr[:durationstr.find('T')]
        secondhalf = durationstr[durationstr.find('T'):]

        if  firsthalf.find('Y') != -1:
            years = _parse_duration_element(firsthalf, 'Y')
        else:
            years = 0

        if firsthalf.find('M') != -1:
            months = _parse_duration_element(firsthalf, 'M')
        else:
            months = 0

        if durationstr.find('W') != -1:
            weeks = _parse_duration_element(durationstr, 'W')
        else:
            weeks = 0

        if firsthalf.find('D') != -1:
            days = _parse_duration_element(firsthalf, 'D')
        else:
            days = 0

        if secondhalf.find('H') != -1:
            hours = _parse_duration_element(secondhalf, 'H')
        else:
            hours = 0

        if secondhalf.find('M') != -1:
            minutes = _parse_duration_element(secondhalf, 'M')
        else:
            minutes = 0

        if secondhalf.find('S') != -1:
            seconds = _parse_duration_element(secondhalf, 'S')
        else:
            seconds = 0

    totaldays = years * 365 + months * 30 + weeks * 7 + days

    return datetime.timedelta(days=totaldays, hours=hours, minutes=minutes, seconds=seconds)

def parse_duration_combined(durationstr):
    #Period of the form P<date>T<time>

    #Split the string in to its component parts
    datepart, timepart = durationstr[1:].split('T') #We skip the 'P'

    datevalue = parse_date(datepart)
    timevalue = parse_time(timepart)

    totaldays = datevalue.year * 365 + datevalue.month * 30 + datevalue.day

    return datetime.timedelta(days=totaldays, hours=timevalue.hour, minutes=timevalue.minute, seconds=timevalue.second, microseconds=timevalue.microsecond)

def _parse_duration_element(durationstr, elementstr):
    #Extracts the specified portion of a duration, for instance, given:
    #durationstr = 'T4H5M6.1234S'
    #elementstr = 'H'
    #
    #returns 4
    #
    #Note that the string must start with a character, so its assumed the
    #full duration string would be split at the 'T'

    durationstartindex = 0
    durationendindex = durationstr.find(elementstr)

    for characterindex in xrange(durationendindex - 1, 0, -1):
        if durationstr[characterindex].isalpha() == True:
            durationstartindex = characterindex
            break

    durationstartindex += 1

    return float(durationstr[durationstartindex:durationendindex])
