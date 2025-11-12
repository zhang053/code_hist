// console.log("hello world")

args = process.argv // node 获取命令行参数
// console.log(args)

function test(x) {
    // console.log("x=" + x)
    x *= 2;
    return x;
}

result = test(args[2])
console.log("result = "+result)