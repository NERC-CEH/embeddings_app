import logging
from typing import List, Tuple

import folium
import spacy
import spacy_streamlit
import streamlit as st
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.location import Location
from streamlit_folium import st_folium

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    ),
)
logger = logging.getLogger(__name__)
nlp_pipe = spacy.load("en_core_web_sm")
geocoder = Nominatim(user_agent="ceh_sample_app")
rl_geocode = RateLimiter(geocoder.geocode, min_delay_seconds=1)


@st.cache_data
def locate(query) -> Location:
    logger.info(f'Geocoding "{query}"')
    return rl_geocode(query, geometry="geojson", country_codes="gb")


def extract_lats_longs(geojson):
    lats = []
    longs = []
    if geojson["type"] == "MultiPolygon":
        for polygon in geojson["coordinates"][0]:
            lats = lats + [coord[1] for coord in polygon]
            longs = longs + [coord[0] for coord in polygon]
    else:
        lats = lats + [coord[1] for coord in geojson["coordinates"][0]]
        longs = longs + [coord[0] for coord in geojson["coordinates"][0]]
    return lats, longs


def extract_geojson_lat_long(locations) -> Tuple[List[int], List[int]]:
    lats = []
    longs = []
    for location in locations:
        loc_lats, loc_longs = extract_lats_longs(location.raw["geojson"])
        lats.extend(loc_lats)
        longs.extend(loc_longs)
    return lats, longs


def calc_bounds(locations: List[Location]) -> List[List[int]]:
    lats, longs = extract_geojson_lat_long(locations)
    lats = lats + [loc.latitude for loc in locations]
    longs = longs + [loc.longitude for loc in locations]
    return [[min(lats), min(longs)], [max(lats), max(longs)]]


def main() -> None:
    st.set_page_config(layout="wide", page_title="NER Spatial Mapping")
    st.title("NER Spatial Mapping")
    left, right = st.columns(2)
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
        map.fit_bounds(calc_bounds(locations))
        st_folium(map)


if __name__ == "__main__":
    main()
