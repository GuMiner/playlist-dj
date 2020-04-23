import time


class Progress:
    def __init__(self, scanning_object, report_every):
        self._object = scanning_object

        self._count = 0
        self._max = -1
        self._start_time = None
        self._report_every = report_every

    def start(self, count):
        self._max = count
        self._start_time = time.monotonic()
        print('  Scanning {} {}...'.format(self._max, self._object))

    def increment(self):
        self._count += 1
        if self._count % self._report_every == 0:
            print('    Scanned {} of {} {}.'.format(
                self._count, self._max, self._object))

    def stop(self):
        return time.monotonic() - self._start_time
