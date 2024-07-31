import logging
from typing import Dict, List

import folium
import numpy as np
import spacy
import spacy_streamlit
import streamlit as st
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.location import Location
from streamlit_folium import folium_static

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    ),
)
logger = logging.getLogger(__name__)
nlp_pipe = spacy.load("en_core_web_md")
geocoder = Nominatim(user_agent="ceh_sample_app")
rl_geocode = RateLimiter(geocoder.geocode, min_delay_seconds=1)


@st.cache_data
def locate(query) -> Location:
    logger.info(f'Geocoding "{query}"')
    return rl_geocode(query, geometry="geojson", country_codes="gb")


def calc_bounds(coords: List[List[float]]) -> List[List[float]]:
    """
    Calculates the bounds for a list of coordinates. Returns the most
    south-westerly point and the most north-easterly point required to
    encapsulate all the coordinates in a bounding box.
    """
    transposed_coords = np.array(coords).T.tolist()
    return [
        [min(transposed_coords[0]), min(transposed_coords[1])],
        [max(transposed_coords[0]), max(transposed_coords[1])],
    ]


def calc_geojson_bounds(geojson: Dict) -> List[List[float]]:
    """
    Unpacks the coordinates provided in a geojson object and calculates a
    bounding box to enclose them. Works with point, polygon and multi-polygon
    geojson types.
    """
    polygons = geojson["coordinates"]
    polygon_bounds = []
    match geojson["type"]:
        case "MultiPolygon":
            for polygon in polygons:
                polygon_bounds.extend(calc_bounds(polygon[0]))
        case "Polygon":
            polygon_bounds.extend(calc_bounds(polygons[0]))
        case "Point":
            polygon_bounds = [polygons]
    return calc_bounds(polygon_bounds)


def get_bounds(locations: List[Location]) -> List[List[int]]:
    location_bounds = []
    for location in locations:
        location_bounds.extend(calc_geojson_bounds(location.raw["geojson"]))
    return calc_bounds(location_bounds)


def flip_coord_lat_long(coord: List[float]) -> List[float]:
    return [coord[1], coord[0]]


def flip_coords_lat_long(coords: List[List[float]]) -> List[List[float]]:
    return [flip_coord_lat_long(coord) for coord in coords]


def main() -> None:
    st.set_page_config(layout="wide", page_title="NER Spatial Mapping")
    st.title("NER Spatial Mapping")
    left, right = st.columns(2)
    locations = []
    with left:
        if query := st.text_input("Enter query"):
            parsed_query = nlp_pipe(query)
            spacy_streamlit.visualize_ner(parsed_query, show_table=False)
            locations = [
                locate(entity.text)
                for entity in parsed_query.ents
                if entity.label_ == "GPE"
            ]
            locations = [loc for loc in locations if loc]
    with right:
        if len(locations) < 1:
            return
        map = folium.Map(location=[0.000000, 0.000000], zoom_start=1)
        for location in locations:
            folium.Marker(
                location=[
                    location.latitude,
                    location.longitude,
                ],
                popup=folium.Popup(location.address),
            ).add_to(map)
            folium.GeoJson(location.raw["geojson"]).add_to(map)
        bounds = get_bounds(locations)
        bounds = flip_coords_lat_long(bounds)
        logger.info(bounds)
        map.fit_bounds(bounds)
        folium_static(map)


if __name__ == "__main__":
    main()
