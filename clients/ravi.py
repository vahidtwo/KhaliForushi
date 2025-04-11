import dataclasses
import datetime

import requests


@dataclasses.dataclass
class RaviOptionsDataclass:
    final_price_diff_percent_by_final_price: float
    cover_call_final_price_diff_percent_by_base_price: float
    symbol: str
    end_date: datetime.date
    delta: float
    highest_bid_price: int
    lowest_ask_price: int
    highest_bid_value: int
    strick_price: int
    cover_call_final_price: int
    cover_call_volume: int
    cover_call: int
    cover_call_profit: float
    cover_call_in_end_date: float
    guarantee: int
    original_symbol: str
    original_symbol_lowest_ask_price: int


class RaviClient:
    token = ""
    url = "https://api.ravindex.ir/graphql"

    def __init__(self, token):
        self.token = token

    def get_covert_call(self, delta, minimum_profit):
        query = """
        query CoverdCallStrategy($after: String, $first: Int, $orderBy: String, $baseSecurity_Ticker_In: [String], $data_Delta_Gte: Float, $endDate_Gte: Date, $endDate_Lte: Date, $strickPriceDiffWithBasePriceRange: RangeInput, $coverCallGte: Int, $coverCallFinalPriceDiffPercentByBasePriceRange: RangeInput, $coverCallVolumeGte: BigInt) {
  options(
    after: $after
    first: $first
    orderBy: $orderBy
    baseSecurity_Ticker_In: $baseSecurity_Ticker_In
    data_Delta_Gte: $data_Delta_Gte
    endDate_Gte: $endDate_Gte
    endDate_Lte: $endDate_Lte
    hasCoverCall: true
    strickPriceDiffWithBasePriceRange: $strickPriceDiffWithBasePriceRange
    coverCallGte: $coverCallGte
    optionType: BUY
    coverCallFinalPriceDiffPercentByBasePriceRange: $coverCallFinalPriceDiffPercentByBasePriceRange
    coverCallVolumeGte: $coverCallVolumeGte
  ) {
    edges {
      node {
        id
        finalPriceDiffPercentByFinalPrice
        coverCallFinalPriceDiffPercentByBasePrice
        security {
          symbol
          id
          orderBook {
            highestBidPrice
            lowestAskPrice
            highestBidValue
            __typename
          }
          __typename
        }
        strickPrice
        coverCallFinalPrice
        coverCallVolume
        coverCall
        coverCallProfit
        coverCallInEndDate
        baseSecurity {
          symbol
          orderBook {
            lowestAskPrice
            __typename
          }
          __typename
        }
        endDate
        data {
          delta
          __typename
        }
        guarantee
        __typename
      }
      __typename
    }
    pageInfo {
      endCursor
      hasNextPage
      __typename
    }
    __typename
  }
}

        """
        today = datetime.date.today()
        data = {
            "operationName": "CoverdCallStrategy",
            "query": query,
            "variables": {
                "coverCallGte": minimum_profit,
                "data_Delta_Gte": delta,
                "endDate_Gte": today.strftime("%Y-%m-%d"),
                "endDate_Lte": (today + datetime.timedelta(days=70)).strftime(
                    "%Y-%m-%d"
                ),
                "first": 20,
                "orderBy": "-coverCall,id",
            },
        }
        return requests.post(url=self.url, json=data)

    @staticmethod
    def parse_covert_call_option_data(response) -> list[RaviOptionsDataclass]:
        data = response.json()
        options = data["data"]["options"]["edges"]
        options_data = []
        for option in options:
            node = option["node"]
            options_data.append(
                RaviOptionsDataclass(
                    final_price_diff_percent_by_final_price=node[
                        "finalPriceDiffPercentByFinalPrice"
                    ],
                    cover_call_final_price_diff_percent_by_base_price=node[
                        "coverCallFinalPriceDiffPercentByBasePrice"
                    ],
                    symbol=node["security"]["symbol"],
                    end_date=datetime.datetime.strptime(node["endDate"], "%Y-%m-%d"),
                    delta=node["data"]["delta"],
                    highest_bid_price=node["security"]["orderBook"]["highestBidPrice"],
                    lowest_ask_price=node["security"]["orderBook"]["lowestAskPrice"],
                    highest_bid_value=node["security"]["orderBook"]["highestBidValue"],
                    guarantee=node["guarantee"],
                    original_symbol=node["baseSecurity"]["symbol"],
                    original_symbol_lowest_ask_price=node["baseSecurity"]["orderBook"][
                        "lowestAskPrice"
                    ],
                    strick_price=node["strickPrice"],
                    cover_call_final_price=node["coverCallFinalPrice"],
                    cover_call_volume=node["coverCallVolume"],
                    cover_call=node["coverCall"],
                    cover_call_profit=node["coverCallProfit"],
                    cover_call_in_end_date=node["coverCallInEndDate"],
                )
            )
        return options_data
