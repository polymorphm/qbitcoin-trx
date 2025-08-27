"""
library: qbitcoin trx
~~~~~~~~~~~~~~~~~~~~~

Basic functions to make transactions in qbitcoin.

Example usage:

import lib_qbitcoin_trx

opener = lib_qbitcoin_trx.make_opener()
conn = lib_qbitcoin_trx.Conn('http://172.17.0.1:9556/')

lib_qbitcoin_trx.ping(opener, conn)
"""

import typing
from dataclasses import dataclass
from urllib import request as url_request
from urllib import error as url_error
import json

def _check_type[T](typ: typing.Type[T], val: typing.Any) -> T:
    if val is None:
        raise TypeError
    
    if typ is typing.Any:
        return val
    
    if not isinstance(val, typ):
        raise TypeError
    
    return val

def _check_nullable_type[T](typ: typing.Type[T], val: typing.Any) -> T | None:
    if val is None or typ is typing.Any:
        return val
    
    if not isinstance(val, typ):
        raise TypeError
    
    return val

DEFAULT_TIMEOUT = 1000.0
DEFAULT_READ_SIZE = 1024 * 1024 * 256

@dataclass
class RpcError(Exception):
    code: int
    message: str
    data: typing.Any = None

def make_opener() -> typing.Any:
    return url_request.build_opener()

@dataclass
class Conn:
    url: str
    # TODO: password ???
    timeout: float = DEFAULT_TIMEOUT
    read_size: int = DEFAULT_READ_SIZE

def rpc(
            opener: typing.Any,
            conn: Conn,
            method: str,
            params: typing.Any,
        ) -> typing.Any:
    req_data = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': method,
        'params': params,
    }
    req = url_request.Request(
        conn.url,
        headers={
            'content-type': 'application/json',
        },
        data=json.dumps(req_data).encode(),
    )
    
    try:
        with opener.open(req, timeout=conn.timeout) as f:
            resp_data_bytes = typing.cast(bytes, f.read(conn.read_size))
    except url_error.HTTPError as e:
        resp_data_bytes = typing.cast(bytes, e.read(conn.read_size))
    
    resp_data = json.loads(resp_data_bytes)
    
    error = _check_nullable_type(dict, resp_data.get('error'))
    result = _check_nullable_type(typing.Any, resp_data.get('result'))
    
    if error is not None:
        error_code = _check_type(int, error['code'])
        error_message = _check_type(str, error['message'])
        error_data = _check_nullable_type(typing.Any, error.get('data'))
        
        if not error_message and isinstance(result, str) and result:
            error_message = result
        
        rpc_error = RpcError(error_code, error_message)
        rpc_error.data = error_data
        
        raise rpc_error
    
    return result

def ping(
            opener: typing.Any,
            conn: Conn,
        ) -> None:
    rpc(opener, conn, 'ping', [])

def get_trx_conf(
            opener: typing.Any,
            conn: Conn,
            trx_id: str,
        ) -> int:
    res = rpc(opener, conn, 'getrawtransaction', [trx_id])
    
    conf = _check_type(int, res['confirmations'])
    
    return conf

def new_address_pair(
            opener: typing.Any,
            conn: Conn,
        ) -> tuple[str, str]:
    res = rpc(opener, conn, 'getnewaddress', [])
    
    address = _check_type(str, res['address'])
    key = _check_type(str, res['private_key'])
    
    return address, key

def get_balance(
            opener: typing.Any,
            conn: Conn,
            address: str,
            conf: int,
        ) -> float:
    res = rpc(opener, conn, 'listunspent', [address, conf])
    
    balance = 0.0
    
    for item in _check_type(list, res):
        item_addr = _check_type(str, item['address'])
        
        if address != item_addr:
            raise AssertionError
        
        balance += _check_type(float, item['amount'])
    
    return balance

def send_balance(
            opener: typing.Any,
            conn: Conn,
            from_address_pairs: dict[str, str],
            to_addresses: dict[str, float],
            change_address: str | None,
            fee: float,
            conf: int,
        ) -> str:
    balance = 0.0
    inputs = []
    
    if change_address is None:
        change_address = next(iter(from_address_pairs.keys()))
    
    for from_address in from_address_pairs.keys():
        res = rpc(opener, conn, 'listunspent', [from_address, conf])
        
        for input_trx_item in _check_type(list, res):
            item_addr = _check_type(str, input_trx_item['address'])
            
            if from_address != item_addr:
                raise AssertionError
            
            balance += _check_type(float, input_trx_item['amount'])
            inputs.append({
                'txid': _check_type(str, input_trx_item['txid']),
                'vout': _check_type(int, input_trx_item['vout']),
            })
    
    change = balance
    outputs = []
    
    for to_address, to_address_amount in to_addresses.items():
        outputs.append({to_address: to_address_amount})
        change -= to_address_amount
    
    change -= fee
    outputs.append({change_address: change})
    
    res = rpc(opener, conn, 'createrawtransaction', [inputs, outputs])
    
    trx = _check_type(str, res)
    keys = list(from_address_pairs.values())
    
    res = rpc(opener, conn, 'signrawtransactionwithkey', [trx, keys])
    
    signed_trx = _check_type(str, res['hex'])
    
    res = rpc(opener, conn, 'sendrawtransaction', [signed_trx])
    
    trx_id = _check_type(str, res)
    
    return trx_id

# vi:filetype=python3:ts=4:sw=4:et
