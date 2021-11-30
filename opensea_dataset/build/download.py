# Opensea Dataset Download Script

"""Opensea Collection Download """

"""
Usage: download.py --name NAME --start 0 --end 10

"""

import re
from absl import app
from absl import flags
import requests
import cairosvg # https://cairosvg.org/documentation/

flags.DEFINE_string('name', 'chain-runners-nft', 'The name of the Opensea NFT collection')
flags.DEFINE_integer('start',0,'Starting collection item number',lower_bound=0)
flags.DEFINE_integer('end',100,'Ending collection item number',lower_bound=1)

FLAGS = flags.FLAGS

def main(_) -> None:
    print(f'Create dataset from NFT collection: {FLAGS.name}')
    print(f'  | Item range: [{FLAGS.start} - {FLAGS.end}]')

    # Find NFT collection assets
    url = f'https://api.opensea.io/api/v1/assets?order_direction=asc&offset=0&limit=1&collection={FLAGS.name}'

    response = requests.request("GET", url)
    asset_data = response.json()

    # NFT image url, svg format
    image_url = asset_data['assets'][0]['image_url']

    # NFT token_id, eg. #1234
    token_id = asset_data['assets'][0]['token_id']

    # NFT name, eg. NFT #1234
    nft_name = asset_data['assets'][0]['name']

    # NFT traits_json, eg. {'race':'robot'}
    traits_json = asset_data['assets'][0]['traits']

    # NFT contract address, eg. 0xdeadbeef
    contract_address = asset_data['assets'][0]['asset_contract']['address']

    print(f'NFT Name: {nft_name} [{token_id}]')
    print(f'  | URL: {image_url}')
    print(f'  | traits: {traits_json}')

    # Find NFT asset current price, download 
    url = f'https://api.opensea.io/api/v1/asset/{contract_address}/{token_id}/'

    response = requests.request("GET", url)
    asset_data = response.json()

    # NFT contract address, eg. 0xdeadbeef
    nft_price = asset_data['orders'][0]['payment_token_contract']['usd_price']

    print(f'  | price: {nft_price}')

    # Write PNG file
    cairosvg.svg2png(url=image_url, write_to=f'./{token_id}.png')

if __name__ == '__main__':
  app.run(main)
