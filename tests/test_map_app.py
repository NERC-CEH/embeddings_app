from unittest import TestCase

import map.map_app


class TestMapApp(TestCase):

    def test_calc_bounds(self):
        data = [[-9.0234247, 57.829], [-8.153736, 56.18254824]]
        result = map.map_app.calc_bounds(data)
        assert result == [[-9.0234247, 56.18254824], [-8.153736, 57.829]]

    def test_calc_geojson_bounds(self):
        multipoly = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[-9.0234247, 57.829], [-8.153736, 56.18254824]]]
            ],
        }
        multipoly_result = map.map_app.calc_geojson_bounds(multipoly)
        assert multipoly_result == [
            [-9.0234247, 56.18254824],
            [-8.153736, 57.829],
        ]

        poly = {
            "type": "Polygon",
            "coordinates": [[[-9.0234247, 57.829], [-8.153736, 56.18254824]]],
        }
        poly_result = map.map_app.calc_geojson_bounds(poly)
        assert poly_result == [[-9.0234247, 56.18254824], [-8.153736, 57.829]]

        point = {"type": "Point", "coordinates": [-9.0234247, 57.829]}
        point_result = map.map_app.calc_geojson_bounds(point)
        assert point_result == [[-9.0234247, 57.829], [-9.0234247, 57.829]]
