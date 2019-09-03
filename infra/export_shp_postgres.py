import infra_lib
import pprint


def add_infraid_info(info):
    for item in info:
        infra_level = infra_lib.get_infra_level(item["path"])
        item["infra_level"] = infra_level
        if item["is_buffer"]:
            item["id"] = item["buffer_distance"] + infra_level


def add_buffer_info(info):
    for item in info:
        buffer_distance = infra_lib.buffer_distance(item["path"])
        is_buffer = bool(buffer_distance)
        item["is_buffer"] = is_buffer
        item["buffer_distance"] = int(buffer_distance) if is_buffer else 0


def export_infra(info):
    info_infra = [item for item in info if not item["is_buffer"]]
    list_infra_levels = [item["infra_level"] for item in info_infra]
    print(list_infra_levels)
    print('deleting infra from postgres')
    infra_lib.delete_infra_postgres(list_infra_levels)
    print('preparing data for postgres')
    data = infra_lib.data_infra_postgres(info_infra)
    print('exporting data for postgres')
    infra_lib.insert_postgres(data)

def export_infra_buffer(info):
    info_infra = [item for item in info if item["is_buffer"]]
    list_ids = [item["id"] for item in info_infra]
    print(list_ids)
    print('deleting infra from postgres')
    infra_lib.delete_infra_buffer_postgres(list_ids)
    print('preparing data for postgres')
    data = infra_lib.data_infra_buffer_postgres(info_infra)
    print('exporting data for postgres')
    infra_lib.insert_postgres_buffer(data)



def start(folder_shp):

    paths = infra_lib.get_shapefiles(folder_shp)

    info = [{"path": item} for item in paths]

    add_buffer_info(info)

    add_infraid_info(info)

    # print([item for item in info if item['id'] == 10048])

    # export_infra(info)

    export_infra_buffer(info)
    # print(info[0])
    # pprint.pprint([item for item in info if item['infra_level'] == 48 and  item['is_buffer']], indent=4)


if __name__ == "__main__":
    start("/home/dyeden/Documents/mapbiomas/infra_vectors/infra_2019")
