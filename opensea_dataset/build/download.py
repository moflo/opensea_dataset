# Opensea Dataset Download Script

"""Opensea Collection Download """

"""
Usage: download.py --name NAME --start 0 --end 10

"""

import json
import cairosvg  # https://cairosvg.org/documentation/
import requests
from absl import app, flags

flags.DEFINE_string(
    "name", "chain-runners-nft", "The name of the Opensea NFT collection"
)
flags.DEFINE_integer("start", 0, "Starting collection item number", lower_bound=0)
flags.DEFINE_integer("end", 10, "Ending collection item number", lower_bound=1)

FLAGS = flags.FLAGS


def save_traits(collection) -> None:
    # Find NFT collection assets
    url = f"https://api.opensea.io/api/v1/collection/{collection}"

    response = requests.request("GET", url)
    collection_data = response.json()

    # Collection traits, dictionary of dictionary
    collection_traits = collection_data["collection"]["traits"]

    # Collection name
    collction_name = collection_data["collection"]["name"]

    # Collection name
    collction_url = collection_data["collection"]["external_url"]

    # Collection name
    collction_name = collection_data["collection"]["name"]

    # Collection market cap
    market_cap = collection_data["collection"]["stats"]["market_cap"]

    # Write JSON file
    nft_json = {}
    nft_json["name"] = collction_name
    nft_json["market_cap"] = market_cap
    nft_json["external_url"] = collction_url
    nft_json["traits"] = collection_traits
    with open(f"./{collection}.json", "w") as outfile:
        json.dump(nft_json, outfile, indent=2)


def save_asset(index, collection) -> None:
    # Find NFT collection assets
    url = f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={index}&limit=1&collection={collection}"

    response = requests.request("GET", url)
    asset_data = response.json()

    # NFT image url, svg format
    image_url = asset_data["assets"][0]["image_url"]

    # NFT token_id, eg. #1234
    token_id = asset_data["assets"][0]["token_id"]

    # NFT name, eg. NFT #1234
    nft_name = asset_data["assets"][0]["name"]

    # NFT traits_json, eg. {'race':'robot'}
    traits_json = asset_data["assets"][0]["traits"]

    # NFT contract address, eg. 0xdeadbeef
    contract_address = asset_data["assets"][0]["asset_contract"]["address"]

    print(f"NFT Name: {nft_name} [{token_id}]")
    print(f"  | URL: {image_url}")
    # print(f'  | traits: {traits_json}')

    # Find NFT asset current price, download
    url = f"https://api.opensea.io/api/v1/asset/{contract_address}/{token_id}/"

    response = requests.request("GET", url)
    asset_data = response.json()

    # NFT contract address, eg. 0xdeadbeef
    nft_price = asset_data["orders"][0]["payment_token_contract"]["usd_price"]

    print(f"  | price: {nft_price}")

    # Write JSON file
    nft_json = {}
    nft_json["name"] = nft_name
    nft_json["token_id"] = token_id
    nft_json["image_url"] = image_url
    nft_json["contract_address"] = contract_address
    nft_json["price"] = nft_price
    nft_json["traits"] = traits_json
    with open(f"./{token_id:>05}.json", "w") as outfile:
        json.dump(nft_json, outfile, indent=2)

    # Write PNG file
    cairosvg.svg2png(
        url=image_url, write_to=f"./{token_id:>05}.png", parent_height=256, parent_width=256
    )


def main(_) -> None:
    print(f"Create dataset from NFT collection: {FLAGS.name}")

    print(f"  | Save traits {FLAGS.name}")
    save_traits(FLAGS.name)

    print(f"  | Item range: [{FLAGS.start} - {FLAGS.end}]")

    index = FLAGS.start
    while index <= FLAGS.end:
        save_asset(index, FLAGS.name)
        index += 1


if __name__ == "__main__":
    app.run(main)
