#!/usr/bin/python

import wolfbot
import time


class slicer(object):

  def __init__(self, wb):
    self.config = wb.config
    self.log = wb.log
    self.period_ms = self.config.get('ir_period_ms', 1000)
    self.slices = self.config.get('ir_slices', 10 )
    self.slice_ms = self.period_ms / self.slices   #  ms per slice
    self.log.debug('Milliseconds per slice: %d' % self.slice_ms)
    self.slice_num = self.config['id'] - 1
    self.slice_offset = self.slice_num * self.slice_ms

  def slice_info(self):
    period_ms = self.period_ms
    slice_ms= self.slice_ms

    now_ms = int(time.time() * 1000)

    cur_period = int(now_ms / period_ms)
    period_start = cur_period * period_ms
    period_end = period_start + period_ms
    self.log.debug('Period start: %d' % period_start)
    self.log.debug('Current time: %d' % now_ms)
    self.log.debug('Period end  : %d' % period_end)

    cur_slice = (now_ms - period_start) / self.slice_ms
    self.log.debug('Current slice: %d' % cur_slice)
    
    start = period_start + self.slice_offset
    end = start + slice_ms
    self.log.debug("My slice : %d" % self.slice_num)
    self.log.debug("My start : %d" % start)
    self.log.debug("My end   : %d" % end)

    return { 'cur_slice': cur_slice, 'start': start, 'end': end }

  def current_slice(self):
    now_ms = int(time.time() * 1000)
    period_ms = self.period_ms

    cur_period = int(now_ms / period_ms)
    period_start = cur_period * period_ms
    cur_slice = (now_ms - period_start) / self.slice_ms
    return cur_slice

  def next_start(self):
    period_ms = self.period_ms

    now_ms = int(time.time() * 1000)
    cur_period = int(now_ms / period_ms)
    period_start = cur_period * period_ms
    start = period_start + self.slice_offset
    if start < now_ms:
      start += period_ms
    return start


  def sleep_until_start(self):
    """ 
    Sleeps until the the beginning of our next slice, so we get a full slice.
    Will sleep even if we're currently in the middle of our slice.
    """

    sleep_ms = self.next_start() - time.time()*1000
    self.log.debug("Sleep for %d ms" % sleep_ms)
    time.sleep(sleep_ms/1000.0)

    return 

  def sleep_until_slice(self):
    """ 
    Sleeps until we're within our slice.  
    Will not sleep if we're currently in the middle of our slice.
    """

    time_ms = time.time()*1000
    if self.slice_num == self.current_slice():
      self.log.debug("Already in my slice")
    else:
      sleep_ms = self.next_start() - time_ms
      self.log.debug("Sleep for %d ms" % sleep_ms)
      time.sleep(sleep_ms/1000.0)
    return 
