
import apache_beam as beam


def _append_key(element, key_name):
    """Reads and append key to the element

    :param element: Collection element
    :param key_name: Key name
    """

    return element[key_name], element


def _build_key(element, build_key):
    """Build key and append it to the element

    :param element: Collection element
    :param build_key: Function for building the key
    """

    key = build_key(element)
    return key, element


def _unnest_elements(element, missing_join_value):
    """Unnest joined elements

    :param element: Tuple that contains the element's key and the result of the joining
    :param missing_join_value: Default value to use if there is no match in the right set
    """

    key, value = element
    left_items = value['left']
    right_items = value['right']

    if len(right_items) > 0:
        right_item = right_items[0]
    elif missing_join_value:
        right_item = missing_join_value
    else:
        right_item = {}

    return list(map(
        lambda left_item: {**left_item, **right_item},
        left_items
    ))


class LeftJoin(beam.PTransform):
    """Transform for making left joins

    :param key_name: Left set key for joining
    :param build_key: Function for building the left set key
    :param missing_join_value: Default value to use if there is no match in the right set
    """

    def __init__(self, key_name=None, build_key=None, missing_join_value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.key_name = key_name
        self.build_key = build_key
        self.missing_join_value = missing_join_value

    def expand(self, p):
        left_p, right_p = p

        if self.key_name:
            left_p = (left_p
                      | 'append_join_key' >> beam.Map(_append_key, self.key_name))
        else:
            left_p = (left_p
                      | 'build_join_key' >> beam.Map(_build_key, self.build_key))

        return (({'left': left_p, 'right': right_p})
                | 'join' >> beam.CoGroupByKey()
                | 'unnest' >> beam.FlatMap(_unnest_elements, self.missing_join_value))
