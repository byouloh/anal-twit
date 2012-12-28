var toFlatArray = function(obj) {
    var flattened = [];

    var join = function(path, key,isArray) {
        if (key.indexOf && key.indexOf(".") != -1) {
            key = key.replace(".", "\\.");
        }
        if (!isArray){
            return ((path === "") ? "" : path + ".") + key;
        }else{
            return ((path === "") ? "" : path);
            }
    }

    var flattenArray = function(arr, path) {
        for (var i=0; i < arr.length; i++) {
            flattenElement(arr,path,i,true);
        }
    }

    var flattenObject = function(obj, path) {
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) {
                flattenElement(obj, path, key,false);
            }
        }
    }

    var flattenElement = function(obj, path, key,isArray) {
        if (toString.call(obj[key]) === '[object Array]') {
            flattenArray(obj[key], join(path, key,isArray));
        } else if (typeof obj[key] == "object") {
            flattenObject(obj[key], join(path, key,isArray));
        } else {
            flattened.push([join(path, key),obj[key]]);
        }
    }

    flattenObject(obj, "");
    return flattened;
};


var handleMessage = function (flat) {
        for (var i = 0, len = flat.length;
                            i < len; i++) {
            countPair(flat[i]);
        }
    },
    countPair = function (pair) {
        if ((pair == null) || !pair.length) {
            return;
        }

        if (scoreboard[pair[0]] == null){
            scoreboard[pair[0]] = {};
        }

        if (scoreboard[pair[0]][pair[1]] == null){
            scoreboard[pair[0]][pair[1]] = 0;
        }

        scoreboard[pair[0]][pair[1]]++;
    };


var scoreboard = {};


onmessage = function (event) {
    message = event.data;
    if (message === 'gimme') {
        postMessage(scoreboard);
    } else {
        handleMessage(toFlatArray(event.data));
    }
}
