# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is where I am putting memory diagnostic code.

https://www.fugue.co/blog/diagnosing-and-fixing-memory-leaks-in-python.html
"""

import linecache
import tracemalloc


def display_top(snapshot, key_type='lineno', limit=100):
	"""
	From the documentation.
	"""
	snapshot = snapshot.filter_traces((
		tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
		tracemalloc.Filter(False, "<unknown>"),
	))
	top_stats = snapshot.statistics(key_type)

	print("Top %s lines" % limit)
	for index, stat in enumerate(top_stats[:limit], 1):
		frame = stat.traceback[0]
		print("#%s: %s:%s: %.1f KiB" % (index, frame.filename, frame.lineno, stat.size / 1024))
		line = linecache.getline(frame.filename, frame.lineno).strip()
		if line:
			print('    %s' % line)

	other = top_stats[limit:]
	if other:
		size = sum(stat.size for stat in other)
		print("%s other: %.1f KiB" % (len(other), size / 1024))
	total = sum(stat.size for stat in top_stats)
	print("Total allocated size: %.1f KiB" % (total / 1024))


class MemTrace:
	"""
	An easy way to call tracemalloc
	"""
	def __init__(self):
		self.snapshots = list()
		tracemalloc.start(10)

	def take_snap(self):
		"""
		This will take a memory snapshot.
		"""
		snapshot = tracemalloc.take_snapshot()
		self.snapshots.append(snapshot)
		return snapshot

	def comp_snap(self, ln: int = 100, pattern: str = '*ImageTk*', comp: str = 'filename'):
		"""
		This will compare the passed snap with the one specified in memory.
		"""
		filters = [tracemalloc.Filter(inclusive=True, filename_pattern=pattern)]

		if len(self.snapshots) > 1:
			filtered_stats = self.snapshots[-1].filter_traces(filters).compare_to(self.snapshots[-2], comp)
			self.show_stats(filtered_stats, ln)

	def show_snap(self, ln: int = 100):
		"""
		This will pretty print a snapshot.
		"""
		display_top(self.snapshots[-1], 'filename', ln)

	@staticmethod
	def show_stats(stats, ln: int = 100):
		"""
		This will print the stats from a series of filtered staps.
		"""
		for stat in stats[:ln]:
			print("{} new KiB {} total KiB {} new {} total memory blocks: ".format(stat.size_diff/1024, stat.size / 1024, stat.count_diff, stat.count))

			for line in stat.traceback.format():
				print(line)

	def comp_n_show(self, ln: int = 100):
		"""
		THis will take a snap and compare it with the last.
		"""
		self.take_snap()
		self.show_snap(ln)
		self.comp_snap(ln)
		print('--------------------------------TRACEBACK---------------------------------')
		self.comp_snap(ln, comp='traceback')
		self.show_snap(ln)
		print('-----------------------------------END------------------------------------')
