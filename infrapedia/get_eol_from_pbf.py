from protobuf_inspector.types import StandardParser
import re
from utils import *


def get_eol_from_pbf():
    parser = StandardParser()
    ids = set()

    path = '.\\data\\data_' + formatted_date
    os.remove(os.path.join(path, 'id_eol.csv'))

    for x in range(0, 4):
        for y in range(0, 3):
            with open(os.path.join(path, 'pbf', '{}-{}-{}.pbf'.format('2', x, y)), 'rb') as fh:
                output = parser.parse_message(fh, "message")
                output = output.split('\n')
                for index, row in enumerate(output):
                    search_object = re.search('[a-z0-9]{24}', row)
                    if search_object != None:
                        id = search_object.group()
                        if not id or id in ids:
                            continue
                        ids.add(id)
                        s_obj = re.search('[0-9]{8}', output[index - 5])
                        if s_obj == None:
                            s_obj = re.search('[0-9]{8}', output[index - 4])
                        if s_obj != None:
                            dump_file([search_object.group(), s_obj.group()], os.path.join(path, 'id_eol.csv'))


if __name__=='__main__':
    get_eol_from_pbf()
