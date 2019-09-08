import sys
import json
import re
import argparse
import os


def get_file(path):
    try:
        return open(path, 'r')
    except FileNotFoundError as e:
        print("Could not find file on path: " + path)
        print(e)


def load_json_contents(f):
    print("--- Loading GeoJSON file...")
    return json.loads(f.read())


def move_field_to_id(json_input, field):
    print("--- Moving {0} field for SalesForce Einstein Analytics Compatibility...".format(field))
    features = json_input["features"]
    for i in features:
        i["id"] = i["properties"][field]
        if args.delete_properties:
            del i["properties"]
    return features


def remove_duplicate_coordinates(features):
    for i in features:
        final_list = []
        coordinates = i["geometry"]["coordinates"]
        for coordinate in coordinates[0]:
            if coordinate not in final_list:
                final_list.append(coordinate)
        i["geometry"]["coordinates"][0] = final_list
    return features


def save_file(path, features):
    print("--- Saving geojson file...")
    out_file = open(path, "w")
    out_file.write(json.dumps(features))
    out_file.close()
    format_geojson(path)


def format_geojson(path):
    prepend_file = open(path, "r")
    line = "{\"type\":\"FeatureCollection\",\"features\":"
    read_file = prepend_file.readlines()
    read_file.insert(0, line)
    prepend_file.close()

    wr = open(path, "w")
    wr.writelines(read_file)
    wr.close()

    with open(path, "a") as file:
        file.write("}")


def convert_polygon_decimals(decimal_points, data):
    content = json.dumps(data)
    decimal_reduced = re.sub("([0-9]+\.[0-9]{0}{1}{2})([0-9]+)".format("{", decimal_points, "}"), r'\1', content, flags=re.M)
    return json.loads(decimal_reduced)


def get_args(argv=None):
    parser = argparse.ArgumentParser(description="GeoJSON formatter for SaleForce Analytics")
    parser.add_argument(
        "source_file_path",
        type=str,
        help="File path of GeoJSON File")
    parser.add_argument(
        "properties_field",
        type=str,
        help="File path of GeoJSON File")
    parser.add_argument(
        "polygon_decimal_points",
        type=int,
        nargs="?",
        const=1,
        default=4,
        help="Set number of decimal points on the polygon coordinates"
    )
    parser.add_argument(
        "delete_properties",
        type=bool,
        nargs="?",
        const=1,
        default=False,
        help="Set to true if you would like to delete the Properties object")
    return parser.parse_args(argv)


if __name__ == '__main__':
    args = get_args(sys.argv[1:])

    input_file = get_file(args.source_file_path)

    print("\nInput File Location: {0}".format(args.source_file_path))
    print("Input File Size: {0} MB\n".format(os.path.getsize(args.source_file_path) >> 20))

    transformed_data = move_field_to_id(load_json_contents(input_file), args.properties_field)
    converted_polygon_data = convert_polygon_decimals(args.polygon_decimal_points, transformed_data)
    de_duplicated_data = remove_duplicate_coordinates(converted_polygon_data)

    output_file_extension = "{0}".format(os.path.splitext(args.source_file_path)[1])
    output_file_name = "{0}".format(os.path.splitext(os.path.basename(args.source_file_path))[0])
    output_file_path = "{0}/{1}_FORMATTED{2}".format(os.path.dirname(args.source_file_path), output_file_name, output_file_extension)

    save_file(output_file_path, de_duplicated_data)

    print("\nOutput File Location: {0}".format(output_file_path))
    print("Output File Size: {0} MB".format(os.path.getsize(output_file_path) >> 20))
    print("\nGeoJSON Conversion Complete")
