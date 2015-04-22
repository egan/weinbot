/*
 * launch.sh: Launch WEINBot control software and watch for crashes.
 *
 * Copyright 2015, Egan McComb
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>

int main(void)
{
	int ret;

	if (setuid(0))
	{
		fprintf(stderr, "Error: Failed setuid()\n");
		exit(EPERM);
	}

	ret = system("python2 weinbot.py");

	if (ret != 0) {
		system("bash resetgpio.sh");
	}

	return 0;
}
