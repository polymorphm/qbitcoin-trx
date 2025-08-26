library: qbitcoin trx
=====================

Basic functions to make transactions in qbitcoin.

Examples::

    import lib_qbitcoin_trx

    opener = lib_qbitcoin_trx.make_opener()
    conn = lib_qbitcoin_trx.Conn('http://172.17.0.1:9556/')

    # EXAMPLE 1: typical sending balance into two separate addresses (leaving small fee)

    lib_qbitcoin_trx.send_balance(
            opener, conn,
            {
                'ECNHfzHvqB2oxhkwZQJVdjuhy6oT6Bqp6Xt': '5HryNbGkwGWrYTAwb3tUaru5ku5Xd73SjiiqmkwcihQrCK9q3VV',
            },
            {
                'ECWDydMT4eEG4m3y7Kpt9mXMsnmWf3AVA83': 0.02,
                'ECLf3a5c4ZCYfJBGiRWHFd3SpZfzWQEdv2d': 0.01,
            },
            None,
            0.000001, 0,
    )

    lib_qbitcoin_trx.get_trx_conf(opener, conn,
            'af65cf5bb6374a4659465e9f592ff885df7451cd168604c25440787f928e2377')

    # EXAMPLE 2: gathering all balances into one place (without fee)

    lib_qbitcoin_trx.send_balance(
            opener, conn,
            {
                'ECLf3a5c4ZCYfJBGiRWHFd3SpZfzWQEdv2d': '5J66dh853DW4oD4wLwLpr9JgYJ2oxEhwVPkv4fcYdsQn7yhSRF3',
                'ECWDydMT4eEG4m3y7Kpt9mXMsnmWf3AVA83': '5JhdiUtErdg6wFTYWUDFLzo3nMNVvbv5QpBWaKvmUYGGYRsi3gL',
                'ECNHfzHvqB2oxhkwZQJVdjuhy6oT6Bqp6Xt': '5HryNbGkwGWrYTAwb3tUaru5ku5Xd73SjiiqmkwcihQrCK9q3VV',
            },
            {},
            None,
            0, 0,
    )

    lib_qbitcoin_trx.get_trx_conf(opener, conn,
            '70bce09b1e5de538ce1d4646f915f971dd5e02f1764c8fec16b0fd53c989b703')

    lib_qbitcoin_trx.get_balance(opener, conn, 'ECLf3a5c4ZCYfJBGiRWHFd3SpZfzWQEdv2d', 0)

    lib_qbitcoin_trx.get_balance(opener, conn, 'ECWDydMT4eEG4m3y7Kpt9mXMsnmWf3AVA83', 0)

    lib_qbitcoin_trx.get_balance(opener, conn, 'ECNHfzHvqB2oxhkwZQJVdjuhy6oT6Bqp6Xt', 0)

    # EXAMPLE 3: sending entire balance into another address (without fee)

    lib_qbitcoin_trx.send_balance(
            opener, conn,
            {
                'ECLf3a5c4ZCYfJBGiRWHFd3SpZfzWQEdv2d': '5J66dh853DW4oD4wLwLpr9JgYJ2oxEhwVPkv4fcYdsQn7yhSRF3',
            },
            {},
            'ECc7siAqYHP4dEVNwBTvAxnEhykguJt2XWz',
            0, 0,
    )

    lib_qbitcoin_trx.get_trx_conf(opener, conn,
            'f707be4958ec2d451cd8aefa7c1bfaa40c65ea5480ea0cfac956308507b5b67f')

    lib_qbitcoin_trx.get_balance(opener, conn, 'ECLf3a5c4ZCYfJBGiRWHFd3SpZfzWQEdv2d', 0)

    lib_qbitcoin_trx.get_balance(opener, conn, 'ECc7siAqYHP4dEVNwBTvAxnEhykguJt2XWz', 0)
