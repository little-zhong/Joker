(function (_0x26763e, _0x2ddce1) {
    const * 0x47402c = a0 * 0x47fb
        , * 0x5d7c2e = * 0x26763e();
    while (!![]) {
        try {
            const * 0x2f3a4a = parseInt(* 0x47402c(0x122)) / 0x1 * (-parseInt(_0x47402c(0x118)) / 0x2) + parseInt(_0x47402c(0x120)) / 0x3 + parseInt(_0x47402c(0x11f)) / 0x4 * (-parseInt(_0x47402c(0x113)) / 0x5) + -parseInt(_0x47402c(0x127)) / 0x6 + -parseInt(_0x47402c(0x119)) / 0x7 + parseInt(_0x47402c(0x12a)) / 0x8 * (-parseInt(_0x47402c(0x11d)) / 0x9) + parseInt(_0x47402c(0x11a)) / 0xa;
            if (_0x2f3a4a === _0x2ddce1)
                break;
            else
                * 0x5d7c2e['push'](* 0x5d7c2e['shift']());
        } catch (_0x357b97) {
            * 0x5d7c2e['push'](* 0x5d7c2e['shift']());
        }
    }
}(a0_0x212c, 0xa868b));
var count = 0x0
    , state = '';
function generateHash(_0x2232e6) {
    const * 0x120258 = a0 * 0x47fb;
    var * 0x324ea1 = this[* 0x120258(0x125)] || this[_0x120258(0x129)];
    const * 0x2a9367 = new TextEncoder()[* 0x120258(0x11c)](_0x2232e6);
    return * 0x324ea1['subtle'][* 0x120258(0x121)]('SHA-256', * 0x2a9367)[* 0x120258(0x11e)](_0x7093d0 => {
        const * 0x16bedf = * 0x120258
            , * 0x219fa9 = new Uint8Array(* 0x7093d0);
        let * 0x46c2dc = * 0x219fa9['reduce']((_0x4ca053, _0x51aaea) => _0x4ca053 + * 0x51aaea[* 0x16bedf(0x114)](0x10)['padStart'](0x2, '0'), '');
        return _0x46c2dc;
    }
    );
}
function generateRandomString(_0x49d1cd) {
    const * 0x3b99f2 = a0 * 0x47fb
        , * 0x2b2506 = * 0x3b99f2(0x12d);
    let _0x47f0f6 = '';
    for (let * 0x10a368 = 0x0; * 0x10a368 < * 0x49d1cd; * 0x10a368++) {
        const * 0x50dacf = Math[* 0x3b99f2(0x126)](Math[_0x3b99f2(0x124)]() * * 0x2b2506[* 0x3b99f2(0x128)]);
        * 0x47f0f6 += * 0x2b2506[_0x50dacf];
    }
    return _0x47f0f6;
}
function a0_0x212c() {
    const * 0x31ef71 =['indexOf', '5443670zPUUVk', 'toString', 'close', 'data', 'UPDATE*RANDOM', '1772IHDilZ', '6484121uOilaB', '36727520jIiqgE', 'START', 'encode', '13446njMxrV', 'then', '4vvniFJ', '2443041yInizk', 'digest', '139gKbRgo', 'require', 'random', 'crypto', 'floor', '3384018tGWdYk', 'length', 'webkitCrypto', '5864MGFwtA', 'command', 'payload', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'];
    a0_0x212c = function () {
        return _0x31ef71;
    }
        ;
    return a0_0x212c();
}
function a0_0x47fb(_0x5cb030, _0x1e5867) {
    const * 0x212c1b = a0 * 0x212c();
    return a0_0x47fb = function (_0x47fba9, _0x1beba8) {
        * 0x47fba9 = * 0x47fba9 - 0x112;
        let * 0x3c1971 = * 0x212c1b[_0x47fba9];
        return _0x3c1971;
    }
        ,
        a0_0x47fb(_0x5cb030, _0x1e5867);
}
function generate(_0x54e554) {
    const * 0x3857fb = a0 * 0x47fb;
    if (state !== _0x3857fb(0x11b)) {
        self[_0x3857fb(0x115)]();
        return;
    }
    const _0x1715b7 = /^00000/
        , _0x3a0860 = generateRandomString(0x30);
    return generateHash('' + * 0x54e554['payload'] + * 0x3a0860)['then'](_0x5adca2 => {
        const * 0x52a3dc = * 0x3857fb;
        count++;
        if (count % 0x2710 === 0x0) { }
        postMessage({
            'command': _0x52a3dc(0x117),
            'randomStr': _0x3a0860
        }),
        * 0x5adca2[* 0x52a3dc(0x112)](_0x54e554[_0x52a3dc(0x123)]) === 0x0 ? (postMessage({
            'command': 'FINISH',
            'nonce': _0x3a0860,
            'hash': _0x5adca2
        }),
                self['close']()) : generate(_0x54e554);
    }
    );
}
onmessage = function (_0x4be69f) {
    const * 0x3f4e34 = a0 * 0x47fb;
    state = * 0x4be69f['data'][* 0x3f4e34(0x12b)],
    * 0x4be69f[* 0x3f4e34(0x116)][_0x3f4e34(0x12b)] === * 0x3f4e34(0x11b) ? generate(* 0x4be69f[_0x3f4e34(0x116)][_0x3f4e34(0x12c)]) : self[_0x3f4e34(0x115)]();
}
    ;