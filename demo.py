import pybudgie.pbreader as pbreader


def main():
    instance = pbreader.read_file('resources/poland_warszawa_2019_ursynow.pb')
    for voter in instance.projects:
        print(voter)
        print()


if __name__ == '__main__':
    main()
