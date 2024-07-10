import telegeography
import infrapedia
import submarinenetworks
import wiki


def telegeography_auto():
    telegeography.get_telegeography_by_api()

def infrapedia_auto():
    infrapedia.download_pbf()
    infrapedia.get_eol_from_pbf()
    infrapedia.get_by_api()



if __name__ == '__main__':
    telegeography.get_telegeography_by_api()
    infrapedia_auto()

