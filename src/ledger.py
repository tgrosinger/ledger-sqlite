import json
import subprocess
from typing import List
import typing


class AmountQuantity(typing.TypedDict):
    decimalMantissa: int
    decimalPlaces: int
    floatingPoint: float


class AmountStyle(typing.TypedDict):
    ascommodityside: str
    ascommodityspaced: bool
    asdecimalpoint: str
    asdigitgroups: str | None  # TODO: str?
    asprecision: int


class Amount(typing.TypedDict):
    acommodity: str
    aprice: str | None  # TODO: str or int?
    aquantity: AmountQuantity
    astyle: AmountStyle


class Posting(typing.TypedDict):
    paccount: str
    pamount: List[Amount]
    pbalanceassertion: str | None
    pcomment: str
    pdate: str | None
    pdate2: str | None
    poriginal: str | None
    pstatus: str  # TODO: Enum?
    ptags: List[str]
    ptransaction_: int
    ptype: str  # TODO: Enum?


class SourcePosition(typing.TypedDict):
    sourceColumn: int
    sourceLine: int
    sourceName: str


class Transaction(typing.TypedDict):
    tcode: str
    tcomment: str
    tdate: str
    tdate2: str | None
    tdescription: str
    tindex: int
    tpostings: List[Posting]
    tprecedingcomment: str
    tsourcepos: List[SourcePosition]
    tstatus: str  # TODO: Enum?
    ttags: List[str]


def get_transactions(filename: str) -> List[Transaction]:
    """
    Retrieve a list of transaction objects as parsed by hledger from the provided input file.
    """
    res = subprocess.run(
        ["/usr/bin/hledger", "print", "-f", filename, "-O", "json"],
        check=True,
        capture_output=True,
    )
    txs: List[Transaction] = json.loads(res.stdout)
    return txs
