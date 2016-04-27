from calendar import month_name, day_abbr
from calendar import Calendar
from membership.models import Calendar as CalendarModel
import datetime

now = datetime.datetime.now()


class CustomCalendar(Calendar):
    def __init__(self):
        super(CustomCalendar, self).__init__(firstweekday=0)

    def itermonthdays(self, year, month):
        """
        Like itermonthdates(), but will yield day numbers. For days outside
        the specified month the day number.
        """
        for date in self.itermonthdates(year, month):
            yield date.day

    def itermonthdays2(self, year, month):
        """
        Like itermonthdates(), but will yield (day number, weekday number)
        tuples. For days outside the specified month the day number is 0.
        """
        for date in self.itermonthdates(year, month):
            yield (date.day, date.weekday(), date.month)


class CustomHTMLCalendar(CustomCalendar):
    """
    This calendar returns complete HTML pages.
    """

    # CSS classes for the day <td>s

    def __init__(self, requested_month):
        self.requested_month = requested_month
        super(CustomHTMLCalendar, self).__init__()

    def formatday(self, day, weekday, month=None,year=None):
        """
        Return a day as a table cell.
        """

        booked = CalendarModel.objects.filter(user_id=self.user.id)
        is_booked= booked.filter(datebooked=datetime.date(day=day,month=month,year=year))

        if month < int(self.requested_month):
            return '<td class="prev-month %s">%d</td>' % ("selected" if is_booked else "",day)
        elif month > int(self.requested_month):
            return '<td class="next-month %s">%d</td>' % ("selected" if is_booked else "",day)
        else:
            return '<td class="%s">%d</td>' % ("selected" if is_booked else "",day)

    def formatweek(self, theweek,year):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, month,year) for (d, wd, month) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<tr><th colspan="7" class="month">%s</th></tr>' % s

    def add_before(self):
        return '<a class="btn-prev fontawesome-angle-left" href="#"></a>'

    def add_after(self):
        return '<a class="btn-next fontawesome-angle-right" href="#"></a>'

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.add_before())
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.add_after())
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week,theyear))
            a('\n')
        a('</table>')
        a('\n')
        a('<span id="datesbooked"></span>')
        return ''.join(v)


class BookCalendar(CustomHTMLCalendar):
    def __init__(self, user,requested_month):
        self.user=user
        super(BookCalendar, self).__init__(requested_month)

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(BookCalendar, self).formatmonth(year, month)

    def day_cell(self, cssclass, body):
        return '<td>%s</td>' %  body

    def formatmonthname(self, theyear, themonth, withyear):
        """
        Return a month name as a table row.
        """
        s = '%s' % month_name[themonth]
        return '<span id="monthtitle">%s</span>' % s

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """

        ret = '<td>%s</td>' % day_abbr[day][0:2]
        return ret

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<thead>%s</thead>' % s
