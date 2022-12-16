from functions.get_user_location import calculate_distance


def test_calculate_distance():
    coordinates_1 = (55.45, 37.37)
    coordinates_2 = (59.53, 30.15)

    expected_result = 625

    assert calculate_distance(coordinates_1[0], coordinates_1[1], coordinates_2[0], coordinates_2[1]) == expected_result
