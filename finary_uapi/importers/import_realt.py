import requests
import json
import re
import os
from finary_uapi.user_generic_assets import (
    get_user_generic_assets,
)
WALLET_ADDRESS = os.environ["WALLET_ADDRESS"]
GNOSIS_API_TOKENLIST_URI = f"https://gnosis.blockscout.com/api/v2/addresses/{WALLET_ADDRESS}/token-balances"


def get_realt_rentals_blockchain():
    url = GNOSIS_API_TOKENLIST_URI
    myWallet = json.loads(requests.get(url).text)
    myRealT_rentals = {}
    MyRealT_API_Header = {
        "Accept": "*/*",
    }

    token_list_req = requests.get(
        "https://api.realt.community/v1/token", headers=MyRealT_API_Header
    ).json()

    tokens_mapping = {row["uuid"].lower(): row for row in token_list_req}
    # print(tokens_mapping)
    total_value = 0
    for item in myWallet:
        token = item.get("token")
        symbol = token.get("symbol")
        contract_adress = token["address"].lower()
        if re.match(r"^REALTOKEN", symbol, re.IGNORECASE):
            find_contract = tokens_mapping[contract_adress]
            balance = float(item["value"]) / pow(10, int(token["decimals"]))
            token_price = find_contract["tokenPrice"]
            myRealT_rentals.update(
                {
                    contract_adress: {
                        "name": symbol,
                        "balance": balance,
                        "contractAddress": contract_adress,
                        "tokenPrice": token_price
                    }
                })
            total_value += token_price * balance
    return myRealT_rentals, total_value


def get_realtportfolio_other_finary(session: requests.Session):
    myFinary_realt_portfolio = get_user_generic_assets(session)
    myFinary_realt_portfolio = list(
        filter(
            lambda x: re.match("^RealT Portfolio", x["name"]),
            myFinary_realt_portfolio["result"],
        )
    )

    if myFinary_realt_portfolio:
        return myFinary_realt_portfolio[0]
    else:
        return None
