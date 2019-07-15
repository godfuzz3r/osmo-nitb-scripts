#!/usr/bin/env python3


def update_monitor(users):
    data = "ID\t\tcreated\t\tIMSI\t\t\tTMSI\t\tnumber\n\n"
    data += "-" * 80
    data += "\n\n"

    for sub in users:
        try:
            user_data = "{0:1}\t{1:2}\t{2:<15}\t\t{3:<10}\t{4}".format(
                sub[0],
                sub[1],
                sub[3],
                sub[7],
                sub[5]
            )
            data += user_data

        except Exception as e:
            print(e)
            print(sub)

        data += "\n"

    print('\x1bc')
    print("\x1b[{};{}H".format(0, 0))
    print("\x1b[2J")
    print(data)
