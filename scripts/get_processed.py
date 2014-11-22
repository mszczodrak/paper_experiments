#!/usr/bin/python


def get_processed(file_name):

	f = open(file_name, "r")
	m = 0
	s = 0

	for line in f.readlines():
		l = line.split()

		if l == []:
			continue

		if l[0] != "SUMMARY":
			continue

		if l[6] == "mean:":
			m = float(l[7])

		if l[6] == "std:":
			s = float(l[7])

	return [m,s]

if __name__ == "__main__":
	get_processed("processed.txt")
