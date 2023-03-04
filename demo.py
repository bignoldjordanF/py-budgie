import pbreader


def main():
    contents = pbreader.read_pb_file('resources/poland_warszawa_2019_ursynow.pb')
    print(contents.metadata)


if __name__ == '__main__':
    main()
