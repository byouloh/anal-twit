var ws = new WebSocket("ws://localhost:8888/socket/");

var count = 0,
    start = +new Date(),
    rate = 0;

ws.onmessage = function (event) {
    count++;
    postMessage(JSON.parse(event.data));
};

var _timeout = null,
    determineRate = function() {
        var now = +new Date(),
            seconds = (now - start) / 1000,
            _rate = Math.round(count / seconds);

        count = 0
        start = +new Date();

        if (_rate !== _rate) {
            _rate = 0;
        }

        rate = _rate;
        setTimeout(determineRate, 1000);
    };

determineRate();


onmessage = function (event) {
    var message = event.data;
    if (message === 'rate') {
        postMessage(rate + "/sec");
    }
};
